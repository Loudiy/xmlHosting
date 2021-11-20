from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import urlopen
import time
import os
import xml.etree.ElementTree as gfg

#### Define time to wait
time_to_sleep = 1200

#### URLs of the website
url_home = "https://hermanosautosales.com"
url_inventory = url_home + "/newandusedcars"

#### Setup of Selenium
# driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
driver = webdriver.Chrome()
driver.get(url_inventory)


#### Get the button "Next" to navigate all the pages in the inventory
button = driver.find_elements_by_css_selector('[aria-label="Next"]')

#### Populate vehicles_urls
vehicles_urls = []

page = driver.page_source
soup = BeautifulSoup(page, features="html.parser")
number_of_pages = soup.find_all("span", attrs={"class": "pager-summary"})

number_of_pages = int([s.strip("Page: ").split(" ") for s in number_of_pages[0].text.strip().split("of")][1][0])
counter = 1
while counter <= number_of_pages:

    page = driver.page_source
    soup = BeautifulSoup(page, features="html.parser")
    vehicles = soup.find_all("div", attrs={"class": "row no-gutters invMainCell"})

    for vehicle in vehicles:
        vehicles_urls += [url_home + vehicle.div.a["href"]]
    try:
        button[0].click()
        time.sleep(1)
    except:
        break
    counter += 1
driver.close()



##### Create xml root
listings = gfg.Element('listings')
listings_title = gfg.SubElement(listings, "title")
listings_title.text = "Hermanos Auto Sales Inc Inventory Feed"
listings_link = gfg.SubElement(listings, "link")
listings_link.set("rel", "external")
listings_link.set("href", "https://hermanosautosales.com/newandusedcars")

for url in vehicles_urls:

    page = urlopen(url)
    soup = BeautifulSoup(page.read().decode("utf-8"), "html.parser")
    main = soup.select('div[class="i10r-detail-main"]')
    
    vehicle_title = main[0].select('h1[class="i10r_detailVehicleTitle"] a')[0].get("aria-label")
    vehicle_trim = main[0].select('h1[class="i10r_detailVehicleTitle"] a span')[0].text
    if vehicle_trim == "":
        vehicle_trim = "Other"
    vehicle_id = main[0].select('div[class="i10r_features"] p[class="i10r_optStock"]')[0].text.split(" ")[-1].strip()
    # vehicle_description = soup.select('#DivNotes div[class="card-body"]')[0].text.strip()
    vehicle_description = vehicle_title + " available now. Contact us for more information."
    vehicle_url = url
    vehicle_make = vehicle_title.split(' ')[1]
    images = soup.select('#showPhotos div[class="card-body"] div[class="row"] a')
    vehicle_images_urls = [image["href"] for image in images]

    # Needs verification
    if vehicle_trim == "":
        vehicle_model = " ".join(vehicle_title.split(' ')[2:])
    else:
        vehicle_model = " ".join(vehicle_title.split(' ')[2:-1])

    vehicle_year = (vehicle_title.split(" ")[0])
    vehicle_mileage = ("".join(
        main[0].select('div[class="i10r_features"] p[class="i10r_optMPG"]')[0].text.split(" ")[-1].strip().split(",")))
    vehicle_drive_train = main[0].select('div[class="i10r_features"] p[class="i10r_optDrive"]')[0].text.split(" ")[
        -1].strip()
    vehicle_vin = main[0].select('div[class="i10r_features"] p[class="i10r_optVin"]')[0].text.split(" ")[-1].strip()
    vehicle_body_style = "OTHER"
    if "manual" in main[0].select('div[class="i10r_features"] p[class="i10r_optTrans"]')[0].text.lower():
        vehicle_transmission = "MANUAL"
    else:
        vehicle_transmission = "AUTOMATIC"
    try:
    	vehicle_price = main[0].select('span[class="price-4"]')[0].text[1:] + " USD"
    except:
    	continue
    vehicle_fuel_type = "OTHER"
    vehicle_latitude = str(39.38134001609587)
    vehicle_longitude = str(-84.55001094834897)
    vehicle_exterior_color = main[0].select('div[class="i10r_features"] p[class="i10r_optColor"]')[0].text.split(" ")[
        -1].strip()
    dealer_id = "UD022948"
    fb_page_id = str(2049585275333899)
    dealer_communication_channel = "CHAT"
    dealer_privacy_policy_url = "https://hermanosautosales.com/privacy"

    #### Check for issues
    if vehicle_drive_train == "4WD":
        vehicle_drive_train = "4X4"
    if vehicle_drive_train == "2WD":
        vehicle_drive_train = "2X4"

    #### Create the xml tree
    vehicle = gfg.SubElement(listings, "listing")

    xml_fb_page_id = gfg.SubElement(vehicle, "fb_page_id")
    xml_fb_page_id.text = fb_page_id

    xml_vehicle_id = gfg.SubElement(vehicle, "vehicle_id")
    xml_vehicle_id.text = vehicle_id

    title = gfg.SubElement(vehicle, "title")
    title.text = vehicle_title

    description = gfg.SubElement(vehicle, "description")
    description.text = vehicle_description

    xml_url = gfg.SubElement(vehicle, "url")
    xml_url.text = vehicle_url

    make = gfg.SubElement(vehicle, "make")
    make.text = vehicle_make

    model = gfg.SubElement(vehicle, "model")
    model.text = vehicle_model

    year = gfg.SubElement(vehicle, "year")
    year.text = vehicle_year

    mileage = gfg.SubElement(vehicle, "mileage")
    mileage_value = gfg.SubElement(mileage, "value")
    mileage_value.text = vehicle_mileage
    mileage_unit = gfg.SubElement(mileage, "unit")
    mileage_unit.text = "MI"

    for image_url in vehicle_images_urls:
        image = gfg.SubElement(vehicle, "image")
        xml_image_url = gfg.SubElement(image, "url")
        xml_image_url.text = image_url

    transmission = gfg.SubElement(vehicle, "transmission")
    transmission.text = vehicle_transmission

    body_style = gfg.SubElement(vehicle, "body_style")
    body_style.text = vehicle_body_style

    drivetrain = gfg.SubElement(vehicle, "drivetrain")
    drivetrain.text = vehicle_drive_train

    vin = gfg.SubElement(vehicle, "vin")
    vin.text = vehicle_vin

    price = gfg.SubElement(vehicle, "price")
    price.text = vehicle_price

    exterior_color = gfg.SubElement(vehicle, "exterior_color")
    exterior_color.text = vehicle_exterior_color

    state_of_vehicle = gfg.SubElement(vehicle, "state_of_vehicle")
    state_of_vehicle.text = "Used"

    fuel_type = gfg.SubElement(vehicle, "fuel_type")
    fuel_type.text = vehicle_fuel_type

    trim = gfg.SubElement(vehicle, "trim")
    trim.text = vehicle_trim

    address = gfg.SubElement(vehicle, "address")
    address.set("format", "simple")
    addr1 = gfg.SubElement(address, "component")
    addr1.set("name", "addr1")
    addr1.text = "1475 S Erie Highway"  # 513-330-5010
    addr2 = gfg.SubElement(address, "component")
    addr2.set("name", "addr2")
    addr2.text = "Hermanos Auto Sales"
    city = gfg.SubElement(address, "component")
    city.set("name", "city")
    city.text = "Hamilton"
    region = gfg.SubElement(address, "component")
    region.set("name", "region")
    region.text = "Ohio"
    postal_code = gfg.SubElement(address, "component")
    postal_code.set("name", "postal_code")
    postal_code.text = "45011"
    country = gfg.SubElement(address, "component")
    country.set("name", "country")
    country.text = "United States of America"
    latitude = gfg.SubElement(vehicle, "latitude")
    latitude.text = vehicle_latitude
    longitude = gfg.SubElement(vehicle, "longitude")
    longitude.text = vehicle_longitude

    xml_dealer_id = gfg.SubElement(vehicle, "dealer_id")
    xml_dealer_id = dealer_id

    dealer_name = gfg.SubElement(vehicle, "dealer_name")
    dealer_name.text = "Hermanos Auto Sale"

    dealer_phone = gfg.SubElement(vehicle, "dealer_phone")
    dealer_phone.text = "001 (513)330-5010"

    xml_dealer_communication_channel = gfg.SubElement(vehicle, "dealer_communication_channel")
    xml_dealer_communication_channel.text = dealer_communication_channel

    xml_dealer_privacy_policy_url = gfg.SubElement(vehicle, "dealer_privacy_policy_url")
    xml_dealer_privacy_policy_url.text = dealer_privacy_policy_url

#### Write the xml File
tree = gfg.ElementTree(listings)
tree.write("xml/xmlIndex.xml", encoding="utf-8", xml_declaration=True)

print("sleeping " + str(time_to_sleep))
time.sleep(time_to_sleep)

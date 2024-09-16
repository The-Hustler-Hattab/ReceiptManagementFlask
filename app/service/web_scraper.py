import subprocess
import time

import pyautogui
import pyperclip
import random

from app.model.generic.zillow_model import ZillowModel, SchoolModel, EventModel
import re


class WebScrapper:

    @staticmethod
    def start_browser(url: str) -> None:
        command = f"chrome {url} --new-window --start-fullscreen"
        subprocess.run(command, shell=True)
        time.sleep(1)


    @staticmethod
    def start_web_scraping_routine() -> ZillowModel:
        WebScrapper.move_to_middle_of_screen()
        WebScrapper.move_to_top_bar()
        pyautogui.leftClick()
        # copy the html
        clipboard_content = WebScrapper.copy_content_from_web_page()
        # Print the clipboard content to the terminal
        # print(clipboard_content)
        pyautogui.hotkey('ctrl', 'w')
        WebScrapper.move_to_search_bar()
        pyautogui.leftClick()
        pyautogui.leftClick()
        pyautogui.leftClick()
        return WebScrapper.clean_zillow_property_data(clipboard_content)

    @staticmethod
    def copy_content_from_web_page() -> str:
        pyautogui.hotkey('ctrl', 'u')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(.1)
        pyautogui.hotkey('ctrl', 'c')
        # Get the current content of the clipboard
        clipboard_content = pyperclip.paste()
        return clipboard_content

    @staticmethod
    def continue_web_scraping_routine(url: str) -> ZillowModel:
        pyautogui.write(url)  # 'interval' controls typing speed
        pyautogui.press('enter')
        time.sleep(random.uniform(4, 6))
        clipboard_content = WebScrapper.copy_content_from_web_page()
        # print(clipboard_content)
        pyautogui.hotkey('ctrl', 'w')
        pyautogui.leftClick()
        pyautogui.leftClick()
        pyautogui.leftClick()
        return WebScrapper.clean_zillow_property_data(clipboard_content)

    @staticmethod
    def clean_zillow_property_data(zillow_property_data: str) -> ZillowModel:
        zillow_model: ZillowModel = ZillowModel()

        zestimate_pattern = r'(?<=\\"zestimate\\":\\")[^"]*(?=\\")'
        match = re.search(zestimate_pattern, zillow_property_data)
        zillow_model.zestimate = match.group() if match else ""

        zestibuck_pattern = r'(?<=\\"zestibuck\\":\\")[^"]*(?=\\")'
        match = re.search(zestibuck_pattern, zillow_property_data)
        zillow_model.zestibuck = match.group() if match else ""

        yrblt_pattern = r'(?<=\\"yrblt\\":\\")[^"]*(?=\\")'
        match = re.search(yrblt_pattern, zillow_property_data)
        zillow_model.yrblt = match.group() if match else ""

        lot_size_pattern = r'(?<=\\"lotSize\\":\\")[^"]*(?=\\")'
        match = re.search(lot_size_pattern, zillow_property_data)
        zillow_model.lot_size = match.group() if match else ""

        sqftrange_pattern = r'(?<=\\"sqftrange\\":\\")[^"]*(?=\\")'
        match = re.search(sqftrange_pattern, zillow_property_data)
        zillow_model.sqftrange = match.group() if match else ""

        sqft_pattern = r'(?<=\\"sqft\\":\\")[^"]*(?=\\")'
        match = re.search(sqft_pattern, zillow_property_data)
        zillow_model.sqft = match.group() if match else ""

        bedrooms_pattern = r'(?<=\\"bedrooms\\":)[^"]*(?=,)'
        match = re.search(bedrooms_pattern, zillow_property_data)
        zillow_model.bedrooms = match.group() if match else ""

        # Bathrooms
        bathrooms_pattern = r'(?<=\\"bathrooms\\":)[^"]*(?=,)'
        match = re.search(bathrooms_pattern, zillow_property_data)
        zillow_model.bathrooms = match.group() if match else ""

        homeType_pattern = r'(?<=\\"homeType\\":\\")[^"]*(?=\\")'
        match = re.search(homeType_pattern, zillow_property_data)
        zillow_model.homeType = match.group() if match else ""

        parcel_pattern = r'(?<=\\"parcelNumber\\":\\")[^"]*(?=\\")'
        match = re.search(parcel_pattern, zillow_property_data)
        zillow_model.parcel_num = match.group() if match else ""

        root_type_pattern = r'(?<=\\"roofType\\":\\")[^"]*(?=\\")'
        match = re.search(root_type_pattern, zillow_property_data)
        zillow_model.roof = match.group() if match else ""

        cooling_pattern = r'(?<=\\"cooling\\":).*?]'
        match = re.search(cooling_pattern, zillow_property_data)
        if match:
            zillow_model.cooling = match.group().replace('\\"', '"')
        else:
            zillow_model.cooling = ""

        heating_pattern = r'(?<=\\"heating\\":).*?]'
        match = re.search(heating_pattern, zillow_property_data)
        if match:
            zillow_model.heating = match.group().replace('\\"', '"')
        else:
            zillow_model.heating = ""

        parking_feature_pattern = r'(?<=\\"parkingFeatures\\":).*?]'
        match = re.search(parking_feature_pattern, zillow_property_data)
        if match:
            zillow_model.parking = match.group().replace('\\"', '"')
        else:
            zillow_model.parking = ""

        exterior_feature_pattern = r'(?<=\\"exteriorFeatures\\":).*?]'
        match = re.search(exterior_feature_pattern, zillow_property_data)
        if match:
            zillow_model.exterior = match.group().replace('\\"', '"')
        else:
            zillow_model.exterior = ""


        construction_materials_pattern = r'(?<=\\"constructionMaterials\\":).*?]'
        match = re.search(construction_materials_pattern, zillow_property_data)
        if match:
            zillow_model.construction_materials = match.group().replace('\\"', '"')
        else:
            zillow_model.construction_materials = ""


        street_pattern = r'(?<=\\"aamgnrc1\\":\\")[^"]*(?=\\")'
        match = re.search(street_pattern, zillow_property_data)
        zillow_model.street = match.group() if match else ""

        city_pattern = r'(?<=\\"city\\":\\")[^"]*(?=\\")'
        match = re.search(city_pattern, zillow_property_data)
        zillow_model.city = match.group() if match else ""

        state_pattern = r'(?<=\\"state\\":\\")[^"]*(?=\\")'
        match = re.search(state_pattern, zillow_property_data)
        zillow_model.state = match.group() if match else ""

        zip_pattern = r'(?<=\\"zip\\":\\")[^"]*(?=\\")'
        match = re.search(zip_pattern, zillow_property_data)
        zillow_model.zip = match.group() if match else ""

        county_pattern = r'(?<=\\"cnty\\":\\")[^"]*(?=\\")'
        match = re.search(county_pattern, zillow_property_data)
        zillow_model.county = match.group() if match else ""

        schools_pattern = r'(?<=,\\"schools\\":).*?]'
        match = re.search(schools_pattern, zillow_property_data)
        schools = []
        if match:
            try:
                schools = match.group(0).replace('\\"', '\"')
                schools = SchoolModel.from_json(schools)
            except Exception as e:
                print(e)
                schools = []
        zillow_model.schools = schools

        events_pattern = r'(?<=\\"priceHistory\\":).*?]'
        match = re.search(events_pattern, zillow_property_data)
        events = []
        if match:
            try:
                events = match.group(0).replace('\\"', '\"')
                events = EventModel.from_json(events)
            except Exception as e:
                print(e)
                events = []
        zillow_model.events = events

        print(f"Zestimate: {zillow_model.zestimate}")
        print(f"Zestibuck: {zillow_model.zestibuck}")
        print(f"Year Built: {zillow_model.yrblt}")
        print(f"Lot Size: {zillow_model.lot_size}")
        print(f"Square Footage Range: {zillow_model.sqftrange}")
        print(f"Square Footage: {zillow_model.sqft}")
        print(f"Bedrooms: {zillow_model.bedrooms}")
        print(f"Bathrooms: {zillow_model.bathrooms}")
        print(f"Home Type: {zillow_model.homeType}")
        print(f"Heating: {zillow_model.heating}")
        print(f"Cooling: {zillow_model.cooling}")
        print(f"Parking: {zillow_model.parking}")
        print(f"Exterior: {zillow_model.exterior}")
        print(f"construction_materials: {zillow_model.construction_materials}")

        print(f"Parcel Number: {zillow_model.parcel_num}")
        print(f"Roof: {zillow_model.roof}")
        print(f"Street: {zillow_model.street}")
        print(f"City: {zillow_model.city}")
        print(f"State: {zillow_model.state}")
        print(f"Zip: {zillow_model.zip}")
        print(f"County: {zillow_model.county}")
        print(f"Schools: {zillow_model.get_schools_as_string()}")
        print(f"Events: {zillow_model.get_events_as_string()}")
        
        return zillow_model

    @staticmethod
    def move_to_search_bar():
        pyautogui.moveTo(-1500, 200, duration=.3)  # search bar

    @staticmethod
    def move_to_top_bar():
        pyautogui.moveTo(-1500, 150, duration=.6)  # top of the bar

    @staticmethod
    def move_to_middle_of_screen():
        pyautogui.moveTo(-1500, 500, duration=.5)  # middle of the screen

#
# # WebScrapper.start_browser("https://www.zillow.com/homes/465-BAIRDFORD-RD-BAIRDFORD,-PA-15006_rb/")
# zillow = WebScrapper.start_web_scraping_routine()
#
#
# print(f"Zestimate: {zillow.zestimate}")
# print(f"Zestibuck: {zillow.zestibuck}")
# print(f"Year Built: {zillow.yrblt}")
# print(f"Lot Size: {zillow.lot_size}")
# print(f"Square Footage Range: {zillow.sqftrange}")
# print(f"Square Footage: {zillow.sqf}")
# print(f"Bedrooms: {zillow.bedrooms}")
# print(f"Bathrooms: {zillow.bathrooms}")
# print(f"Home Type: {zillow.homeType}")
# print(f"Heating: {zillow.heating}")
# print(f"Cooling: {zillow.cooling}")
# print(f"Parking: {zillow.parking}")
# print(f"Exterior: {zillow.exterior}")
# print(f"construction_materials: {zillow.construction_materials}")
#
# print(f"Parcel Number: {zillow.parcel_num}")
# print(f"Roof: {zillow.roof}")
# print(f"Street: {zillow.street}")
# print(f"City: {zillow.city}")
# print(f"State: {zillow.state}")
# print(f"Zip: {zillow.zip}")
# print(f"County: {zillow.county}")
# print(f"Schools: {zillow.get_schools_as_string()}")
# print(f"Events: {zillow.get_events_as_string()}")
#

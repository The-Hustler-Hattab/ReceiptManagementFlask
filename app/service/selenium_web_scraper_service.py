# import json
#
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium_stealth import stealth
#
# from app.model.generic.zillow_model import ZillowModel, SchoolModel
# import re
#
# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument(
#     "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
# )
# chrome_options.add_extension("F:\chrome\extenstion\stealth\OFFPHOBPEDOHKENCKINEJACPJODCHGMN_2_1_0_0.crx")
# service = Service()
# driver = webdriver.Chrome(service=service, options=chrome_options)
# # Apply Selenium Stealth
# stealth(driver,
#         languages=["en-US", "en"],
#         vendor="Google Inc.",
#         platform="Linux",
#         webgl_vendor="Intel Inc.",
#         renderer="Intel Iris OpenGL Engine",
#         fix_hairline=True,
#         )
# # Execute a JavaScript script to force override navigator properties
# driver.execute_script("""
#     Object.defineProperty(navigator, 'platform', {
#         get: function () { return 'Linux'; }
#     });
# """)
#
#
# class ZillowScraper:
#     # Initialize the Chrome WebDriver
#
#     @staticmethod
#     def clean_zillow_property_data(zillow_property_data: str)-> ZillowModel:
#         zillow_model: ZillowModel = ZillowModel()
#
#         zestimate_pattern = r'(?<="zestimate":")[^"]*(?=")'
#         zillow_model.zestimate  = re.search(zestimate_pattern, zillow_property_data).group() if re.search(
#             zestimate_pattern, zillow_property_data) else ""
#
#         zestibuck_pattern = r'(?<="zestibuck":")[^"]*(?=")'
#         zillow_model.zestibuck = re.search(zestibuck_pattern, zillow_property_data).group() if re.search(
#             zestibuck_pattern, zillow_property_data) else ""
#
#         yrblt_pattern = r'(?<="yrblt":")[^"]*(?=")'
#         zillow_model.yrblt = re.search(yrblt_pattern, zillow_property_data).group() if re.search(
#             yrblt_pattern, zillow_property_data) else ""
#
#         lot_size_pattern = r'Lot size:\s*([^<]+)'
#         match = re.search(lot_size_pattern, zillow_property_data)
#         zillow_model.lot_size = match.group(1) if match else ""
#
#         sqftrange_pattern = r'(?<="sqftrange":")[^"]*(?=")'
#         zillow_model.sqftrange = re.search(sqftrange_pattern, zillow_property_data).group() if re.search(
#             sqftrange_pattern, zillow_property_data) else ""
#
#         sqft_pattern =r'(?<="sqft":")[^"]*(?=")'
#         zillow_model.sqft = re.search(sqft_pattern, zillow_property_data).group() if re.search(
#             sqft_pattern, zillow_property_data) else ""
#
#         # Bedrooms
#         bedrooms_pattern = r'Bedrooms:\s*([^<]+)'
#         match = re.search(bedrooms_pattern, zillow_property_data)
#         zillow_model.bedrooms = match.group(1) if match else ""
#
#         # Bathrooms
#         bathrooms_pattern = r'Bathrooms:\s*([^<]+)'
#         match = re.search(bathrooms_pattern, zillow_property_data)
#         zillow_model.bathrooms = match.group(1) if match else ""
#
#         homeType_pattern = r'(?<=\\"homeType\\":\\")[^"]*(?=\\")'
#         zillow_model.homeType = re.search(homeType_pattern, zillow_property_data).group() if re.search(
#             homeType_pattern, zillow_property_data) else ""
#
#         # Heating features
#         heating_pattern = r'Heating features:\s*([^<]+)'
#         match = re.search(heating_pattern, zillow_property_data)
#         zillow_model.heating = match.group(1) if match else ""
#
#         # Cooling features
#         cooling_pattern = r'Cooling features:\s*([^<]+)'
#         match = re.search(cooling_pattern, zillow_property_data)
#         zillow_model.cooling = match.group(1) if match else ""
#
#         # Parking features
#         parking_pattern = r'Parking features:\s*([^<]+)'
#         match = re.search(parking_pattern, zillow_property_data)
#         zillow_model.parking = match.group(1) if match else ""
#
#         # Exterior features
#         exterior_pattern = r'Exterior features:\s*([^<]+)'
#         match = re.search(exterior_pattern, zillow_property_data)
#         zillow_model.exterior = match.group(1) if match else ""
#
#         # Parcel number
#         parcel_num_pattern = r'Parcel number:\s*([^<]+)'
#         match = re.search(parcel_num_pattern, zillow_property_data)
#         zillow_model.parcel_num = match.group(1) if match else ""
#
#         # Construction materials
#         construction_materials_pattern = r'Construction materials:\s*([^<]+)'
#         match = re.search(construction_materials_pattern, zillow_property_data)
#         zillow_model.construction_materials = match.group(1) if match else ""
#
#         # Roof
#         roof_pattern = r'Roof:\s*([^<]+)'
#         match = re.search(roof_pattern, zillow_property_data)
#         zillow_model.roof = match.group(1) if match else ""
#
#         street_pattern = r'(?<="aamgnrc1":")[^"]*(?=")'
#         zillow_model.street = re.search(street_pattern, zillow_property_data).group() if re.search(
#             street_pattern, zillow_property_data) else ""
#
#         city_pattern = r'(?<="city":")[^"]*(?=")'
#         zillow_model.city = re.search(city_pattern, zillow_property_data).group() if re.search(
#             city_pattern, zillow_property_data) else ""
#
#         state_pattern = r'(?<="state":")[^"]*(?=")'
#         zillow_model.state = re.search(state_pattern, zillow_property_data).group() if re.search(
#             state_pattern, zillow_property_data) else ""
#
#         zip_pattern = r'(?<="zip":")[^"]*(?=")'
#         zillow_model.zip = re.search(zip_pattern, zillow_property_data).group() if re.search(
#             zip_pattern, zillow_property_data) else ""
#
#         county_pattern = r'(?<="cnty":")[^"]*(?=")'
#         zillow_model.county = re.search(county_pattern, zillow_property_data).group() if re.search(
#             county_pattern, zillow_property_data) else ""
#
#         events_pattern = r'(?<=label=")Date: .*?Event: .*?(?=" class=)'
#         events = re.findall(events_pattern, zillow_property_data)
#         # Check if events are found before assigning to zillow_model.events
#         zillow_model.events = events if events else ""
#
#         schools_pattern = r'(?<=,\\"schools\\":).*?]'
#         match = re.search(schools_pattern, zillow_property_data)
#         schools = []
#         if match:
#             try:
#                 schools = match.group(0).replace('\\"', '\"')
#                 schools = SchoolModel.from_json(schools)
#             except Exception as e:
#                 print(e)
#                 schools = []
#         zillow_model.schools = schools
#
#         return zillow_model
#
#
#     @staticmethod
#     def get_zillow_property_uncleaned_data(zillow_link: str)-> str:
#         driver.get(zillow_link)  # Replace this with your target URL
#
#         return driver.page_source
#
#     @staticmethod
#     def close_driver():
#         driver.quit()
#
#     @staticmethod
#     def get_zillow_property_data(zillow_link: str)-> ZillowModel:
#         uncleaned_data = ZillowScraper.get_zillow_property_uncleaned_data(zillow_link)
#
#         return ZillowScraper.clean_zillow_property_data(uncleaned_data)
#
#
# # driver.get("https://www.whatismybrowser.com/#google_vignette")
# # # uncleaned_data =ZillowScraper.get_zillow_property_uncleaned_data("https://www.zillow.com/homes/134-Marwood-Dr-Pittsburgh,-PA-15241_rb/")
# # # uncleaned_data =ZillowScraper.get_zillow_property_uncleaned_data("https://www.zillow.com/homes/506-Oak-Ave-Elizabeth,-PA-15037_rb/")
# # uncleaned_data =ZillowScraper.get_zillow_property_uncleaned_data("https://www.zillow.com/homes/88-Oakwood-Rd-Pittsburgh-PA-15205_rb/")
# # uncleaned_data =ZillowScraper.get_zillow_property_uncleaned_data("https://www.zillow.com/homes/1010-MCCLURE-ST-HOMESTEAD,-PA-15120_rb/")
# #
# #
# #
# # cleaned_data = ZillowScraper.clean_zillow_property_data(uncleaned_data)
# # print(uncleaned_data)
# # print(f'zestimate:  {cleaned_data.zestimate}')
# # print(f'zestibuck:  {cleaned_data.zestibuck}')
# # print(f'yrblt:  {cleaned_data.yrblt}')
# # print(f'lot_size:  {cleaned_data.lot_size}')
# # print(f'sqftrange:  {cleaned_data.sqftrange}')
# # print(f'sqft:  {cleaned_data.sqft}')
# # print(f'bedrooms:  {cleaned_data.bedrooms}')
# # print(f'bathrooms:  {cleaned_data.bathrooms}')
# # print(f'homeType:  {cleaned_data.homeType}')
# # print(f'heating:  {cleaned_data.heating}')
# # print(f'cooling:  {cleaned_data.cooling}')
# # print(f'parking:  {cleaned_data.parking}')
# # print(f'exterior:  {cleaned_data.exterior}')
# # print(f'parcel_num:  {cleaned_data.parcel_num}')
# # print(f'construction_materials:  {cleaned_data.construction_materials}')
# # print(f'roof:  {cleaned_data.roof}')
# #
# # print(f'street:  {cleaned_data.street}')
# # print(f'city:  {cleaned_data.city}')
# # print(f'state:  {cleaned_data.state}')
# # print(f'zip:  {cleaned_data.zip}')
# # print(f'county:  {cleaned_data.county}')
# #
# # print(cleaned_data.get_events_as_string())
# # print(cleaned_data.get_schools_as_string())
#
#
#
#
#
#
#
#
#

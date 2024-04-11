pin_input = input("Enter comma seperated pincodes/area name:- ")
pincodes = pin_input.split(",")

pincodes=list(set(pincodes))

print(len(pincodes))

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from amplitude import Amplitude, BaseEvent

import re
import os
import json
import time


from bs4 import BeautifulSoup

amplitude = Amplitude(api_key='9c409472a568606cd3135e6f7908c434')

actual_city = input("Enter city name if pincodes are from same city or just enter no, Note this is the file name data is being added to:- ")

import pandas as pd

event_properties = {
    "user_id": pin_input,
}

event_body = {
    "user_id": pin_input,
    "event_type": "Scrapping_Started",
    "time": int(time.time() * 1000),  # Current time in milliseconds
}

event = BaseEvent(event_type="scrapping", user_id=pin_input)

amplitude.track(event)

def insert_data_to_excel(file_path, data_lists, sheet_name='Sheet1'):
    # Create a DataFrame from the data_lists
    data = {'Column1': data_lists[0], 'Column2': data_lists[1], 'Column3': data_lists[2]}
    df = pd.DataFrame(data)

    # Check if the file exists
    if os.path.exists(file_path):
        # Load the existing Excel file
        existing_df = pd.read_excel(file_path, sheet_name)
        
        # Append new data to the existing DataFrame

        updated_df = existing_df._append(df, ignore_index=True)

        # Write the updated DataFrame back to the Excel file
        updated_df.to_excel(file_path, index=False, sheet_name=sheet_name)

        print(f"Data appended to existing file: {file_path}")

    else:
        # Create a new Excel file
        df.to_excel(file_path, index=False, sheet_name=sheet_name)

        print(f"Data written to new file: {file_path}")



#city = input('Enter locality/pincode :- ')
keyword = input('Enter Keyword:- ')

# city = "560001"
# keyword = "brokers"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)
# locality = 'Bangalore'
# city = 'Marthahalli'
# time.sleeP(10)


for i in pincodes:
	time.sleep(5)
	prop_name =[]
	prop_number =[]
	city = str(i)
	#listPageSearchLocality
	#driver.get("https://www.google.com")
	print(f"Pincode:- {city}")
	driver.get("https://www.google.com/search?sca_esv=572136157&tbs=lf:1,lf_ui:2&tbm=lcl&sxsrf=AM9HkKm5-8noxsveYPpsZrOhyvFXFjyY6Q:1696940491941&q=brokers+in+bangalore&rflfq=1&num=10&sa=X&ved=2ahUKEwih2Of5u-uBAxWdcmwGHQPeCIkQjGp6BAhDEAE#rlfi=hd:;si:;mv:[[13.0349001,77.7147157],[12.910548299999999,77.5470954]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2")
	driver.maximize_window()
	time.sleep(10)
	wait.until(EC.element_to_be_clickable((By.XPATH, 
	    "/html/body/div[2]/div[2]/form/div[1]/div[1]/div[2]/div/div[3]/div[1]"))).click()
	driver.find_element(By.ID,"APjFqb").send_keys( keyword+" in "+city+Keys.ENTER)
	# driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
	print("Scrapping in progress...............")
	while True:
		try:
			time.sleep(5)
			driver.get(driver.find_element("id","pnnext").get_attribute('href'))
			soup = BeautifulSoup(driver.page_source,'html.parser')
			for div in soup.select('.rllt__details'):
				try:
					name = div.findChildren("div")[3].text
					prop = div.findChildren("div")[0].text
				except:
					continue
				if "·" in name:
					prop_number.append(name[name.rindex("·")+2:].replace(" ",""))
					prop_name.append(prop)
				else:
					try:
						int(name.replace(" ",""))
						prop_number.append(name.replace(" ",""))
						prop_name.append(prop)
					except:
						pass
		except:
			break

	print("Scrapping over, converting the data.....")
	print(f"The length of props in {city} is {len(prop_name)}")
	db = {k:v for k,v in zip(prop_name, prop_number)}
	#print(db)

	def write_json(new_data, filename=f'{city}.json'):
	    with open(filename,'r+') as file:
	          # First we load existing data into a dict.
	        file_data = json.load(file)
	        # Join new_data with file_data inside emp_details
	        file_data.update(new_data)
	        # Sets file's current position at offset.
	        file.seek(0)
	        # convert back to json.
	        json.dump(file_data, file, indent = 2)

	path = f'./{city}.json'

	if os.path.isfile(path):
		print("File exists")
		write_json(db)
	else:
		with open(f"{city}.json", "w+") as f:
			json.dump(db, f, indent=2)
		write_json(db)

	if actual_city == "no":
		file_path = f'./{city}.xlsx'
		sheet_name = city
	else:
		file_path = f'./{actual_city}.xlsx'
		sheet_name = actual_city
	list_of_area_or_pincode = [city]*len(prop_name)
	data_lists=[
		prop_name,
		prop_number,
		list_of_area_or_pincode
	]

	insert_data_to_excel(file_path, data_lists, sheet_name)






import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

# Initialize the WebDriver
driver = webdriver.Chrome()  # Ensure correct path to chromedriver if needed
driver.get('https://www.nepalstock.com.np/')
time.sleep(5)

# Wait for date to be visible
date_div = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "ticker__date"))
)
date_span = date_div.find_element(By.TAG_NAME, "span")
print(f"Date: {date_span.text}")

# Wait for the gainer button to be visible and clickable
gainer_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "nepsemarket__gl"))
)

# Click the 'Top Gainers' tab
top_gainer_button = gainer_button.find_element(By.ID, 'gainers-tab')
top_gainer_button.click()

# Wait for the table to load
table1 = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "(//table[contains(@class, 'table')])[3]"))
)

# Initialize list to store top gainers
top_gainer = []

# Find the table body
body = table1.find_element(By.TAG_NAME, "tbody")

# Retry locating elements inside the loop to avoid StaleElementReferenceException
rows = body.find_elements(By.TAG_NAME, 'tr')
for row in rows:
    try:
        # Re-fetch row elements to avoid stale reference issues
        columns = row.find_elements(By.TAG_NAME, 'td')

        if len(columns) >= 4:  # Ensure the row has enough columns
            company_details = {
                'name': columns[0].find_element(By.TAG_NAME, 'a').text,
                'LTP': columns[1].text,
                'Pt. change': columns[2].text,
                '% change': columns[3].text
            }
            top_gainer.append(company_details)

    except StaleElementReferenceException:
        # If the element is stale, skip this iteration and try with the next row
        print("StaleElementReferenceException encountered, skipping row.")
        continue

# Write the top gainers to a JSON file
with open('top_gainer.json', 'w') as json_file:
    json.dump(top_gainer, json_file, indent=4)

print("Top gainers data saved to 'top_gainer.json'")

# Wait for the loser button to be visible and clickable
loser_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'losers-tab'))
)

# Click the 'Top Losers' tab
loser_button.click()

# Wait for the table to load
tablel = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "(//table[contains(@class, 'table')])[4]"))
)

# Initialize list to store top losers
top_loser = []

# Find the table body
bodyl = tablel.find_element(By.TAG_NAME, "tbody")

# Retry locating elements inside the loop to avoid StaleElementReferenceException
rowsl = bodyl.find_elements(By.TAG_NAME, 'tr')
for row in rowsl:
    try:
        # Re-fetch row elements to avoid stale reference issues
        columns = row.find_elements(By.TAG_NAME, 'td')

        if len(columns) >= 4:
            company_details = {
                'name': columns[0].find_element(By.TAG_NAME, 'a').text,
                'LTP': columns[1].text,
                'Pt. change': columns[2].text,
                '% change': columns[3].text
            }
            top_loser.append(company_details)

    except StaleElementReferenceException:
        # If the element is stale, skip this iteration and try with the next row
        print("StaleElementReferenceException encountered, skipping row.")
        continue

# Write the top losers to a JSON file
with open('top_loser.json', 'w') as json_file:
    json.dump(top_loser, json_file, indent=4)

print("Top losers data saved to 'top_loser.json'")

# Wait for the "Top Turnover" table to load (fixing the XPath)
table_t = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "(//table[contains(@class, 'table')])[5]"))
)

top_turnover = []

body_t = table_t.find_element(By.TAG_NAME, "tbody")
rows_t = body_t.find_elements(By.TAG_NAME, 'tr')

# Loop through the rows of the "Top Turnover" table
for row in rows_t:
    try:
        columns = row.find_elements(By.TAG_NAME, 'td')

        if len(columns) >= 3:
            company_details = {
                'name': columns[0].find_element(By.TAG_NAME, 'a').text,
                'turnover': columns[1].text,
                'LTP': columns[2].text
            }

            top_turnover.append(company_details)

    except StaleElementReferenceException:
        print("StaleElementReferenceException encountered, skipping row.")
        continue

# Write the top turnover to a JSON file
with open('top_turnover.json', 'w') as json_file:
    json.dump(top_turnover, json_file, indent=4)

print("Top turnover data saved to 'top_turnover.json'")

# Close the browser
driver.quit()

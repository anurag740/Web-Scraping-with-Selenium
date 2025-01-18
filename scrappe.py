import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
service = Service('/your chromedriver path')
driver = webdriver.Chrome(service=service, options=options)

def extract_case_study_data(case_url):
    try:
        driver.get(case_url)

        # Extract Company Name
        company_name_element = driver.find_elements(By.XPATH, '//span[contains(text(), "Customer:")]/following-sibling::a')
        company_name = company_name_element[0].text if company_name_element else 'N/A'

        # Extract Industry / Vertical
        industry_element = driver.find_elements(By.XPATH, '//span[contains(text(), "Industry:")]')
        industry = industry_element[0].find_element(By.XPATH, './parent::node()').text.replace('Industry:', '').strip() if industry_element else 'N/A'

        # Extract Quoted Person and Role
        quote_element = driver.find_elements(By.XPATH, '//p[contains(@class, "mb-0")]')
        person_quoted = quote_element[0].text.split('—')[1].split(',')[0].strip() if quote_element else 'N/A'
        role = ','.join(quote_element[0].text.split('—')[1].split(',')[1:]).strip() if quote_element else 'N/A'

        # Extract Region and Country
        location_element = driver.find_elements(By.XPATH, '//span[contains(text(), "Location:")]')
        location = location_element[0].find_element(By.XPATH, './parent::node()').text.replace('Location:', '').strip() if location_element else 'N/A'
        country = location.split('with')[0].strip() if 'with' in location else location

        return {
            'Company Name': company_name,
            'Industry / Vertical': industry,
            'Person Quoted': person_quoted,
            'Role / Designation': role,
            'Region': location,
            'Country': country
        }

    except Exception as e:
        print(f"Error extracting data from {case_url}: {e}")
        return {
            'Company Name': 'N/A',
            'Industry / Vertical': 'N/A',
            'Person Quoted': 'N/A',
            'Role / Designation': 'N/A',
            'Region': 'N/A',
            'Country': 'N/A'
        }


url = "https://www.genesys.com/customer-stories"
driver.get(url)


try:
    print("Locating case study links...")
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/customer-stories/")]'))
    )
    case_links = driver.find_elements(By.XPATH, '//a[contains(@href, "/customer-stories/")]')
    case_urls = [link.get_attribute('href') for link in case_links]
    print(f"Found {len(case_urls)} case study links.")
except Exception as e:
    print(f"Error locating case study links: {e}")
    driver.quit()
    exit()

all_data = []
for url in case_urls:
    print(f"Scraping {url}")
    case_data = extract_case_study_data(url)
    all_data.append(case_data)

driver.quit()



df = pd.DataFrame(all_data)
df.drop_duplicates(inplace=True)
output_file = 'genesys_case_studies.csv'
df.to_csv(output_file, index=False)
print(f"Data successfully saved to {output_file}")

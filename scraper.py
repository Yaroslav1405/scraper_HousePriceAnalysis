# Import required modules
from seleniumbase import Driver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


def extract_data(MAX_PAGES=55):

    # Initialize an empty dictionary to store apartment data
    apts_data = {}
    
    # Create DataFrame to store apartments data
    df = pd.DataFrame(columns=[
        'District', 'Address', 'Price', 'Area', 'Rooms', 'Floor', 
        'Material', 'Year', 'Renovated', 'Published'
    ])
    # Initialize page count and driver
    page_count = 1
    driver = Driver(uc=True)


    while page_count < MAX_PAGES:
        # Set URL for scraping
        scrape_url = f'https://flatfy.ua/uk/%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B6-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80-%D0%BB%D1%8C%D0%B2%D1%96%D0%B2?page={page_count}'
        
        # Open URL and wait for the page to load
        driver.uc_open_with_reconnect(scrape_url, 20)
        wait = WebDriverWait(driver, 20)
        wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "realty-preview__base"))
        )
        
        # Load all listings on the page with Soup
        soup = BeautifulSoup(driver.page_source, 'lxml')
        listings = soup.find_all('div', class_='feed-layout__item-holder')
        
        # For loop to go over all listings on the page
        for listing in listings:
            # Find apartment data
            data = listing.find('div', class_='realty-preview__content-column')
            
            if not data:
                continue
            
            # Extract data from the listing
            try: 
                district_tag = data.find('a', class_='realty-preview-sub-title')
                district = district_tag.text.strip() if district_tag else 'N/A'

                address_tag = data.find('h3', class_='realty-preview-title')
                address = address_tag.text.strip() if address_tag else 'N/A'

                price_tag = data.find('div', class_='realty-preview-price--main')
                price = price_tag.text.strip() if price_tag else 'N/A'
            
                
                # Function to extract additional information
                properties = data.find_all('div', class_='realty-preview-properties-item')    
                def get_additional_info(index):
                    try:
                        info = properties[index].find('span', class_='realty-preview-info')
                        return info.text.strip() if info else 'N/A'
                    
                    except IndexError:
                        return 'N/A'
                    
                # Extract additional information
                rooms = get_additional_info(0)
                area = get_additional_info(1)
                floor = get_additional_info(2)
                renovated = get_additional_info(3)
                material = get_additional_info(4)
                year = get_additional_info(5)

                # Extract date published
                date_published = data.find_all('div', class_='Grid-module_col__der3x Grid-module_col6__mDNQA')
                date_published = date_published[1].get_text(strip=True)
                
                # Store current apartment data in a dictionary
                apts_data = {
                    'District': district,
                    'Address': address,
                    'Price': price,
                    'Area': area,
                    'Rooms': rooms,
                    'Floor': floor,
                    'Material': material,
                    'Year': year,
                    'Renovated': renovated,
                    'Published': date_published
                }
                
                # Concatenate the new data with the existing DataFrame
                df = pd.concat([df, pd.DataFrame([apts_data])], ignore_index=True)
                time.sleep(5)
                
            except Exception as e:
                print(f"Error extracting data: {e}")
                
        # Save data to CSV after each page load    
        print('Saving data from page: ', page_count)
        df.to_csv('houseData.csv', index=False)
        page_count += 1
        
    # Quit the driver
    driver.quit()
    
def main():
    start_time = time.time()
    extract_data()
    print('*'*40)
    print(f'\n\nTime to complete the scraping: {time.time()-start_time} seconds\n\n')
    print('*'*40)
    
if __name__ == '__main__':
    main()
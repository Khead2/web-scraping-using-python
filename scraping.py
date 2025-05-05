from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd

url = "https://www.tokopedia.com/nova-collection99/review"  # Example: "https://www.tokopedia.com/p/handphone-tablet/handphone-smartphone?src=search&ob=5&st=product"


options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)
driver.get(url)  # Run in headless mode (no GUI)

data = []
for i in range(0, 3):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    container = soup.find_all('article', attrs={'class':'css-1pr2lii'})

    for containers in container:
        try:
            nama = containers.find('span', attrs={'class':'name'}).text
            review = containers.find('span', attrs={'data-testid':'lblItemUlasan'}).text
            rate_container = containers.find('div', attrs={'data-testid':'icnStarRating'})
            rate = rate_container.get('aria-label') if rate_container else 'Tidak ada'.text
            
            data.append(
                {
                    'Nama': nama,
                    'Ulasan': review,
                    'Rating' : rate
                    
                }
                
            ) # Wait for the page to load``
        except AttributeError:
            continue

time.sleep(2)
driver.find_element(By.CSS_SELECTOR, "button[aria-label^='Laman berikutnya']").click()
time.sleep(3)

print(data)
df = pd.DataFrame(data, columns=['Nama','Ulasan','Rating'])
df.to_csv("Tokopedia.csv", index=False)
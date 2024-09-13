from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}


# Extract data form the biggest European retailer.
class DataExtract:
    def __init__(self):
        self.company_name = []
        self.product_name = []
        self.product_price = []

    # Use BeautifulSoup to extract first company data. Company Name, Product Name, Product Price.
    # Also, can extract link for product.
    def first_company(self):
        response = requests.get("https://en.zalando.de/mens-clothing-jeans-skinny-fit/lee-jeans/?order=activation_date")
        data = response.text
        soup = BeautifulSoup(data, "html.parser")

        all_name_elements = soup.select(".Zhr-fS h3")
        for name in all_name_elements:
            if len(name.text) < 4:
                self.company_name.append(name.text)
            else:
                self.product_name.append(name.text)

        all_price = soup.select("._78xIQ- p .lystZ1")
        for price in all_price:
            self.product_price.append(price.text.replace("\xa0", ""))

    # Use BeautifulSoup to extract second company data. Company Name, Product Name, Product Price.
    # Also, can extract link for product.
    def second_company(self):
        response = requests.get("https://en.zalando.de/mens-clothing-jeans-skinny-fit/levi/?order=activation_date")
        data = response.text
        soup = BeautifulSoup(data, "html.parser")
        all_name_elements = soup.select(".EKabf7")
        for name in all_name_elements:
            if name.text == "Levi's®":
                self.company_name.append(name.text)

        all_prod_name = soup.select("header > .Zhr-fS >.sDq_FX")
        for prod_name in all_prod_name:
            self.product_name.append(prod_name.text)

        all_price = soup.select("p > .sDq_FX")
        for price in all_price:
            if "€" in price.text:
                self.product_price.append(price.text.replace("\xa0", ""))

    # Use Selenium for store data and compare in Google Form. Also, can create Excel document.
    def store_data(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-search-engine-choice-screen")
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=chrome_options)

        for n in range(len(self.company_name)):
            driver.get("NewGoogleFormDoc")

            company_name_access = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/'
                                                                      'div/div[2]/div/div[1]/div/div[1]/input')
            company_name_access.click()
            time.sleep(1)
            company_name_access.send_keys(self.company_name[n])

            product_name_access = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/'
                                                                      'div/div[2]/div/div[1]/div/div[1]/input')
            product_name_access.click()
            time.sleep(1)
            product_name_access.send_keys(self.product_name[n])

            product_price_access = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/'
                                                                       'div/div[2]/div/div[1]/div/div[1]/input')
            product_price_access.click()
            product_price_access.send_keys(self.product_price[n])
            button = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
            button.click()
        driver.quit()


bot = DataExtract()
bot.first_company()
bot.second_company()
bot.store_data()

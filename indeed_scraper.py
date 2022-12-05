import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


# create class for our scraper
class IndeedScraper:
    # setup options and webdriver from selenium
    chrome_options = Options()
    # need to add 'user-gent' in you use headless mode
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                '(KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36')
    # this option will start your browser in the background
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()),
                              options=chrome_options)

    def __init__(self, web_page, occupation, location, numbers_of_pages):
        self.web_page = web_page
        self.occupation = occupation
        self.location = location
        self.numbers_of_pages = numbers_of_pages
        self.job_list = []

    # function inserts users inputs into submit from
    def submit_form(self):
        self.driver.get(self.web_page)
        self.driver.implicitly_wait(0.5)
        # insert users occupation
        self.driver.find_element(By.XPATH,
                                 "/html/body/div/div[2]/div/span/div[4]/div[2]/div/div/div/div/form/div/div[1]/div/div[1]/div/div[2]/input").send_keys(
            self.occupation)
        # activate element by adding javascript
        element = self.driver.find_element(By.XPATH, '//*[@id="text-input-where"]')
        self.driver.execute_script("arguments[0].click();", element)
        # activate element to be able to delete pre installed values
        self.driver.find_element(By.XPATH, '//*[@id="text-input-where-suggestion-list"]/ul/li').click()
        time.sleep(2)
        # deleted pre install values
        self.driver.find_element(By.XPATH, '//*[@id="jobsearch"]/div/div[2]/div/div[1]/div/div[2]/span').click()
        # insert users location
        self.driver.find_element(By.XPATH, '//*[@id="text-input-where"]').send_keys(self.location, Keys.ARROW_DOWN)
        time.sleep(2)
        try:
            # select firs element from drop down menu
            select_one = self.driver.find_element(By.XPATH, '//*[@id="text-input-where-suggestion-list-selected"]')
            self.driver.execute_script("arguments[0].click();", select_one)
        # user made some typos in location so no suggestions can be fined
        except NoSuchElementException:
            print("Probably your location is wrong , but we will try to find something")
        finally:
            # submit form
            self.driver.find_element(By.ID, 'jobsearch').submit()

        return self.driver

    def scrape_job(self, driver):
        try:
            # find all elements with jobs descriptions
            driver.find_element(By.CSS_SELECTOR, "td.resultContent")
            text_box = driver.find_elements(By.CSS_SELECTOR, "td.resultContent")
            driver.implicitly_wait(3)
            # return list of elements
            return text_box
        except NoSuchElementException:
            # if nothing was found you will see some hints in prompt
            no_result = driver.find_element(By.CSS_SELECTOR, "div.jobsearch-NoResult-messageHeader")
            print(no_result.get_attribute("textContent"))
            print("Search suggestions: ")
            suggestions = driver.find_elements(By.CSS_SELECTOR, "ul.jobsearch-NoResult-suggestions")
            for x in suggestions:
                sug_result = x.get_attribute("innerHTML")
                soup = BeautifulSoup(sug_result, "html.parser")
                sugg_list = soup.find_all("li")
                for _ in sugg_list:
                    text_hints = _.text
                    print(" ", f"{text_hints}")
            exit()

    # loop through all element in the list which was returned from scrape_job function
    def scrape_loop(self, text_box):
        for job in text_box:
            # getting html from element
            resalt = job.get_attribute("innerHTML")
            # using BeautifulSoup to get all data
            soup = BeautifulSoup(resalt, "html.parser")
            try:
                title = soup.find("a", class_="jcs-JobTitle css-jspxzf eu4oa1w0").text
            except:
                title = "None"
            try:
                company_name = soup.find("span", class_="companyName").text
            except:
                company_name = "None"
            try:
                location = soup.find("div", class_="companyLocation").text
            except:
                location = "None"
            try:
                wage = soup.find("div", class_="attribute_snippet").text
            except:
                wage = "None"
            # append data to empty "job_list"
            self.job_list.append({"Title": title, "Company name": company_name, "Location": location, "Wage": wage})

    # trying to find next page element also close subscription pop-up
    def nex_page(self, n):
        if n > 0:
            try:
                self.driver.find_element(By.CSS_SELECTOR, "a[data-testid='pagination-page-next']").click()
            except ElementClickInterceptedException:
                self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/button").click()
            try:
                self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/button").click()
            except NoSuchElementException or ElementClickInterceptedException:
                pass

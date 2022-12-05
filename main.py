import json
from indeed_scraper import *
from chek_user_input import *

# create some variable with webpage
web_p = "https://ca.indeed.com/"

# prompting the user for input
user_input_occupations = input("Wright desired occupation: ")
user_input_location = input("Wright location where to search: ")
user_numbers_of_pages = check_input()

# creating class example with our parameters
crawl = IndeedScraper(web_p, user_input_occupations, user_input_location, user_numbers_of_pages)

# call class method to submit form with user input
dr = crawl.submit_form()

while user_numbers_of_pages:
    # getting all elements with jobs description
    t_box = crawl.scrape_job(dr)
    # scrape and append data to job_list
    crawl.scrape_loop(t_box)
    user_numbers_of_pages -= 1
    # move to the next page
    crawl.nex_page(user_numbers_of_pages)

crawl.driver.quit()
# creating and writing data to file
with open("ca.indeed.json", "w", encoding="utf-8") as f:
    json.dump(crawl.job_list, f, ensure_ascii=False)
print("Scraped data has been written to dump file ")


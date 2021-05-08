from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import parameters
from time import sleep
from parsel import Selector
import csv 

def validate_field(field):
    field = 'No Results'
    return field

writer = csv.writer(open(parameters.file_name,'w'),delimiter=',',quoting=csv.QUOTE_MINIMAL)
writer.writerow(['Name', 'Job Title', 'Company', 'Location', 'URL'])

# initiate webdriver Chrome
driver = webdriver.Chrome('C:/chromedriver/bin/chromedriver')

# Navigate to a page: linkedin.com
driver.get('https://www.linkedin.com')

# Login credentials: username and password * Password is not protected here
username = driver.find_element_by_class_name('login-email')
username.send_keys(parameters.linkedin_username)
sleep(0.5)

password = driver.find_element_by_class_name('login-password')
password.send_keys(parameters.linkedin_password)
sleep(0.5)

login_button = driver.find_element_by_id('login-submit')
login_button.click()
sleep(0.5)

# google search
driver.get('https://www.google.com')
sleep(3)

search_query = driver.find_element_by_name('q')
search_query.send_keys(parameters.search_query)
sleep(0.5)

search_query.send_keys(Keys.RETURN)
sleep(3)

# Extract LinkedIn URLS
linkedin_urls = driver.find_elements_by_class_name('iUh30')
linkedin_urls = [url.text for url in linkedin_urls]
sleep(0.5)

for url in linkedin_urls:
    driver.get(url)
    sleep(5)
    sel = Selector(text=driver.page_source)

    name = sel.xpath('//*[starts-with(@class,"pv-top-card-section__name")]/text()').extract_first()

    if name:
        name = name.strip()
    else:
        name = validate_field(name)
    job_title = sel.xpath('//*[starts-with(@class,"pv-top-card-section__headline")]/text()').extract_first()

    if job_title:
        job_title = job_title.strip()
    else:
        job_title = validate_field(job_title)

    company = sel.xpath('//*[starts-with(@class,"pv-top-card-v2-section__entity-name pv-top-card-v2- \
        section__company-name")]/text()').extract_first()

    if company:
        company = company.strip()
    else:
        company = validate_field(company)

    location = sel.xpath('//*[starts-with(@class, \
            "pv-top-card-section__location")]/text()').extract_first()

    if location:
        location = location.strip()
    else:
        location = validate_field(location)

    linkedin_url = driver.current_url
    writer.writerow([name,job_title,company,location,linkedin_url])
    
driver.quit()




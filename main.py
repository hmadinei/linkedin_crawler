from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import logging
import parameters


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options, executable_path=CHROMEDRIVER_PATH) 
    
    return driver
    
def linkedin_sign_in(URL):

    driver.get(URL)
    
    username = driver.find_element(by='id', value='session_key')
    username.send_keys(parameters.linkedin_username)
    sleep(0.5)
    
    password = driver.find_element(by='id', value='session_password')
    password.send_keys(parameters.linkedin_password)
    sleep(0.5)
    
    sign_in_button = driver.find_element(by='xpath', value='//*[@type="submit"]')
    sign_in_button.click()
    sleep(2)


def find_connections():
    
    network_url = LINKEDIN_URL + '/mynetwork/invite-connect/connections/'
    
    driver.get(network_url)    
    sleep(5)
    
    a_tags = driver.find_elements(by='css selector', value='div a')
    all_urls = [a_tag.get_attribute('href') for a_tag in a_tags]
    
    linkedin_urls = [(url) for url in all_urls if url.startswith('https://www.linkedin.com/in')]
    # remove duplicated url
    linkedin_urls = list(set(linkedin_urls)) 
    
    for linkedin_url in linkedin_urls:
        fetch_connections_data(linkedin_url)
    
def fetch_connections_data(linkedin_url):
    driver.get(linkedin_url)
    sleep(5)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # find name
    name = soup.find('h1', {'class': 'text-heading-xlarge inline t-24 v-align-middle break-words'})

    if name:
        name = name.get_text().strip()

    # find job title
    job_title = soup.find('div', {'class': 'text-body-medium break-words'})

    if job_title:
        job_title = job_title.get_text().strip()

    # find company
    company = soup.find('div', {'aria-label': 'Current company'})

    if company:
        company = company.get_text().strip()
        
    # find college
    college = soup.find('div', {'aria-label': 'Education'})

    if college:
        college = college.get_text().strip()
        
    # find location
    location = soup.find('span', {'class': 'text-body-small inline t-black--light break-words'})

    if location:
        location = location.get_text().strip()
    
    logging.info(name + job_title + company + college + location)
    
    print("******************************")    
    print("name:", name)
    print("job title:", job_title)
    print("company:", company)
    print("college:", college)
    print("location:", location)
    print("******************************\n\n")
    
if __name__ == "__main__":
    
    logging.basicConfig(filename="linkedin.log",
                    filemode='a',
                    format='%(asctime)s, %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
    
    CHROMEDRIVER_PATH = "/home/hannane/Downloads/chromedriver"
    LINKEDIN_URL = "https://www.linkedin.com" 
    
    driver = create_driver()
    linkedin_sign_in(LINKEDIN_URL)
    find_connections()
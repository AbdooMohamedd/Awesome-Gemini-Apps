import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Path to your ChromeDriver
chrome_driver_path = r'chromedriver-win64\chromedriver.exe'

# Define the WebDriver setup without proxy
def setup_driver():
    chrome_options = Options()
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def start_voting(driver):
    try:
        # Open the webpage
        driver.get('https://ai.google.dev/competition/vote')

        time.sleep(2)

        # Click the "Start Voting" button only once
        start_button = driver.find_element(By.CLASS_NAME, 'gemini-start-button')
        ActionChains(driver).move_to_element(start_button).click(start_button).perform()

        time.sleep(2)
        
    except Exception as e:
        print(f"Error during start voting: {e}")

def scrape_projects(driver):
    try:
        # Scroll to the bottom of the page to ensure all projects load
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        page_html = driver.page_source

        soup = BeautifulSoup(page_html, 'html.parser')
        project_links = soup.find_all('a', class_='gemini-vote-card-link')

        project_urls = ['https://ai.google.dev' + link.get('href') for link in project_links if link.get('href')]

        return project_urls
    except Exception as e:
        print(f"Error during scraping: {e}")
        return []

def save_to_csv(urls, filename='project_links.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['URL'])
        for url in urls:
            writer.writerow([url])

all_project_urls = []

driver = setup_driver()

start_voting(driver)

# Repeat the shuffle and scrape process 100 times (adjust as needed)
for i in range(1500):
    print(f"Shuffle iteration {i + 1}")

    urls = scrape_projects(driver)
    all_project_urls.extend(urls)

    # Click the "Shuffle it up!" button
    try:
        shuffle_button = driver.find_element(By.CLASS_NAME, 'gemini-spin-button')
        ActionChains(driver).move_to_element(shuffle_button).click(shuffle_button).perform()
        print("Clicked the 'Shuffle it up!' button.")
    except Exception as e:
        print("Error finding or clicking the 'Shuffle it up!' button:", e)
        driver.quit()
        exit()

    time.sleep(2)

save_to_csv(all_project_urls)

for url in all_project_urls:
    print(url)

driver.quit()

import time
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from job import Job 

class JobScraper:
    
    def __init__(self, query, location):
        PATH = '/usr/local/bin/chromedriver'
        self.query = query
        self.location = location
        self.service = Service(executable_path=PATH)
        self.driver = webdriver.Chrome(service=self.service)
        
    def __del__(self):
        self.driver.quit()
        
    def compileJobs(self, results, *args):
        jobs = []
        # Job Title, Company, Location, Link - Args Order
        # Create Job Objects from Job Postings
        for count, result in enumerate(results):
            try:
                job_title = result.find_element(by= By.CSS_SELECTOR, value= args[0]).text if result.find_element(by= By.CSS_SELECTOR, value= args[0]) else 'N/A'
                company = result.find_element(by= By.CSS_SELECTOR, value= args[1]).text if result.find_element(by= By.CSS_SELECTOR, value= args[1]) else 'N/A'
                location = result.find_element(by= By.CSS_SELECTOR, value= args[2]).text if result.find_element(by= By.CSS_SELECTOR, value= args[2]) else 'N/A'
                link = result.find_element(by= By.CSS_SELECTOR, value= args[3]).get_attribute('href') if result.find_element(by= By.CSS_SELECTOR, value= args[3]) else 'N/A'
            except:
                pass
            jobs.append(Job(job_title, company, location, link))
        return jobs
    
    def searchIndeed(self):
        self.driver.get('https://www.indeed.com/')
        # Query Job Postings
        self.driver.find_element(by= By.ID, value='text-input-what').send_keys(self.query)
        location_field = self.driver.find_element(by= By.ID, value='text-input-where')
        location_field.click()
        self.driver.find_element(by= By.XPATH, value='//*[@id="jobsearch"]/div/div[2]/div/div[1]/div/div[2]/span').click()
        location_field.send_keys(self.location)
        self.driver.find_element(by= By.XPATH, value='//*[@id="jobsearch"]/button').click()
        # Click on Filter Button
        self.driver.find_element(By.XPATH, '//*[@id="filter-dateposted"]').click()
        # Apply 7-day filter
        self.driver.find_element(By.XPATH,'//*[@id="filter-dateposted-menu"]/li[3]/a').click()
        # Retrieve Job Postings from Each Page
        jobs = []
        while (True):
            try:
                ul = self.driver.find_element(by= By.CSS_SELECTOR, value="ul[class^='jobsearch']")
                results = ul.find_elements(by= By.CSS_SELECTOR, value='div[class^="job_seen"]')
                jobs += self.compileJobs(
                results,
                "span[id^='jobTitle']",
                "span[class^='companyName']",
                "div[class^='companyLocation']",
                "a[class^='jcs-']"
                )
                # Go to next page
                next_page = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"a[data-testid='pagination-page-next']")))
                next_page.click()
            except:
                break
        return jobs
            
            
    def searchZipRecruiter(self):
        self.driver.get('https://ziprecruiter.com/')
        self.driver.find_element(by= By.ID, value='search1').send_keys(self.query)
        location_field = self.driver.find_element(by= By.ID, value='location1')
        location_field.click()
        self.driver.find_element(by= By.XPATH, value='//*[@id="search_form_1"]/div[1]/div[2]/button').click()
        location_field.send_keys(self.location)
        self.driver.find_element(by= By.CSS_SELECTOR, value="button[class^='t_job_search']").click()
        time.sleep(2)
        background = self.driver.find_element(by= By.CSS_SELECTOR, value="div[class^= 'modal-dialog']")
        self.driver.execute_script("arguments[0].click();", background)
        load_button = self.driver.find_element(By.XPATH,'//*[@id="primary"]/section[2]/div/button')
        if (load_button):
            load_button.click()
        count_header = self.driver.find_element(By.XPATH,'//*[@id="job_results_headline"]/h1[2]').text
        count = ''
        for char in count_header:
            if char.isnumeric():
                count += char
        for i in range(int(int(count)/20)):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        results = self.driver.find_elements(by= By.CSS_SELECTOR, value="article[class^='job_result']")
        jobs = []
        jobs += self.compileJobs(
            results,
            "span[class='just_job_title']",
            "a[class^='t_org']",
            "a[class^='t_location']",
            "a[class^='job_link']"
        )
        return jobs
    
    def searchMonster(self):
        pass
    
    def searchCareerBuilder(self):
        pass
    
    def searchGlassDoor(self):
        pass
    

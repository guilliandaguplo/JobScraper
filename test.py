from jobScraper import JobScraper

query = 'software engineering internship'
location = 'fullerton, ca'
scraper = JobScraper(query, location)

scraper.searchZipRecruiter()
scraper.driver.quit()

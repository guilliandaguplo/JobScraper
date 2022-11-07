from jobScraper import JobScraper
from googleSheets import GoogleSheets
from datetime import datetime

def newQuery(query, location, spreadsheetID):
    scraper = JobScraper(query, location)
    jobList = scraper.searchIndeed()
    jobList += scraper.searchZipRecruiter()
    jobSet = set(jobList)

    googleSheets = GoogleSheets(spreadsheet_id=spreadsheetID)
    sheetTitle = datetime.today().strftime('%a %b %-d/%Y')
    newSheet = googleSheets.create(sheetTitle)
    googleSheets.append(jobSet,spreadsheet_id= spreadsheetID, range_name= f'{sheetTitle}!A1:E')
    googleSheets.resizeColumns(newSheet.get('replies')[0]['addSheet']['properties']['sheetId'])
  
def main():
    newQuery('entry-level "child development"', 'fullerton, ca', '1PTdXfsNYQpqGfeGiRdc4EeVywwe_ha9DPLCMwjtRIlc')
    newQuery('entry-level "public health"', 'fullerton, ca', '1wsO3qQVuXOow4g1uKQzOM5NDs7ZZVP88cqZ9BC5jgmw')
    newQuery('"computer science" internship', 'fullerton, ca', '1SLDULmFWKfK03A7bQydnijrqZtb6BIdoquHZ_PA1a9U')
    

if __name__ == '__main__':
    main()
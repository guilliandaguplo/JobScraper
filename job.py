from datetime import datetime


class Job:
    def __init__(self, title='', company='', location='', link=''):
        self.title = title
        self.company = company
        self.location = location
        self.link = link
        self.queryDate = f"Week of {datetime.today().strftime('%d/%m/%Y')}"
       
        
    def __eq__(self, other) -> bool:
        return self.title == other.title and self.company == other.company and self.location == other.location
    
    def __repr__(self) -> str:
        return f"Job({self.title}, {self.company}, {self.location}, {self.queryDate})"
    
    def __hash__(self) -> int:
        return hash((self.link,self.title,self.location))
    
    def get_title(self):
        return self.title

    def get_company(self):
        return self.company
    
    def get_location(self):
        return self.location
    
    def get_postedDate(self):
        return self.queryDate
    
    def getApplicationLink(self):
        return self.link
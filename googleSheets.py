from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly','https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1PTdXfsNYQpqGfeGiRdc4EeVywwe_ha9DPLCMwjtRIlc'
RANGE_NAME = 'Sheet1!A2:E'

class GoogleSheets:
        
    def __init__(self, spreadsheet_id = SPREADSHEET_ID, range_name = RANGE_NAME):
        self.authenticate()
        self.service = build('sheets', 'v4', credentials=self.creds)
        # Call the Sheets API
        self.sheet = self.service.spreadsheets()
        self.spreadsheet_id = spreadsheet_id
        self.range_name = range_name
        
    def authenticate(self):
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
    
    def append(self, jobSet, spreadsheet_id, range_name):
        try:
            body = []
            self.range_name = range_name
            for job in jobSet:
                jobDetails = []
                jobDetails.append(job.get_title())
                jobDetails.append(job.get_company())
                jobDetails.append(job.get_location())
                jobDetails.append(job.getApplicationLink())
                body.append(jobDetails)
            custom_range = range_name[:range_name.find('!')+1]
            values = [
                ['Job Title', 'Company', 'Location', 'Application Link']
            ]
            custom_body = {
                'values': values
            }
            self.sheet.values().update(spreadsheetId=spreadsheet_id, range=f'{custom_range}A1', valueInputOption='USER_ENTERED', body= custom_body).execute()
            self.sheet.values().append(
                spreadsheetId= self.spreadsheet_id, 
                range= self.range_name,
                valueInputOption= 'USER_ENTERED', insertDataOption='INSERT_ROWS', 
                body= {
                    "majorDimension": "ROWS",
                    "values":body
                }
                ).execute()
        except HttpError as err:
            print(err)
            
    def resizeColumns(self, sheet_id):
        try:
            requests = []
            requests.append({
                "autoResizeDimensions": {
                    "dimensions": {
                    "sheetId": sheet_id,
                    "dimension": "COLUMNS",
                    "startIndex": 0,
                    "endIndex": 3
                    }
                }
            })
            body = {
                'requests': requests
            }
            response = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id,body=body).execute()
            return response
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error
    
    def create(self, title):
        try:
            body = {
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': title,
                    }
                }
            }]
            }
            result = self.sheet.batchUpdate(
                spreadsheetId= self.spreadsheet_id,
                body=body).execute()
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

                

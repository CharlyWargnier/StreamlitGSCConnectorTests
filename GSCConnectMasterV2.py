import asyncio
import streamlit as st
import searchconsole
import pandas as pd
import os

st.title("#1 TEST with  Josh's Code")


#from httpx_oauth.clients.google import GoogleOAuth2
#
#from httpx_oauth.oauth2 import OAuth2


#import datetime
#from datetime import date, timedelta
#import httplib2
#from googleapiclient.discovery import build
#from oauth2client.client import OAuth2WebServerFlow
#from collections import defaultdict
#from dateutil import relativedelta
#import argparse
#from oauth2client import client
#from oauth2client import file
#from oauth2client import tools
#import re
#from urllib.parse import urlparse
# 
#site = 'https://www.yoursite.com'    # Property to extract

site = 'https://www.tatielou.co.uk/'    # Property to extract

num_days = 5                    # Number of Days, Months to Extract
#creds = 'client_secrets.json'   # Credential file from GSC
#creds = '/content/GSCTatieLouCredentials.json'

creds = 'JSON_keys\GSCTatieLouCredentialsNonLegacy.json'
#creds = '/content/GSCTatieLouCredentialsNonLegacy02.json'
output = 'gsc_data.csv'


#import json
#x =  '{ "name":"John", "age":30, "city":"New York"}'
#y = json.loads(x)
#st.write(y["age"])

#FinalJSON = 'credentials.json'
#st.write(FinalJSON)
#st.write(type(FinalJSON))

#y = json.loads('credentials.json')
#st.write(y)
#
#st.stop()

# SAVE FINAL credentials.json
# WORKING WORKING WORKING WORKING WORKING WORKING WORKING 


from pathlib import Path

my_file = Path("credentials.json")

if my_file.is_file():
    account = searchconsole.authenticate(client_config='JSON_keys\GSCTatieLouCredentialsNonLegacy.json',credentials='credentials.json')
    st.write('Yes, credentials.json exists')
else:
    account = searchconsole.authenticate(client_config='JSON_keys\GSCTatieLouCredentialsNonLegacy.json',serialize='credentials.json')
    st.write('No, credentials.json doesnt exist')
    # file exists


import json

with open("credentials.json", "r") as f:
    my_dict = json.load(f)
#print(my_dict)
st.header("credentials.json")
st.write(my_dict)



#st.stop()

# lOAD FINAL credentials.json

#Working!
#account = searchconsole.authenticate(client_config='JSON_keys\GSCTatieLouCredentialsNonLegacy.json',credentials='credentials.json')

#account = searchconsole.authenticate(client_config='client_secrets.json',
#                                     credentials='credentials.json')
#

#webproperty = account['https://www.tatielou.co.uk/']
#report = webproperty.query.range('today', days=-7).dimension('query').get()


#st.cache()
#def accountLaunch():
#    searchconsole.authenticate(client_config='JSON_keys\GSCTatieLouCredentialsNonLegacy.json')
#
#accountLaunch()


#account = searchconsole.authenticate(client_config='JSON_keys\GSCTatieLouCredentialsNonLegacy.json')
webproperty = account['https://www.tatielou.co.uk/']
report = webproperty.query.range('today', days=-7).dimension('query').get()


st.checkbox("checkboxTest")

st.write(report.rows)


st.stop()
#let's build a pandas dataframe with the search console data




st.title("#1 Google OAuth2 flow")

"## Configuration"

client_id = st.text_input("Client ID")
client_secret = st.text_input("Client secret")
redirect_uri = st.text_input("Redirect URI", "http://localhost:8000/redirect")

if client_id and client_secret and redirect_uri:
    client = GoogleOAuth2(client_id, client_secret)
else:
    client = None
    
"## Authorization URL"

async def write_authorization_url():
    authorization_url = await client.get_authorization_url(
        redirect_uri,
        scope=["profile", "email"],
        extras_params={"access_type": "offline"},
    )
    st.write(authorization_url)

if client:
    asyncio.run(write_authorization_url())
else:
    "Waiting client configuration..."

"## Callback"

if client:
    code = st.text_input("Authorization code")
else:
    code = None
    "Waiting client configuration..."

"## Access token"

async def write_access_token(code):
    token = await client.get_access_token(code, redirect_uri)
    st.write(token)

if code:
    asyncio.run(write_access_token(code))
    st.write(type(code))
else:
    "Waiting authorization code..."

########################


import pandas as pd

def get_search_console_data(webproperty, days=-365):
  if webproperty is not None:
    query = webproperty.query.range(start='today', days=days).dimension('date')
    r = query.get()
    df = pd.DataFrame(r.rows)
    return df

  print("Web property doesn't exist, please select a valid one from this list")
  print(account.webproperties)

  return None

df = get_search_console_data(webproperty)


st.write(df)



#account = searchconsole.authenticate(client_config="GSCTatieLouCredentials.json", serialize='credentials.json', flow="console")
#account = searchconsole.authenticate(client_config=creds, serialize="authorizedcreds.dat", flow="console")

account = searchconsole.authenticate(client_config=creds, credentials="authorizedcreds.dat")

#account = searchconsole.authenticate(client_config='client_secrets.json',
#                                     credentials='credentials.json')

st.stop()



# Get Domain Name to Create a Project
def get_domain_name(start_url):
    domain_name = '{uri.netloc}'.format(uri=urlparse(start_url))  # Get Domain Name To Name Project
    domain_name = domain_name.replace('.','_')
    return domain_name
 
 
# Create a project Directory for this website
def create_project(directory):
    if not os.path.exists(directory):
        print('Create project: '+ directory)
        os.makedirs(directory)
 
def authorize_creds(creds):
    # Variable parameter that controls the set of resources that the access token permits.
    SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly'] 
 
    # Path to client_secrets.json file
    CLIENT_SECRETS_PATH = creds
 
    # Create a parser to be able to open browser for Authorization
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[tools.argparser])
    flags = parser.parse_args([])
 
    flow = client.flow_from_clientsecrets(
        CLIENT_SECRETS_PATH, scope = SCOPES,
        message = tools.message_if_missing(CLIENT_SECRETS_PATH))
 
    # Prepare credentials and authorize HTTP
    # If they exist, get them from the storage object
    # credentials will get written back to a file.
    #storage = file.Storage('authorizedcreds.dat')
    storage = file.Storage("authorizedcreds.dat")
    
    credentials = storage.get()
 
    # If authenticated credentials don't exist, open Browser to authenticate
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, flags)
    http = credentials.authorize(http=httplib2.Http())
    webmasters_service = build('webmasters', 'v3', http=http)
    return webmasters_service
 
# Create Function to execute your API Request
def execute_request(service, property_uri, request):
    return service.searchanalytics().query(siteUrl=property_uri, body=request).execute()
 
# Create function to write to CSV
def write_to_csv(data,filename):
    if not os.path.isfile(filename):
        data.to_csv(filename)
    else: # else it exists so append without writing the header
        data.to_csv(filename, mode='a', header=False)
 
# Read CSV if it exists to find dates that have already been processed.
def get_dates_from_csv(path):
    if os.path.isfile(path):
        data = pd.read_csv(path)
        data = pd.Series(data['date'].unique())
        return data
    else:
        pass



# Create function to extract all the data
def extract_data(site,creds,num_days,output):
    
    global df
    #nonlocal df
    
    domain_name = get_domain_name(site)
    create_project(domain_name)
    full_path = domain_name + '/' + output
    current_dates = get_dates_from_csv(full_path)
 
    webmasters_service = authorize_creds(creds)
 
    # Set up Dates
    end_date = datetime.date.today() - relativedelta.relativedelta(days=3)
    start_date = end_date - relativedelta.relativedelta(days=num_days)
    delta = datetime.timedelta(days=1) # This will let us loop one day at the time
    scDict = defaultdict(list)
 
    while start_date <= end_date:
        if current_dates is not None and current_dates.str.contains(datetime.datetime.strftime(start_date,'%Y-%m-%d')).any():
            print('Existing Date: %s' % start_date)
            start_date += delta     
        else:
            print('Start date at beginning: %s' % start_date)
 
            maxRows = 25000 # Maximum 25K per call 
            numRows = 0     # Start at Row Zero
            status = ''     # Initialize status of extraction
 
 
            while (status != 'Finished') : # Test with i < 10 just to see how long the task will take to process.
                request = {
                    'startDate': datetime.datetime.strftime(start_date,'%Y-%m-%d'),
                    'endDate': datetime.datetime.strftime(start_date,'%Y-%m-%d'),
                    'dimensions': ['date','page','query'],
                    'rowLimit': maxRows, 
                    'startRow': numRows
                }
 
                response = execute_request(webmasters_service, site, request)
 
                try:
                #Process the response
                    for row in response['rows']:
                        scDict['date'].append(row['keys'][0] or 0)    
                        scDict['page'].append(row['keys'][1] or 0)
                        scDict['query'].append(row['keys'][2] or 0)
                        scDict['clicks'].append(row['clicks'] or 0)
                        scDict['ctr'].append(row['ctr'] or 0)
                        scDict['impressions'].append(row['impressions'] or 0)
                        scDict['position'].append(row['position'] or 0)
                    print('successful at %i' % numRows)
 
                except:
                    print('error occurred at %i' % numRows)
 
                #Add response to dataframe 
                df = pd.DataFrame(data = scDict)
                df['clicks'] = df['clicks'].astype('int')
                df['ctr'] = df['ctr']*100
                df['impressions'] = df['impressions'].astype('int')
                df['position'] = df['position'].round(2)
 
                print('Numrows at the start of loop: %i' % numRows)
                try: 
                    numRows = numRows + len(response['rows'])
                except:
                    status = 'Finished'
                print('Numrows at the end of loop: %i' % numRows)
                if numRows % maxRows != 0:
                    status = 'Finished'
         
            start_date += delta  
            print('Start date at end: %s' % start_date) 
            write_to_csv(df,full_path)
    return df

#st.write(df)

df = extract_data(site,creds,num_days,output)
#df.sort_values('clicks',ascending=False)

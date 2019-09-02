# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gmail_quickstart]
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors
from apiclient import discovery
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime
import datetime
import csv
import simplejson as json
import base64
import email
from apiclient import errors


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    userInfo = service.users().getProfile(userId='me').execute()
    print("UserInfo is \n %s" % (userInfo))


    user_id =  'me'
    label_id_one = 'INBOX'
    read_msgs = service.users().messages().list(userId='me', labelIds=[label_id_one]).execute()
    msg_list = read_msgs['messages']
    #print(msg_list)
    final_list = []
    for msgs in msg_list:
        temp_dict = {}
        m_id = msgs['id']
        messageRaw = service.users().messages().get(userId='me', id=m_id, format='raw').execute()
        messageFull = service.users().messages().get(userId='me', id=m_id, format='full').execute()
        '''
        payld = message['payload']
        headr = payld['headers']
        for one in headr:  # getting the Subject
            if one['name'] == 'Subject':
                msg_subject = one['value']
                temp_dict['Subject'] = msg_subject

        for two in headr:  # getting the date
            if two['name'] == 'Date':
                msg_date = two['value']
                date_parse = (parser.parse(msg_date))
                m_date = (date_parse.date())
                temp_dict['Date'] = str(m_date)

        for three in headr:  # getting the Sender
            if three['name'] == 'From':
                msg_from = three['value']
                temp_dict['Sender'] = msg_from
        '''

        '''
        '''

        msg_str = base64.urlsafe_b64decode(messageRaw['raw'])
        msg_str = str(msg_str, 'utf-8')
        mime_msg = email.message_from_string(msg_str)




        if "data" in messageFull['payload']['parts'][0]['body']:
            message= messageFull['payload']['parts'][0]['body']['data']
            messageb = base64.urlsafe_b64decode(message)
            messagec = str(messageb, 'utf-8')
            messaged = email.message_from_string(messagec)
            print(messaged)
        elif "data" in messageFull['payload']['parts'][0]['parts'][0]['body']:
            message = messageFull['payload']['parts'][0]['parts'][0]['body']['data']
            messageb = base64.urlsafe_b64decode(message)
            messagec = str(messageb, 'utf-8')
            messaged = email.message_from_string(messagec)
            print(messaged)


        for part in mime_msg.walk():
            #print(part.get_content_type())
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)

                #print(part.get_payload())


        '''
        content = messageFull['payload']['parts'][0]['body']['data']
        msg_body = base64.urlsafe_b64decode(content).decode('utf-8')
        print (msg_body)
        '''



        #mime_msg = email.message_from_string(msg_str)
        '''  
        temp_dict['Snippet'] = msg_body  # fetching message snippet
        print(temp_dict)
        final_list.append(temp_dict)
        '''





    with open('mails.json', 'w') as json_file:
        json.dump(final_list, json_file, sort_keys=True, indent=4)




if __name__ == '__main__':
    main()




# [END gmail_quickstart]

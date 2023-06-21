from __future__ import print_function

import os.path
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from random import choices
from string import ascii_lowercase, digits

def email_hash():
    return "".join(choices(ascii_lowercase + digits, k=10))

print(email_hash())

class GmailClient:
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    LOCAL_PART = "aqamobileflex"
    DOMAIN = "gmail.com"
    USER_ID = "me"
    MSG_TIMEOUT = 600 * 1000

    def __init__(self, address: str = None):
        self.address = address or f"{self.LOCAL_PART}+{email_hash()}@{self.DOMAIN}"
        self.service = None
        self.auth()
        self.msg_count = 0
        # self.update_msg_count()

    def auth(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'lib\gmail\credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build("gmail", "v1", credentials=creds)

    def get_all_messages(self):
        result =  self.service.users().messages().list(userId=self.USER_ID).execute()
        return [m["id"] for m in result.get("messages", [])]

    def get_last_hash_massage(self):
        all_msg = self.get_all_messages()
        return all_msg[0]

    def get_msg_raw(self, msg_id: str):
        return self.service.users().messages().get(userId=self.USER_ID, id=msg_id, format="raw").execute()



    def get_activation_code(self) -> str:
        msg_id = self.get_last_hash_massage()
        msg_raw = self.get_msg_raw(msg_id)
        snippet = msg_raw['snippet']
        code = re.findall(r"\d{4}", snippet)
        return code[0]

    def get_reset_code(self) -> str:
        return self.get_activation_code()
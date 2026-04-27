import os
import time
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json

# 1. The NEW updated Gemini package
from google import genai

# --- CONFIGURATION ---
SCOPES = ['https://mail.google.com/']

# CRITICAL: Replace the text inside the quotes with your ACTUAL API key from Google AI Studio.
# It usually starts with "AIza..."
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")    

# Initialize the new GenAI Client
client = genai.Client(api_key=GEMINI_API_KEY)

def get_gmail_service():
    """Authenticates and connects to Gmail."""
    creds = None
    
    # 1. CLOUD MODE: If running on Render, read from Environment Variables
    token_env = os.environ.get("GMAIL_TOKEN")
    if token_env:
        print("Using cloud environment variables for Gmail login...")
        token_dict = json.loads(token_env)
        creds = Credentials.from_authorized_user_info(token_dict, SCOPES)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        return build('gmail', 'v1', credentials=creds)
        
    # 2. LOCAL MODE: If running on your laptop, read the file
    print("Using local files for Gmail login...")
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    return build('gmail', 'v1', credentials=creds)

def generate_ai_draft(email_content):
    """Uses Gemini 1.5 Flash to summarize the email and write a draft."""
    prompt = f"""
    Read the following email. 
    1. Write a very brief 1-sentence summary of what the email is about.
    2. Write a professional, polite draft response.
    
    Email content:
    {email_content}
    """
    
    # Using the new package syntax
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text

def check_emails_and_draft():
    service = get_gmail_service()
    
    # Search for Unread Emails in the Inbox
    results = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD']).execute()
    messages = results.get('messages', [])

    if not messages:
        print('No new messages found.')
        return

    print(f"Found {len(messages)} new messages. Processing...")

    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        
        headers = msg['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), "No Subject")
        sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), "Unknown Sender")
        
        # --- NEW: Skip automated or no-reply emails ---
        if "no-reply" in sender.lower() or "noreply" in sender.lower() or "newsletter" in sender.lower():
            print(f"Skipping automated/no-reply email from: {sender}")
            service.users().messages().modify(
                userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}
            ).execute()
            continue

        body = msg.get('snippet', '')
        print(f"Processing email from: {sender}")

        # Generate the AI Response
        ai_response = generate_ai_draft(body)

        # Create the Draft
        message_draft = EmailMessage()
        message_draft.set_content(ai_response)
        message_draft['To'] = sender
        message_draft['Subject'] = f"Re: {subject}"
        
        encoded_message = base64.urlsafe_b64encode(message_draft.as_bytes()).decode()
        create_message = {'message': {'raw': encoded_message}}
        
        service.users().drafts().create(userId='me', body=create_message).execute()
        print("Draft created successfully!")

        # Mark as read
        service.users().messages().modify(
            userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}
        ).execute()

from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Email AI Assistant is awake and running!"

def run_email_loop():
    print("Starting Email AI Assistant background loop...")
    while True:
        try:
            check_emails_and_draft()
        except Exception as e:
            print(f"An error occurred: {e}")
        
        print("Sleeping for 5 minutes...")
        time.sleep(300)

if __name__ == '__main__':
    # Start the email checker in a background thread
    thread = threading.Thread(target=run_email_loop)
    thread.daemon = True
    thread.start()
    
    # Start the web server to keep Render happy
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
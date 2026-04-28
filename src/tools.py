from langchain.tools import tool
from apify_client import ApifyClient
import smtplib
from email.mime.text import MIMEText
import os

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
AUTH_TOKEN = os.getenv("TWITTER_AUTH_TOKEN")
CT0_VALUE = os.getenv("TWITTER_CT0")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
client = ApifyClient(APIFY_TOKEN)

@tool
def fetch_tweets(username:str):
  """Fetch the latest tweet from the Twitter username provided by the user."""

  run_input = {
      "mode": "search",
      "searchTerms": [f"from:{username}"],
      "searchMode": "Latest",
      "maxResults": 1,
      "twitterCookie": f"auth_token={AUTH_TOKEN}; ct0={CT0_VALUE}",
      "proxy": {"useApifyProxy": False}  # Bypass Apify proxy

  }
  # run_input["twitterCookie"]

  run = client.actor("automation-lab/twitter-scraper").call(run_input=run_input)

  dataset = client.dataset(run["defaultDatasetId"]).list_items().items
  tweets = []
  for item in dataset:
    tweets.append({
        "text" : item.get('text', 'N/A'),
        "url" : item.get('url', 'N/A'),
        "Date" : item.get('createdAt', 'N/A')
    })
  return str(tweets)

@tool
def send_email(receiver_email: str, subject: str = "Latest Tweets", message: str = ""):
  """Send email with tweet summary. Use Gmail app password.
  Args:
  message: tweets """


  receiver_email = str(RECEIVER_EMAIL)

  sender_email= str(SENDER_EMAIL)
  password = str(GMAIL_PASSWORD)
  msg= MIMEText(message)
  msg['Subject']= "Latest News Update"
  msg["From"]= sender_email
  msg["To"]= receiver_email

  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.starttls()
  server.login(sender_email, password)
  server.sendmail(sender_email, receiver_email, msg.as_string())
  server.quit()
  return f"Email sent successfully to {receiver_email}"

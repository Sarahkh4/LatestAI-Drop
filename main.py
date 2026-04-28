import schedule    
import time
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
import os
from dotenv import load_dotenv
#loading it before using the tools cs tools are using the env variables
load_dotenv()
from src.tools import fetch_tweets, send_email
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

model = init_chat_model(
    model = "gpt-4o-mini",
    model_provider = "openai",
    api_key = OPENAI_API_KEY,
    base_url = OPENAI_BASE_URL
)

agent = create_agent(
    model = model,
    tools = [fetch_tweets, send_email],
    system_prompt = """You are a news agent. Fetch latest tweets with fetch_tweets, summarize, then send via send_email."""
)


def run_agent():
  result = agent.invoke(
      {'messages':[{"role" : "user", "content" : "Get latest tweet from sam altman and send email"}]}
  )

  return result["messages"][-1].content


run_agent() # Run immediately once

schedule.every(2).minutes.do(run_agent)

while True:
    schedule.run_pending()   
    time.sleep(60)




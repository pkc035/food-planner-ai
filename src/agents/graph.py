import os
import langchain
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from tools.weather import get_current_weather
from db.loader import search_restaurant_tool

langchain.debug = True

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    # model="gemini-3.1-flash-lite",
    google_api_key=os.environ.get("GOOGLE_API_KEY"),
    transport="rest"
)

tools = [get_current_weather, search_restaurant_tool]

agent_executor = create_react_agent(llm, tools)
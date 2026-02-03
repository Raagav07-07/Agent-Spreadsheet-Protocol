import requests
from google.adk.agents import Agent
from datetime import datetime
from google.adk.tools import FunctionTool 
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
import asyncio
from google.adk.models import LiteLlm
import os
from dotenv import load_dotenv
load_dotenv()
BASE_URL="http://127.0.0.1:8001/asp"



def tool_discover():
    """
    Discover available spreadsheet tools.
    Returns:
    A list of available tools with their details.
    """
    response=requests.get(f"{BASE_URL}/discover")
    data=response.json()
    return data["payload"]["tools"]

tool_discover=FunctionTool(func=tool_discover)

def tool_read_range(sheet, cell_range):
    """
    Read a range of cells from a spreadsheet.
    Args:
    sheet (str): The name of the sheet to read from.
    cell_range (str): The range of cells to read (e.g., "A1:C10").
    Returns:
    A list of dictionaries representing the rows in the specified range.
    """
    payload={"sheet":sheet,"range":cell_range}
    response=requests.post(f"{BASE_URL}",json={
        "type":"READ_RANGE",
        "payload":payload
    })
    data=response.json()
    return data["payload"]["rows"]

tool_read_range=FunctionTool(func=tool_read_range)

def tool_get_sheet_list():
    """
    Get the list of available sheets in the spreadsheet.
    Returns:
    A list of sheet names.
    """
    payload={}
    response=requests.post(f"{BASE_URL}",json={
        "type":"SHEET_LIST",
        "payload":payload
    })
    data=response.json()
    return data["payload"]["sheets"]
tool_get_sheet_list=FunctionTool(func=tool_get_sheet_list)

root_agent=Agent(
    name="root_agent",
    model=LiteLlm(model="gemini/gemini-3-flash-preview",api_key=os.getenv("GEMINI_API_KEY")),
    description="""You are a helpful assistant that interacts with a spreadsheet via the Agent Spreadsheet Protocol (ASP).
    You should use only the provided tools to interact with the spreadsheet.

    **CRITICAL**: 
    - Always discover available tools before attempting to use them.
    - Should not use tools unncecessarily only when needed to answer user queries.
    1. Use the 'tool_discover' to find out what tools are available with description of the tools available. 
    2. Use 'tool_get_sheet_list' to get the list of available sheets.
    3. Use 'tool_read_range' to read specific ranges from the sheets.
    """,
    tools=[tool_discover,tool_read_range,tool_get_sheet_list]
)


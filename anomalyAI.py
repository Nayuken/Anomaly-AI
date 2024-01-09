from google.cloud import bigquery
from pandasai.llm import OpenAI
from pandasai import Agent
import pandas as pd
from pandasai import SmartDataframe
import os
import streamlit

"""
TODO: 
- Create Streamlit
- GET BigQuery sample data [x]
- GET AWS sample data []
- GET Azure sample data []
- look in to open source AI to use to help with security
- automate above processes
- Implement bigqueryNL
- Product engineering video that ben posted in further AI slack
- Tagging project idea QA: get all GA4 tags within a container and map their parameters to an excel doc

References: 
- https://cloud.google.com/python/docs/reference/bigquery/latest
- https://www.kdnuggets.com/2023/05/pandas-ai-generative-ai-python-library.html
- https://docs.pandas-ai.com/en/latest/
- https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series

Required reading for using this script:
- https://cloud.google.com/bigquery/docs/reference/libraries
- https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key
"""

### Big Query integration ###
project_id = ''  # Provide your project's ID
query_path = ""  # Provide your project's Path
client = bigquery.Client(project=project_id)
QUERY = (f'''
SELECT *
FROM `{query_path}`
LIMIT 50
''')

query_job = client.query(QUERY)
rows = query_job.result()

### THIS WILL NEED TO BE EDITED DEPENDING ON THE DATA SET YOU USE FROM BIGQUERY ###
dateList = []
workplace_change_list = []
grocery = []
for row in rows:
    dateList.append(row.date)
    workplace_change_list.append(row.workplaces_percent_change_from_baseline)
    grocery.append(row.grocery_and_pharmacy_percent_change_from_baseline)

### DataFrame implementation (THIS WILL ASLO NEED TO BE CHANGED TO FIT YOUR DATA SET) ###
df = pd.DataFrame({
    "date": dateList,
    "workplace": workplace_change_list,
    "grocery": grocery
})
df1 = pd.DataFrame()
df2 = pd.DataFrame()
df3 = pd.DataFrame()

### Ai Configuration ###
api_key = ""  # Provide your open API Key
llm = OpenAI(api_token=api_key)

### Agent implementation ###
agent = Agent(df, config={"llm": llm}, memory_size=10)
agent_Running = "c"
while agent_Running:
    user_Input = input("Provide a question: ")
    response = agent.chat(user_Input)
    explanation = agent.explain()
    print("Agent: ", response)
    print("Explanation: ", explanation)
    response = ""
    agent_Running = input("Enter C if you would like to continue ").lower()
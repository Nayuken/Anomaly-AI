from google.cloud import bigquery
from pandasai.llm import OpenAI
from pandasai import Agent
import pandas as pd
from pandasai import SmartDataframe
import os
import streamlit

# Note for later statiscal rethinking
# Get streamlit template for GPT
# use this https://www.kdnuggets.com/2023/05/pandas-ai-generative-ai-python-library.html
# take BQ database -> bring in to pandas DF -> have pandas AI create visualization based off of a user response

"""
TODO: 
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
- 
"""

# Big Query integration
project_id = ''
query_path = ""
client = bigquery.Client(project=project_id)
QUERY = (f'''
SELECT *
FROM `{query_path}`
LIMIT 50
''')

query_job = client.query(QUERY)
rows = query_job.result()
dateList = []
workplace_change_list = []
grocery = []
for row in rows:
    dateList.append(row.date)
    workplace_change_list.append(row.workplaces_percent_change_from_baseline)
    grocery.append(row.grocery_and_pharmacy_percent_change_from_baseline)

### PandasAI integration ###
df = pd.DataFrame({
    "date": dateList,
    "workplace": workplace_change_list,
    "grocery": grocery
})
df1 = pd.DataFrame()
df2 = pd.DataFrame()
df3 = pd.DataFrame()
api_key = ""
llm = OpenAI(api_token=api_key)

# df = SmartDataframe(df, config={"llm": llm})
# response = df.chat("You are a data analyst can you tell from the data provided on what dates anomalies occured?")

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

# TOOO: refine output
# look in to machine learning for
# IDP program ask for particiation

# Phase 1.5 ML implementation for the actual anomaly detection https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series
'''
It is easy to write a wrapper around openAI and build a APP but we need to focus on some of these following areas -
Fine tune models
PII and Content Safety
Formating Output
Evaluating Output
LLM Operation in production
'''
# Ask practice lead for forcasting
# Step 2 Agent clarification wip:
# questions = agent.clarification_questions()
# for question in questions:
#   print(question)

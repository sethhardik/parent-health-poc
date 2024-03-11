import streamlit as st
import pathlib
import textwrap
import pandas as pd
from twilio.rest import Client
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
import requests
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from markdown import markdown
import re
import os
from streamlit_extras.app_logo import add_logo

def logo():
    add_logo("/Users/deepanshumishra/EMA Code/logo.png", height=300)
api_key_sheets= 'AIzaSyAsFcHXA4Klz9HsRHKak_QeyDmzU7CBOdw'
url="https://docs.google.com/spreadsheets/d/1UwbQZIpONmoUb12TFXpVOSxUvFT8xeOTOlcLoLSdq4c/edit?usp=sharing"
spreadsheet_id = url.split("/")[5]
RANGE_NAME = 'Sheet1!A1:E6'
def authenticate_sheets(api_key_sheets):
  return build( 'sheets', 'v4', developerKey = api_key_sheets).spreadsheets()
sheets  = authenticate_sheets(api_key_sheets)
result = sheets.values().get(spreadsheetId=spreadsheet_id, range=RANGE_NAME).execute()
values = result.get('values', [])
df = pd.DataFrame(values)
df.columns = df.iloc[0]
df = df[1:]
df.set_index(df.columns[0],inplace=True)
account_sid = 'ACb658d1d5610d3f63137449e42d15859a'
auth_token = '00305a8bea1bcfb33de9b52fc68ebdc8'
client = Client(account_sid, auth_token)
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
genai.configure(api_key='AIzaSyDrl058zWba4yT-MKpDqU5S5gak4tw-l_M')
model = genai.GenerativeModel('gemini-pro')

# Company information (replace with your company details)


# Mobile number input with validation
def is_valid_mobile_number(mobile_number):
  """Checks if the input is a valid 10-digit mobile number."""
  return mobile_number.isdigit() and len(mobile_number) == 10
st.title('AgeWell Assist')

logo()

st.write("AgeWell Assist")

mobile_number_parent = st.text_input("Enter Mobiler Number of Parent", key="mobile_number_parent")
if mobile_number_parent:
  if not is_valid_mobile_number(mobile_number_parent):
    st.error("Please enter a valid 10-digit mobile number.")
  else:
    st.success("Mobile number saved.")

mobile_number_child = st.text_input("Enter your Mobile Number", key="mobile_number_child")
if mobile_number_child:
  if not is_valid_mobile_number(mobile_number_child):
    st.error("Please enter a valid 10-digit mobile number.")
  else:
    st.success("Mobile number saved.")
    message_choice = st.radio("Choose Message Type", ("Morning Message", "Evening Message"))
    if message_choice == "Morning Message":
        type_choice = st.radio("Whom to send", ("Parent", "Children"))
        if type_choice == 'Parent':
            result = st.button("Send Message")
            if result:
                text = 'We are an Elderly Care StartUp, we solve for the pursuit of active lifestyle for parents and transparency over health of parent for the children who lead busy lives. We take data from health monitoring devices and use AI nudges into habit forming action for the parents and also report the updates to the adult children.  Below is the data coming from a wearable for past 5 days coverted to a string format.' + df.to_string() + 'I want you to analyze the entire data first and make sense of it and do the following, 1. Write whatsapp messages to parent on Day 5. Two messages should be going out for Day 5, morning message and evening messages. Both the message should be habit forming.2. Morning message should contain how the health has been for past two days and how the step count has been, what is the trend leading to, all of should in a paragraph, make sure this has emoji and is habit forming and personalized.3. Evening message should first summarise the health stats on Day 5, and if the situtation is good, go for motivation, if the stats arent great suggest the activity increase and mention the parameter of concern. Push towards active lifestyle and goals to be met. Make it habit forming. 4. The Morning message should begin with \"Day 5: Morning Message\" and the evening message should being with\"Day 5: Evening Message\"'''
                response = model.generate_content(text)
                html = markdown(response.text)
                text = ''.join(BeautifulSoup(html).findAll(text=True))
                morning_message_pattern = re.compile(r'Day 5: Morning Message(.*?)Day 5: Evening Message', re.DOTALL)
                morning_message_match = morning_message_pattern.search(text)
                if morning_message_match:
                    morning_message = morning_message_match.group(1).strip()
                else:
                    morning_message ="Morning Message not found."
                message = client.messages.create(
                from_='whatsapp:+14155238886',
                body=morning_message,
                to='whatsapp:+91'+str(mobile_number_parent))
        if type_choice == 'Children':
            result = st.button("Send Message")
            if result:
                text = 'We are an Elderly Care StartUp, we solve for the pursuit of active lifestyle for parents and transparency over health of parent for the children who lead busy lives. We take data from health monitoring devices and use AI nudges into habit forming action for the parents and also report the updates to the adult children.  Below is the data coming from a wearable for past 5 days coverted to a string format.' + df.to_string() + 'Above is the data of parent, I want you to analyze the entire data first and make sense of it and do the following, 1. Write whatsapp messages to an Adult Children named "Deepanshu" on Day 5. Two messages should be going out for Day 5, morning message and evening messages. Both the message should be personalized and address the reporting of health of their parents.2. Morning message should contain how the health has been for past two days, what might be the cause of worry and if they need a doctor consultation and how the step count has been (Target is 8000) and  what is the trend leading to, all of should in a paragraph less than 150 words, make sure this has emoji and is habit forming and personalized.3. Evening message should first summarise the health stats on Day 5 and what their active lifestyle for the day, and if the situtation is looking better, or if they need to be on alert; give some suggestion to adult children about their parent under 150 words.5. Keep the messages well structred 6. The Morning message should begin with \"Day 5: Morning Message\" and the evening message should being with\"Day 5: Evening Message\"'''
                response = model.generate_content(text)
                html = markdown(response.text)
                text = ''.join(BeautifulSoup(html).findAll(text=True))
                morning_message_pattern = re.compile(r'Day 5: Morning Message(.*?)Day 5: Evening Message', re.DOTALL)
                morning_message_match = morning_message_pattern.search(text)
                if morning_message_match:
                    morning_message = morning_message_match.group(1).strip()
                else:
                    morning_message ="Morning Message not found."
                account_sid = 'ACb658d1d5610d3f63137449e42d15859a'
                auth_token = '00305a8bea1bcfb33de9b52fc68ebdc8'
                client = Client(account_sid, auth_token)

                from_whatsapp_number = 'whatsapp:+14155238886'
#                    7982415452
                to_whatsapp_number = 'whatsapp:+917982415452'

                message = client.messages.create(body='Report',
                       media_url='https://i.ibb.co/j9CbryY/9b3b0209-5d74-4f04-a38f-ca59d471b28c.jpg',
                       from_=from_whatsapp_number,
                       to='whatsapp:+91'+str(mobile_number_child))
                message = client.messages.create(
                from_='whatsapp:+14155238886',
                body=morning_message,
                to='whatsapp:+91'+str(mobile_number_child))
    if message_choice == "Evening Message":
            type_choice = st.radio("Choose Message Type", ("Parent", "Children"))
            if type_choice == 'Parent':
                result = st.button("Send Message")
                if result:
                    text = 'We are an Elderly Care StartUp, we solve for the pursuit of active lifestyle for parents and transparency over health of parent for the children who lead busy lives. We take data from health monitoring devices and use AI nudges into habit forming action for the parents and also report the updates to the adult children.  Below is the data coming from a wearable for past 5 days coverted to a string format.' + df.to_string() + 'I want you to analyze the entire data first and make sense of it and do the following, 1. Write whatsapp messages to parent on Day 5. Two messages should be going out for Day 5, morning message and evening messages. Both the message should be habit forming.2. Morning message should contain how the health has been for past two days and how the step count has been, what is the trend leading to, all of should in a paragraph, make sure this has emoji and is habit forming and personalized.3. Evening message should first summarise the health stats on Day 5, and if the situtation is good, go for motivation, if the stats arent great suggest the activity increase and mention the parameter of concern. Push towards active lifestyle and goals to be met. Make it habit forming. 4. The Morning message should begin with \"Day 5: Morning Message\" and the evening message should being with\"Day 5: Evening Message\"'''
                    response = model.generate_content(text)
                    html = markdown(response.text)
                    text = ''.join(BeautifulSoup(html).findAll(text=True))
                    morning_message_pattern = re.compile(r'Day 5: Evening Message(.*)', re.DOTALL)
                    morning_message_match = morning_message_pattern.search(text)
                    if morning_message_match:
                        morning_message = morning_message_match.group(1).strip()
                    else:
                        morning_message ="Morning Message not found."
                    message = client.messages.create(
                    from_='whatsapp:+14155238886',
                    body=morning_message,
                    to='whatsapp:+91'+str(mobile_number_parent))
            if type_choice == 'Children':
                result = st.button("Send Message")
                if result:
                    text = 'We are an Elderly Care StartUp, we solve for the pursuit of active lifestyle for parents and transparency over health of parent for the children who lead busy lives. We take data from health monitoring devices and use AI nudges into habit forming action for the parents and also report the updates to the adult children.  Below is the data coming from a wearable for past 5 days coverted to a string format.' + df.to_string() + 'Above is the data of parent, I want you to analyze the entire data first and make sense of it and do the following, 1. Write whatsapp messages to an Adult Children named "Deepanshu" on Day 5. Two messages should be going out for Day 5, morning message and evening messages. Both the message should be personalized and address the reporting of health of their parents.2. Morning message should contain how the health has been for past two days, what might be the cause of worry and if they need a doctor consultation and how the step count has been (Target is 8000) and  what is the trend leading to, all of should in a paragraph less than 150 words, make sure this has emoji and is habit forming and personalized.3. Evening message should first summarise the health stats on Day 5 and what their active lifestyle for the day, and if the situtation is looking better, or if they need to be on alert; give some suggestion to adult children about their parent under 150 words. 4. The Morning message should begin with \"Day 5: Morning Message\" and the evening message should being with\"Day 5: Evening Message\"'''
                    response = model.generate_content(text)
                    html = markdown(response.text)
                    text = ''.join(BeautifulSoup(html).findAll(text=True))
                    morning_message_pattern = re.compile(r'Day 5: Evening Message(.*)', re.DOTALL)
                    morning_message_match = morning_message_pattern.search(text)
                    if morning_message_match:
                        morning_message = morning_message_match.group(1).strip()
                    else:
                        morning_message ="Morning Message not found."
                    message = client.messages.create(
                    from_='whatsapp:+14155238886',
                    body=morning_message,
                    to='whatsapp:+91'+str(mobile_number_child))

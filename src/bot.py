#########
#!/bin/env/python3

import google.generativeai as genai
import os
import requests
import threading
import time



# Load API Key securely from environment variables
 
GEMINI_API_KEY = "AIzaSyATh-8xlK-3SHL2JS_Oz_SsJqSMDIqzPwk"
genai.configure(api_key="AIzaSyATh-8xlK-3SHL2JS_Oz_SsJqSMDIqzPwk")  # Replace with your actual API Key


models = genai.list_models()
for model in models:
    print(model.name)  # Print available model names

if not GEMINI_API_KEY:
    print("❌ ERROR: API Key is not found! Setting it manually.")
    GEMINI_API_KEY = "AIzaSyATh-8xlK-3SHL2JS_Oz_SsJqSMDIqzPwk"

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"


# Function to send a request to Google Gemini API
def chat_with_gemini(prompt):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{
                "text": f"""
                    You are an AI healthcare assistant providing structured medical guidance based on symptoms. 
                    You are NOT a doctor, but you can suggest possible causes and general remedies. 
                    Make sure to provide a **structured and easy-to-read** response following this format: 
                    Give a genuine conern and tell feel sorry got your sufferening
                    🩺 **<b>Possible Causes:</b>**  
                    Provide a **list of likely medical conditions** based on the symptoms.  
                    Explain in **simple, clear language** and **avoid overly complex medical jargon**.  

                    🏠 **<b>Home Remedies:</b>**  
                    Suggest **natural remedies, lifestyle changes, and over-the-counter treatments** that might help.  
                    Make sure the advice is practical and easy to follow.  

                    🚨 **<b>Emergency Alert:</b>**  
                    If symptoms indicate a **serious condition or require urgent care**, highlight **when to see a doctor**.  
                    Warn if symptoms persist for **more than 2 days** or if there are **severe warning signs**.  
                     Lastly tell a soft feed back and tell him get well soon type msg   
                    Here is the patient's information:  
                    **Symptoms:** {prompt}
                    """

            }]
        }]
    }

    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {response.json()}"

# Modify the chatbot class to use Google Gemini
class Reply:
    def __init__(self, query):
        self.query = query

    def send(self, interactive=False):
        bot_response = chat_with_gemini(self.query.message)
        print(f"Prompt >> {self.query.get_message()}")
        print(bot_response)
        return bot_response

class Query:
    def __init__(self, message="who are you ?"):
        self.message = message
        self.description = message
        self.params = {}
    
    def set_message(self, message):
        self.message = message
        self.description = message
        return self.message
    
    def set_param(self, key, value):
        text = f"My {key} is: {value}"
        self.params[key] = text
    
    def create_message(self):
        text = []
        for value in self.params.values():
            text.append(value)
        text.append(self.message)
        self.message = ", ".join(text) + '\n'
        return self
    
    def get_message(self):
        return self.description

if __name__ == "__main__":
    # Test Cases
    text = "I have a headache and some pain in my neck"
    ki2kid = Query(text)
    ki2kid.set_param("age", 22)
    ki2kid.set_param("gender", "male")

    text2 = "I can't see clearly"
    mano = Query(text2)
    mano.set_param("age", 15)
    mano.set_param("gender", "male")

    # Create the message
    ki2kid.create_message()

    # Reply takes a Query and returns a response
    answer = Reply(ki2kid)
    rep = answer.send(interactive=True)
    print(rep)

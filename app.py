from flask import Flask, render_template, request, jsonify
import requests
import google.generativeai as genai
import os

app = Flask(__name__)

# Load API Key
GEMINI_API_KEY = "AIzaSyATh-8xlK-3SHL2JS_Oz_SsJqSMDIqzPwk"

GOOGLE_API_KEY = "AIzaSyCwJS6hL1PTJ-dd_LLw11Cg9ff-CoLkn_A" 

genai.configure(api_key=GEMINI_API_KEY)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    if "followUp" in data:
        # Process the follow-up query separately, if needed.
        follow_up_query = data.get("followUp")
        # Build a prompt or conversation context as necessary.
        prompt = f"Follow-up question: {follow_up_query}"
    else:
        # Process initial conversation data.
        name = data.get("name", "Patient")
        age = data.get("age", "Unknown")
        symptoms = data.get("symptoms", "")
        additional_symptoms = data.get("additionalSymptoms", "")

        prompt = f"""
            Assume Yourself an AI healthcare assistant providing structured medical guidance based on symptoms. You are NOT a doctor, but you can suggest possible causes and general remedies.
            Make sure to provide a structured and easy-to-read response following this format:


            👤 Patient Name: {name}
            🤝 Age: {age}
            🤒 Primary Symptoms: {symptoms}
            🔍 Additional Symptoms: {additional_symptoms}
            write all the information given in the previous 4 lines with the above given emoji
            a breaking line after this <hr>

            write a short message like I am sorry to hear about you health of 2-3 lines

            **🛑 Input Validation (Very Important):**
            - Before proceeding, analyze the user’s symptom input carefully.
            - If the input is **not a recognized symptom** (random text, gibberish, or irrelevant words), do **not** provide any medical response.
            - Instead, respond **only** with this polite message:
            
            ❝ I am your virtual healthcare assistant, and I noticed that your input doesn't seem to be a valid symptom.  
            Please provide relevant medical symptoms so that I can assist you better. ❞

            **🚀 If the input is valid, then proceed with the following structure:**
            - **🩺 Possible Causes:** [List general possible conditions in bullet points with emoji 🔹]
            - **🏠 Home Remedies:** [Provide practical treatment suggestions with emoji 🍃]
            - **🚨 Emergency Alert:** [Highlight severe symptoms with some writings requiring urgent care with bullet emoji ⚠️]
            
            After this, give a message that says **"Get well soon"** in a polite and encouraging way.

            
            If the user types "No" or "Exit", acknowledge them and politely close the conversation with a **get well soon** message.
        """

    
    # Generate AI response as before...
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        if not response or not hasattr(response, "text"):
            return jsonify({"reply": "<b>⚠️ AI Response Failed. Try Again.</b>"})
        bot_reply = response.text
        formatted_reply = bot_reply.replace("**", "").replace("*", "").replace("\n", "<br>")
        formatted_html = f"""
            <div style="background-color: white; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 10px #ddd; font-family: Arial;">
                {formatted_reply}
            </div>
        """
        return jsonify({"reply": formatted_html})
    except Exception as e:
        return jsonify({"reply": f"<b>❌ Error:</b> {str(e)}"})

def geocode_location(location):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={GOOGLE_API_KEY}"
    print("DEBUG: Geocoding URL:", url)
    response = requests.get(url)
    data = response.json()
    print("DEBUG: Geocoding response:", data)
    if data["results"]:
        loc = data["results"][0]["geometry"]["location"]
        return loc["lat"], loc["lng"]
    return None, None

def get_nearby_hospitals(lat, lng, radius=5000):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type=hospital&key={GOOGLE_API_KEY}"
    print("DEBUG: Places URL:", url)
    response = requests.get(url)
    data = response.json()
    print("DEBUG: Places response:", data)
    hospitals = []
    if "results" in data:
        for result in data["results"]:
            hospitals.append({
                "name": result.get("name"),
                "address": result.get("vicinity")
            })
    return hospitals

@app.route("/nearby_hospitals", methods=["POST"])
def nearby_hospitals():
    data = request.json
    location = data.get("location")
    if not location:
        return jsonify({"hospitals": []})
    lat, lng = geocode_location(location)
    if lat is None or lng is None:
        return jsonify({"hospitals": []})
    hospitals = get_nearby_hospitals(lat, lng)
    return jsonify({"hospitals": hospitals})


if __name__ == "__main__":
    app.run(debug=True)

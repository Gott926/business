from flask import Flask, request, jsonify, make_response, Response
from pymongo import MongoClient
from datetime import datetime
import requests

app = Flask(__name__)
connection = MongoClient(
        "mongodb+srv://sviatoslavlatyk11:F3omowNLEcvi6uMn@cluster0.urtg1xc.mongodb.net/?appName=Cluster0")
database = connection.get_database("Portfolio")
collection = database.get_collection("Users")

# Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = '7341811756:AAFL2i7_4vTl1PrCFn5TPl-xutgZSee0euA'
TELEGRAM_CHAT_ID = '807515475'

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=payload)
    return response

@app.route('/register', methods=['POST'])
def register():
    content = request.get_json()
    # Extract data from request
    name = content['name']
    email = content['email']
    phone_number = content['phone_number']
    time = datetime.now()

    # Insert data into MongoDB
    result = collection.insert_one({
        "name": name,
        "email": email,
        "phone_number": phone_number,
        "time": time
    })

    # Check if insertion was successful
    if result.acknowledged:
        # Send notification via Telegram
        message = f"New registration: \n---------------- \nName: {name} \n---------------- \nEmail: {email} \n---------------- \nPhone Number: {phone_number} \n---------------- \nTime: {time}"
        send_telegram_message(message)
        return Response("", 200)
    else:
        return Response("", 500)

if __name__ == '__main__':
    app.run()
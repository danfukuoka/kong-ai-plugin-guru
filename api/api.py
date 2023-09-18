from flask import Flask, request
from flask_cors import CORS
import openai
import requests

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['POST'])
def ia():

    #openai.api_key = "YOU_AI_API_KEY"  # Replace with your API key


    user_message = str(request.data)
    #user_message = "I need a plugin for tracing using opentelemetry."
    #user_message = "I need a plugin to transform GraphQL upstream into REST."

    print("user_message" + user_message)

    url = "http://kong-kong-admin.kong:8001/plugins"
    headers = {"kong-admin-token": "123456"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        plugins_json = response.text
    else:
        print("Error: Unable to fetch data from the API.")

    prompt = """
    Hello. Can you provide a kong plugin in declarative Kong format (Deck)?
    I will tell what kind of plugin I need.
    You will search this plugin in this list:  '""" + plugins_json + """'.
    If you find the plugin that I want in this list, transform this in Deck, 
    remove informations about routes and services and give it to me, 
    and do not give a general example.
    If you do not find it, please inform me that there is no plugin of this kind already configured, 
    and then search in your database for how to use the plugin that is most likely to solve my problem.
    """

    print(prompt+user_message)
    print("processing...")

    completion = openai.ChatCompletion.create( # Change the function Completion to ChatCompletion
    model = 'gpt-3.5-turbo',
    messages = [ # Change the prompt parameter to the messages parameter
        {'role': 'user', 'content': prompt+user_message}
    ],
    temperature = 0  
    )

    print(completion['choices'][0]['message']['content']) # Change how you access the message content

    return completion['choices'][0]['message']['content']

import logging
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from asyncio import run
from openaichat import OpenAIChatImpl
from kandinsky import Kadninsky_impl
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
 
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
KANDINSKY_API_KEY = os.getenv('KANDINSKY_API_KEY')
KADNINSKY_SECRET_KEY = os.getenv('KADNINSKY_SECRET_KEY')
IMGUR_CLIENT_ID= os.getenv('IMGUR_CLIENT_ID')
PROXY_LOGIN = os.getenv('PROXY_LOGIN')
PROXY_PASSWORD = os.getenv('PROXY_PASSWORD')
PROXY_IP = os.getenv('PROXY_IP')
PROXY_PORT = os.getenv('PROXY_PORT')
YOUKNOW_URL = os.getenv('YOUKNOW_URL')
VALIDATIONS_URL = os.getenv('VALIDATIONS_URL')

class Server:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app, origins=str(YOUKNOW_URL))
        self.openaichat = OpenAIChatImpl(OPENAI_API_KEY=OPENAI_API_KEY, PROXY_LOGIN=PROXY_LOGIN, PROXY_PASSWORD=PROXY_PASSWORD, PROXY_IP=PROXY_IP, PROXY_PORT=PROXY_PORT)
        self.kandinsky = Kadninsky_impl('https://api-key.fusionbrain.ai/', KANDINSKY_API_KEY, KADNINSKY_SECRET_KEY)
        self.setup_routes()
        
    def setup_routes(self):

        @self.app.route('/call_openai', methods=['GET', 'OPTIONS'])
        def call_openai():
            result = run(self.openaichat.call_openai(request.args.get('action'), request.args.get('title'), request.args.get('units'), request.args.get('chapterName'), request.args.get('transcript')))
            return jsonify(result)

        @self.app.route('/call_kandinsky', methods=['GET', 'OPTIONS'])
        def call_kandinsky():
            result = run(self.kandinsky.call_kandinsky(request.args.get('prompt'), IMGUR_CLIENT_ID))
            return jsonify(result)

    def run(self, debug, port, host):
        self.app.run(debug=debug, port=port, host=host)


if __name__ == '__main__':
    server = Server()
    server.run(debug=True, port=8225, host=str(VALIDATIONS_URL))

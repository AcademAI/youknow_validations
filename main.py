import logging
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from asyncio import run

from ggchat import GigaChat_impl
from kandinsky import Kadninsky_impl
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

GIGACHAT_CLIENT_SECRET = os.getenv('GIGACHAT_CLIENT_SECRET')
GIGACHAT_CREDENTIALS = os.getenv('GIGACHAT_CREDENTIALS')
KANDINSKY_API_KEY = os.getenv('KANDINSKY_API_KEY')
KADNINSKY_SECRET_KEY = os.getenv('KADNINSKY_SECRET_KEY')
IMGUR_CLIENT_ID= os.getenv('IMGUR_CLIENT_ID')


class Server:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app, origins='http://0.0.0.0:3000')
        self.gigachat = GigaChat_impl(GIGACHAT_CREDENTIALS, 'GIGACHAT_API_PERS', False)
        self.kandinsky = Kadninsky_impl('https://api-key.fusionbrain.ai/', KANDINSKY_API_KEY, KADNINSKY_SECRET_KEY)
        self.setup_routes()
        
    def setup_routes(self):
        
        @self.app.route('/call_gigachat', methods=['GET', 'OPTIONS'])
        def createUnitsNChapters():
            result = run(self.gigachat.call_gigachat(request.args.get('action'), request.args.get('title'), request.args.get('units')))
            return jsonify(result)

        @self.app.route('/call_kandinsky', methods=['GET', 'OPTIONS'])
        def call_kandinsky():
            result = run(self.kandinsky.call_kandinsky(request.args.get('prompt'), IMGUR_CLIENT_ID))
            return jsonify(result)

    
    def run(self, debug, port, host):
        self.app.run(debug=debug, port=port, host=host)

if __name__ == '__main__':
    server = Server()
    server.run(debug=True, port=8225, host='0.0.0.0')

import logging
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from asyncio import run
import tenacity

from gigachat import GigaChat_impl
from kandinsky import Kadninsky_impl
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

GIGACHAT_CLIENT_SECRET = os.getenv('GIGACHAT_CLIENT_SECRET')
GIGACHAT_CREDENTIALS = os.getenv('GIGACHAT_CREDENTIALS')
KANDINSKY_API_KEY = os.getenv('KANDINSKY_API_KEY')
KADNINSKY_SECRET_KEY = os.getenv('KADNINSKY_SECRET_KEY')


class Server:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app, origins='http://0.0.0.0:3000')
        self.gigachat = GigaChat_impl(GIGACHAT_CREDENTIALS, 'GIGACHAT_API_PERS', False)
        self.kandinsky = Kadninsky_impl('https://api.kandinsky.ai/', KANDINSKY_API_KEY, KADNINSKY_SECRET_KEY)
        self.setup_routes()
        
    def setup_routes(self):
        
        @self.app.route('/call_gigachat', methods=['GET', 'OPTIONS'])
        def createUnitsNChapters():
            result = run(self.gigachat.call_gigachat(request.args.get('action'), request.args.get('user_prompt')))
            return jsonify(result)

        @self.app.route('/call_kandinsky', methods=['GET', 'OPTIONS'])
        def call_kandinsky():
            return jsonify(self.kandinsky.generate(request.args.get('prompt'), request.args.get('model'), request.args.get('images'), request.args.get('width'), request.args.get('height')))

    
    def run(self, debug, port, host):
        self.app.run(debug=debug, port=port, host=host)

if __name__ == '__main__':
    server = Server()
    server.run(debug=True, port=8225, host='0.0.0.0')

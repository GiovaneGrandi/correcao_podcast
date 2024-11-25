from flask import Flask
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # Adiciona o caminho da raiz do projeto ao sys.path
from config import *
from blueprints.chatbot.chatbot import chatbot_bp
from blueprints.newdocument.newdocument import newdocument_bp
from blueprints.podcast.podcast import podcast_bp
from blueprints.chat.chat import chat_bp


app = Flask(__name__, static_folder='../static', template_folder='templates')
app.register_blueprint(chatbot_bp, url_prefix="/chatbot")
app.register_blueprint(newdocument_bp, url_prefix="/newdocument")
app.register_blueprint(podcast_bp, url_prefix="/podcast")
app.register_blueprint(chat_bp, url_prefix="/chat")


if __name__ == '__main__':
    app.run(debug=True)
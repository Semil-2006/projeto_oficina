import os
import time
import json
import random
import sqlite3
import threading
from datetime import datetime
from flask import Flask, render_template, jsonify, request, redirect
import google.generativeai as genai
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Carregar variáveis de ambiente
load_dotenv()

# Configurações iniciais
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'supersecretkey')
DATABASE = 'viewers.db'
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
CLIENT_SECRETS_FILE = "client_secret.json"  # Baixe este arquivo do Google Cloud Console

# Configurar Gemini
genai.configure(api_key=GEMINI_API_KEY)
gemini = genai.GenerativeModel('gemini-pro')

# Escopos necessários para a API do YouTube
SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly"
]

# Inicializar banco de dados
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS viewers
                 (id TEXT PRIMARY KEY, username TEXT, points INTEGER, last_interaction TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS raffles
                 (id INTEGER PRIMARY KEY, command TEXT, prize TEXT, winner TEXT, date TEXT)''')
    conn.commit()
    conn.close()

init_db()

def get_credentials():
    creds = None
    token_file = 'token.json'
    
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_secrets_file(
                CLIENT_SECRETS_FILE,
                scopes=SCOPES,
                redirect_uri='http://localhost:5000/callback')
            
            auth_url, _ = flow.authorization_url(prompt='consent')
            print(f'Por favor, acesse este URL para autorizar: {auth_url}')
            return None
    
    # Salvar as credenciais para a próxima execução
    with open(token_file, 'w') as token:
        token.write(creds.to_json())
    
    return creds

class LiveChatBot:
    def __init__(self, live_chat_id, credentials):
        self.live_chat_id = live_chat_id
        self.last_chat_id = None
        self.keyword_responses = {
            "bug": "Aqui está um meme para alegrar seu dia de debug! 🐞",
            "erro": "Erro é só uma feature não documentada! 😉",
            "python": "```python\nprint('Hello, Pythonista!')\n```",
            "javascript": "```javascript\nconsole.log('Hello, World!');\n```",
            "ia": "Interessado em IA? Que tal este snippet:\n```python\nimport tensorflow as tf\nprint(tf.__version__)```"
        }
        self.meme_keywords = ["bug", "erro", "loop", "syntax", "crash"]
        self.raffles = {}
        self.active_commands = {
            "!python": {"active": False, "participants": [], "prize": "Curso de Python"},
            "!ia": {"active": False, "participants": [], "prize": "Ebook de IA"}
        }
        
        # Criar serviço autenticado
        self.youtube = build('youtube', 'v3', credentials=credentials)
        
    def fetch_messages(self):
        try:
            response = self.youtube.liveChatMessages().list(
                liveChatId=self.live_chat_id,
                part="snippet,authorDetails",
                pageToken=self.last_chat_id
            ).execute()
            
            self.last_chat_id = response.get('nextPageToken')
            return response.get('items', [])
        except HttpError as e:
            print(f"Erro na API: {e}")
            return []

    def process_message(self, message):
        msg_text = message['snippet']['displayMessage'].lower()
        user_id = message['authorDetails']['channelId']
        username = message['authorDetails']['displayName']
        author_details = message['authorDetails']
        
        # Atualizar pontos
        self.update_points(user_id, username)
        
        # Verificar comandos de sorteio
        if msg_text.startswith('!'):
            self.handle_raffle(msg_text, user_id, username, author_details)
            return
        
        # Respostas automáticas
        for keyword, response in self.keyword_responses.items():
            if keyword in msg_text:
                self.send_message(response)
                break
        
        # Gerar memes
        if any(kw in msg_text for kw in self.meme_keywords):
            meme_response = self.generate_tech_meme(msg_text)
            self.send_message(meme_response)
            
        # Resposta com IA para perguntas técnicas
        if "?" in msg_text and len(msg_text.split()) > 3:
            ai_response = self.generate_ai_response(msg_text)
            self.send_message(ai_response)

    def handle_raffle(self, command, user_id, username, author_details):
        # Comandos de participação
        base_command = command.split()[0]
        if base_command in self.active_commands and self.active_commands[base_command]["active"]:
            if user_id not in self.active_commands[base_command]["participants"]:
                self.active_commands[base_command]["participants"].append(user_id)
                self.send_message(f"{username} entrou no sorteio! 🎉")
        
        # Comandos de moderação (iniciar/finalizar sorteios)
        if base_command == "!startsorteio" and author_details.get('isChatModerator'):
            parts = command.split()
            if len(parts) >= 3:
                raffle_cmd = parts[1]
                prize = " ".join(parts[2:])
                self.start_raffle(raffle_cmd, prize)
            else:
                self.send_message("Formato: !startsorteio [comando] [prêmio]")
                
        if base_command == "!sorteiar" and author_details.get('isChatModerator'):
            parts = command.split()
            if len(parts) >= 2:
                raffle_cmd = parts[1]
                self.draw_winner(raffle_cmd)
            else:
                self.send_message("Formato: !sorteiar [comando]")

    def start_raffle(self, command, prize):
        if command in self.active_commands:
            self.active_commands[command]["active"] = True
            self.active_commands[command]["prize"] = prize
            self.active_commands[command]["participants"] = []
            self.send_message(f"🎉 SORTEIO INICIADO! Digite {command} para concorrer a: {prize}")

    def draw_winner(self, command):
        if command in self.active_commands and self.active_commands[command]["active"]:
            participants = self.active_commands[command]["participants"]
            if participants:
                winner_id = random.choice(participants)
                winner = self.get_username(winner_id)
                prize = self.active_commands[command]["prize"]
                
                self.send_message(f"🎉 PARABÉNS {winner}! Você ganhou: {prize}")
                self.record_raffle(command, prize, winner_id)
                self.active_commands[command]["active"] = False

    def record_raffle(self, command, prize, winner):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO raffles (command, prize, winner, date) VALUES (?, ?, ?, ?)",
                  (command, prize, winner, datetime.now().isoformat()))
        conn.commit()
        conn.close()

    def update_points(self, user_id, username):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        
        # Verificar se usuário existe
        c.execute("SELECT points FROM viewers WHERE id = ?", (user_id,))
        viewer = c.fetchone()
        
        if viewer:
            new_points = viewer[0] + 1
            c.execute("UPDATE viewers SET points = ?, last_interaction = ? WHERE id = ?",
                      (new_points, datetime.now().isoformat(), user_id))
        else:
            c.execute("INSERT INTO viewers (id, username, points, last_interaction) VALUES (?, ?, ?, ?)",
                      (user_id, username, 1, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()

    def get_username(self, user_id):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT username FROM viewers WHERE id = ?", (user_id,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else "Usuário Desconhecido"

    def generate_tech_meme(self, context):
        try:
            prompt = f"Crie uma descrição engraçada de meme de programação sobre: {context}. Máximo 15 palavras."
            response = gemini.generate_content(prompt)
            return f"🤖 MEME TECH: {response.text}"
        except Exception as e:
            print(f"Erro ao gerar meme: {e}")
            return "🤖 Bug no meme! Tente novamente mais tarde."

    def generate_ai_response(self, question):
        try:
            prompt = f"Responda como especialista em programação de forma direta e útil (máx 2 linhas): {question}"
            response = gemini.generate_content(prompt)
            return f"🤖 IA: {response.text}"
        except Exception as e:
            print(f"Erro ao gerar resposta IA: {e}")
            return "🤖 Estou com problemas técnicos. Pergunte algo mais tarde!"

    def send_message(self, message):
        try:
            # Limitar mensagens muito longas
            if len(message) > 200:
                message = message[:197] + "..."

            self.youtube.liveChatMessages().insert(
                part="snippet",
                body={
                    "snippet": {
                        "liveChatId": self.live_chat_id,
                        "type": "textMessageEvent",
                        "textMessageDetails": {
                            "messageText": message
                        }
                    }
                }
            ).execute()
        except HttpError as e:
            print(f"Erro ao enviar mensagem: {e}")

    def run(self):
        print("Bot iniciado...")
        while True:
            messages = self.fetch_messages()
            for message in messages:
                self.process_message(message)
            time.sleep(5)

# Dashboard Flask
@app.route('/')
def dashboard():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Top 10 participantes
    c.execute("SELECT username, points FROM viewers ORDER BY points DESC LIMIT 10")
    top_viewers = c.fetchall()
    
    # Últimos sorteios
    c.execute("SELECT command, prize, winner, date FROM raffles ORDER BY date DESC LIMIT 5")
    raffles = c.fetchall()
    
    # Atividade recente
    c.execute("SELECT username, last_interaction FROM viewers ORDER BY last_interaction DESC LIMIT 10")
    recent_activity = c.fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                          top_viewers=top_viewers,
                          raffles=raffles,
                          recent_activity=recent_activity)

@app.route('/data')
def data():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT username, points FROM viewers ORDER BY points DESC")
    data = c.fetchall()
    conn.close()
    return jsonify([{"username": row[0], "points": row[1]} for row in data])

@app.route('/authorize')
def authorize():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri='http://localhost:5000/callback')
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri='http://localhost:5000/callback')
    
    flow.fetch_token(authorization_response=request.url)
    
    # Salvar credenciais
    with open('token.json', 'w') as token:
        token.write(flow.credentials.to_json())
    
    return "Autenticação concluída! Você pode fechar esta aba."

# Função para obter o chat ID da live ativa
def get_live_chat_id(credentials):
    try:
        youtube = build('youtube', 'v3', credentials=credentials)
        
        broadcasts = youtube.liveBroadcasts().list(
            part="snippet",
            broadcastStatus="active"
        ).execute()

        if broadcasts.get('items'):
            broadcast_id = broadcasts['items'][0]['id']
            broadcast = youtube.liveBroadcasts().list(
                part="liveChatId",
                id=broadcast_id
            ).execute()
            return broadcast['items'][0]['liveChatId']
        return None
    except HttpError as e:
        print(f"Erro ao buscar live: {e}")
        return None

if __name__ == '__main__':
    # Obter credenciais
    credentials = get_credentials()
    
    if credentials:
        live_chat_id = get_live_chat_id(credentials)
        if live_chat_id:
            bot = LiveChatBot(live_chat_id, credentials)
            bot_thread = threading.Thread(target=bot.run)
            bot_thread.daemon = True
            bot_thread.start()
            app.run(port=5000, debug=True)
        else:
            print("Nenhuma live ativa encontrada. Inicie sua transmissão primeiro.")
    else:
        print("Autenticação necessária. Execute o aplicativo e acesse /authorize para autenticar.")
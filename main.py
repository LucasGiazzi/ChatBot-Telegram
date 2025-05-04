import os
import logging
import openai
import pyttsx3
import speech_recognition as sr
from pydub import AudioSegment
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ApplicationBuilder
from dotenv import load_dotenv
import json

load_dotenv()

# Tokens
bot_token = os.getenv("TELEGRAM_TOKEN")
openai_token = os.getenv("OPENAI_API_KEY")

openai.api_key = openai_token

# Prompt base do FuricoBot (com IA)
base_prompt = (
    "Você é o FuricoBot, um bot extrovertido, idolatrado pelos fãs da FURIA. "
    "Seu foco é o time de Counter-Strike 2 da FURIA. Responda com entusiasmo, sendo direto e divertido. "
    "Responda apenas sobre o time de Counter-Strike. Se não souber a resposta, diga que vai ficar de olho nos próximos jogos."
    "Apenas fale sobre CS:GO quando falar sobre eventos passados, por que agora existe o Counter-Strike 2 no lugar do CS:GO. Então toda vez que for falar sobre o CS:GO, utilizar Counter-Strike 2, CS2 ou preferencialmente Counter-Strike"
)

file_path = os.path.join(os.path.dirname(__file__), 'data', 'faq.json')

# Respostas fixas com múltiplas palavras-chave
with open(file_path, "r", encoding="utf-8") as f:
    faq_data = json.load(f)

# Inicializando o motor de texto-para-fala (TTS)
engine = pyttsx3.init()

def generate_audio(response_text: str) -> str:
    """Função para gerar um arquivo de áudio a partir de texto usando pyttsx3"""
    audio_file = "response.mp3"
    engine.save_to_file(response_text, audio_file)
    engine.runAndWait()
    return audio_file

def transcribe_audio(audio_file: str) -> str:
    """Função para transcrever áudio para texto usando a biblioteca speech_recognition"""
    recognizer = sr.Recognizer()

    # Conversão de OGG para WAV (caso o áudio seja OGG)
    audio = AudioSegment.from_ogg(audio_file)
    audio.export("user_audio.wav", format="wav")

    # Abre o arquivo de áudio WAV
    with sr.AudioFile("user_audio.wav") as source:
        audio = recognizer.record(source)  # Lê todo o áudio

    try:
        # Transcrição do áudio
        text = recognizer.recognize_google(audio, language="pt-BR")
        return text
    except sr.UnknownValueError:
        return "Desculpe, não consegui entender o áudio."
    except sr.RequestError:
        return "Erro ao tentar se comunicar com o serviço de transcrição."

# Função para obter resposta do ChatGPT
async def get_gpt_response(user_message: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": base_prompt}, {"role": "user", "content": user_message}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Erro no ChatGPT: {e}")
        return "Aí complicou... deu ruim aqui. Tenta de novo mais tarde, furioso!"

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salve, salve furioso! Eu sou o FuricoBot, pronto pra falar sobre Counter-Strike?")

# Lidando com mensagens
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()

    # Verifica palavras-chave nas respostas fixas
    for item in faq_data.values():
        if any(keyword in user_message for keyword in item["keywords"]):
            await update.message.reply_text(item["resposta"])
            return

    # Se não encontrar nenhuma correspondência, chama o GPT
    reply = await get_gpt_response(user_message)
    
    # Envia a resposta de texto
    await update.message.reply_text(reply)

# Lidando com mensagens de áudio
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Baixando o áudio enviado
        audio_file = await update.message.audio.get_file()
        audio_file.download("user_audio.ogg")

        # Transcrever o áudio
        transcription = transcribe_audio("user_audio.ogg")
        logging.info(f"Áudio transcrito: {transcription}")

        # Obter resposta do GPT com base na transcrição
        reply = await get_gpt_response(transcription)
        
        # Envia a resposta de texto
        await update.message.reply_text(reply)

        # Remove os arquivos de áudio após o processamento
        os.remove("user_audio.ogg")
        os.remove("user_audio.wav")
    except Exception as e:
        logging.error(f"Erro ao processar o áudio: {e}")
        await update.message.reply_text("Ocorreu um erro ao processar o áudio. Tente novamente!")

# Main
if __name__ == '__main__':
    if not bot_token or not openai_token:
        logging.error("Configure as variáveis TELEGRAM_TOKEN e OPENAI_API_KEY.")
        exit()

    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.AUDIO, handle_audio))

    logging.info("FuricoBot rodando...")
    app.run_polling()

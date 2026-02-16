import flet as ft
import speech_recognition as sr
from plyer import tts
from groq import Groq
import threading
import base64

API_KEY = "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"
client = Groq(api_key=API_KEY)

def main(page: ft.Page):
    page.title = "VEGA"
    page.bgcolor = "black"
    page.padding = 0

    # HTML UI
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <style>
            body { background-color: #000000; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: monospace; overflow: hidden; }
            .reactor { width: 200px; height: 200px; border: 5px solid #00ff00; border-radius: 50%; display: flex; justify-content: center; align-items: center; box-shadow: 0 0 30px #00ff00; animation: pulse 2s infinite; }
            h1 { color: #00ff00; font-size: 40px; text-shadow: 0 0 10px #00ff00; margin-top: 20px; }
            @keyframes pulse { 0% { box-shadow: 0 0 20px #00ff00; opacity: 0.8; } 50% { box-shadow: 0 0 60px #00ff00; opacity: 1; } 100% { box-shadow: 0 0 20px #00ff00; opacity: 0.8; } }
        </style>
    </head>
    <body>
        <div class="reactor"></div>
        <h1>V E G A</h1>
    </body>
    </html>
    """
    b64_html = base64.b64encode(html_code.encode('utf-8')).decode('utf-8')
    webview = ft.WebView(url=f"data:text/html;base64,{b64_html}", expand=True)
    page.add(webview)

    def speak(text):
        try: tts.speak(text)
        except: pass

    def listen_loop():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            speak("Online.")
            while True:
                try:
                    audio = r.listen(source)
                    text = r.recognize_google(audio).lower()
                    if "vega" in text:
                        cmd = text.replace("vega", "").strip()
                        if cmd:
                            chat = client.chat.completions.create(model="llama3-8b-8192", messages=[{"role":"user","content":cmd}])
                            speak(chat.choices[0].message.content)
                except: pass

    threading.Thread(target=listen_loop, daemon=True).start()

ft.app(target=main)
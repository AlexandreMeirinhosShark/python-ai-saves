import pyttsx3 as tts
import speech_recognition as sr
from datetime import datetime

def speak(text):
    """Fala o texto indicado — reinicializa engine para evitar bloqueio"""
    print(f"Assistant: {text}")
    engine = tts.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    engine.setProperty('voice', voices[3].id)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

recognition = sr.Recognizer()

with sr.Microphone() as source:
    recognition.adjust_for_ambient_noise(source, duration=1)
    speak("Olá, sou Maria, o teu assistente virtual. Como posso ajudar?")
    print("Preparado e ouvindo... (diz 'para' parra sair)\n")

    while True:
        try:
            print("Ouvindo...")
            audio = recognition.listen(source, timeout=5, phrase_time_limit=10)
            print("Reconhecendo...")
            query = recognition.recognize_google(audio, language='pt-PT')
            print(f"Disseste: {query}\n")

            if query.lower() in ["para", "sai"]:
                speak("Adeus!")
                break

            if "como estás" in query.lower():
                speak("Estou bem, obrigada!")
            elif "nome" in query.lower():
                speak("Chamo-me Maria.")
            elif "tempo" in query.lower():
                speak(f"A hora atual é: {datetime.now().strftime('%H:%M')}.")
            else:
                speak("Desculpa, não ouvi.")

        except sr.WaitTimeoutError:
            print("Voz não detetada, ouvindo outra vez...\n")
            continue
        except sr.UnknownValueError:
            speak("Desculpa, Não apanhei. Por favor repéte.")
            continue
        except Exception as e:
            print(f"Erro: {e}")
            continue

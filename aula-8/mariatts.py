import pyttsx3 as tts
import speech_recognition as sr
from datetime import datetime
import wikipedia as wiki
import pywhatkit
from time import sleep
import os

def speak(text):
    """Fala o texto indicado — reinicializa engine para evitar bloqueio"""
    print(f"Assistente: {text}")
    engine = tts.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    engine.setProperty('voice', voices[3].id)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

recognition = sr.Recognizer()
wiki.set_lang("pt")

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
            elif "procura" in query.lower():
                result = " ".join(w for w in query.lower().split() if w != "procura")
                speak(f"De acordo com a Wikipédia, {wiki.summary(result, sentences=2)}")
            elif "toca" in query.lower():
                song = query.lower().replace("toca", "").strip()
                speak(f"Tocando {song} no YouTube.")
                pywhatkit.playonyt(song)
            elif "mensagem" in query.lower():
                speak("Qual é o número? ")
                numb = input("Número: ")
                if numb:
                    speak("Enviando mensagem...")
                    zxa = query.lower().replace("mensagem", "").strip()
                    pywhatkit.sendwhatmsg_instantly(numb, zxa)
                    sleep(2)
                    file_path = "PyWhatKit_DB.txt"
                    if os.path.exists(file_path):
                        with open(file_path, "w") as f:
                            f.write("")
                else:
                    speak("O teu número não foi digitado. Tente novamente.")
            else:
                speak("Desculpa, não ouvi.")

        except sr.WaitTimeoutError:
            print("Voz não detetada, ouvindo outra vez...\n")
            continue
        except sr.UnknownValueError:
            speak("Desculpa, Não apanhei. Por favor repita.")
            continue
        except wiki.exceptions.WikipediaException:
            speak("Não percebi o que queres procurar. Por favor repita.")
        except Exception as e:
            print(f"Erro: {e}")
            continue

import speech_recognition as sr
import pyttsx3

def escribir_mensaje(mensaje):
    # Inicializar el motor de síntesis de voz
    engine = pyttsx3.init()
    engine.say(mensaje)
    engine.runAndWait()

def escuchar_audio():
    # Inicializar el reconocedor de voz
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Di algo...")
        audio = r.listen(source)

        try:
            # Utilizar el reconocedor de voz para transcribir el audio a texto
            texto = r.recognize_google(audio, language="es-ES")
            return texto
        except sr.UnknownValueError:
            print("No se pudo reconocer el audio.")
        except sr.RequestError as e:
            print(f"Error al solicitar los resultados del reconocimiento de voz; {e}")

# Ejemplo de uso
mensaje = escuchar_audio()
if mensaje:
    print("Texto detectado:", mensaje)
    #escribir_mensaje(mensaje)

prompts=mensaje

import openai 

openai.api_key = "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" 
#while True: 
prompt = prompts
#if prompt == "exit": 
    #break 
completion = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=2048) 

print(completion.choices[0].text)
import pyaudio
import numpy as np

# Configuración de la grabación de audio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Crear objeto de PyAudio
audio = pyaudio.PyAudio()

# Obtener el índice del dispositivo de entrada del micrófono
input_device_index = None
for i in range(audio.get_device_count()):
    info = audio.get_device_info_by_index(i)
    if info['maxInputChannels'] > 0:
        input_device_index = i
        break

# Comprobar si se encontró un dispositivo de entrada del micrófono
if input_device_index is None:
    print("No se encontró un dispositivo de entrada del micrófono.")
    audio.terminate()
    exit()

# Configurar el flujo de audio
stream = audio.open(
    input_device_index=input_device_index,
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

print("Iniciando grabación. Presiona Ctrl+C para detener.")

try:
    while True:
        # Leer datos del flujo de audio
        data = stream.read(CHUNK)
        # Convertir los datos en un array de tipo numpy
        audio_data = np.frombuffer(data, dtype=np.int16)
        # Realizar cualquier procesamiento adicional necesario aquí
        # ...

except KeyboardInterrupt:
    print("Grabación detenida.")

# Detener el flujo de audio
stream.stop_stream()
stream.close()
audio.terminate()

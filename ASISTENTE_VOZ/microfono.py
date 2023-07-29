import pyaudio

# Obtén la lista de dispositivos de entrada
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"Index: {i}, Name: {info['name']}")

# Configura el dispositivo de entrada deseado
input_device_index =1
stream = p.open(input_device_index=input_device_index,
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024)

# Lee los datos del micrófono
data = stream.read(1024)

# Cierra el flujo de audio
stream.stop_stream()
stream.close()
p.terminate()

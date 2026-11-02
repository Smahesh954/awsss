import sounddevice as sd
from scipy.io.wavfile import write

duration = 10
sample_rate = 16000

print("Recording starts now. Speak clearly for 10 seconds!")

audio = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="int16"
)

sd.wait()

write("meeting.wav", sample_rate, audio)

print("Saved fresh recording to meeting.wav")

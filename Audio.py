import sounddevice as sd
from scipy.io.wavfile import write
from openai import OpenAI

client = OpenAI(api_key="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")

def record_and_save_audio(filename="audio.wav", duration=7, samplerate=44100):
    try:
        input_device_id = 0  # Change this to the desired input device ID
        audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=2, dtype='int16', device=input_device_id)

        sd.wait()

        # Save the audio data to a WAV file
        write(filename, samplerate, audio_data)

        # Obtain transcript from OpenAI API
        with open("audio.wav", "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file, 
                response_format="text",
                language="en"
            )

        # Save the transcript to a text file
        text_filename = "transcript.txt"
        with open(text_filename, "w") as text_file:
            text_file.write(transcript)

        return transcript

    except KeyboardInterrupt:
        print("\nRecording stopped.")

if __name__ == "__main__":
    output_filename = "audio.wav"
    record_and_save_audio(output_filename)

import streamlit as st
import whisper
import time
from pydub import AudioSegment
import ffmpeg

# Function to check if ffmpeg and ffprobe are installed
def check_ffmpeg():
    try:
        ffmpeg.probe('')
    except ffmpeg.Error as e:
        st.error("ffmpeg is not installed or not found in the PATH")
        return False
    return True

# Load the Whisper model
model = whisper.load_model("base")

# Title of the Streamlit app
st.title(" SEMA: Audio Transcription App")

# Check if ffmpeg and ffprobe are installed
if check_ffmpeg():
    # Upload audio file
    audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])

    if audio_file is not None:
        # Save the uploaded file to disk
        with open("uploaded_audio.m4a", "wb") as f:
            f.write(audio_file.getbuffer())

        # Convert audio to the required format
        audio = AudioSegment.from_file("uploaded_audio.m4a")
        audio.export("converted_audio.wav", format="wav")

        # Transcribe the audio file
        result = model.transcribe("converted_audio.wav")

        # Split the transcription into sentences
        sentences = result["text"].split(". ")

        # Display each sentence with a delay
        st.write("Transcription:")
        for sentence in sentences:
            if sentence.strip():  # Check if the sentence is not empty
                st.write(sentence.strip() + ".")
                time.sleep(2)  # Add a short delay before displaying the next sentence
else:
    st.error("ffmpeg is required but not found. Please install ffmpeg to use this app.")

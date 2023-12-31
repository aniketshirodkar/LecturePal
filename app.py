# Import necessary libraries and modules
from flask import Flask, render_template, request, jsonify
import assemblyai as aai
from transformers import pipeline
import requests
import os
import tempfile

# Initialize Flask app
app = Flask(__name__)

# Initialize a summarization pipeline using the transformers library
summarizer = pipeline("summarization", model="Falconsai/text_summarization")

# Replace with your AssemblyAI API key
aai.settings.api_key = "d1fadd54d7a646d5a1fb0636577b10f6"

# Define the index route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Define the route for handling video transcription
@app.route('/transcribe', methods=['POST'])
def transcribe():
    # Check if the file is present in the request
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    # Check if a file is selected
    if file.filename == '':
        return "No selected file"

    # Save the uploaded file to a temporary location
    temp_dir = tempfile.TemporaryDirectory()
    temp_file_path = os.path.join(temp_dir.name, file.filename)
    file.save(temp_file_path)

    try:
        # Use AssemblyAI to transcribe the video
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(temp_file_path)
        result = transcript.text

    except aai.error.AssemblyAIError as e:
        # Handle AssemblyAI API errors
        result = f"ErrorA: {e}"

    finally:
        # Clean up the temporary directory
        temp_dir.cleanup()

    # Render the transcribe_result.html template with the transcription result
    return render_template('transcribe_result.html', transcription=result)

# Function to split text into chunks for summarization
# Summarizer works best with smaller chunks
def split_text_into_chunks(text, words_per_chunk=500):
    words = text.split()
    chunks = [words[i:i + words_per_chunk] for i in range(0, len(words), words_per_chunk)]
    return [' '.join(chunk) for chunk in chunks]

# Define the route for summarization
@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        # Get the text from the request
        text = request.json.get('text', '')
        text = text.replace("&#39;", "'")
        
        # Split text into chunks and summarize each chunk
        chunks = split_text_into_chunks(text, words_per_chunk=330)
        summary = []
        for i, chunk in enumerate(chunks, start=1):
            summary.append(summarizer(chunk, max_length=230, min_length=30, do_sample=False)[0]['summary_text'])
        
        # Join the summaries and return as JSON
        summary = "\n\n".join(summary)
        print(summary)
        return jsonify({'summary': summary}), 200, {'Content-Type': 'application/json'}

    except Exception as e:
        return jsonify({'error': f"Error summarizing: {e}"})


# Run the Flask app if the script is executed directly
if __name__ == '__main__':
    app.run(debug=True)

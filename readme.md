# Video Transcription and Summarization Web App

This Flask web application allows users to upload video files for transcription and provides a summarization feature using AssemblyAI and the transformers library.

## Prerequisites

Make sure you have the following installed:

- [Python](https://www.python.org/downloads/) (>=3.6)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repo.git
    ```
2. Install the required packages:

    ```bash
    pip install flask assemblyai transformers
    ```

## Usage

1. Run the Flask application:

    ```bash
    python app.py
    ```

2. Open your web browser and go to [http://localhost:5000/](http://localhost:5000/).

3. Upload a video file for transcription.

4. View the transcription result.

5. Click the "Summarize" button to obtain a summary of the transcription.

## Configuration

- Replace `YOUR_ASSEMBLYAI_API_KEY` in `app.py` with your AssemblyAI API key.

## Dependencies

- Flask
- AssemblyAI
- Transformers (Hugging Face)


# Faceless Video Generator

Faceless Video Generator is an AI-powered tool for creating engaging videos from any topic. By leveraging state-of-the-art AI for script generation, text-to-speech audio synthesis, and background video matching, this project generates complete videos with minimal user input.

## Features

- **Script Generation:** Automatically generates a script based on the provided topic.
- **Audio Synthesis:** Utilizes text-to-speech technology to generate high-quality audio narration.
- **Timed Captions:** Creates captions that align with the audio for accessibility and clarity.
- **Background Video Search:** Searches and fetches suitable background video clips via video search queries.
- **Video Rendering:** Combines the synthesized audio, captions, and background visuals to produce the final video output.
- **Gradio Interface:** Provides a user-friendly interactive interface for generating videos.

## Prerequisites

- Python 3.8 or later
- [Gradio](https://gradio.app/) for the web interface
- Required Python packages listed in `requirements.txt`

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/Faceless-video.git
   cd Faceless-video
    ```

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **API Keys:**

    -   This project requires API keys for various services.
    -   Create a `.env` file in the project root directory.
    -   Add your API keys to the `.env` file as follows:

        ```
        GROQ_API_KEY=your_groq_api_key
        PEXELS_API_KEY=your_pexels_api_key
        ```

        > **Note:** Ensure you have accounts and API keys for Groq, and Pexels.

## Usage

1.  **Run the Gradio Interface:**

    ```bash
    python app.py
    ```

2.  **Access the Interface:**

    -   Open your web browser and go to the address provided in the console (usually `http://localhost:7860`).

3.  **Generating Videos:**

    -   Enter the topic for the video.
    -   Click the "Generate Video" button.
    -   The script, audio, captions, and video will be generated automatically.
    -   The final video will be displayed in the interface.

## Configuration

You can configure various aspects of the video generation process by modifying the parameters in the Gradio interface or directly in the Python scripts.

-   **Script Length:** Adjust the length of the generated script.
-   **Voice Settings:** Customize the voice used for audio synthesis.
-   **Video Clip Duration:** Set the duration of the background video clips.
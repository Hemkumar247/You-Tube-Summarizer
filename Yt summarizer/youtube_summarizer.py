import requests
import os
import google.generativeai as genai
from dotenv import load_dotenv

def summarize_youtube_transcript(video_id):
    # Step 1: Extract the YouTube video transcript
    url = "https://www.searchapi.io/api/v1/search"
    params = {
        "engine": "youtube_transcripts",
        "video_id": video_id,
        "api_key": "yjCgm5n6uxqa9haDABsC8bDQ"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "transcripts" not in data or not data["transcripts"]:
        return "No transcript found for this video."

    transcript_text = ""
    for item in data["transcripts"]:
        transcript_text += item["text"] + " "

    # Step 2: Summarize the transcript using Gemini
    gemini_api_key = < your API Key Here >
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-pro')

    # Split the transcript into chunks (if needed)
    max_chunk_length = 10000  # Adjust as needed
    chunks = [transcript_text[i:i + max_chunk_length] for i in range(0, len(transcript_text), max_chunk_length)]

    summaries = []
    for chunk in chunks:
        prompt = f"Summarize the following text: {chunk}"
        try:
            response = model.generate_content(prompt)
            summaries.append(response.text)
        except Exception as e:
            return f"Error during summarization: {e}"

    # Combine the summaries
    final_summary = "\\n".join(summaries)

    return final_summary

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    # Extract video ID from URL
    try:
        video_id = video_url.split("v=")[1].split("&")[0]
    except IndexError:
        print("Invalid YouTube URL.")
        exit()
    summary = summarize_youtube_transcript(video_id)
    print(summary)

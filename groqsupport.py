import os
import requests
import logging

class GroqSupport:
    def __init__(self, api_key=None):
        self.logger = logging.getLogger(__name__)
        if api_key is None:
            self.api_key = os.environ.get("GROQ_API_KEY")
        else:
            self.api_key = api_key

        # Check if API key is set
        if not self.api_key:
            self.logger.error("API key not found or empty.")
            # For debugging purposes only; remove in production
            print("API key is missing or empty.")

        self.endpoint = "https://api.groq.com/openai/v1/chat/completions"
  

    def get_meditation_prompt(self):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (compatible; TechCrunchFarsiBot/1.0)'
        }

        data = {
            "model": "gemma2-9b-it",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a meditation coach that provides a bilingual meditation text for a 1-5 minutes practice. The first part will be in English, without delimeters followed by its Persian translation."
                },
                {
                    "role": "user",
                    "content": "Please provide a meditation."
                }
            ],
            "temperature": 0.7,
        }

        response = requests.post(self.endpoint, json=data, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            # Extract the message from Groq's response (considering the format)
            return response_data['choices'][0]['message']['content']
        else:
            self.logger.error(f"Error fetching meditation prompt: {response.status_code}")
            print("Error fetching meditation prompt.")
            return None

    # def translate_title(self, content):

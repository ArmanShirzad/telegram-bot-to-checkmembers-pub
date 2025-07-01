# MemCast Telegram Bot
![memcastbot](https://github.com/user-attachments/assets/6532f75d-263c-41b3-a394-612f22ac3d0f)

MemCast is a versatile Telegram bot offering users a range of services, including daily meditation prompts, AI chatbot interactions, and media downloads. To access these features, users are encouraged to join our Telegram channel.

## Features

- **Daily Meditation Prompts:** Receive bilingual (English and Persian) meditation prompts to enhance mindfulness.
- **AI Chatbot Interaction:** Engage in conversations with an AI-powered chatbot for various inquiries.
- **Media Downloads:** Access and download a selection of media content.
- **Channel Membership Verification:** Ensures users are members of the designated Telegram channel to utilize services.

## Commands

- `/start` - Start the bot // شروع ربات
- `/meditate` - Receive a meditation prompt // دریافت مدیتیشن
- `/chat` - Chat with the AI bot // گفتگو با ربات
- `/download` - Access media downloads // دانلود رسانه
- `/help` - Get help // دریافت راهنما
- `/feedback` - Send feedback // ارسال بازخورد

## Setup and Installation

### Prerequisites

- Python 3.8+
- A Telegram bot token (create one via [BotFather](https://t.me/BotFather))
- Groq API key

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/MemCast.git
   cd MemCast
   ```

2. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**

   Create a `.env` file in the project root directory and add the following:

   ```env
   TELEGRAM_TOKEN=your_telegram_bot_token
   GROQ_API_KEY=your_groq_api_key
   CHANNEL_USERNAME=your_channel_username_without_@
   ```

5. **Run the Bot:**

   ```bash
   python bot.py
   ```

## Usage

- **Start the Bot:** Send `/start` to initiate interaction.
- **Begin Meditation:** Send `/meditate` to receive a meditation prompt.
- **Chat with AI:** Send `/chat` to engage with the AI chatbot.
- **Download Media:** Send `/download` to access available media.
- **Get Help:** Send `/help` to see available commands.
- **Send Feedback:** Send `/feedback` followed by your message to provide feedback.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.


 Arckybot - Your AI Assistant

#![logo](https://github.com/user-attachments/assets/ad887a34-b2e8-4ed4-8a48-8c6885dcd4e6)



## Overview

Arckybot is a sleek AI assistant chatbot created with Streamlit and powered by Groq's LLaMa 3.2 90B model. With its distinctive purple-themed interface, Arckybot provides an intuitive chat experience for users seeking AI-powered guidance and troubleshooting assistance.

## Features

- **Custom UI**: Elegant chat interface with a distinctive purple color scheme
- **Natural Responses**: Real-time typing animation for a more engaging experience
- **Chat History**: Conversation tracking with timestamps for each message
- **Advanced AI**: Integration with Groq's LLaMa 3.2 90B model for high-quality responses
- **Responsive Design**: Clean layout that adapts to different screen sizes

## Project Structure

```
arckybot/
├── __pycache__/     # Python cache directory
├── .env             # Environment variables file (API keys)
├── .gitignore       # Git ignore rules
├── conversation_history.json  # Conversation data storage
├── logo.png         # Application logo
├── README.md        # This documentation file
└── streamlit_app.py # Main application code
```

## Setup Instructions

1. Ensure you have Python 3.7+ installed
2. Install the required dependencies:
   ```bash
   pip install streamlit requests python-dotenv
   ```

3. Create or edit your `.env` file with your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. Run the application:
   ```bash
   streamlit run streamlit_app.py
   ```

## Customization Options

### Visual Theme
Modify the CSS in the `set_page_style()` function to change colors, fonts, or layout elements.

### AI Configuration
Change the model or system prompt in the `generate_response()` method:

```python
payload = {
    'model': 'llama-3.2-90b-vision-preview',  # Change model here
    'messages': [
        {"role": "system", "content": "You are Arckybot, a helpful AI assistant for troubleshooting and guidance."},  # Customize personality here
        {"role": "user", "content": user_input}
    ]
}
```

## Requirements

- Python 3.7+
- Streamlit
- Requests
- python-dotenv
- Groq API access

# Arckybot

![Arckybot Logo](logo.png)

Arckybot is an AI assistant developed with Streamlit and using the Groq API to answer questions and assist with problem solving.

##  Features
-  **Interactive chatbot** with a modern and fluid user interface
-  **Use of Groq API** to generate precise responses
-  **Customized interface** with a clean and pleasant style
-  **Conversation history** to track exchanges
-  **API key management** via a `.env` file

##  Project structure

![Capture d'écran 2025-03-31 014529](https://github.com/user-attachments/assets/ec62615c-3972-4e23-85dc-64ba5615f481)

- `streamlit_app.py`: Main application code
- `.env`: Stores the Groq API key
- `conversation_history.json`: Saves conversation history
- `logo.png`: Application logo
- `README.md`: Project documentation

##  Installation and setup
### 1️ Clone the repository
```bash
git clone https://github.com/linathabet101/Arckybot.git
cd Arckybot
```

### 2️ Create virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate  #  macOS/Linux
venv\Scripts\activate  #  Windows
pip install -r requirements.txt
```

### 3️ Configure API Key
Create a .env file at project root and add:
```ini
GROQ_API_KEY=your_api_key_here
```

### 4️ Launch the application
```bash
streamlit run streamlit_app.py
```
The application will be available at:  [http://localhost:8501](http://localhost:8501)


![Capture d'écran 2025-03-31 024028](https://github.com/user-attachments/assets/8285a96e-a94d-4551-874c-c99e71c7260f)


##  Usage
1. Enter a question in the chat box.
2. Arckybot generates a response using Groq API.3. Conversation history is displayed dynamically.

##  Example

![Capture d'écran 2025-03-31 023917](https://github.com/user-attachments/assets/a3527286-be92-4f96-91ed-bf9d19b881dc)












##  Contact
e-mail address: linathabet101@gmail.com


import os
import requests
import streamlit as st
from dotenv import load_dotenv
import time
import random

# Load API key
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

# Arckybot class
class Arckybot:
    def __init__(self):
        self.api_key = API_KEY
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def generate_response(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": 'llama-3.1-8b-instant',
            "messages": [
                {"role": "system", "content": "You are Arckybot, an expert AI in maintenance. Answer as clearly and accurately as possible."},
                {"role": "user", "content": prompt},
            ],
        }
        response = requests.post(self.url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return "Arckybot encountered an error."

# --- PAGE CONFIG ---
st.set_page_config(page_title="Arckybot vs Expert", layout="wide")

# --- INIT STATE ---
if "score" not in st.session_state:
    st.session_state.score = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "game_on" not in st.session_state:
    st.session_state.game_on = True
if "questions_asked" not in st.session_state:
    st.session_state.questions_asked = 0
if "arcky_response" not in st.session_state:
    st.session_state.arcky_response = None
if "evaluation_done" not in st.session_state:
    st.session_state.evaluation_done = False
if "current_question" not in st.session_state:
    st.session_state.current_question = ""

# Constants
MAX_QUESTIONS = 15
POINTS_FOR_EVALUATION = 5
POINTS_FOR_EXPERT_ANSWER = 10
POINTS_PARTIAL_CORRECT = 3
REWARD_THRESHOLD = 100
REWARD_DISCOUNT = "70%"

# --- INIT BOT ---
bot = Arckybot()

# --- HEADER with Title ---
header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    st.title("Arckybot vs Expert")
    st.subheader("Devine la bonne réponse à un problème de maintenance")

# --- PROGRESS BAR ---
progress_text = f"Question {st.session_state.questions_asked}/{MAX_QUESTIONS}"
progress_bar = st.progress(st.session_state.questions_asked / MAX_QUESTIONS)

# --- SCORE DISPLAY --- (centered, animated, one-line)
st.markdown(f"""
<style>
/* Default style for light mode */
.score-box {{
    width: 100%;
    max-width: 100%;
    font-size: 18px;
    font-weight: normal;
    color: #1E88E5;
    padding: 8px 0;
    border-radius: 8px;
    background: linear-gradient(135deg, #E3F2FD, #BBDEFB); /* Light blue gradient */
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    text-align: center;
    animation: pulse 2s infinite;
    margin: 10px 0 20px 0;
}}

/* Green score box for when threshold is reached */
.score-box-success {{
    background: linear-gradient(135deg, #E8F5E9, #C8E6C9); /* Light green gradient */
    color: #2E7D32; /* Darker green text */
    animation: success-pulse 2s infinite;
}}

/* Override style for dark theme */
@media (prefers-color-scheme: dark) {{
    .score-box {{
        background: linear-gradient(135deg, #0A1B2A, #102840); /* Very dark blue gradient */
        color: #BBDEFB;  /* Lighter blue text for contrast in dark mode */
        box-shadow: 0 2px 10px rgba(16, 40, 64, 0.6); /* Subtle dark blue shadow */
    }}
    
    .score-box-success {{
        background: linear-gradient(135deg, #1B3624, #1E4620); /* Dark green gradient for dark mode */
        color: #81C784; /* Light green text for contrast in dark mode */
        box-shadow: 0 2px 10px rgba(46, 125, 50, 0.4); /* Green shadow */
    }}
}}

@keyframes pulse {{
    0% {{ box-shadow: 0 0 0 0 rgba(30, 136, 229, 0.4); }}
    70% {{ box-shadow: 0 0 0 10px rgba(30, 136, 229, 0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(30, 136, 229, 0); }}
}}

@keyframes success-pulse {{
    0% {{ box-shadow: 0 0 0 0 rgba(46, 125, 50, 0.4); }}
    70% {{ box-shadow: 0 0 0 10px rgba(46, 125, 50, 0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(46, 125, 50, 0); }}
}}
</style>

<div class="score-box {{'score-box-success' if st.session_state.score >= REWARD_THRESHOLD else ''}}">
    Score : {st.session_state.score} points / {REWARD_THRESHOLD} pour gagner la réduction
</div>
""", unsafe_allow_html=True)

# --- INPUT & GAME LOGIC ---
if st.session_state.game_on and st.session_state.questions_asked < MAX_QUESTIONS:
    
    # Question input phase
    if not st.session_state.arcky_response:
        question = st.text_input("Pose une question liée à une panne (ou problème) :", 
                               key="user_question", 
                               value=st.session_state.current_question)
        if st.button("Soumettre la question", key="submit_question", 
                   help="Posez votre question à Arckybot"):
            if question:
                st.session_state.current_question = question
                with st.spinner("Arckybot réfléchit..."):
                    arcky_answer = bot.generate_response(question)
                    st.session_state.arcky_response = arcky_answer
                    st.session_state.questions_asked += 1
                    progress_bar.progress(st.session_state.questions_asked / MAX_QUESTIONS)
                st.rerun()
    
    # Evaluation phase
    elif not st.session_state.evaluation_done:
        st.markdown(f"**Arckybot:** {st.session_state.arcky_response}")
        st.markdown("### Évaluez la réponse d'Arckybot:")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Correcte", key="correct_btn"):
                st.session_state.history.append(("Arckybot", st.session_state.arcky_response))
                st.session_state.history.append(("Évaluation", "Correcte"))
                st.session_state.evaluation_done = True
                st.session_state.score += POINTS_FOR_EVALUATION
                st.rerun()
        with col2:
            if st.button("Partiellement correcte", key="partial_btn"):
                st.session_state.history.append(("Arckybot", st.session_state.arcky_response))
                st.session_state.history.append(("Évaluation", "Partiellement correcte"))
                st.session_state.evaluation_done = True
                st.session_state.score += POINTS_PARTIAL_CORRECT
                st.rerun()
        with col3:
            if st.button("Incorrecte", key="incorrect_btn"):
                st.session_state.history.append(("Arckybot", st.session_state.arcky_response))
                st.session_state.history.append(("Évaluation", "Incorrecte"))
                st.session_state.evaluation_done = True
                st.session_state.score += POINTS_FOR_EVALUATION
                st.rerun()
    
    # Expert answer phase
    else:
        st.markdown(f"**Arckybot:** {st.session_state.arcky_response}")
        
        # Get last evaluation from history
        last_eval = next((item[1] for item in reversed(st.session_state.history) if item[0] == "Évaluation"), None)
        st.markdown(f"**Évaluation:** {last_eval}")
        
        st.markdown("### Votre réponse d'expert (optionnel):")
        expert_answer = st.text_area("Expliquez la bonne réponse au problème (optionnel):", key="expert_input", height=150)
        
        # Submit the expert answer (or skip)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Soumettre votre expertise", key="submit_expert"):
                if expert_answer:
                    st.session_state.history.append(("Expert", expert_answer))
                    st.session_state.score += POINTS_FOR_EXPERT_ANSWER
                st.session_state.arcky_response = None
                st.session_state.evaluation_done = False
                st.session_state.current_question = ""
                st.success(f"Réponse soumise! +{POINTS_FOR_EXPERT_ANSWER} points")
                st.rerun()
    
        with col2:
            if st.button("Passer cette question", key="skip_question"):
                # Skip expert answer and move to next question
                st.session_state.arcky_response = None
                st.session_state.evaluation_done = False
                st.session_state.current_question = ""
                st.success("Question passée!")
                st.rerun()

# --- END GAME STATE ---
elif st.session_state.questions_asked >= MAX_QUESTIONS:
    st.markdown("## Partie terminée!")
    st.markdown(f"### Score final: {st.session_state.score} points")
    
    # Check if reward threshold met
    if st.session_state.score >= REWARD_THRESHOLD:
        st.success(f"""
            FÉLICITATIONS!
            Vous avez gagné une réduction de {REWARD_DISCOUNT} sur les produits Arcana Soft!
            Utilisez le code: ARCKYEXPERT2025 lors de votre prochain achat.
        """)
    else:
        st.warning(f"""
            Si proche!
            Il vous manquait {REWARD_THRESHOLD - st.session_state.score} points pour obtenir la réduction de {REWARD_DISCOUNT}.
            Essayez encore pour gagner le prix!
        """)
    
    if st.button("Nouvelle partie", key="reset_game"):
        st.session_state.history = []
        st.session_state.score = 0
        st.session_state.questions_asked = 0
        st.session_state.arcky_response = None
        st.session_state.evaluation_done = False
        st.session_state.current_question = ""
        st.rerun()

# --- CONVERSATION HISTORY ---
if st.session_state.history:
    st.markdown("## Historique des échanges")
    for author, msg in st.session_state.history:
        with st.container():
            if author == "Évaluation":
                st.markdown(f"**Évaluation:** {msg}")
            else:
                st.markdown(f"**{author}:** {msg}")


# Sidebar with logo, game rules and info
with st.sidebar:
    st.image("Arcky.png", width=120)
    
    st.markdown("## Règles du jeu")
    st.markdown(f"""
    1. Posez 15 questions sur la maintenance  
    2. Évaluez la réponse d'Arckybot  
    3. Donnez votre réponse d'expert  
    4. Gagnez des points:  
       - +{POINTS_FOR_EVALUATION} points pour évaluation correcte/incorrecte  
       - +{POINTS_PARTIAL_CORRECT} points pour évaluation partielle  
       - +{POINTS_FOR_EXPERT_ANSWER} points pour votre réponse  
    5. Atteignez {REWARD_THRESHOLD} points pour une réduction de {REWARD_DISCOUNT}!
    """)
    
    st.markdown("---")
    st.markdown("## Seuil de récompense")
    progress_to_reward = min(st.session_state.score / REWARD_THRESHOLD, 1.0)
    st.progress(progress_to_reward)
    st.markdown(f"{st.session_state.score} / {REWARD_THRESHOLD} points")
    
    st.markdown("---")
    st.markdown("## Arcana Soft")
    st.markdown("Solutions professionnelles de maintenance assistée par IA")
    st.markdown("[https://www.arcana-soft.com](https://www.arcana-soft.com)")

from dotenv import load_dotenv
import gradio as gr
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# --- Step 1: Define Mood Response Logic ---
def mood_suggestions(mood: str) -> str:
    mood = mood.lower()
    if "happy" in mood:
        return "That's wonderful! 🌟 Keep spreading positivity. Maybe write down one thing you're grateful for today."
    elif "sad" in mood or "down" in mood:
        return "I'm sorry you're feeling low 💙. Try a 5-minute walk, listen to your favorite song, or take a deep breath."
    elif "stressed" in mood or "anxious" in mood:
        return "Stress is tough 😔. How about a quick breathing exercise? Inhale for 4s, hold 4s, exhale 4s."
    elif "angry" in mood:
        return "Anger is natural ❤️. Maybe step away for a bit or write down your thoughts to release the tension."
    elif "neutral" in mood or "ok" in mood:
        return "Got it 👍. Even on neutral days, a small habit like journaling or stretching can lift your energy."
    else:
        return "Thanks for sharing 💬. Would you like to tell me a bit more about how you're feeling?"

# --- Step 2: Wrap in LLM Agent (optional, adds friendliness) ---
def mood_check(message: str, history: list) -> str:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

    system_message = """You are a kind and supportive Mood Check-in Assistant.
    Always respond with empathy and encouragement.
    After acknowledging the user's mood, share 1 simple tip, activity, or suggestion.
    """

    # Basic prompt (you can expand with LangChain agent if you want tool calling later)
    prompt = ChatPromptTemplate.from_messages(
        [("system", system_message),
         ("human", "{input}")]
    )

    formatted = prompt.format_messages(input=message)
    ai_response = llm.invoke(formatted)

    # Combine LLM response + mood-specific suggestion
    suggestion = mood_suggestions(message)
    return f"{ai_response.content}\n\n💡 Tip: {suggestion}"

# --- Step 3: UI Setup ---
PAGE_TITLE = "AI Mood Check-in Buddy 💬"
LOGO_URL = "https://raw.githubusercontent.com/hereandnowai/images/refs/heads/main/logos/logo-of-here-and-now-ai.png"
ASSISTANT_AVATAR_URL = "https://raw.githubusercontent.com/hereandnowai/images/refs/heads/main/logos/caramel-face.jpeg"

description_md = f"""
<img src='{LOGO_URL}' width='500' style='display: block; margin: auto;'>
<br>Your friendly AI Mood Buddy 🤗. Share your feelings and get small tips to feel better or stay positive!
"""

gr.ChatInterface(
    fn=mood_check,
    title=PAGE_TITLE,
    description=description_md,
    chatbot=gr.Chatbot(
        type='messages',
        avatar_images=[None, ASSISTANT_AVATAR_URL]
    ),
    type='messages'
).launch()

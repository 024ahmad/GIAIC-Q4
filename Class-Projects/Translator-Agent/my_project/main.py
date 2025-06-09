# streamlit_translator_app.py

from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import os
import streamlit as st
import asyncio

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Streamlit Page Settings
st.set_page_config(page_title="Translator Agent", layout="centered")
st.title("🌍 AI Translator Agent")
st.markdown("Use AI to translate your sentence into another language instantly.")

# Check for API key
if not gemini_api_key:
    st.error("❌ GEMINI_API_KEY is not set. Please check your .env file.")
    st.stop()

# Initialize OpenAI client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Define model and config
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Define agent
translator = Agent(
    name="Translator Agent",
    instructions=(
        "You are a translator agent. The user will provide a sentence along with the name of the target language. "
        "Identify the target language from the input and translate only the sentence into that language. "
        "Reply with translation only — no explanation."
    )
)

# Main input section
with st.container():
    st.markdown("### ✍️ Enter the sentence you want to translate:")
    user_input = st.text_area("Type your sentence below", height=70)

    st.markdown("### 🌐 Select Target Language:")
    language_options = ["Roman Urdu", "Urdu", "English", "French", "Spanish", "German", "Chinese"]
    cols = st.columns(len(language_options))
    target_language = None
    for i, lang in enumerate(language_options):
        if cols[i].button(lang):
            target_language = lang

# If language selected and input given
if target_language and user_input.strip():
    prompt = f"Translate this into {target_language}: {user_input}"
    with st.spinner(f"Translating into {target_language}..."):
        try:
            # Ensure asyncio loop is available
            try:
                asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # Call translator agent
            response = Runner.run_sync(
                translator,
                input=prompt,
                run_config=config
            )
            st.success("✅ Translation Complete:")
            st.text_area("📘 Translated Sentence", response.final_output, height=100)

        except Exception as e:
            st.error(f"❌ Error occurred: {e}")

elif target_language and not user_input.strip():
    st.warning("⚠️ Please enter a sentence to translate.")


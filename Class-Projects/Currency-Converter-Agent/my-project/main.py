import streamlit as st
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, Runner, function_tool
import requests
import os
from dotenv import load_dotenv
import asyncio

# --- Load environment variable ---
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# --- Tool Function (Real-time API Call) ---
@function_tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    try:
        response = requests.get(f"https://open.er-api.com/v6/latest/{from_currency}")
        data = response.json()

        if data["result"] != "success":
            return f"Failed to get exchange rate for {from_currency}."

        rate = data["rates"].get(to_currency)
        if rate is None:
            return f"Conversion rate from {from_currency} to {to_currency} is not available."

        converted = amount * rate
        return f"{amount} {from_currency} is approximately {converted:.2f} {to_currency} (live rate)."

    except Exception as e:
        return f"Error occurred: {str(e)}"

# --- Agent Setup ---
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

agent = Agent(
    name="Currency Converter Agent",
    instructions="You convert currency using the tool provided.",
    tools=[convert_currency]
)

# --- Currency Dropdown Options with Flags ---
currency_options = {
    "🇺🇸 USD": "USD",
    "🇵🇰 PKR": "PKR",
    "🇪🇺 EUR": "EUR",
    "🇮🇳 INR": "INR",
    "🇬🇧 GBP": "GBP",
    "🇨🇦 CAD": "CAD",
    "🇦🇪 AED": "AED",
    "🇯🇵 JPY": "JPY",
    "🇨🇳 CNY": "CNY",
    "🇦🇺 AUD": "AUD"
}

# --- Streamlit UI ---
st.set_page_config(page_title="💱 Currency Converter", page_icon="💹", layout="centered")
st.markdown("<h1 style='text-align: center;'>💱 Currency Converter (Live using Agent)</h1>", unsafe_allow_html=True)
st.markdown("### 🔄 Convert currency using real-time exchange rates and OpenAI agent")

with st.form("conversion_form"):
    amount = st.number_input("💵 Enter amount", min_value=0.0, step=1.0, format="%.2f")

    col1, col2 = st.columns(2)
    with col1:
        from_currency_label = st.selectbox("🌐 From Currency", options=list(currency_options.keys()))
    with col2:
        to_currency_label = st.selectbox("🌍 To Currency", options=list(currency_options.keys()))

    submitted = st.form_submit_button("🔁 Convert")

# --- Conversion Logic (async-safe) ---
if submitted:
    from_currency = currency_options[from_currency_label]
    to_currency = currency_options[to_currency_label]

    if from_currency == to_currency:
        st.warning("❗ Please select two different currencies.")
    else:
        query = f"Convert {amount} {from_currency} to {to_currency}"
        with st.spinner("🔄 Converting with Agent..."):
            result = asyncio.run(Runner.run(agent, query, run_config=config))
            st.success("✅ Conversion complete!")
            st.markdown(f"""
                <div style='
                    background-color: #f0f8ff;
                    padding: 20px;
                    border-radius: 10px;
                    border: 1px solid #ccc;
                    font-size: 18px;
                    text-align: center;
                '>
                    {result.final_output}
                </div>
            """, unsafe_allow_html=True)

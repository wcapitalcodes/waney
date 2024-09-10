import uuid
from regex import W
import streamlit as st
import openai
from llama_index.llms.openai import OpenAI
from modules.retirement_calculator import show_form_dialog
from langchain_community.chat_message_histories import ChatMessageHistory
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from mixpanel import Mixpanel


try:
    from llama_index import (
        VectorStoreIndex,
        ServiceContext,
        Document,
        SimpleDirectoryReader,
    )
except ImportError:
    from llama_index.core import (
        VectorStoreIndex,
        ServiceContext,
        Document,
        SimpleDirectoryReader,
    )

st.set_page_config(
    page_title="Chat with Wani. Answer all your questions related to Wahine Capital, women and finance.",
    page_icon="",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)
st.sidebar.header("Chat with Wani")
st.sidebar.write(
    "Chat with Wani. Answer all your questions related to Wahine Capital, women and finance. \n Whatever Wani says is not financial advice, and users should seek further knowledge through a financial advisor. Contact Wahine Capital at hellowahine@wcapital.asia or ask Wahine Experts at https://wahine.wcapital.asia/ask."
)

openai.api_key = st.secrets.openai_key

mp = Mixpanel(st.secrets["mixpanel"]["token"])

user_id = str(uuid.uuid4())

# Track a page view
mp.track(user_id, "Page View", {"page": "Wani Chat"})

gradient_text_html = """
<style>
 .st-emotion-cache-1c7y2kd {
                flex-direction: row-reverse;
                text-align: right;
            }
.gradient-text {
    font-weight: bold;
    background: -webkit-linear-gradient(left, #8e1246, #047481);
    background: linear-gradient(to right, #8e1246, #047481);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline;
    font-size: 3em;
}
</style>
<div style="display: flex;align-items:center;margin-bottom:50px;"><img src="https://assets.lifeofw.com/waney.png" width="80px" style="margin-right:10px;" /><div class="flex flex-col"><h5 class="gradient-text">Chat with Wani</h5><h6>Wani will answer all your questions related to Wahine Capital, W Vault, Women and Finance. Whatever Wani says is not financial advice, and users should seek further knowledge through a financial advisor..</h6></div></div>
"""
# Load Google Sheets credentials from Streamlit secrets
gsheet_credentials = {
    "type": st.secrets["connections"]["gsheets"]["type"],
    "project_id": st.secrets["connections"]["gsheets"]["project_id"],
    "private_key_id": st.secrets["connections"]["gsheets"]["private_key_id"],
    "private_key": st.secrets["connections"]["gsheets"]["private_key"],
    "client_email": st.secrets["connections"]["gsheets"]["client_email"],
    "client_id": st.secrets["connections"]["gsheets"]["client_id"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": st.secrets["connections"]["gsheets"][
        "client_x509_cert_url"
    ],
    "universe_domain": "googleapis.com",
}

# Define the scope for Google Sheets API
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]


# Function to append data to Google Sheets
def append_data(input, email=""):
    # Authenticate and create a client to interact with Google Sheets
    credentials = Credentials.from_service_account_info(
        gsheet_credentials, scopes=scope
    )
    gc = gspread.authorize(credentials)

    # Open the Google Sheet by URL
    sheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
    sh = gc.open_by_url(sheet_url)

    # Select the first worksheet
    worksheet = sh.sheet1

    # Append the new row
    email = st.experimental_user.email if st.experimental_user.email else ""
    worksheet.append_row([input, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), email])


st.markdown(gradient_text_html, unsafe_allow_html=True)
avatar_url = "https://assets.lifeofw.com/waney.png"


# Initialize the chat messages history
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi there! I'm Wani, your friendly assistant bot here to help with any questions you have about Wahine Capital, W Vault, Women, and Finance. Just a quick note: I'm still in Beta, so please avoid sharing any confidential or sensitive information during our chat. Thanks! 😊",
            "avatar": avatar_url,
        }
    ]


@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(
        text="Loading and indexing our database – hang tight! This should take 1-2 minutes."
    ):
        reader = SimpleDirectoryReader(input_dir=st.secrets["data_dir"], recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(
            llm=OpenAI(
                model="gpt-4o",
                temperature=0.5,
                system_prompt="You are 'Wani', a supportive AI financial coach specializing in budgeting, personal finance, and goal-setting. Focus on empowering women to achieve financial well-being.  Prioritize inquiries about budgeting, financial planning, reaching goals, Wahine Capital products (especially those for women), and W Vault investments.  Always state: 'This isn't financial advice. Consult an advisor or contact Wahine Capital at hellowahine@wcapital.asia or visit https://wahine.wcapital.asia/ask.' when discussing finances. Empathize with users' financial concerns, offer encouragement, and provide clear, actionable answers in their language.",
            )
        )
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index


index = load_data()

# Initialize the chat engine
if "chat_engine" not in st.session_state.keys():
    st.session_state.chat_engine = index.as_chat_engine(
        chat_mode="condense_question", verbose=True
    )

col1, col2 = st.columns(2)
with col1:
    if st.button("Who is Wahine Capital?", use_container_width=True):
        question = "Who is Wahine Capital?"
        st.session_state.messages.append(
            {"role": "user", "content": question, "is_user": True}
        )
with col2:
    if st.button("What is a Digital Vault?", use_container_width=True):
        question = "What is Digital Vault?"
        st.session_state.messages.append(
            {"role": "user", "content": question, "is_user": True}
        )
col3, col4 = st.columns(2)
with col3:
    if st.button("What is W Vault?", use_container_width=True):
        question = "What is W Vault?"
        st.session_state.messages.append(
            {"role": "user", "content": question, "is_user": True}
        )
with col4:
    if st.button("What is Notifier List?", use_container_width=True):
        question = "What is Notifier List?"
        st.session_state.messages.append(
            {"role": "user", "content": question, "is_user": True}
        )

col5, col6 = st.columns(2)

with col5:
    if st.button("What is Access List?", use_container_width=True):
        question = "What is Access List?"
        st.session_state.messages.append(
            {"role": "user", "content": question, "is_user": True}
        )


# Prompt for user input and save to chat history
if prompt := st.chat_input("Your question"):
    st.session_state.messages.append(
        {"role": "user", "content": prompt, "is_user": True}
    )

    append_data(prompt)
    mp.track(user_id, "Chat Input", {"input_data": prompt})

# Display the prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar", None)):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant", avatar=avatar_url):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(
                st.session_state.messages[-1]["content"]
            )
            st.write(response.response)
            message = {
                "role": "assistant",
                "content": response.response,
                "avatar": avatar_url,
            }
            st.session_state.messages.append(message)  # Add response to message history

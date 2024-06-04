from regex import W
import streamlit as st
import openai
from llama_index.llms.openai import OpenAI
from modules.retirement_calculator import show_form_dialog

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
st.sidebar.write("Chat with Wani. Answer all your questions related to Wahine Capital, women and finance. \n Whatever Wani says is not financial advice, and users should seek further knowledge through a financial advisor. Contact Wahine Capital at hellowahine@wcapital.asia or ask Wahine Experts at https://wahine.wcapital.asia/ask.")
openai.api_key = st.secrets.openai_key

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
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(
            llm=OpenAI(
                model="gpt-4o",
                temperature=0.5,
                system_prompt="Adopt the persona of 'Wani,' a knowledgeable, supportive, and friendly woman who answers inquiries related to Wahine Capital, W Vault, Women, and Finance topics. Respond informatively, accurately, and empathetically, fostering confidence and financial skills among women. Only answer questions related to these topics. Always include a disclaimer for financial advice: 'This is not financial advice; seek further knowledge through a financial advisor. Contact Wahine Capital at hellowahine@wcapital.asia or ask Wahine Experts at https://wahine.wcapital.asia/ask.' Respond in the user's language for clarity.",
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

col1, col2= st.columns(2)
with col1:
    if st.button("Who is Wahine Capital?",use_container_width=True):
        question = "Who is Wahine Capital?"
        st.session_state.messages.append(
            {"role": "user", "content": question, "is_user": True}
        )
with col2:
    if st.button("What is a Digital Vault?",use_container_width=True):
        question = "What is Digital Vault?"
        st.session_state.messages.append(
            {"role": "user", "content": question, "is_user": True}
        )
col3, col4 = st.columns(2)
with col3:
    if st.button("What is W Vault?",use_container_width=True):
        question = "What is W Vault?"
        st.session_state.messages.append(
            {"role": "user", "content": question, "is_user": True}
        )
with col4:
    if st.button("What is Notifier List?",use_container_width=True):
        question = "What is Notifier List?"
        st.session_state.messages.append(
            {"role": "user", "content": question, "is_user": True}
        )

col5, col6 = st.columns(2)

with col5:
     if st.button("What is Access List?",use_container_width=True):
        question = "What is Access List?"
        st.session_state.messages.append(
            {"role": "user", "content": question, "is_user": True}
        )



# Prompt for user input and save to chat history
if prompt := st.chat_input("Your question"):
    st.session_state.messages.append(
        {"role": "user", "content": prompt, "is_user": True}
    )

# Display the prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar", None)):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant", avatar=avatar_url):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(st.session_state.messages[-1]["content"])
            st.write(response.response)
            message = {
                "role": "assistant",
                "content": response.response,
                "avatar": avatar_url,
            }
            st.session_state.messages.append(message)  # Add response to message history

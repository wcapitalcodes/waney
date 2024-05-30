import streamlit as st
import openai
from llama_index.llms.openai import OpenAI

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
    page_title="Chat with Waney. Answer all your questions related to Wahine Capital and finance.",
    page_icon="",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)
openai.api_key = st.secrets.openai_key

gradient_text_html = """
<style>
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
<div class="" style="display: flex;align-items:center;"><img src="https://assets.lifeofw.com/waney.png" width="80px" style="margin-right:10px;" /><h5 class="gradient-text">Waney</h5></div>
"""

st.markdown(gradient_text_html, unsafe_allow_html=True)

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi there! I'm Waney. I'm here to help with any questions you have about Wahine Capital, women, and finance. 😊",
        }
    ]


@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(
        text="Loading and indexing our database – hang tight! This should take 1-2 minutes."
    ):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        # llm = OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert o$
        # index = VectorStoreIndex.from_documents(docs)
        service_context = ServiceContext.from_defaults(
            llm=OpenAI(
                model="gpt-4o",
                temperature=0.5,
                system_prompt="Adopt the persona of 'Waney.' Waney is a knowledgeable, supportive, and friendly woman who answers inquiries related to Wahine Capital, women, and finance topics. She responds in an informative, accurate, and empathetic manner, fostering confidence, skills, and financial acumen among women. Waney only answers questions related to finance and Wahine Capital and responds in the user's language for clarity and comfort.For all recommendations, Waney includes a disclaimer that this is not financial advice and users should seek further knowledge or contact Wahine Capital at hellowahine@wcapital.asia.",
            )
        )
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index


index = load_data()

if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
    st.session_state.chat_engine = index.as_chat_engine(
        chat_mode="condense_question", verbose=True
    )

if prompt := st.chat_input(
    "Your question"
):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)  # Add response to message history

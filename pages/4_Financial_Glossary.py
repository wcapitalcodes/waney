import uuid
import streamlit as st
import pandas as pd
from mixpanel import Mixpanel

st.set_page_config(page_title="Financial Glossary", page_icon="📝")
st.sidebar.header("📝 Financial Glossary")
st.sidebar.write("Definitions for common financial terms at the tip of your fingers.")
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
<div style="display: flex;align-items:center;margin-bottom:30px;"><h5 style="font-size:50px">📝</h5><div class="flex flex-col"><h5 class="gradient-text">Financial Glossary</h5><h6>Let's define some financial terms.</h6></div></div>
"""

mp = Mixpanel(st.secrets['mixpanel']['token'])

user_id = str(uuid.uuid4())

# Track a page view
mp.track(user_id, 'Page View', {
    'page': 'Financial Glossary'
})

st.markdown(gradient_text_html, unsafe_allow_html=True)

st.write(
    pd.read_csv('./pages/Financial_Terms.csv')
)
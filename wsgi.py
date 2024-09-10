import streamlit.web.bootstrap as bootstrap
from streamlit import config as streamlit_config

streamlit_config.set_option("server.headless", True)
streamlit_config.set_option("server.enableCORS", False)
streamlit_config.set_option("server.enableXsrfProtection", False)

def server():
    bootstrap.run("Wani_Chat.py", "", [], flag_options={})

if __name__ == "__main__":
    server()
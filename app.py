import streamlit as st
from openai import OpenAI

#Pages

welcome = st.Page("home/welcome.py", title="Welcome", icon=":material/mood:", default=True)
explainer = st.Page("home/explainer.py", title="Explainer", icon=":material/trending_up:")

preferences = st.Page("tools/preferences.py", title="Preferences", icon=":material/tune:")
upload_files = st.Page("tools/upload_files.py", title="Upload Files", icon=":material/upload_file:")
manage_api_keys = st.Page("tools/manage_api_keys.py", title="Manage API keys", icon=":material/key:")
file_viewer = st.Page("tools/file_viewer.py", title="View Files", icon=":material/search:")

agora_v2 = st.Page("agora/agora_v2.py", title="Open Chat", icon=":material/robot_2:")
agora_v3 = st.Page("agora/agora_v3.py", title="Guided Chat", icon=":material/explore:")

thank_you = st.Page("more/thank_you.py", title="Thank You", icon=":material/star:")
about = st.Page("more/about.py", title="About", icon=":material/info:")
disclaimer = st.Page("more/disclaimer.py", title="Disclaimer", icon=":material/warning:")

#Navigation

pg = st.navigation(
    {
        "Home": [welcome, explainer],
        "Tools": [preferences, upload_files, manage_api_keys, file_viewer],
        "Agora": [agora_v2, agora_v3],
        "More": [thank_you, about, disclaimer],
    }
)


#API Keys -> Session State
if "openai_api_key" not in st.session_state:
    st.session_state["openai_api_key"] = st.secrets["api_keys"]["openai_api_key"]



#Default Settings -> Session State

if "disclaimer_acknowledged" not in st.session_state:
    st.session_state["disclaimer_acknowledged"] = False
if "last_page_visited" not in st.session_state:
    st.session_state["last_page_visited"] = "home/welcome.py"

# - Pref
if "avatar_choice" not in st.session_state:
    st.session_state["avatar_choice"] = "🗽"
if "topic_choice" not in st.session_state:
    st.session_state["topic_choice"] = "Artificial_Intelligence"
if "model_choice" not in st.session_state:
    st.session_state["model_choice"] = "gpt-4o"

# - Agora v2
if "agora_v2_instructions_viewed" not in st.session_state:
    st.session_state["agora_v2_instructions_viewed"] = False
if "agora_v2_assistant_id" not in st.session_state:
    st.session_state["agora_v2_assistant_id"] = None
if "agora_v2_thread_id" not in st.session_state:
    st.session_state["agora_v2_thread_id"] = None
if "agora_v2_vector" not in st.session_state:
    st.session_state["agora_v2_vector"] = None

# - Agora v3
if "agora_v3_instructions_viewed" not in st.session_state:
    st.session_state["agora_v3_instructions_viewed"] = False
if "agora_v3_assistant_id" not in st.session_state:
    st.session_state["agora_v3_assistant_id"] = None
if "agora_v3_thread_id" not in st.session_state:
    st.session_state["agora_v3_thread_id"] = None
if "agora_v3_vector" not in st.session_state:
    st.session_state["agora_v3_vector"] = None
if "agora_v3_qqg_id" not in st.session_state:
    st.session_state["agora_v3_qqg_id"] = None
if "agora_v3_thread_qqg_id" not in st.session_state:
    st.session_state["agora_v3_thread_qqg_id"] = None
if "agora_v3_query_choice" not in st.session_state:
    st.session_state["agora_v3_query_choice"] = None



#Run it!
pg.run()
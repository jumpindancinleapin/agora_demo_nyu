import streamlit as st

st.session_state["last_page_visited"] = "home/explainer.py"

#Messaging
st.title("What is this?")

st.write(
    """
    ***This*** is a custom webapp built on **Python**, **Streamlit**, and **OpenAI**.
    
    Soon, you'll meet **Agora** and **Queequeg**, two AI assistants trained in legal research.

    For navigation, use the buttons (below) to follow the demonstration flow I've set, 
    or navigate freely using the side menu (left, accessible via arrow on mobile).

    Next, you'll choose some preferences, and go on a tour of the platform. 
    """
)


st.divider()


#Nav
foot_lt, foot_rt = st.columns(2)
with foot_lt:
    if st.button("<- Welcome", use_container_width=True):
        st.switch_page("home/welcome.py")

with foot_rt:
    if st.button("Preferences ->", use_container_width=True, type="primary"):
        st.switch_page("tools/preferences.py")


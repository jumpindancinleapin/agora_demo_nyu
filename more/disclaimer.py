import streamlit as st

last_page_visited = st.session_state["last_page_visited"]


#Messaging
st.header("Before you meet Agora...")
st.write(
    """
    This app is not collecting personal infomation.
    However, user prompts are sent to third party APIs which may process and log the user prompts.
    Please **avoid inputting any sensitive, personal, or confidential information** while 
    using this app.
    """
)

#Input
st.session_state["disclaimer_acknowledged"] = st.toggle(
    "Click to acknowledge.",
    value=st.session_state["disclaimer_acknowledged"],
)

if st.session_state["disclaimer_acknowledged"]:
    st.write("User acknowledged ✔")


st.divider()


#Nav
foot_lt, foot_m, foot_rt = st.columns(3)


with foot_m:
    if last_page_visited in ["agora/agora_v2.py", "agora/agora_v3.py"]:
        if st.session_state["disclaimer_acknowledged"]:
            if st.button("Continue ->", type="primary", use_container_width=True):
                st.switch_page(last_page_visited)
        else:
            st.button("Acknowledge to Continue", disabled=True, use_container_width=True)
    else:
        if st.button("<- Previous Page"):
            st.switch_page(last_page_visited)



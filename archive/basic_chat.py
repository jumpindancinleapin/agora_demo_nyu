import streamlit as st
from openai import OpenAI


nav_lt, nav_md, nav_rt = st.columns(3)
with nav_lt:
    if st.button("<- Manage API Keys", use_container_width=True):
        st.switch_page("sources/manage_api_keys.py")

with nav_rt:
    if st.button("Multi-File Q&A ->", use_container_width=True):
        st.switch_page("tools/multi_file.py")

st.title("Basic Chat")
st.write("Converse with a model of your choosing.")
model_choice = st.radio(
        "Model:",
        ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o"],
        captions=["Older", "Fast, cheap", "Robust, pricier"],
        horizontal=True,
    )

st.divider()

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]



for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message(msg["role"], avatar=st.session_state["avatar_choice"]).write(msg["content"])
    else:
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    client = OpenAI(api_key=st.session_state["openai_api_key"])
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar=st.session_state["avatar_choice"]).write(prompt)
    response = client.chat.completions.create(model=model_choice, messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)


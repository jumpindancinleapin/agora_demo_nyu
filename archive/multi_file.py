import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
import openai


openai.api_key = st.session_state["openai_api_key"]

nav_lt, nav_md, nav_rt = st.columns(3)
with nav_lt:
    if st.button("<- Single File Q&A", use_container_width=True):
        st.switch_page("tools/basic_chat.py")

with nav_rt:
    if st.button("Controlled Assistant ->", use_container_width=True):
        st.switch_page("tools/controlled_assistant.py")



st.title("Multi-File Q&A")
st.write("**LlamaIndex** has been introduced, which digests multiple files and offers an ***index*** that our model references while formulating responses.")
model = st.radio(
    "Model",
    ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o"],
    index=2,
    horizontal=True,
)

st.divider()


Settings.llm = OpenAI(model=model)

directory_path = st.session_state["topic_choice"]

documents = SimpleDirectoryReader(f"resources/data/{directory_path}").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()



if "llama-messages" not in st.session_state:
    st.session_state["llama-messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state["llama-messages"]:
    if msg["role"] == "user":
        st.chat_message(msg["role"], avatar=st.session_state["avatar_choice"]).write(msg["content"])
    else:
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state["llama-messages"].append({"role": "user", "content": prompt})
    st.chat_message("user", avatar=st.session_state["avatar_choice"]).write(prompt)
    response = query_engine.query(st.session_state["llama-messages"][-1]["content"])
    msg = response.response
    st.session_state["llama-messages"].append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)



import streamlit as st
import time
from openai import OpenAI


def wait_on_run(run):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=st.session_state["ca_thread_id"],
            run_id=run.id,
        )
        time.sleep(0.5)
    return run


nav_lt, nav_md, nav_rt = st.columns(3)
with nav_lt:
    if st.button("<- Multi-File Q&A", use_container_width=True):
        st.switch_page("tools/multi_file.py")

with nav_rt:
    if st.button("TBD ->", use_container_width=True):
        print("NOT IMPL (assistant_control.py)")

st.title("Controlled Assistant")
st.write("Here, we have an OpenAI ***Assistant*** that has been instructed to behave as a research partner, and to avoid encroaching upon law students' responsibilities. Ask **Agora** to write an essay for your contracts class, or state an opinion on a pertinent legal issue.")


model_choice = st.radio(
        "Model:",
        ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o"],
        horizontal=True,
        disabled=True,
        index=2,
    )

with st.sidebar:
    st.write("**Status:**")

st.divider()

client = OpenAI(api_key=st.session_state["openai_api_key"])

if "ca_assistant_id" not in st.session_state:
    
    assistant = client.beta.assistants.create(
    name="Legal Research Assistant",
    instructions="You are a legal research assistant named Agora. You answer with facts, and avoid encroaching upon the users critical thinking. Do not write complete drafts for essays.",
    model="gpt-4o",
    )
    st.session_state["ca_assistant_id"] = assistant.id
    with st.sidebar:
        st.write("New assistant created.")



with st.sidebar:
    st.write("Assistant ready.")

if "ca_thread_id" not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state["ca_thread_id"] = thread.id
    with st.sidebar:
        st.write("New thread created.")

with st.sidebar:
    st.write("Thread open.")

if len(client.beta.threads.messages.list(thread_id=st.session_state["ca_thread_id"]).data) < 2:
    client.beta.threads.messages.create(
        thread_id=st.session_state["ca_thread_id"],
        role="user",
        content="Hi, please introduce yourself, and offer help with legal research.",
    )


messages_pre_run = client.beta.threads.messages.list(thread_id=st.session_state["ca_thread_id"])

if messages_pre_run.data[0].role == "user": 

    run = client.beta.threads.runs.create(
        thread_id=st.session_state["ca_thread_id"],
        assistant_id=st.session_state["ca_assistant_id"],
    )

    run = wait_on_run(run)

    with st.sidebar:
        st.write("Run conducted.")
else:
    with st.sidebar:
        st.write("No run conducted.")

messages_post_run = client.beta.threads.messages.list(thread_id=st.session_state["ca_thread_id"])

#st.write(messages.data[1].content[0].text.value)
#st.write(messages.data[0].content[0].text.value)

for msg in reversed(messages_post_run.data[:-1]):
    
    if msg.role == "user":
        st.chat_message(msg.role, avatar=st.session_state["avatar_choice"]).write(msg.content[0].text.value)
    else:
        st.chat_message(msg.role).write(msg.content[0].text.value)    
    

if prompt := st.chat_input():
    client.beta.threads.messages.create(
        thread_id=st.session_state["ca_thread_id"],
        role="user",
        content=prompt,
    )
    st.chat_message("user", avatar=st.session_state["avatar_choice"]).write(prompt)
    
    user_instigated_run = client.beta.threads.runs.create(
        thread_id=st.session_state["ca_thread_id"],
        assistant_id=st.session_state["ca_assistant_id"],
    )
    user_instigated_run = wait_on_run(user_instigated_run)
    with st.sidebar:
        st.write("User-instigated run conducted.")
    
    response = client.beta.threads.messages.list(thread_id=st.session_state["ca_thread_id"]).data[0]

    st.chat_message("assistant").write(response.content[0].text.value)

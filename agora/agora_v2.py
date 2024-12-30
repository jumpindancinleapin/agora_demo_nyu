import streamlit as st

last_page_visited = st.session_state["last_page_visited"]
st.session_state["last_page_visited"] = "agora/agora_v2.py"

#Disclaimer control
if st.session_state["disclaimer_acknowledged"] == False:
    st.switch_page("more/disclaimer.py")


from openai import OpenAI
import time
import os

#Helper functions
def wait_on_run(run):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=st.session_state["agora_v2_thread_id"],
            run_id=run.id
        )
        time.sleep(0.2)
    return run

#Status init

with st.sidebar:
    st.write("**Restart**")
    if st.button(":material/replay:"):
        st.session_state["agora_v2_thread_id"] = None
        st.session_state["agora_v2_assistant_id"] = None
        st.session_state["agora_v2_vector"] = None
        st.session_state["agora_v2_instructions_viewed"] = False

    st.write("**Status**")


#Nav
head_l, head_r = st.columns(2)
with head_l:
    if st.button("<- View Files", use_container_width=True):
        st.switch_page("tools/file_viewer.py")
with head_r:
    if st.button("Guided Chat ->", use_container_width=True, type="primary"):
        st.switch_page("agora/agora_v3.py")
    

#Messaging
st.title("Open Chat with Agora :material/robot_2:")

if st.session_state["agora_v2_instructions_viewed"] == False:
    st.write(
        """
        We made it! Thank you for coming along. Here is **Agora** at last. 
        Agora has read the files you chose, and is ready to get down to business.
        Agora takes a few seconds to spin up, and a few seconds to respond to your queries. 
        Don't worry; Agora is working for ***you***!

        **Ask Agora about a detail in the files you chose. To find Agora's boundaries, 
        request they write an essay or state an opinion.**

        These instructions will go away once you begin your chat.
        To read them again, click **Restart** in the side menu. This will
        also restart the chat.
        """
    )

st.session_state["agora_v2_instructions_viewed"] = True

topic_choice = st.session_state["topic_choice"]
st.write(f"**Agora** has been trained on the `{topic_choice}` directory.")

st.divider()

#Open Client
client = OpenAI(api_key=st.session_state["openai_api_key"])

#Thread - create or plug in
thread = None
if st.session_state["agora_v2_thread_id"] == None:
    thread = client.beta.threads.create()
    st.session_state["agora_v2_thread_id"] = thread.id

#Assistant - create new or plug in
assistant = None
if st.session_state["agora_v2_assistant_id"] == None:
    
    with st.spinner("Creating Agora instance..."):
    
        #Create Agora
        assistant = client.beta.assistants.create(
        name="Legal Research Assistant",
        instructions="You are a legal research assistant named Agora. You answer with facts, and avoid encroaching upon the users critical thinking. Do not write complete drafts for essays.",
        model=st.session_state["model_choice"],
        tools=[{"type": "file_search"}],
        )
        st.session_state["agora_v2_assistant_id"] = assistant.id

        #Prompt Agora
        client.beta.threads.messages.create(
            thread_id=st.session_state["agora_v2_thread_id"],
            role="user",
            content="Hi, please introduce yourself, and offer help with legal research."
        )

        #Initial Run
        init_run = client.beta.threads.runs.create(
            thread_id=st.session_state["agora_v2_thread_id"],
            assistant_id=st.session_state["agora_v2_assistant_id"]
        )
      
        init_run = wait_on_run(init_run)



#Vector - create new or plug in
vector = None
topic_path = st.session_state["topic_choice"]
if st.session_state["agora_v2_vector"] == None:

    with st.spinner("Creating new vector..."):

        vector = client.beta.vector_stores.create(name="Files")
        file_names = os.listdir(f"resources/data/{topic_path}")
        file_paths = [f"resources/data/{topic_path}/{file_name}" for file_name in file_names]
        file_streams = [open(file_path, "rb") for file_path in file_paths]
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector.id,
            files=file_streams
        )
        st.session_state["agora_v2_vector"] = vector
else:
    vector = st.session_state["agora_v2_vector"]


#Give the Vector to the Assistant
assistant = client.beta.assistants.update(
    assistant_id = st.session_state["agora_v2_assistant_id"],
    tool_resources = {"file_search": {"vector_store_ids": [vector.id]}}
)


#Chat
#Load Messages 
messages = client.beta.threads.messages.list(thread_id=st.session_state["agora_v2_thread_id"])

for message in reversed(messages.data[:-1]):
    if message.role == "user":
        st.chat_message(message.role, avatar=st.session_state["avatar_choice"]).write(message.content[0].text.value)
    else:
        st.chat_message(message.role, avatar=":material/robot_2:").write(message.content[0].text.value)


#New Message

if prompt := st.chat_input():
    st.chat_message("user", avatar=st.session_state["avatar_choice"]).write(prompt)
    client.beta.threads.messages.create(
        thread_id=st.session_state["agora_v2_thread_id"],
        role="user",
        content=prompt,
    )

    user_run = client.beta.threads.runs.create(
        thread_id = st.session_state["agora_v2_thread_id"],
        assistant_id = st.session_state["agora_v2_assistant_id"],
    )
 
    with st.spinner("Running user query..."):
        user_run = wait_on_run(user_run)

    response = client.beta.threads.messages.list(thread_id=st.session_state["agora_v2_thread_id"]).data[0]
    st.chat_message("assistant", avatar=":material/robot_2:").write(response.content[0].text.value)

with st.sidebar:
    st.success("Ready", icon=":material/check_circle:")
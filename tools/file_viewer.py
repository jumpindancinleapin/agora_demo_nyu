import streamlit as st
import os


st.session_state["last_page_visited"] = "tools/file_viewer.py"


#Messaging
st.title("View Files")
st.write(
    """
    The files below correspond to the **topic** choice you made. 
    You can explore all of the topics here using the controls below. 
    If a topic piques your interest, return to **Preferences** to select it.
    To limit computation, Agora and Queequeg train on one topic at a time.
    This file viewer cuts off longer files at a certain length.
    """
)

st.divider()

#Inputs
directories = os.listdir("resources/data")

topic_path = st.segmented_control(
    "Choose topic:",
    directories,
    default=st.session_state["topic_choice"]
)

directory_path = f"resources/data/{topic_path}"

file_path = None

if topic_path != None:
    files = os.listdir(directory_path)

    file_path = st.segmented_control(
        "Choose file:",
        files,
        default=files[0]
    )

st.divider()

#File section

if topic_path == None:
    st.write("No topic selected, please make a selection above.")
else:
    if file_path == None:
        st.write("No file selected, please make a selection above.")

    else:
        full_path = f"{directory_path}/{file_path}"
        with open(full_path, "r") as file:
            text = file.read()
            if len(text) > 500:
                text = text[:500]
                text = text + " **[...]**"
            st.write(text)




st.divider()


#Nav
foot_lt, foot_rt = st.columns(2)
with foot_lt:
    if st.button("<- Manage API Keys", use_container_width=True):
        st.switch_page("tools/manage_api_keys.py")

with foot_rt:
    if st.button("Open Chat ->", use_container_width=True, type="primary"):
                st.switch_page("agora/agora_v2.py")
        





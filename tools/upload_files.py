import streamlit as st

st.session_state["last_page_visited"] = "tools/upload_files.py"


#Messaging
st.title("Upload Files")
st.write(
    """
    I have handled file uploading for this demo, but here a 
    user would upload files and organize them into **topics**.
    """    
)

st.divider()

#File Uploader
uploaded_file = st.file_uploader("Upload your file(s)", type=["csv", "txt", "xlsx"], accept_multiple_files=True, disabled=True)

# - Actual code removed, lightening payload for Columbia, page is illustrative



#Nav
st.divider()

foot_lt, foot_md, foot_rt = st.columns(3)
with foot_lt:
    if st.button("<- Preferences", use_container_width=True):
        st.switch_page("tools/preferences.py")

with foot_rt:
    if st.button("Manage API Keys ->", use_container_width=True, type="primary"):
        st.switch_page("tools/manage_api_keys.py")


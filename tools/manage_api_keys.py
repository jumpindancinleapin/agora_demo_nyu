import streamlit as st


st.session_state["last_page_visited"] = "tools/manage_api_keys.py"

#Messaging
st.title("Manage API Keys")
st.write(
    """
    API Keys are secret passwords to access third-party APIs. I have hidden mine in the app for use in this demo. When you chat with Agora,
    an OpenAI server will know to charge me a few cents.
    """
)
st.divider()

#Inputs
st.text_input("OpenAI API Key", disabled=True, type="password", value="Nice try!")
st.text_input("Anthropic API Key", disabled=True, type="password", value="Not quite...")
# - actual code is removed, lightening payload for Columbia, page is just illustrative


#Nav
st.divider()
foot_lt, foot_md, foot_rt = st.columns(3)
with foot_lt:
    if st.button("<- Upload Files", use_container_width=True):
        st.switch_page("tools/upload_files.py")
with foot_rt:
    if st.button("View Files ->", use_container_width=True, type="primary"):
        st.switch_page("tools/file_viewer.py")


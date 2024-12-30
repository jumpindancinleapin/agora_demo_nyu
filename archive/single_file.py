import streamlit as st
import anthropic



st.title("Single File Q&A")
st.write("File referencing has been introduced, which allows a use to query ")
st.radio(
    "Model",
    ["gpt-3.5-turbo", "gpt-4o-mini", "claude-2"],
    index=2,
    disabled=True,
    horizontal=True
)

nav_lt, nav_md, nav_rt = st.columns(3)
with nav_lt:
    if st.button("<- Basic Chat", use_container_width=True):
        st.switch_page("tools/basic_chat.py")

with nav_rt:
    if st.button("Multi-File Q&A ->", use_container_width=True):
        st.switch_page("tools/multi_file.py")

st.divider()

uploaded_file = st.file_uploader("Upload an article", type=("txt", "md"))

question = st.text_input(
    "Ask something about the article",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question and not anthropic_api_key:
    st.info("Please add your Anthropic API key to continue.")

if uploaded_file and question and anthropic_api_key:
    article = uploaded_file.read().decode()
    prompt = f"""{anthropic.HUMAN_PROMPT} Here's an article:\n\n
    {article}\n\n\n\n{question}{anthropic.AI_PROMPT}"""

    client = anthropic.Client(api_key=st.session_state["anthropic_api_key"])
    response = client.completions.create(
        prompt=prompt,
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model="claude-2", #"claude-2" for Claude 2 model
        max_tokens_to_sample=100,
    )
    st.write("### Answer")
    st.write(response.completion)
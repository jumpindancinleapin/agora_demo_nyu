import streamlit as st

st.session_state["last_page_visited"] = "more/thank_you.py"


#Helper functions
def reset_demo():
    
    st.session_state["disclaimer_acknowledged"] = False
    st.session_state["last_page_visited"] = "home/welcome.py"

    # - Pref
    
    st.session_state["avatar_choice"] = "🗽"
    st.session_state["topic_choice"] = "Artificial_Intelligence"
    st.session_state["model_choice"] = "gpt-4o"

    # - Agora v2
    st.session_state["agora_v2_instructions_viewed"] = False
    st.session_state["agora_v2_assistant_id"] = None
    st.session_state["agora_v2_thread_id"] = None
    st.session_state["agora_v2_vector"] = None

    # - Agora v3
    st.session_state["agora_v3_instructions_viewed"] = False
    st.session_state["agora_v3_assistant_id"] = None
    st.session_state["agora_v3_thread_id"] = None
    st.session_state["agora_v3_vector"] = None
    st.session_state["agora_v3_qqg_id"] = None
    st.session_state["agora_v3_thread_qqg_id"] = None
    st.session_state["agora_v3_query_choice"] = None



#Messaging
st.title("Thank you!")
st.write(
    """
    This web-and-tech space, it is my home turf. I am 
    thankful for an opportunity to be seen at my best. 

    My message is this: I am not an AI enthusiast; not a 
    Linkedin personality with AI in my bio and 
    posts about who should be doing what. 
    I am a practioner. This app is an attempt to 
    solve a problem and support the success of others. 

    As I learn more about the values of NYU Law,
    I will iterate upon this webapp to protect them. 
    
    Thank you for your time and consideration. 


    All the best,

    ***Jake Lindsay***

    L43133966
    """
)

st.divider()

#Nav
foot_l, foot_r = st.columns(2)

with foot_l:
    if st.button(":material/info: Learn how Agora works", use_container_width=True):
        st.switch_page("more/about.py")
with foot_r:
    if st.button(":material/replay: Start Demo Over", use_container_width=True):
        reset_demo()
        st.switch_page("home/welcome.py")


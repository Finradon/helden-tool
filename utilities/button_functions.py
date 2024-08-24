from hero import hero
import streamlit as st

def change_hero(name: str):

    path = "json/" + name + ".json"
    with open(path, 'r') as file:
        data = file.read()
    st.session_state['hero'] = hero.from_json(data)

def reset_hero():
    if "hero" in st.session_state:
        name = st.session_state["hero"].name

        path = "json/" + name + ".json"
        with open(path, 'r') as file:
            data = file.read()
        st.session_state['hero'] = hero.from_json(data)
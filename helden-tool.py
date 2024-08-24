import streamlit as st
from hero import hero
from utilities.formatting import life_points_correction

if 'hero' not in st.session_state:
    with open('json/Sdick.json', 'r') as file:
        data = file.read()
    st.session_state['hero'] = hero.from_json(data)
held: hero = st.session_state['hero']
st.title(held.name)

ratio = 100/held.max_lep
st.progress(life_points_correction(int(held.lep*ratio)), f"**Lebenspunkte: {held.lep}/{held.max_lep}**")

col1, col2 = st.columns([6, 1])
with col1:
    damage_slider = st.slider("**Schaden**", min_value=1, max_value=30)
    #damage_input = st.number_input("**Schaden**", min_value=0)

with col2:
    tp_button1 = st.button("TP", on_click=held.receive_damage, kwargs={"value": damage_slider, "tp": True})
    sp_button1 = st.button("SP", on_click=held.receive_damage, kwargs={"value": damage_slider, "tp": False})
    #tp_button2 = st.button("Nr TP", on_click=held.receive_damage, kwargs={"value": damage_input, "tp": True})
    #sp_button2 = st.button("Nr SP", on_click=held.receive_damage, kwargs={"value": damage_input, "tp": False})


col11, col21 = st.columns([6, 1])
with col11:
    healing_slider = st.slider("**Heilung**", min_value=1, max_value=30)

with col21:
    st.markdown("######")
    tp_button1 = st.button("Heilen", on_click=held.receive_healing, kwargs={"value": healing_slider })


c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("**Wunden**", held.wound_count)
with c2:
    st.metric("**Rüstung**", held.rs)
with c3:
    st.metric("**Initiative**", held.ini)
with c4:
    st.metric("**LEP-Status**", held.state)

st.divider()

col12, col22, col32 = st.columns(3)
with col12:
    # attack roll button
    c1, c2 = st.columns([1, 3])
    with c1:
        atbutton = st.button(f'AT: {held.at}')
    with c2:
        if atbutton:
            st.subheader(held.attack_roll())

with col22:
    # attack roll button
    c1, c2 = st.columns([1, 3])
    with c1:
        atbutton = st.button(f'PA: {held.pa}')
    with c2:
        if atbutton:
            st.subheader(held.parry_roll())

with col32:
    ini = st.number_input(label="Ini", value=None, label_visibility="hidden", min_value=0)
    ini_button = st.button("Set Ini", on_click=held.set_ini, kwargs={"value": ini})

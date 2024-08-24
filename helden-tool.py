import streamlit as st
from hero import hero
from utilities.formatting import life_points_correction
import utilities.button_functions as bt_funcs

with st.sidebar:
    ailin = st.button("Ailin", on_click=bt_funcs.change_hero, kwargs={"name": "Ailin"})
    frinja = st.button("Frinja", on_click=bt_funcs.change_hero, kwargs={"name": "Frinja"})
    nadoran = st.button("Nadoran", on_click=bt_funcs.change_hero, kwargs={"name": "Nadoran"})
    sdick = st.button("Sdick", on_click=bt_funcs.change_hero, kwargs={"name": "Sdick"})
    rest = st.button("Reset", on_click=bt_funcs.reset_hero)


if 'hero' not in st.session_state:
     st.title("Helden-Tool")
     st.markdown("Ein Tool um Wunden, Niedrige LE und mehr für DSA4.1 zu verwalten.")
     st.markdown("Einfach links eine:n Held:in auswählen.")
else:

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


    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("**Initiative**", held.ini)
        st.metric("**LEP**", held.lep)
    with c2:
        st.metric("**Rüstung**", held.rs)
        st.metric("**LEP-Status**", held.state)
    with c3:
        st.metric("**GS**", held.gs)
        st.metric("**Wunden**", held.wound_count)
    with c4:
        st.metric("**MR**", held.mr)
        st.metric("**TP**", held.print_tp())



    st.divider()

    col12, col22, col32 = st.columns(3)
    with col12:
        # attack roll button
        c1, c2 = st.columns([1, 3])
        with c1:
            atbutton = st.button(f'AT{held.at}')
        with c2:
            if atbutton:
                st.subheader(held.attack_roll())
        ini = st.number_input(label="Ini", value=None, label_visibility="hidden", min_value=0)
        ini_button = st.button("Set Ini", on_click=held.set_ini, kwargs={"value": ini})

    with col22:
        # parry roll button
        c1, c2 = st.columns([1, 3])
        with c1:
            pabutton = st.button(f'PA{held.pa}')
        with c2:
            if pabutton:
                st.subheader(held.parry_roll())
        rs = st.number_input(label="RS", value=None, label_visibility="hidden", min_value=0)
        rs_button = st.button("Set RS", on_click=held.set_rs, kwargs={"value": rs})

    with col32:
        # dodge roll button
        c1, c2 = st.columns([1, 3])
        with c1:
            awbutton = st.button(f'AW{held.aw}')
        with c2:
            if awbutton:
                st.subheader(held.dodge_roll())

    axx = st.toggle("**Axxeleratus**", on_change=held.toggle_axxeleratus, value=held.axx)

    # if held.name == "Sdick":
    #     nchurr = st.toggle("***Ruf des N'Churr***", on_change=held.toggle_nchurr, value=held.nchurr)
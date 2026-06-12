import streamlit as st
import random

st.set_page_config(page_title="Juego Hacker", page_icon="👑")

st.title("Juego Hacker de Paolo 👑")

# Inicializar el juego
if 'secreto' not in st.session_state:
    st.session_state.secreto = random.randint(1, 100)
    st.session_state.intentos = 0
    st.session_state.ganado = False
    st.session_state.rango = ""

st.write("Adivina el número del 1 al 100")

if not st.session_state.ganado:
    intento = st.number_input("Tu número:", min_value=1, max_value=100, step=1)
    
    if st.button("ADIVINAR 🎯"):
        st.session_state.intentos += 1
        
        if intento < st.session_state.secreto:
            st.warning("Muy bajo 👇")
        elif intento > st.session_state.secreto:
            st.warning("Muy alto 👆")
        else:
            st.session_state.ganado = True
            intentos = st.session_state.intentos
            
            if intentos <= 7:
                st.session_state.rango = "HACKER 🧠🔥"
            elif intentos <= 15:
                st.session_state.rango = "PRO 📚"
            else:
                st.session_state.rango = "NOVATO 💪"

if st.session_state.ganado:
    st.balloons()
    st.success(f"¡GANASTE JEFE! 🎯")
    st.info(f"Lo lograste en {st.session_state.intentos} intentos")
    st.info(f"RANGO: {st.session_state.rango}")
    
    if st.button("JUGAR DE NUEVO 🔄"):
        st.session_state.secreto = random.randint(1, 100)
        st.session_state.intentos = 0
        st.session_state.ganado = False
        st.session_state.rango = ""
        st.rerun()

st.caption(f"Intentos: {st.session_state.intentos}")
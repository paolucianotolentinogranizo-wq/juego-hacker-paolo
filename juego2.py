import streamlit as st
import random

st.title("✊✋✌️ Piedra, Papel o Tijera")

opciones = ["Piedra", "Papel", "Tijera"]
eleccion_usuario = st.radio("Elige tu arma:", opciones)

if st.button("¡PELEAR!"):
    eleccion_pc = random.choice(opciones)
    st.write(f"La PC eligió: **{eleccion_pc}**")
    
    if eleccion_usuario == eleccion_pc:
        st.info("¡Empate! 🤝")
    elif (eleccion_usuario == "Piedra" and eleccion_pc == "Tijera") or (eleccion_usuario == "Papel" and eleccion_pc == "Piedra") or (eleccion_usuario == "Tijera" and eleccion_pc == "Papel"):
        st.success("¡Ganaste! 🔥")
    else:
        st.error("Perdiste therian 😢") 

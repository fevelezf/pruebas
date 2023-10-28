import streamlit as st
nombres = ["Juan", "María", "Pedro", "Luisa", "Ana"]

# Crear un diccionario a partir de la lista de nombres con 0 como valor
diccionario_nombres = dict(zip(nombres, [0] * len(nombres)))

# Puedes imprimir el diccionario resultante
print(diccionario_nombres)


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Cargar el archivo CSV con los usuarios
usuarios_df = pd.read_csv('usuarios.csv')

# Inicializar la variable de sesión para el nombre de usuario
if 'username' not in st.session_state:
    st.session_state.username = None

# Obtener el nombre de usuario actual después del inicio de sesión
def get_current_user():
    return st.session_state.username

# Función para cargar o crear un archivo CSV para el usuario actual
def get_user_data(username):
    user_data_filename = f"{username}_data.csv"
    if not os.path.exists(user_data_filename):
        # Si el archivo no existe, crea un DataFrame vacío
        return pd.DataFrame({'Fecha': [], 'Tipo': [], 'Categoría': [], 'Monto': []})
    else:
        # Si el archivo existe, carga los datos desde el archivo CSV
        return pd.read_csv(user_data_filename)

# Función para registrar un nuevo usuario
def registrar_usuario(username, password):
    global usuarios_df

    # Verificar si el usuario ya existe
    if username in usuarios_df['Username'].values:
        return False, "El usuario ya existe. Por favor, elija otro nombre de usuario."

    # Agregar el nuevo usuario al DataFrame
    nuevo_usuario = pd.DataFrame({'Username': [username], 'Password': [password]})
    usuarios_df = pd.concat([usuarios_df, nuevo_usuario], ignore_index=True)

    # Guardar el DataFrame actualizado en el archivo CSV
    usuarios_df.to_csv('usuarios.csv', index=False)

    return True, "Registro exitoso. Ahora puede iniciar sesión."

def verificar_credenciales(username, password):
    # Lee el archivo CSV de usuarios
    try:
        usuarios_df = pd.read_csv('usuarios.csv')
    except FileNotFoundError:
        return False, "No se encontraron usuarios registrados."

    # Verifica las credenciales
    if (usuarios_df['Username'] == username).any() and (usuarios_df['Password'] == password).any():
        return True, "Inicio de sesión exitoso."
    else:
        return False, "Credenciales incorrectas. Por favor, verifique su nombre de usuario y contraseña."
    

# Función para registrar un gasto o ingreso
def registrar_dato(tipo):
    fecha = st.text_input("Ingrese la fecha (YYYY-MM-DD):")
    categoria = st.text_input("Ingrese la categoría:")
    monto = st.number_input("Ingrese el monto:")
    username = get_current_user()
    user_data = get_user_data(username)
    nuevo_dato = pd.DataFrame({'Fecha': [fecha], 'Tipo': [tipo], 'Categoría': [categoria], 'Monto': [monto]})
    user_data = pd.concat([user_data, nuevo_dato], ignore_index=True)
    user_data.to_csv(f"{username}_data.csv", index=False)
    if st.button("Registrar"):
        st.success(f"{tipo} registrado exitosamente.")    

# Función para mostrar los gastos e ingresos del usuario actual
def mostrar_gastos_ingresos():
    username = get_current_user()
    user_data = get_user_data(username)

    st.write(f"Gastos e Ingresos de {username}:")
    st.dataframe(user_data)

# Título de la aplicación
st.title("Seguimiento de Gastos Personales")

# Menú desplegable en la barra lateral
menu_option = st.sidebar.selectbox("Menú", ["Inicio", "Registro", "Salir"])

# Si el usuario ya ha iniciado sesión, mostrar los botones
if get_current_user() is not None:
    st.write(f"Bienvenido, {get_current_user()}!")

    # Botones para registrar gasto, ingreso o ver registros
    option = st.radio("Selecciona una opción:", ("Registrar Gasto", "Registrar Ingreso", "Ver Registros"))

    if option == "Registrar Gasto":
        st.header("Registrar Gasto")
        with st.form("registrar_gasto_form"):
            fecha = st.text_input("Ingrese la fecha (YYYY-MM-DD):")
            categoria = st.text_input("Ingrese la categoría:")
            monto = st.number_input("Ingrese el monto:")
            if st.form_submit_button("Registrar"):
                username = get_current_user()
                user_data = get_user_data(username)
                nuevo_dato = pd.DataFrame({'Fecha': [fecha], 'Tipo': ['Gasto'], 'Categoría': [categoria], 'Monto': [monto]})
                user_data = pd.concat([user_data, nuevo_dato], ignore_index=True)
                user_data.to_csv(f"{username}_data.csv", index=False)
                st.success("Gasto registrado exitosamente.")
    if option == "Registrar Ingreso":
        st.header("Registrar Ingreso")
        with st.form("registrar_Ingreso_form"):
            fecha = st.text_input("Ingrese la fecha (YYYY-MM-DD):")
            categoria = st.text_input("Ingrese la categoría:")
            monto = st.number_input("Ingrese el monto:")
            if st.form_submit_button("Registrar"):
                username = get_current_user()
                user_data = get_user_data(username)
                nuevo_dato = pd.DataFrame({'Fecha': [fecha], 'Tipo': ['Ingreso'], 'Categoría': [categoria], 'Monto': [monto]})
                user_data = pd.concat([user_data, nuevo_dato], ignore_index=True)
                user_data.to_csv(f"{username}_data.csv", index=False)
                st.success("Ingreso registrado exitosamente.") 
    if st.button("Ver Gastos e Ingresos"):
        mostrar_gastos_ingresos()
else:
    # Inicio de sesión
    if menu_option == "Inicio":
        st.write("Bienvenido al inicio de la aplicación.")

        # Campos de inicio de sesión
        username = st.text_input("Nombre de Usuario:")
        password = st.text_input("Contraseña:", type="password")

        if st.button("Iniciar Sesión"):
            login_successful, message = verificar_credenciales(username, password)
            if login_successful:
                st.success(message)
                st.session_state.username = username  # Almacenar el nombre de usuario en la sesión
            else:
                st.error(message)
    elif menu_option == "Registro":
        st.write("Registro de Usuario")

        # Campos de registro
        new_username = st.text_input("Nuevo Nombre de Usuario:")
        new_password = st.text_input("Nueva Contraseña:", type="password")

        if st.button("Registrarse"):
            registration_successful, message = registrar_usuario(new_username, new_password)
            if registration_successful:
                st.success(message)
            else:
                st.error(message)
    elif menu_option == "Salir":
        st.balloons()
        st.stop()
        #hola
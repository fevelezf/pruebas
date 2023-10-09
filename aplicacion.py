import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cargar el archivo CSV con los usuarios
usuarios_df = pd.read_csv('usuarios.csv')


# Crear un DataFrame de pandas para registrar los gastos
data = {'Fecha': [], 'Categoría': [], 'Monto': []}
df = pd.DataFrame(data)

# Función para registrar un nuevo usuario
def registrar_usuario(username, password):
    global usuarios_df

    # Verificar si el usuario ya existe
    if username in usuarios_df['Username'].values:
        return False, "El usuario ya existe. Por favor, elija otro nombre de usuario."

    # Agregar el nuevo usuario al DataFrame
    nuevo_usuario = pd.DataFrame({'Username': [username], 'Password': [password]})
    usuarios_df = pd.concat([usuarios_df, nuevo_usuario], ignore_index=True)

    return True, "Registro exitoso. Ahora puede iniciar sesión."

# ...

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
    

# Título de la aplicación
st.title("Seguimiento de Gastos Personales")

# Menú desplegable en la barra lateral
menu_option = st.sidebar.selectbox("Menú", ["Inicio", "Registro", "Salir"])

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
            opcion = st.selectbox("Seleccione una opción:", ["Agregar Gasto", "Calcular Estadísticas"])
            if opcion == "Agregar Gasto":
                fecha = st.text_input("Ingrese la fecha (YYYY-MM-DD):")
                categoria = st.text_input("Ingrese la categoría del gasto:")
                monto = st.number_input("Ingrese el monto del gasto:")
            elif opcion == "Calcular Estadísticas":
                if not df.empty:
                    # Estadísticas generales
                    promedio_total = df['Monto'].mean()
                    gasto_total = df['Monto'].sum()

                    # Estadísticas por categoría
                    estadisticas_por_categoria = df.groupby('Categoría')['Monto'].sum()

                    st.write("\nEstadísticas Generales:")
                    st.write(f"Promedio Mensual: {promedio_total}")
                    st.write(f"Gasto Total: {gasto_total}")

                    st.write("\nEstadísticas por Categoría:")
                    st.write(estadisticas_por_categoria)

                    # Crear un gráfico de pastel de la distribución de gastos por categoría
                    fig, ax = plt.subplots()
                    ax.pie(estadisticas_por_categoria, labels=estadisticas_por_categoria.index, autopct='%1.1f%%')
                    ax.set_title('Distribución de Gastos por Categoría')
                    st.pyplot(fig)
                else:
                    st.warning("No hay datos de gastos para calcular estadísticas.")
        else:
            st.error(message)
elif menu_option == "Registro":
    st.write("Registro de Usuario")

    # Campos de registro
    new_username = st.text_input("Nuevo Nombre de Usuario:")
    new_password = st.text_input("Nueva Contraseña:", type="password")

    if st.button("Registrar"):
        registration_successful, message = registrar_usuario(new_username, new_password)
        if registration_successful:
            st.success(message)
        else:
            st.error(message)
elif menu_option == "Salir":
    st.balloons()
    st.stop()

# Guardar los datos en un archivo CSV
if not df.empty:
    df.to_csv('gastos_personales.csv', index=False)
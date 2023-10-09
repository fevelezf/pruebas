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
    # Verificar si el usuario ya existe
    if username in usuarios_df['Usuario'].values:
        return "El usuario ya existe. Por favor, inicia sesión."
    
    # Agregar el nuevo usuario al DataFrame
    nuevo_usuario = pd.DataFrame({'Usuario': [username], 'Contraseña': [password]})
    usuarios_df = usuarios_df.append(nuevo_usuario, ignore_index=True)
    usuarios_df.to_csv('usuarios.csv', index=False)  # Guardar el DataFrame en el archivo CSV
    
    return "Registro exitoso. Ahora puedes iniciar sesión."

# ...

# Función para iniciar sesión
def iniciar_sesion(username, password):
    # Buscar el usuario en el DataFrame
    user_row = usuarios_df[usuarios_df['Usuario'] == username]
    
    if user_row.empty:
        return "El usuario no existe. Regístrate primero."
    
    stored_password = user_row.iloc[0]['Contraseña']
    
    if password == stored_password:
        return "Inicio de sesión exitoso."
    else:
        return "Contraseña incorrecta. Inténtalo de nuevo."
    

# Título de la aplicación
st.title("Seguimiento de Gastos Personales")

# Menú desplegable en la barra lateral
menu_option = st.sidebar.selectbox("Menú", ["Inicio", "Registro", "Salir"])

# Opciones del menú
if menu_option == "Inicio":
    st.write("Bienvenido al inicio de la aplicación.")
elif menu_option == "Registro":
    # Agregar Gasto
    fecha = st.text_input("Ingrese la fecha (YYYY-MM-DD):")
    categoria = st.text_input("Ingrese la categoría del gasto:")
    monto = st.number_input("Ingrese el monto del gasto:")

    if st.button("Agregar Gasto"):
        # Agregar el gasto al DataFrame
        df.loc[len(df)] = [fecha, categoria, monto]
        st.success("Gasto agregado exitosamente.")
elif menu_option == "Salir":
    st.balloons()
    st.stop()

# Botón de "Entrar" para acceder a la aplicación
if st.button("Entrar"):
    # Modificar la sección "Entrar" en el menú
    st.subheader("Inicio de Sesión")
    username = st.text_input("Nombre de Usuario:")
    password = st.text_input("Contraseña:", type="password")
    
    if st.button("Iniciar Sesión"):
        mensaje = iniciar_sesion(username, password)
        st.write(mensaje)
        
        if mensaje == "Inicio de sesión exitoso.":
            # Menú principal
            opcion = st.selectbox("Seleccione una opción:", ["Agregar Gasto", "Calcular Estadísticas"])

            if opcion == "Agregar Gasto":
                fecha = st.text_input("Ingrese la fecha (YYYY-MM-DD):")
                categoria = st.text_input("Ingrese la categoría del gasto:")
                monto = st.number_input("Ingrese el monto del gasto:")

                if st.button("Agregar Gasto"):
                    # Agregar el gasto al DataFrame
                    df.loc[len(df)] = [fecha, categoria, monto]
                    st.success("Gasto agregado exitosamente.")

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

# Guardar los datos en un archivo CSV
if not df.empty:
    df.to_csv('gastos_personales.csv', index=False)
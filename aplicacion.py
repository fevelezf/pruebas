import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from tinydb import TinyDB, Query
import requests
from forex_python.converter import CurrencyRates


# Cargar el CSS personalizado
with open("custom.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# Función para crear un gráfico de barras por categorías de gastos e ingresos (Sebastian)
def crear_grafico_barras_categorias():
    '''Esta funcion realiza un gráfico de barras de la 
    gastos sumatoria de ingresos por categoria que
    haya tenido el usuario
    '''
    User = Query()
    username = st.session_state.username
    user_data = db_data.search(User.username == username)

    # Filtrar datos de gastos e ingresos
    categorias_gastos = {}
    categorias_ingresos = {}

    for d in user_data:
        if d['Tipo'] == 'Gasto':
            categoria = d['Categoría']
            monto = d['Monto']
            if categoria in categorias_gastos:
                categorias_gastos[categoria] += monto
            else:
                categorias_gastos[categoria] = monto
        elif d['Tipo'] == 'Ingreso':
            categoria = d['Categoría']
            monto = d['Monto']
            if categoria in categorias_ingresos:
                categorias_ingresos[categoria] += monto
            else:
                categorias_ingresos[categoria] = monto

    # Nos ayudamos de el tipo de dato set para poder crear la lista completa
    # De categorías
    categorias_g = set(list(categorias_gastos.keys()))
    categorias_i = set(list(categorias_ingresos.keys()))
    categorias = list(categorias_g.union(categorias_i))
    gastos = [categorias_gastos[categoria] if categoria in categorias_gastos else 0 for categoria in categorias]
    ingresos = [categorias_ingresos[categoria] if categoria in categorias_ingresos else 0 for categoria in categorias]

    # Posiciones en el eje x
    x = np.arange(len(categorias))

    # Ancho de las barras
    width = 0.35

    # Crear el gráfico de barras
    fig, ax = plt.subplots()
    # Primero graficamos gastos y luego ingresos
    ax.bar(x - width/2, gastos, width, label='Gastos', color='red')
    ax.bar(x + width/2, ingresos, width, label='Ingresos', color='green')

    ax.set_xlabel('Categorías')
    ax.set_ylabel('Monto')
    ax.set_title(f'Gastos e Ingresos por Categoría de {username}')
    ax.set_xticks(x)
    ax.set_xticklabels(categorias, rotation=45, ha="right")
    ax.legend()

    st.pyplot(fig)

# Función para crear un gráfico de torta de gastos e ingresos (Sebastian)
def crear_grafico_barras_gastos_ingresos():
    '''Esta funcion realiza un gráfico de barras de de la sumatoria
    de gastos e ingresos que haya tenido el usuario
    '''
    User= Query()
    username = st.session_state.username
    user_data = db_data.search(User.username == username)
    
    # Filtrar datos de gastos e ingresos
    gastos = [d['Monto'] for d in user_data if d['Tipo'] == 'Gasto']
    ingresos = [d['Monto'] for d in user_data if d['Tipo'] == 'Ingreso']
    
    # Calcular el total de gastos e ingresos
    total_gastos = sum(gastos)
    total_ingresos = sum(ingresos)
    
    # Crear el gráfico de barras
    labels = ['Gastos', 'Ingresos']
    values = [total_gastos, total_ingresos]
    colors = ['red', 'green']
    
    fig, ax = plt.subplots()
    ax.bar(labels, values, color=colors)
    ax.set_ylabel('Porcentaje')
    st.pyplot(fig)


# Obtener el nombre de usuario actual después del inicio de sesión
def get_current_user():
    '''Esta funcion obtiene el nombre del usuario actual despues
    del inicio de sesion
    '''
    return st.session_state.username


# Función para registrar un nuevo usuario
def registrar_usuario(username, password, first_name, last_name, email, confirm_password):
    '''Esta funcion usa la libreria tinydb para registrar un usuario en un archivo llamado
    db_users
    '''
    User = Query()
    # Verifica si el usuario ya existe en la base de datos
    if db_users.search(User.username == username):
        return False, "El usuario ya existe. Por favor, elija otro nombre de usuario."

    # Verifica si las contraseñas coinciden
    if password != confirm_password:
        return False, "Las contraseñas no coinciden. Por favor, vuelva a intentar."

    # Agrega el nuevo usuario a la base de datos
    db_users.insert({'username': username, 'password': password, 'first_name': first_name, 'last_name': last_name, 'email': email})

    return True, "Registro exitoso. Ahora puede iniciar sesión."


# Función para verificar credenciales
def verificar_credenciales(username, password):
    '''Esta funcion recibe como argumento el username y el password y verifica que
    sean inguales para permitir el ingreso al sistema
    '''
    User = Query()
    # Busca el usuario en la base de datos
    user = db_users.get((User.username == username) & (User.password == password))
    if user:
        return True, "Inicio de sesión exitoso."
    else:
        return False, "Credenciales incorrectas. Por favor, verifique su nombre de usuario y contraseña."


# Función para mostrar los gastos e ingresos del usuario actual
def mostrar_gastos_ingresos():
    '''Esta funcion hace un filtrado en db_data segun el usuario en ese momento y 
    muestra los gastos e ingresos
    '''
    username = st.session_state.username
    User = Query()
    user_data = db_data.search(User.username == username)
    st.write(f"Gastos e Ingresos de {username}:")

    # Convierte los datos en un DataFrame de pandas
    df = pd.DataFrame(user_data)

    # Muestra el DataFrame en forma de tabla
    st.write(df)
    crear_grafico_barras_gastos_ingresos()

# Reemplaza 'TU_API_KEY' con tu clave de API real
api_url = "https://v6.exchangerate-api.com/v6/5efa5e3798ad3392d4156ae7/latest/USD"
api_key = "5efa5e3798ad3392d4156ae7"
api_key2 = "1bdda545040932925faee4fffae66d7e"
# Función para convertir moneda
def convertir_moneda(cantidad, moneda_origen, moneda_destino):
    # Parámetros para la solicitud a la API
    params = {
        "base": moneda_origen,
        "symbols": moneda_destino
    }

    # Realiza la solicitud a la API para obtener la tasa de conversión
    response = requests.get("https://v6.exchangerate-api.com/v6/1bdda545040932925faee4fffae66d7e/latest/USD")
    st.write(response)
    # Procesa la respuesta de la API
    if response.status_code == 200:
        data = response.json()

        # Verifica si la clave 'rates' existe en data
        if 'rates' in data:
            exchange_rate = data['rates'][moneda_destino]

            # Realiza la conversión de moneda con la tasa obtenida
            converted_amount = cantidad * exchange_rate
            return converted_amount
        else:
            # Maneja el caso en el que 'rates' no está presente en data
            return None
    else:
        # Maneja errores si la solicitud a la API no tiene éxito
        return None
    

def crear_fon_com(usernam, fon_name, members):
    # Añadimos el fondo común a la base de datos con la función
    # Insert pero primero creamos un diccionario donde el valor
    # por defecto del aporte de todos los miembros sea 0
    members = members.split(", ")
    members.append(usernam)
    mem_dic = dict(zip(members, [0] * len(members)))
    db_us_fon_com.insert({"username": usernam, "fon_name": fon_name, "members": mem_dic})


def mostrar_fon_com(fon_elegido):
    User = Query()
    username = st.session_state.username
    fon_data = db_us_fon_com.search(
        (User.username == username) & (User.fon_name == fon_elegido))
    df_mem = pd.Series(fon_data[0]["members"])
    st.write(df_mem)
    return(fon_data[0]["members"].keys())

def upd_fon(fon_elegido , miem, amount):
    User = Query()
    username = st.session_state.username
    st.write(fon_elegido, miem, amount)
    fon_data = db_us_fon_com.search(
        (User.username == username) & (User.fon_name == fon_elegido))
    st.write(fon_data)
    data_act = fon_data[0]["members"]
    data_act[miem]+=amount
    db_us_fon_com.update({"members": data_act}, ((User.username == username) & (User.fon_name == fon_elegido)))
    st.success("Se ha registrado correctamente")




# Inicializa la base de datos para usuarios y gastos e ingresos
db_users = TinyDB('usuarios.json')
db_data = TinyDB('data.json')
db_us_fon_com = TinyDB('us_fon_com.json')

# Inicializar la variable de sesión para el nombre de usuario
if 'username' not in st.session_state:
    st.session_state.username = None

# Título de la aplicación
st.title("Seguimiento de Gastos Personales")

# Menú desplegable en la barra lateral
if get_current_user() is not None:
    # Sidebar menu options for logged-in users
    menu_option = st.sidebar.selectbox("Menú", ["Pagina Principal", "Registrar Gasto", "Registrar Ingreso", "Mostrar Gastos e Ingresos",
                                                "Crear Fondo Común", "Fondos comunes", "Cerrar Sesión"])
else:
    # Sidebar menu options for non-logged-in users
    menu_option = st.sidebar.selectbox("Menú", ["Inicio", "Inicio de Sesion", "Registro","Conversion de Moneda"])

# Si el usuario elige "Cerrar Sesión", restablecer la variable de sesión a None
if menu_option == "Cerrar Sesión":
    st.session_state.username = None
    st.success("Sesión cerrada con éxito. Por favor, inicie sesión nuevamente.")

# Si el usuario ya ha iniciado sesión, mostrar los botones
if get_current_user() is not None:

    if menu_option == "Pagina Principal":
        username = get_current_user()
        st.write(f'<h4 style="font-size: 26px; font-weight: bold; text-align: center;">Hola {username}!</h4>', unsafe_allow_html=True)

        # Calculate total expenses and income for the user
        User = Query()
        user_data = db_data.search(User.username == username)
        gastos = sum(d['Monto'] for d in user_data if d['Tipo'] == 'Gasto')
        ingresos = sum(d['Monto'] for d in user_data if d['Tipo'] == 'Ingreso')

        # Display the total expenses and income
        st.write(f"<h4 style='font-size: 26px;'>En total te has gastado: {gastos}</h4>", unsafe_allow_html=True)
        st.write(f"<h4 style='font-size: 26px;'>Has tenido unos ingresos por el valor de: {ingresos}</h4>", unsafe_allow_html=True)


    # Botones para registrar gasto, ingreso o ver registros
    if menu_option == "Registrar Gasto":
        st.header("Registrar Gasto")
        with st.form("registrar_gasto_form"):
            fecha = st.date_input("Fecha del Gasto")
            # Cambiar el campo de texto por un menú desplegable para la categoría
            categoria_gastos = st.selectbox("Seleccione la categoría:", ["Alimentación", "Cuentas y pagos", "Casa", "Transporte", "Ropa", "Salud e higiene", "Diversión", "Otros gastos"])
            monto = st.number_input("Ingrese el monto:")
            if st.form_submit_button("Registrar"):
                username = st.session_state.username
                db_data.insert({'username': username, 'Fecha': str(fecha), 'Tipo': 'Gasto', 'Categoría': categoria_gastos, 'Monto': monto})
                st.success("Gasto registrado exitosamente.")
                # Limpiar los campos después de registrar el gasto
                fecha = ""
                categoria_gastos = ""
                monto = 0.0

    # Establecer la opción del menú seleccionada en la variable de estado
    st.session_state.option = ""
    if menu_option == "Registrar Ingreso":
        st.header("Registrar Ingreso")
        with st.form("registrar_Ingreso_form"):
            fecha = st.date_input("Fecha del Ingreso")
            categoria_ingresos = st.selectbox("Seleccione la categoría:", ['Salario', 'Varios'])
            monto = st.number_input("Ingrese el monto:")
            if st.form_submit_button("Registrar"):
                username = st.session_state.username
                db_data.insert({'username': username, 'Fecha': str(fecha), 'Tipo': 'Ingreso', 'Categoría': categoria_ingresos, 'Monto': monto})
                st.success("Ingreso registrado exitosamente.")

    if menu_option == "Mostrar Gastos e Ingresos":
        mostrar_gastos_ingresos()
        crear_grafico_barras_categorias()

    if menu_option == "Crear Fondo Común":
        st.header("Crear Fondo Común")
        fon_name = st.text_input("Nombre del Fondo Común:")
        Members = st.text_input("Integrantes del fondo(Por favor separar cor\
                                coma y espacio)")
        if st.button("Registrar"):
            crear_fon_com(st.session_state.username, fon_name, Members)
            st.success("El fondo ha sido creado")

    if menu_option == "Fondos comunes":
        st.header("Tus Fondos Comunes")
        User = Query()
        username = st.session_state.username
        fon_data = db_us_fon_com.search(User.username == username)

        if fon_data:
            User = Query()
            username = st.session_state.username
            fon_data = db_us_fon_com.search(User.username == username)
            df =  pd.DataFrame(fon_data)
            lista = df["fon_name"].to_list()
            selected_fon = st.selectbox("Elija el fondo al que desee acceder",
                        lista)
            if selected_fon:
                User = Query()
                username = st.session_state.username
                fon_data = db_us_fon_com.search(
                (User.username == username) & (User.fon_name == selected_fon))
                df_mem = pd.Series(fon_data[0]["members"])
                st.write(df_mem)
                lista = fon_data[0]["members"].keys()
                miem = st.selectbox('Seleccione el miembro', lista)
                amount = st.number_input('Ingresa la cantidad que deseas añadir o retirar', min_value=1.0, step=1.0)
                    #if st.form_submit_button("Actualizar"):
                    #if st.form_submit_button("Actualizar"):
                        #st.write("ssssss")
                        # username = miem
                        #db_data.insert({'username': username, 'Fecha': str(fecha), 'Tipo': 'Ingreso', 'Categoría': categoria_ingresos, 'Monto': monto})
                        #st.success("Ingreso registrado exitosamente.")
                        #st.success(selected_fon, miem, amount)
                        #upd_fon(selected_fon, miem, amount)
            if st.button("Actualizr"):
                upd_fon(selected_fon, miem, amount)


        else:
            st.write("Aún no tienes un fondo común, \
                    anímate a crear uno")


else:

    if menu_option == "Conversion de Moneda":
        st.title('Conversor de divisas en tiempo real')

        c = CurrencyRates()

        amount = st.number_input('Ingresa la cantidad que deseas convertir', min_value=1.0, step=1.0)

        from_currency = st.selectbox('De:', ['USD', 'EUR', 'JPY', 'GBP', 'AUD', 'CAD'])
        to_currency = st.selectbox('A:', ['USD', 'EUR', 'JPY', 'GBP', 'AUD', 'CAD'])

        if st.button('Convertir'):
            conversion_rate = c.get_rate(from_currency, to_currency)
            converted_amount = conversion_rate * amount
            st.write(f'{amount} {from_currency} son equivalentes a {converted_amount} {to_currency}')
    if menu_option == "Inicio":
        # Enlace a consejos financieros
        st.header("Consejos Financieros")
        st.write("Aquí encontrarás consejos financieros útiles para mejorar tus finanzas personales.")
        st.write("1. Ahorra una parte de tus ingresos cada mes.")
        st.write("2. Crea un presupuesto y ajústate a él.")
        st.write("3. Paga tus deudas a tiempo.")
        st.write("4. Invierte tu dinero sabiamente.")
        st.write("5. Educa tu mente financiera.")

        # Enlace a videos de YouTube
        st.header("Ahorrar no es solo guardar, sino tambien, saber gastar")
        st.write('<h4 style="font-size: 26px; color: #000000; font-family: cursive; font-weight: bold; text-align: center;">Y para ti... ¿Qué es ahorrar?</h4>', unsafe_allow_html=True)

        st.video("https://www.youtube.com/watch?v=KDxhvehEius&ab_channel=MedallaMilagrosa")

        st.write('<h4 style="font-size: 26px; color: #000000; font-family: cursive; font-weight: bold; text-align: center;">Tan facil como jugar... es ahorrar</h4>', unsafe_allow_html=True)

        st.video("https://www.youtube.com/watch?v=gqtojhFaSlE&ab_channel=Bancolombia")

        st.write('<h4 style="font-size: 26px; color: #000000; font-family: cursive; font-weight: bold; text-align: center;">Y... ¿Sabes que es un ciclo economico?</h4>', unsafe_allow_html=True)

        st.video("https://www.youtube.com/watch?v=7jklUV3QE70&list=PLYV86yxR8Np89gAhNR8LTpSe7_QthTMHY&index=4&ab_channel=MedallaMilagrosa")

        st.write('<h2 style="font-size: 30px; color: #000000; font-family: cursive; font-weight: bold; text-align: center;">¡Prepara tu camino hacia un futuro financiero más sólido! Regístrate ahora.</h2>', unsafe_allow_html=True)





    # Inicio de sesión
    if menu_option == "Inicio de Sesion":
        st.write("Bienvenido al inicio de la aplicación.")

        # Campos de inicio de sesión
        username = st.text_input("Nombre de Usuario:")
        password = st.text_input("Contraseña:", type="password")

        if st.button("Iniciar Sesión"):
            login_successful, message = verificar_credenciales(username, password)
            if login_successful:
                st.success(message)
                # Almacenar el nombre de usuario en la sesión
                st.session_state.username = username  
            else:
                st.error(message)
    elif menu_option == "Registro":
        st.write("Registro de Usuario")

        # Campos de registro
        first_name = st.text_input("Nombre del Usuario:")
        last_name = st.text_input("Apellidos del Usuario:")
        email = st.text_input("Correo electronico del Usuario:")
        new_username = st.text_input("Nuevo Nombre de Usuario:")
        new_password = st.text_input("Nueva Contraseña:", type = "password")
        confirm_password = st.text_input("Confirmar contraseña:", type = "password")

        # Crear dos columnas para los botones
        col1, col2 = st.columns(2)
        # Casilla de verificación para aceptar la política de datos personales
        # Inicializa la variable aceptar_politica
        
        # Variable de estado para rastrear si el usuario ha visto la política
        if 'politica_vista' not in st.session_state:
            st.session_state.politica_vista = False

        # Botón para abrir la ventana emergente en la segunda columna
        if col2.button("Ver Política de Tratamiento de Datos"):
            with open("politica_datos.txt", "r") as archivo:
                politica = archivo.read()
                with st.expander("Política de Tratamiento de Datos",expanded=True):
                    st.write(politica)
                    st.session_state.politica_vista = True
                # Casilla de verificación para aceptar la política
        aceptar_politica = st.checkbox("Acepta la política de datos personales")
        # Botón de registro de usuario en la primera columna
        if col1.button("Registrarse") and aceptar_politica and st.session_state.politica_vista:
            registration_successful, message = registrar_usuario(new_username, new_password, first_name, last_name, email, confirm_password)
            if registration_successful:
                st.success(message)
            else:
                st.error(message)

        if not aceptar_politica:
            st.warning("Por favor, acepta la política de datos personales antes de registrarte.")

        if not st.session_state.politica_vista:
            st.warning("Por favor, ve la política de datos personales antes de registrarte.")



    elif menu_option == "Salir":
        st.balloons()
        st.stop()

# Botón acerca de nosotros esquina inferior derecha (Sebastian)
st.markdown('<a class="popup-button" href="https://docs.google.com/document/d/e/2PACX-1vSIomi8VyMbiALUI7HIL-I94KqkAB6jVr5OtJztLis_plX4uiHcSexuGu17V8WcccZOPt4V7nCoIkZw/pub" target="_blank">Acerca de nosotros</a>',
            unsafe_allow_html=True)
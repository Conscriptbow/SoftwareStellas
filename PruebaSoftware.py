import time
import streamlit as st
import plotly_express as px
import pandas as pd
import sqlite3
import numpy as np
from streamlit.state.session_state import WidgetArgs
conn = sqlite3.connect('data.db')
c = conn.cursor()

#BD BASA EN DISCO
    #CREAR TABLA BD
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')
    #AGREGAR USER Y PASSWORD
def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()
    #LOGIN
def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data
    #CAMBIAR PASSWORD
def change_password(password,username):
    c.execute('UPDATE userstable SET password =? WHERE username =?',(password,username))
    conn.commit()
    #VER TODOS LOS USUARIOS
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

#TITULO / IMAGENES / PORTADA 
def home():   
    st.set_option('deprecation.showfileUploaderEncoding',False)
    md_logo1 = 'https://seeklogo.com/images/C/cecytem-logo-57EA94498B-seeklogo.com.png'
    md_logo2 = 'https://www.paratodomexico.com/imagenes/estados-de-mexico/mexico/escudo_estado_mexico.png'
    title_container = st.container()
    col1, col2 = st.columns([15,5])
    with title_container:
        with col1:
            st.image(md_logo1, width=150)
        with col2:   
            st.image(md_logo2, width=150)
    
    st.markdown('****')
    st.markdown("<h1 style='text-align: center;'>Colegio de Estudios Científicos y Tecnológicos del Estado de México</h1>", unsafe_allow_html=True)
    st.markdown('---')

#ACCESO
def acceder():
    username = st.sidebar.text_input("Nombre de usuario: ")
    password = st.sidebar.text_input("Contraseña: ", type = 'password')
    if st.sidebar.checkbox("Acceder"):
        create_usertable()
        result = login_user(username,password)
        if result:
                st.success("Te has logeado como: {}".format(username))                          
                lectura_archivo()
        else:
                st.warning("Incorrecto Nombre de usuario/Contraseña")
    elif st.sidebar.checkbox("¿Olvido su contraseña?"):
        st.header("Cambio de contraseña:")      
        user = st.text_input("Nombre de usuario:") 
        new_pass = st.text_input("Contraseña:", type='password')  
        if st.checkbox("Cambiar"):
            change_password(new_pass,user) 
            st.success("Se cambio su contraseña")

#SIGN UP
def sign():
    st.subheader("Crear nueva cuenta:")
    new_user = st.text_input("Nombre de usuario:")
    new_password = st.text_input("Contraseña:", type='password')
    if st.button("Signup"):
        create_usertable()
        add_userdata(new_user, new_password)
        st.success("Nueva cuenta creada, puede ingresar")

#BARRA LATERAL --MENU--
def menu():
    home()
    md_logo3 = 'https://cdn-icons-png.flaticon.com/128/633/633970.png'
    st.sidebar.image(md_logo3, width=120)
    st.sidebar.markdown('---')
    st.sidebar.markdown("<h1 style='text-align: center;'>STELLAS COMPANY | V1.01</h1>", unsafe_allow_html=True)
    st.sidebar.markdown('---')
    st.sidebar.markdown("<h1 style='text-align: center;'>MENU</h1>", unsafe_allow_html=True)
    menu = ["Acceder", "Sign Up", "Cerrar Sesión"]
    choice = st.sidebar.selectbox("", menu)
    
    if choice == "Sign Up":
        sign()
    elif choice == "Acceder":
        acceder()

#FILTRO DATOS
def filtro():
    semestre = st.sidebar.multiselect("Seleccione el semestre: ", options=datos["Semestre"].unique())
    carrera = st.sidebar.multiselect("Seleccione la carrera: ", options=datos["Carrera"].unique())
    grupo = st.sidebar.multiselect("Seleccione el grupo: ", options=datos["Grupo"].unique())
    asignatura = st.sidebar.multiselect("Seleccione la asignatura: ", options=datos["Asignatura"].unique())
    datos_selection = datos.query("Grupo==@grupo and Semestre==@semestre and Carrera == @carrera and Asignatura == @asignatura")
    st.subheader("TABLA CON DATOS FILTRADOS: ")
    st.dataframe(datos_selection)

#COLOR
def color_negative_red(value):
  """
  Colors elements in a dateframe
  green if positive and red if
  negative. Does not color NaN
  values.
  """

  if value == 5:
    color = 'red'
  elif value > 5:
    color = 'green'
  else:
    color = 'black'

  return 'color: %s' % color

#BARRA AJUSTES Y LECTURA ARCHIVO
def lectura_archivo():
    st.subheader("INSERTAR ARCHIVO:")
    # CARGA DE ARCHIVOS
    archivo_cargado = st.file_uploader(label="Sube aqui tus archivos CSV o Excel.",
                         type=['csv','xlsx'])
    global datos
    # si el archivo cargado no es ninguno
    if archivo_cargado is not None:
        print(archivo_cargado)
        try:
            datos = pd.read_csv(archivo_cargado)   
        except Exception as e:
            st.markdown("<h3 style='text-align: center;'>TABLA DE BASE DE DATOS</h3>", unsafe_allow_html=True)
            print(e)
            datos = pd.read_excel(archivo_cargado)
            my_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1)

    global cols_num
    try:
        #COLOR DATOS REPROBADOS
        #tabla = datos.style.applymap(color_negative_red, subset=['P1'])
        #tabla = datos.style.set_properties (** {'border': '1.3px solid green','color': 'blanco'})
        st.write(datos)
        menu = st.radio("",("Filtro", "Turno Matutino", "Turno Vespertino", "Promedios"),)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        st.markdown('---')
        if menu == 'Filtro':
            st.sidebar.markdown('---')
            filtro()
        elif menu == 'Turno Matutino':
            cols_num = list(datos.select_dtypes(['float','int','object']).columns)
            a=100
            frames = []
            for i in range(0,6):
                if a == 104:
                    a=200
                elif a == 204:
                    a=300
                elif a == 304:
                    a=400
                elif a == 404:
                    a=500
                elif a==504:
                    a=600
                for j in range(0,4):
                    a = a + 1
                    grupoMatutino = datos.loc[datos['Grupo'] == a]
                    frames.append(grupoMatutino)
            df = pd.concat(frames, sort=False)
            st.subheader("TABLA TURNO MATUTINO: ")
            st.dataframe(df)
            grafico()
        elif menu == 'Turno Vespertino':
            a=104
            frames2 = []
            for i in range(0,6):
                if a == 108:
                    a=204
                elif a == 208:
                    a=304
                elif a == 308:
                    a=404
                elif a == 408:
                    a=504
                elif a==508:
                    a=604
            for j in range(0,4):
                    a = a + 1
                    grupoTarde = datos.loc[datos['Grupo'] == a]
                    frames2.append(grupoTarde)
            dc = pd.concat(frames2, sort = False)
            st.subheader("TABLA TURNO VESPERTINO: ")
            st.dataframe(dc)
            grafico()
            #Promedio por grupo, materia...
        elif menu == 'Promedios':
            st.subheader("PROMEDIOS: ")
            ndf = datos.pivot_table(index = ['Grupo', 'Carrera'],columns=['Asignatura', 'Semestre'],aggfunc={'P1':np.average,'P2':np.average})
            ndf
    except Exception as e:
        print(e)
        st.write("Porfavor suba su archivo a la aplicación")

#GRAFICO
def grafico():
    st.subheader("Gráfico: ")
    try:
            x_val = st.selectbox('Seleccione x: ', options = ['P1', 'P2', 'P3', 'FIN'])
            y_val = st.selectbox('Seleccione y: ', options = ['Carrera', 'Semestre','Grupo'])
            plot = px.box(data_frame=datos, x=x_val,y=y_val, width=600, height=400)
            st.plotly_chart(plot)
    except Exception as e:
        print(e)
#DESPLIEGE DEL PROGRAMA
menu()
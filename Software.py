import datetime
import time
import streamlit as st
import plotly_express as px
import pandas as pd
from PIL import Image
import sqlite3
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
conn = sqlite3.connect('data.db')
c = conn.cursor()

#DISEÑO
def design():
    #TITULO    
    st.set_option('deprecation.showfileUploaderEncoding',False)
    title_container = st.container()
    col1, col3 = st.columns([15, 5])
    with title_container:
        with col1:
                st.image('https://seeklogo.com/images/C/cecytem-logo-57EA94498B-seeklogo.com.png', width=150)
        with col3:
                st.image('https://www.paratodomexico.com/imagenes/estados-de-mexico/mexico/escudo_estado_mexico.png', width=150)
    st.markdown("<h1 style='text-align: center;'>Colegio de Estudios Científicos y Tecnológicos del Estado de México</h1>", unsafe_allow_html=True)
    #st.video('https://www.youtube.com/watch?v=8K_9mlscRfg&ab_channel=VIDEOSDEIMPACTO')

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
            st.subheader("TABLA CECYTEM: ")
            print(e)
            datos = pd.read_excel(archivo_cargado)
            my_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1)

    global cols_num
    try:
        st.write(datos)# tipos de datos del df, seleccion de columns
        menu = ["Turno Matutino", "Turno Vespertino"]
        semestre = st.sidebar.multiselect("Seleccione el semestre: ", options=datos["Semestre"].unique())
        carrera = st.sidebar.multiselect("Seleccione la carrera: ", options=datos["Carrera"].unique())
        grupo = st.sidebar.multiselect("Seleccione el grupo: ", options=datos["Grupo"].unique())
        asignatura = st.sidebar.multiselect("Seleccione la asignatura: ", options=datos["Asignatura"].unique())
        datos_selection = datos.query("Grupo==@grupo and Semestre==@semestre and Carrera == @carrera and Asignatura == @asignatura")
        #Indice aprobación todo los datos
        Aprobacion()
        #DATOS RESUMIDOS
        prueba1 = datos.describe()
        st.subheader("DATOS RESUMIDOS: ")
        prueba = prueba1.iloc[[1,3,4,5,6,7],[3,4,5,7]]
        prueba
        #Promedio por grupo, materia...
        st.subheader("PROMEDIOS: ")
        ndf = datos.pivot_table(index = ['Grupo', 'Carrera'],columns=['Asignatura', 'Semestre'],aggfunc={'P1':np.average,'P2':np.average})
        ndf
        try:
            st.subheader("TABLA CON DATOS FILTRADOS: ")
            st.dataframe(datos_selection)
            choice =st.selectbox("Seleccione el turno: ", menu)
            if choice == "Turno Matutino":
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
            elif choice == "Turno Vespertino":
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
        except Exception as e:
            print(e)
            st.write("No has seleccionado el turno")
    except Exception as e:
        print(e)
        st.write("Porfavor suba su archivo a la aplicación")

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

#INGRESO A LA PLATAFORMA
def seguridad():
    design()
    st.sidebar.image('https://www.pinclipart.com/picdir/big/564-5647199_transparent-home-icon-clipart-circle-transparent-home-icon.png',width=100)
    menu = ["Acceder", "SignUp", "Cerrar Sesión"]
    choice = st.sidebar.selectbox("MENU", menu)
    if choice == "Cerrar Sesión":
        st.info("Has cerrado sesión")
    elif choice == "Acceder":
        username = st.sidebar.text_input("Nombre de usuario")
        password = st.sidebar.text_input("Contraseña", type = 'password')
        if st.sidebar.checkbox("Acceder"):
            create_usertable()
            result = login_user(username,password)
            if result:
                st.success("Te has logeado como: {}".format(username))                          
                lectura_archivo()
            else:
                st.warning("Incorrect Username/Password")
        elif st.sidebar.checkbox("¿Olvido su contraseña?"):
            st.subheader("Cambiar password")      
            user = st.text_input("Username") #INGRESAR USUARIO EL CUAL NOS VA SERVIR COMO REFERENCIA
            new_pass = st.text_input("Password", type='password') #INGRESAR LA NUEVA CONTRASEÑA z 
            if st.checkbox("Change"):
                change_password(new_pass,user) #FUNCION PARA CAMBIAR CONTRASEÑA
                st.success("Se cambio su contraseña")
    elif choice == "SignUp":
        st.subheader("Crear nueva cuenta")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, new_password)
            st.success("New account")
            st.info("Puede ingresar")

def grafico():
    st.subheader("Gráfico de barras:")
    st.subheader("Gráfico: ")
    try:
            x_val = st.selectbox('Seleccione x: ', options = ['P1', 'P2', 'P3', 'FIN'])
            y_val = st.selectbox('Seleccione y: ', options = ['Carrera', 'Semestre','Grupo'])
            plot = px.box(data_frame=datos, x=x_val,y=y_val,width=600, height=400)
            st.plotly_chart(plot)
    except Exception as e:
        print(e)

def Aprobacion():
    pruebasP = []

    for i in range(0, len(datos)):
        if datos.empty:
            continue
        pruebas = datos['Plantel'].unique()
        pruebasP.append(pruebas)

    #################################PLANTEL
    indicePlantel1 = []
    indiceAproP1 = datos.loc[datos['P1'] >= 6]
    porcentajeP1 = (len(indiceAproP1)*100)/len(datos)
    indicePlantel1.append(porcentajeP1)
    plantel = pd.DataFrame(data=indicePlantel1)
    plantel.rename(columns={0:'APROBACIÓN P1(%)'}, inplace=True)
    for i in range (0, len(plantel)):
        plantel.rename(index={i:pruebasP[i]}, inplace=True)
    ################################################
    indicePlantel2 = []
    indiceAproP2 = datos.loc[datos['P2'] >= 6]
    porcentajeP2 = (len(indiceAproP2)*100)/len(datos)
    indicePlantel2.append(porcentajeP2)
    plantel2 = pd.DataFrame(data=indicePlantel2)
    plantel2.rename(columns={0:'APROBACIÓN P2(%)'}, inplace=True)
    for i in range (0, len(plantel2)):
        plantel2.rename(index={i:pruebasP[i]}, inplace=True)
    ##########################################################################
    indicePlantel3 = []
    indiceAproP3 = datos.loc[datos['P3'] >= 6]
    porcentajeP3 = (len(indiceAproP3)*100)/len(datos)
    indicePlantel3.append(porcentajeP3)
    plantel3 = pd.DataFrame(data=indicePlantel3)
    plantel3.rename(columns={0:'APROBACIÓN P3(%)'}, inplace=True)
    for i in range (0, len(plantel3)):
        plantel3.rename(index={i:pruebasP[i]}, inplace=True)
    ##########################################################################
    indicePlantelFin = []
    indiceAproFin = datos.loc[datos['FIN'] >= 6]
    porcentajePFin = (len(indiceAproFin)*100)/len(datos)
    indicePlantelFin.append(porcentajePFin)
    plantelFin = pd.DataFrame(data=indicePlantelFin)
    plantelFin.rename(columns={0:'APROBACIÓN FIN(%)'}, inplace=True)
    for i in range (0, len(plantelFin)):
        plantelFin.rename(index={i:pruebasP[i]}, inplace=True)
    ############################################################################
    indicePlantelR = []
    indiceRP1 = datos.loc[datos['P1']<=5]
    porcentajeRP1 = (len(indiceRP1)*100)/len(datos)
    indicePlantelR.append(porcentajeRP1)
    plantelR=pd.DataFrame(data=indicePlantelR)
    plantelR.rename(columns={0:'REPROBACIÓN P1 (%)'}, inplace=True)
    for i in range (0, len(plantelR)):
        plantelR.rename(index={i:pruebasP[i]}, inplace=True)
    #########################################################################
    indicePlantelR2 = []
    indiceRP2 = datos.loc[datos['P2']<=5]
    porcentajeRP2 = (len(indiceRP2)*100)/len(datos)
    indicePlantelR2.append(porcentajeRP2)
    plantelR2=pd.DataFrame(data=indicePlantelR2)
    plantelR2.rename(columns={0:'REPROBACIÓN P2 (%)'}, inplace=True)
    for i in range (0, len(plantelR2)):
        plantelR2.rename(index={i:pruebasP[i]}, inplace=True)
    ############################################################################
    indicePlantelR3 = []
    indiceRP3 = datos.loc[datos['P3']<=5]
    porcentajeRP3 = (len(indiceRP3)*100)/len(datos)
    indicePlantelR3.append(porcentajeRP3)
    plantelR3=pd.DataFrame(data=indicePlantelR3)
    plantelR3.rename(columns={0:'REPROBACIÓN P3 (%)'}, inplace=True)
    for i in range (0, len(plantelR3)):
        plantelR3.rename(index={i:pruebasP[i]}, inplace=True)
    ############################################################################
    indicePlantelRFin = []
    indiceRPFin = datos.loc[datos['FIN']<=5]
    porcentajeRFin = (len(indiceRPFin)*100)/len(datos)
    indicePlantelRFin.append(porcentajeRFin)
    plantelRFin=pd.DataFrame(data=indicePlantelRFin)
    plantelRFin.rename(columns={0:'REPROBACIÓN FIN (%)'}, inplace=True)
    for i in range (0, len(plantelRFin)):
        plantelRFin.rename(index={i:pruebasP[i]}, inplace=True)
    ###########################################################################

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
    
############################################################## Mañana
    indiceMañana = []
    for i in range(0, len(frames)):
        primerGrupo=frames[i].loc[frames[i]['P1']>=6]
        if primerGrupo.empty:
            continue
        porcentaje = (len(primerGrupo)*100)/len(frames[i])
        indiceMañana.append(porcentaje)

    mañana=pd.DataFrame(data=indiceMañana)
    mañana.rename(columns={0:'APROBACIÓN P1(%)'}, inplace=True)

    ######################################################
    pruebasm = []

    for i in range(0, len(frames)):
        if frames[i].empty:
            continue
        pruebas = frames[i]['Grupo'].unique()
        pruebasm.append(pruebas)

    for i in range (0, len(mañana)):
        mañana.rename(index={i:int(pruebasm[i])}, inplace=True)

    ################################################
    indiceMañanaP2 = []
    for i in range(0, len(frames)):
        primerGrupo=frames[i].loc[frames[i]['P2']>=6]
        if primerGrupo.empty:
            continue
        porcentaje = (len(primerGrupo)*100)/len(frames[i])
        indiceMañanaP2.append(porcentaje)
    
    mañanap2 = pd.DataFrame(data=indiceMañanaP2)
    mañanap2.rename(columns={0:'APROBACIÓN P2(%)'}, inplace=True)
    for i in range (0, len(mañanap2)):
        mañanap2.rename(index={i:int(pruebasm[i])}, inplace=True)

    ################################################
    indiceMañanaP3 = []
    for i in range(0, len(frames)):
        primerGrupo=frames[i].loc[frames[i]['P3']>=6]
        if primerGrupo.empty:
            continue
        porcentaje = (len(primerGrupo)*100)/len(frames[i])
        indiceMañanaP3.append(porcentaje)

    mañanap3 = pd.DataFrame(data=indiceMañanaP3)
    mañanap3.rename(columns={0:'APROBACIÓN P3(%)'}, inplace=True)
    for i in range (0, len(mañanap3)):
        mañanap3.rename(index={i:int(pruebasm[i])}, inplace=True)
    ###############################################
    indiceMañanaFin = []
    for i in range(0, len(frames)):
        primerGrupo=frames[i].loc[frames[i]['FIN']>=6]
        if primerGrupo.empty:
            continue
        porcentaje = (len(primerGrupo)*100)/len(frames[i])
        indiceMañanaFin.append(porcentaje)

    mañanafin = pd.DataFrame(data=indiceMañanaFin)
    mañanafin.rename(columns={0:'APROBACIÓN FIN(%)'}, inplace=True)
    for i in range (0, len(mañanafin)):
        mañanafin.rename(index={i:int(pruebasm[i])}, inplace=True)
    ################################################ Tarde

    indiceTarde = []
    for i in range(0, len(frames2)):
        segundoGrupo=frames2[i].loc[frames2[i]['P1']>=6]
        if segundoGrupo.empty:
            continue
        porcentaje = (len(segundoGrupo)*100)/len(frames2[i])
        indiceTarde.append(porcentaje)

    tarde=pd.DataFrame(data=indiceTarde)
    tarde.rename(columns={0:'APROBACIÓN P1(%)'}, inplace=True)

    pruebast = []
    for i in range(0, len(frames2)):
        if frames2[i].empty:
            continue
        pruebas = frames2[i]['Grupo'].unique()
        pruebast.append(pruebas)

    for i in range (0, len(tarde)):
        tarde.rename(index={i:int(pruebast[i])}, inplace=True)

    #############################################################
    indiceTardeP2 = []
    for i in range(0, len(frames2)):
        segundoGrupo=frames2[i].loc[frames2[i]['P2']>=6]
        if segundoGrupo.empty:
            continue
        porcentaje = (len(segundoGrupo)*100)/len(frames2[i])
        indiceTardeP2.append(porcentaje)

    tardeP2=pd.DataFrame(data=indiceTardeP2)
    tardeP2.rename(columns={0:'APROBACIÓN P2(%)'}, inplace=True)

    for i in range (0, len(tarde)):
        tardeP2.rename(index={i:int(pruebast[i])}, inplace=True)
    ############################################################
    indiceTardeP3 = []
    for i in range(0, len(frames2)):
        segundoGrupo=frames2[i].loc[frames2[i]['P3']>=6]
        if segundoGrupo.empty:
            continue
        porcentaje = (len(segundoGrupo)*100)/len(frames2[i])
        indiceTardeP3.append(porcentaje)

    tardeP3=pd.DataFrame(data=indiceTardeP3)
    tardeP3.rename(columns={0:'APROBACIÓN P3(%)'}, inplace=True)

    for i in range (0, len(tardeP3)):
        tardeP3.rename(index={i:int(pruebast[i])}, inplace=True)
    #########################################################
    indiceTardeFin = []
    for i in range(0, len(frames2)):
        segundoGrupo=frames2[i].loc[frames2[i]['FIN']>=6]
        if segundoGrupo.empty:
            continue
        porcentaje = (len(segundoGrupo)*100)/len(frames2[i])
        indiceTardeFin.append(porcentaje)

    tardeFin=pd.DataFrame(data=indiceTardeFin)
    tardeFin.rename(columns={0:'APROBACIÓN Fin(%)'}, inplace=True)

    for i in range (0, len(tarde)):
        tardeFin.rename(index={i:int(pruebast[i])}, inplace=True)
    ######################################################### indice repro
    indiceMañanaR = []
    for i in range(0, len(frames)):
        primerGrupo=frames[i].loc[frames[i]['P1']<=5]
        if primerGrupo.empty:
            continue
        porcentaje = (len(primerGrupo)*100)/len(frames[i])
        indiceMañanaR.append(porcentaje)

    mañanaR=pd.DataFrame(data=indiceMañanaR)
    mañanaR.rename(columns={0:'REPROBACIÓN P1(%)'}, inplace=True)
    
    for i in range (0, len(mañanaR)):
        mañanaR.rename(index={i:int(pruebasm[i])}, inplace=True)

    #############################################################
    indiceMañanaR2 = []
    for i in range(0, len(frames)):
        primerGrupo=frames[i].loc[frames[i]['P2']<=5]
        if primerGrupo.empty:
            continue
        porcentaje = (len(primerGrupo)*100)/len(frames[i])
        indiceMañanaR2.append(porcentaje)

    mañanaR2=pd.DataFrame(data=indiceMañanaR2)
    mañanaR2.rename(columns={0:'REPROBACIÓN P2(%)'}, inplace=True)
    
    for i in range (0, len(mañanaR2)):
        mañanaR2.rename(index={i:int(pruebasm[i])}, inplace=True)
   
    ###############################################################
    indiceMañanaR3 = []
    for i in range(0, len(frames)):
        primerGrupo=frames[i].loc[frames[i]['P3']<=5]
        if primerGrupo.empty:
            continue
        porcentaje = (len(primerGrupo)*100)/len(frames[i])
        indiceMañanaR3.append(porcentaje)

    mañanaR3=pd.DataFrame(data=indiceMañanaR3)
    mañanaR3.rename(columns={0:'REPROBACIÓN P3(%)'}, inplace=True)
    
    for i in range (0, len(mañanaR3)):
        mañanaR3.rename(index={i:int(pruebasm[i])}, inplace=True)
    ###############################################################
    indiceMañanaFin = []
    for i in range(0, len(frames)):
        primerGrupo=frames[i].loc[frames[i]['FIN']<=5]
        if primerGrupo.empty:
            continue
        porcentaje = (len(primerGrupo)*100)/len(frames[i])
        indiceMañanaFin.append(porcentaje)

    mañanaRFin=pd.DataFrame(data=indiceMañanaFin)
    mañanaRFin.rename(columns={0:'REPROBACIÓN FIN(%)'}, inplace=True)
    
    for i in range (0, len(mañanaRFin)):
        mañanaRFin.rename(index={i:int(pruebasm[i])}, inplace=True)

    ###########################################################
    indiceTardeR = []
    for i in range(0, len(frames2)):
        segundoGrupo=frames2[i].loc[frames2[i]['P1']<=5]
        if segundoGrupo.empty:
            continue
        porcentaje = (len(segundoGrupo)*100)/len(frames2[i])
        indiceTardeR.append(porcentaje)

    tardeR=pd.DataFrame(data=indiceTardeR)
    tardeR.rename(columns={0:'REPROBACIÓN P1(%)'}, inplace=True)

    for i in range (0, len(tarde)):
        tardeR.rename(index={i:int(pruebast[i])}, inplace=True)
    ##########################################################
    indiceTardeR2 = []
    for i in range(0, len(frames2)):
        segundoGrupo=frames2[i].loc[frames2[i]['P2']<=5]
        if segundoGrupo.empty:
            continue
        porcentaje = (len(segundoGrupo)*100)/len(frames2[i])
        indiceTardeR2.append(porcentaje)

    tardeR2=pd.DataFrame(data=indiceTardeR2)
    tardeR2.rename(columns={0:'REPROBACIÓN P2(%)'}, inplace=True)

    for i in range (0, len(tarde)):
        tardeR2.rename(index={i:int(pruebast[i])}, inplace=True)
    #############################################################
    indiceTardeR3 = []
    for i in range(0, len(frames2)):
        segundoGrupo=frames2[i].loc[frames2[i]['P3']<=5]
        if segundoGrupo.empty:
            continue
        porcentaje = (len(segundoGrupo)*100)/len(frames2[i])
        indiceTardeR3.append(porcentaje)

    tardeR3=pd.DataFrame(data=indiceTardeR3)
    tardeR3.rename(columns={0:'REPROBACIÓN P3(%)'}, inplace=True)

    for i in range (0, len(tardeR3)):
        tardeR3.rename(index={i:int(pruebast[i])}, inplace=True)
    #################################################################
    indiceTardeRFin = []
    for i in range(0, len(frames2)):
        segundoGrupo=frames2[i].loc[frames2[i]['FIN']<=5]
        if segundoGrupo.empty:
            continue
        porcentaje = (len(segundoGrupo)*100)/len(frames2[i])
        indiceTardeRFin.append(porcentaje)

    tardeRFin=pd.DataFrame(data=indiceTardeRFin)
    tardeRFin.rename(columns={0:'REPROBACIÓN FINAL(%)'}, inplace=True)

    for i in range (0, len(tardeRFin)):
        tardeRFin.rename(index={i:int(pruebast[i])}, inplace=True)
    ########################################################################## Impresión dataframes
    pf = pd.concat([plantel, plantel2, plantel3, plantelFin, plantelR, plantelR2, plantelR3, plantelRFin], axis=1)
    pf
    st.subheader("INDICE DE APROBACIÓN Y REPROBACIÓN MATUTINO")
    df = pd.concat([mañana, mañanap2, mañanap3, mañanafin, mañanaR, mañanaR2, mañanaR3, mañanaRFin], axis=1)
    df
    st.subheader("INDICE DE APROBACIÓN Y REPROBRACIÓN VESPERTINO")
    dc = pd.concat([tarde, tardeP2, tardeP3, tardeFin, tardeR, tardeR2, tardeR3, tardeRFin], axis=1)
    dc
#FUNCION PRINCIPAL        
seguridad()
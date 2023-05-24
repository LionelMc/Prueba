import pandas as pd 
import numpy as np
from datetime import datetime
import missingno as msno 
import seaborn as sns
import matplotlib.pyplot as plt 
import streamlit as st
import folium
import streamlit as st
from streamlit_folium import folium_static


st.markdown('# Accidentes aéreos:')
st.markdown('***')

# Cargamos el Dataframe solo con esas columnas 
df = pd.read_csv('accidentes_data.csv')

# DF0: MOSTRAMOS LA DATA 
st.markdown('## Cargamos los datos')

if st.checkbox('Vista de datos:'):
    col1, col2, col3, col4 = st.columns(4)
    
    if col1.button('Mostrar Head'):
        st.write(df.head())
    if col2.button('Mostrar Sample'):
        st.write(df.sample(5))
    if col3.button('Mostrar Tail'):
        st.write(df.tail())
    if col4.button('Mostrar Data'):
        st.write(df)


# DF1: CANTIDAD DE ACCIDENTES POR AÑO
st.markdown('## Cantidad de accidentes por año')

# Convertir la columna "fecha" a formato de fecha
df['fecha'] = pd.to_datetime(df['fecha'])
# Crear las columnas "año" y "mes"
df['fecha_año'] = df['fecha'].dt.year
df['fecha_mes'] = df['fecha'].dt.month

df['muertos'] = df['all_aboard'].fillna(0)
# Obtener los años únicos
años_únicos = sorted(df['fecha_año'].unique())

# Obtener los años mínimo y máximo
año_min = min(años_únicos)
año_max = max(años_únicos)

# Permitir al usuario seleccionar el rango de años
años_seleccionados = st.slider('Rango de años', int(año_min), int(año_max), (int(año_min), int(año_max)))

# Filtrar los datos por el rango de años seleccionado
df_filtrado = df[(df['fecha_año'] >= años_seleccionados[0]) & (df['fecha_año'] <= años_seleccionados[1])]

# Contar la cantidad de accidentes por año filtrado
accidentes_por_año_filtrado = df_filtrado['fecha_año'].value_counts().sort_index()

# Obtener los tres años con mayor cantidad de accidentes
top_3_años = accidentes_por_año_filtrado.nlargest(3)

# Crear la figura y los ejes
fig, ax = plt.subplots(figsize=(15, 6))

# Crear el gráfico de línea
ax.plot(accidentes_por_año_filtrado.index, accidentes_por_año_filtrado.values)

# Configurar el eje x
ax.set_xticks(accidentes_por_año_filtrado.index[::5])

# Agregar etiquetas al gráfico para los tres años con mayor cantidad de accidentes
for i, (año, cantidad) in enumerate(top_3_años.items()):
    color = f'C{i}'
    ax.annotate(f'{cantidad} ({año})', xy=(año, cantidad), xytext=(año+1, cantidad+10), ha='left', va='center', fontsize=10, arrowprops=dict(facecolor=color, arrowstyle='wedge,tail_width=0.7', alpha=0.7, edgecolor='none'), bbox=dict(boxstyle='round,pad=0.3', fc=color, alpha=0.7))

# Configurar título y etiquetas de los ejes
ax.set_title('CANTIDAD DE ACCIDENTES POR AÑO', fontsize=18, fontweight='bold', color='black')
ax.set_xlabel('Año', fontsize=13, fontweight='normal')
ax.set_ylabel('Cantidad de accidentes', fontsize=13, fontweight='normal')

# Ajustar los límites del eje y para que las etiquetas queden dentro del gráfico
ax.set_ylim(0, accidentes_por_año_filtrado.max() * 1.2)

# Mostrar el gráfico en Streamlit
st.pyplot(fig)



# DF2: ACCIDENTES vs MUERTOS
st.markdown('## Accidentes vs Muertos')

# Crear la tabla dinámica con los datos filtrados
tabla = pd.pivot_table(df_filtrado, values=['fecha', 'muertos'], index='fecha_año', aggfunc={'fecha': 'count', 'muertos': 'sum'})

# Renombrar las columnas
tabla.columns = ['Accidentes', 'Muertos']

# Crear la figura con el tamaño deseado
fig, ax1 = plt.subplots(figsize=(15, 6))

# Crear el gráfico de línea para los accidentes
plt.title('ACCIDENTES vs MUERTOS', fontsize=18, fontweight='bold', color='black')
ax1.plot(tabla.index, tabla['Accidentes'], color='blue', label='Accidentes')
ax1.set_xlabel('Año', fontsize=13, fontweight='normal')
ax1.set_ylabel('Cantidad de accidentes', fontsize=13, fontweight='normal')
ax1.tick_params(axis='y', labelcolor='blue')

# Crear el segundo eje y para los muertos
ax2 = ax1.twinx()
ax2.plot(tabla.index, tabla['Muertos'], color='red', label='Muertos')
ax2.set_ylabel('Cantidad de muertos')
ax2.tick_params(axis='y', labelcolor='red')

# Agregar leyendas al gráfico
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

# Mostrar el gráfico en Streamlit
st.pyplot(fig)



# DF3: CANTIDAD DE ACCIDENTES POR MES & AERONAVE
st.markdown('## Accidentes: Mes & Aeronave')

# Filtrar los datos de la columna 'ac_type_clasif2'
clasif2 = ['Avión', 'Helicóptero', 'Dirigible', 'Hidroavión', 'Globo aerostático']
df1 = df_filtrado[df_filtrado['ac_type_clasif2'].isin(clasif2)]

# Crear las columnas "mes" y "año"
df1['mes'] = df1['fecha'].dt.strftime('%b').str.upper()

# Contar la cantidad de accidentes por mes y clasificación 2
accidentes_por_mes_y_clasif2 = df1.groupby(['mes', 'ac_type_clasif2'])['fecha'].count().reset_index(name='cantidad')

# Crear el DataFrame resumen
resumen = accidentes_por_mes_y_clasif2.pivot(index='mes', columns='ac_type_clasif2', values='cantidad').fillna(0)

# Ordenar el DataFrame resumen por la columna 'Subtotal'
resumen = resumen.sort_values(by=resumen.columns.tolist(), ascending=True)

# Verificar si hay datos para mostrar
if resumen.empty or resumen.sum().sum() == 0:
    st.write('No hay datos disponibles para el rango de años seleccionado.')
else:
    # Crear el gráfico de barras apiladas
    fig, ax = plt.subplots(figsize=(10, 6))
    grafico = resumen.plot(kind='barh', stacked=True, ax=ax)

    # Agregar etiquetas al gráfico
    ax.set_title('CANTIDAD DE ACCIDENTES POR MES & AERONAVE', fontsize=18, fontweight='bold', color='black')
    ax.set_xlabel('Cantidad de accidentes', fontsize=13, fontweight='normal')
    ax.set_ylabel('Mes', fontsize=13, fontweight='normal')

    # Cambiar el nombre de la leyenda de la columna 'ac_type_clasif2' a 'aeronave'
    handles, labels = grafico.get_legend_handles_labels()
    leyenda = ax.legend(handles, labels, title='Aeronave:')
    leyenda.get_title().set_weight('bold')

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)



# DF4: CANTIDAD DE ACCIDENTES POR MES & CONTINENTE
st.markdown('## Accidentes por Mes & Continente')

# Filtrar los datos de la columna 'Ruta_continente'
continentes = ['Americas', 'Europe', 'Asia', 'Africa', 'Oceania']
df1 = df_filtrado[df_filtrado['Ruta_continente'].isin(continentes)]

# Crear las columnas "mes" y "año"
df1['mes'] = df1['fecha'].dt.strftime('%b').str.upper()

# Contar la cantidad de accidentes por mes y continente
accidentes_por_mes_y_continente = df1.groupby(['mes', 'Ruta_continente'])['fecha'].count().reset_index(name='cantidad')

# Crear el DataFrame resumen
resumen = accidentes_por_mes_y_continente.pivot(index='mes', columns='Ruta_continente', values='cantidad').fillna(0)
resumen['Subtotal'] = resumen.sum(axis=1)

# Ordenar el DataFrame resumen por la columna 'Subtotal'
resumen = resumen.sort_values(by='Subtotal', ascending=True)

# Eliminar del DataFrame resumen la columna 'Subtotal'
resumen = resumen.drop('Subtotal', axis=1)

# Crear el gráfico de barras apiladas
fig, ax = plt.subplots(figsize=(10, 6))
grafico = resumen.plot(kind='barh', stacked=True, ax=ax)

# Agregar etiquetas al gráfico
ax.set_title('CANTIDAD DE ACCIDENTES POR MES & CONTINENTE', fontsize=18, fontweight='bold', color='black')
ax.set_xlabel('Cantidad de accidentes', fontsize=13, fontweight='normal')
ax.set_ylabel('Mes', fontsize=13, fontweight='normal')

# Cambiar el nombre de la leyenda de la columna 'Ruta_continente' a 'Continente'
handles, labels = grafico.get_legend_handles_labels()
labels = [label.replace('Americas', 'America') for label in labels]
leyenda = ax.legend(handles, labels, title='Continente:')
leyenda.get_title().set_weight('bold')

# Mostrar el gráfico en Streamlit
st.pyplot(fig)



# DF5: ACCIDENTES & MAPA
st.markdown('## Accidentes registrados en el Mapa')

def mostrar_mapa():
    # Obtener la cantidad de accidentes por país
    accidentes_por_pais = df['Ruta_pais'].value_counts()

    # Crear un diccionario que asocie cada país con sus coordenadas correspondientes
    coordenadas_por_pais = {}
    for index, row in df.iterrows():
        pais = row['Ruta_pais']
        lat = row['Ruta_lat']
        lon = row['Ruta_lon']
        if pais not in coordenadas_por_pais and not pd.isna(lat) and not pd.isna(lon):
            coordenadas_por_pais[pais] = (lat, lon)

    # Crear el mapa
    mapa = folium.Map(location=[20, 0], zoom_start=2)

    # Agregar los marcadores al mapa
    for pais, coordenadas in coordenadas_por_pais.items():
        freq = accidentes_por_pais[pais].astype(int)
        if freq > 0:
            freq_custom = freq / 30
            radius = freq_custom
            folium.CircleMarker(
                location=coordenadas,
                radius=radius,
                color='red',
                fill=True,
                fill_color='red',
                fill_opacity=0.7,
                tooltip=f'{pais}: {freq} accidentes'
            ).add_to(mapa)

    # Mostrar el mapa en Streamlit
    folium_static(mapa)

# Llamar a la función para mostrar el mapa en Streamlit
mostrar_mapa()


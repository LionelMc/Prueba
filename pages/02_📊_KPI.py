import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.markdown("# KPI's:")
st.markdown('***')

# Cargar los datos y convertir la columna "fecha" al tipo de dato fecha
df = pd.read_csv("accidentes_data.csv", parse_dates=['fecha'])

# Agregar el filtro de rango de años
year_range = st.slider('Rango de años:', min_value=int(df['fecha'].dt.year.min()), max_value=int(df['fecha'].dt.year.max()), value=(int(df['fecha'].dt.year.min()), int(df['fecha'].dt.year.max())))

# Filtrar el DataFrame según el rango de años seleccionado
df_filtered = df[(df['fecha'].dt.year >= year_range[0]) & (df['fecha'].dt.year <= year_range[1])]

# Calcular los resúmenes y gráficos utilizando df_filtered
resumen_anual = df_filtered.groupby(df_filtered['fecha'].dt.year).agg({'fecha': 'count', 'all_aboard': 'sum', 'cantidad de fallecidos': 'sum'}).rename(columns={'fecha': 'accidentes'}).reset_index()

# Calcular la tasa de mortalidad anual (%)
resumen_anual['tasa_mortalidad'] = (resumen_anual['cantidad de fallecidos'] / resumen_anual['all_aboard']) * 100

# Calcular la variación anual de la tasa de mortalidad (%)
resumen_anual['var_mortalidad'] = (resumen_anual['tasa_mortalidad'].diff(-1) / resumen_anual['tasa_mortalidad']) * 100

# Calcular el Índice de Supervivencia (IS)
resumen_anual['indice_supervivencia'] = (resumen_anual['all_aboard'] - resumen_anual['cantidad de fallecidos']) / resumen_anual['all_aboard'] * 100

# Calcular el Promedio de Fallecidos por Accidente (PFA)
resumen_anual['prom_fallecidos'] = resumen_anual['cantidad de fallecidos'] / resumen_anual['accidentes']

# Estilo personalizado para los gráficos
plt.style.use('seaborn-darkgrid')

# Crear una lista con los nombres de los KPIs
kpi_names = ['Promedio de Fallecidos', 'Índice de Supervivencia', 'Índice de mortalidad total', 'Reducción porcentual del índice de mortalidad']

# Recorrer la lista de nombres de KPIs y los datos resumidos correspondientes
for i, kpi_name in enumerate(kpi_names):
    st.markdown(f'### KPI {i+1}: {kpi_name}')
    if i == 0:
        # G1 - Gráfico de Líneas
        fig1, ax1 = plt.subplots(figsize=(15, 6))
        ax1.plot(resumen_anual['fecha'], round(resumen_anual['prom_fallecidos'], 2), color='blue', marker='o', markersize=6)
        ax1.axhline(y=30, color='red', linestyle='--', linewidth=2)
        ax1.set_xlabel('Año', fontsize=13, fontweight='bold')
        ax1.set_ylabel('Fallecidos', fontsize=13, fontweight='bold')
        ax1.set_title('Fallecidos por Accidente', fontsize=16, fontweight='bold')
        ax1.legend(['Prom_fallecidos', 'Objetivo < 30%'], fontsize=12, loc='lower left')
        avg_value = resumen_anual['prom_fallecidos'].mean()
        bbox_props = dict(boxstyle='round', facecolor='white', edgecolor='black', linewidth=1)
        ax1.text(0.95, 0.95, f'Promedio: {avg_value:.2f}', transform=ax1.transAxes, fontsize=11, verticalalignment='top', horizontalalignment='right', bbox=bbox_props)
        st.pyplot(fig1)
    elif i == 1:
        # G1 - Gráfico de Líneas
        fig2, ax2 = plt.subplots(figsize=(15, 6))
        ax2.plot(resumen_anual['fecha'], round(resumen_anual['indice_supervivencia'], 2), color='blue', marker='o', markersize=6)
        ax2.axhline(y=50, color='red', linestyle='--', linewidth=2)
        ax2.set_xlabel('Año', fontsize=13, fontweight='bold')
        ax2.set_ylabel('Índice de Supervivencia (%)', fontsize=13, fontweight='bold')
        ax2.set_title('Índice de Supervivencia por año', fontsize=16, fontweight='bold')
        ax2.legend(['Índice', 'Objetivo > 50%'], fontsize=12, loc='lower left')
        avg_value = resumen_anual['indice_supervivencia'].mean()
        bbox_props = dict(boxstyle='round', facecolor='white', edgecolor='black', linewidth=1)
        ax2.text(0.95, 0.95, f'Promedio: {avg_value:.2f}', transform=ax2.transAxes, fontsize=11, verticalalignment='top', horizontalalignment='right', bbox=bbox_props)
        st.pyplot(fig2)
    elif i == 2:
        # G2 - Gráfico de Área
        fig3, ax3 = plt.subplots(figsize=(12, 6))
        ax3.fill_between(resumen_anual['fecha'], 0, resumen_anual['tasa_mortalidad'], color='blue', alpha=0.4)
        ax3.axhline(y=65, color='red', linestyle='--', linewidth=2)
        ax3.set_xlabel('Año', fontsize=13, fontweight='bold')
        ax3.set_ylabel('Tasa de mortalidad (%)', fontsize=13, fontweight='bold')
        ax3.set_title('Indice de mortalidad total por año', fontsize=16, fontweight='bold')
        ax3.legend(['Índice', 'Objetivo < 65%'], fontsize=12, loc='lower left')
        avg_value = resumen_anual['tasa_mortalidad'].mean()
        bbox_props = dict(boxstyle='round', facecolor='white', edgecolor='black', linewidth=1)
        ax3.text(0.95, 0.95, f'Promedio: {avg_value:.2f}', transform=ax3.transAxes, fontsize=11, verticalalignment='top', horizontalalignment='right', bbox=bbox_props)
        st.pyplot(fig3)
    elif i == 3:
        # G3 - Gráfico de Líneas con Puntos
        fig4, ax4 = plt.subplots(figsize=(12, 6))
        ax4.plot(resumen_anual['fecha'], round(resumen_anual['var_mortalidad'], 2), color='blue', marker='o', markersize=6)
        ax4.axhline(y=5, color='red', linestyle='--', linewidth=2)
        ax4.set_xlabel('Año', fontsize=13, fontweight='bold')
        ax4.set_ylabel('Variación del índice de mortalidad total (%)', fontsize=13, fontweight='bold')
        ax4.set_title('Variación porcentual del índice de mortalidad total', fontsize=16, fontweight='bold')
        ax4.legend(['Variación del índice', 'Objetivo < 5%'], fontsize=12, loc='lower left')
        avg_value = resumen_anual['var_mortalidad'].mean()
        bbox_props = dict(boxstyle='round', facecolor='white', edgecolor='black', linewidth=1)
        ax4.text(0.95, 0.95, f'Promedio: {avg_value:.2f}', transform=ax4.transAxes, fontsize=11, verticalalignment='top', horizontalalignment='right', bbox=bbox_props)
        st.pyplot(fig4)



# ## OTRA OPCION:
# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt

# st.markdown("# KPI's:")
# st.markdown('***')

# # Cargar los datos y convertir la columna "fecha" al tipo de dato fecha
# df = pd.read_csv("accidentes_data.csv", parse_dates=['fecha'])

# # Agregar el filtro de rango de años
# year_range = st.slider('Rango de años:', min_value=int(df['fecha'].dt.year.min()), max_value=int(df['fecha'].dt.year.max()), value=(int(df['fecha'].dt.year.min()), int(df['fecha'].dt.year.max())))

# # Filtrar el DataFrame según el rango de años seleccionado
# df_filtered = df[(df['fecha'].dt.year >= year_range[0]) & (df['fecha'].dt.year <= year_range[1])]

# # Calcular los resúmenes y gráficos utilizando df_filtered
# resumen_anual = df_filtered.groupby(df_filtered['fecha'].dt.year).agg({'fecha': 'count', 'all_aboard': 'sum', 'cantidad de fallecidos': 'sum'}).rename(columns={'fecha': 'accidentes'}).reset_index()

# # Calcular la tasa de mortalidad anual (%)
# resumen_anual['tasa_mortalidad'] = (resumen_anual['cantidad de fallecidos'] / resumen_anual['all_aboard']) * 100

# # Calcular la variación anual de la tasa de mortalidad (%)
# resumen_anual['var_mortalidad'] = (resumen_anual['tasa_mortalidad'].diff(-1) / resumen_anual['tasa_mortalidad']) * 100

# # Calcular el Índice de Supervivencia (IS)
# resumen_anual['indice_supervivencia'] = (resumen_anual['all_aboard'] - resumen_anual['cantidad de fallecidos']) / resumen_anual['all_aboard'] * 100

# # Calcular el Promedio de Fallecidos por Accidente (PFA)
# resumen_anual['prom_fallecidos'] = resumen_anual['cantidad de fallecidos'] / resumen_anual['accidentes']

# # Estilo personalizado para los gráficos
# plt.style.use('seaborn-darkgrid')

# # Crear una figura y ejes para los subgráficos de 2x2
# fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))

# # Recorrer los ejes de los subgráficos
# for ax in axes.flatten():
#     ax.set_xlabel('Año', fontsize=10, fontweight='bold')

# # Gráfico 1: Promedio de Fallecidos
# axes[0, 0].set_title('KPI 1: Promedio de Fallecidos')
# axes[0, 0].plot(resumen_anual['fecha'], round(resumen_anual['prom_fallecidos'], 2), color='blue', marker='o', markersize=6)
# axes[0, 0].axhline(y=30, color='red', linestyle='--', linewidth=2)
# axes[0, 0].set_ylabel('Fallecidos', fontsize=10, fontweight='bold')
# axes[0, 0].legend(['Prom_fallecidos', 'Objetivo < 30%'], fontsize=8, loc='lower left')

# # Gráfico 2: Índice de Supervivencia
# axes[0, 1].set_title('KPI 2: Índice de Supervivencia')
# axes[0, 1].plot(resumen_anual['fecha'], round(resumen_anual['indice_supervivencia'], 2), color='blue', marker='o', markersize=6)
# axes[0, 1].axhline(y=50, color='red', linestyle='--', linewidth=2)
# axes[0, 1].set_ylabel('Índice de Supervivencia (%)', fontsize=10, fontweight='bold')
# axes[0, 1].legend(['Índice', 'Objetivo > 50%'], fontsize=8, loc='lower left')

# # Gráfico 3: Tasa de Mortalidad
# axes[1, 0].set_title('KPI 3: Tasa de Mortalidad')
# axes[1, 0].fill_between(resumen_anual['fecha'], 0, resumen_anual['tasa_mortalidad'], color='blue', alpha=0.4)
# axes[1, 0].axhline(y=65, color='red', linestyle='--', linewidth=2)
# axes[1, 0].set_xlabel('Año', fontsize=10, fontweight='bold')
# axes[1, 0].set_ylabel('Tasa de mortalidad (%)', fontsize=10, fontweight='bold')
# axes[1, 0].legend(['Índice', 'Objetivo < 65%'], fontsize=8, loc='lower left')

# # Gráfico 4: Variación de la Tasa de Mortalidad
# axes[1, 1].set_title('KPI 4: Variación de la Tasa de Mortalidad')
# axes[1, 1].plot(resumen_anual['fecha'], round(resumen_anual['var_mortalidad'], 2), color='blue', marker='o', markersize=6)
# axes[1, 1].axhline(y=5, color='red', linestyle='--', linewidth=2)
# axes[1, 1].set_xlabel('Año', fontsize=10, fontweight='bold')
# axes[1, 1].set_ylabel('Variación del índice de mortalidad total (%)', fontsize=10, fontweight='bold')
# axes[1, 1].legend(['Variación del índice', 'Objetivo < 5%'], fontsize=8, loc='lower left')

# # Ajustar el espaciado entre los subgráficos
# plt.tight_layout()

# # Mostrar la figura con los subgráficos
# st.pyplot(fig)

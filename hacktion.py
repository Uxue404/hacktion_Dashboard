import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts

# Cargar datos
file_path = 'Salary_Data.csv'
data = pd.read_csv(file_path)

st.title('Análisis de Datos de Salarios')

# Mostrar datos
st.subheader('Datos')
st.write(data)

# Filtros interactivos
st.sidebar.subheader('Filtros')
gender_filter = st.sidebar.multiselect('Filtrar por Género', options=data['Gender'].unique(), default=data['Gender'].unique())
education_filter = st.sidebar.multiselect('Filtrar por Nivel de Educación', options=data['Education Level'].unique(), default=data['Education Level'].unique())

filtered_data = data[(data['Gender'].isin(gender_filter)) & (data['Education Level'].isin(education_filter))]

# Visualización del Género
st.subheader('Distribución por Género')
gender_counts = filtered_data['Gender'].value_counts().to_dict()
gender_options = {
    "tooltip": {"trigger": "item"},
    "series": [{
        "type": "pie",
        "radius": "50%",
        "data": [{"value": v, "name": k} for k, v in gender_counts.items()],
    }]
}
st_echarts(gender_options)

# Visualización del Nivel de Educación
st.subheader('Distribución por Nivel de Educación')
education_counts = filtered_data['Education Level'].value_counts().to_dict()
education_options = {
    "tooltip": {"trigger": "item"},
    "series": [{
        "type": "pie",
        "radius": "50%",
        "data": [{"value": v, "name": k} for k, v in education_counts.items()],
    }]
}
st_echarts(education_options)

# Comparativa de Salario y Años de Experiencia por Género
st.subheader('Salario vs Años de Experiencia por Género')
salary_experience_options = {
    "xAxis": {"type": "category", "data": filtered_data['Years of Experience'].tolist()},
    "yAxis": {"type": "value"},
    "series": [
        {
            "data": filtered_data['Salary'].tolist(),
            "type": "scatter",
        }
    ],
    "tooltip": {"trigger": "axis"},
}
st_echarts(salary_experience_options)

# Comparativa de Salario por Nivel de Educación
st.subheader('Salario por Nivel de Educación')
salary_education_options = {
    "xAxis": {"type": "category", "data": filtered_data['Education Level'].unique().tolist()},
    "yAxis": {"type": "value"},
    "series": [
        {
            "data": filtered_data.groupby('Education Level')['Salary'].mean().tolist(),
            "type": "bar",
        }
    ],
    "tooltip": {"trigger": "axis"},
}
st_echarts(salary_education_options)

# Comparativa de Años de Experiencia por Nivel de Educación
st.subheader('Años de Experiencia por Nivel de Educación')
experience_education_options = {
    "xAxis": {"type": "category", "data": filtered_data['Education Level'].unique().tolist()},
    "yAxis": {"type": "value"},
    "series": [
        {
            "data": filtered_data.groupby('Education Level')['Years of Experience'].mean().tolist(),
            "type": "bar",
        }
    ],
    "tooltip": {"trigger": "axis"},
}
st_echarts(experience_education_options)

# Otros componentes interactivos
st.subheader('Interacción Adicional')
if st.button('Actualizar Datos'):
    st.write('Datos actualizados!')

selected_gender = st.radio('Selecciona Género:', ['Todos'] + list(data['Gender'].unique()))
if selected_gender != 'Todos':
    filtered_data = data[data['Gender'] == selected_gender]
    st.write(f'Mostrando datos para {selected_gender}')
    st.write(filtered_data)

selected_education = st.selectbox('Selecciona Nivel de Educación', ['Todos'] + list(data['Education Level'].unique()))
if selected_education != 'Todos':
    filtered_data = data[data['Education Level'] == selected_education]
    st.write(f'Mostrando datos para {selected_education}')
    st.write(filtered_data)

age_range = st.slider('Rango de Edad', min_value=int(data['Age'].min()), max_value=int(data['Age'].max()), value=(int(data['Age'].min()), int(data['Age'].max())))
filtered_data = data[(data['Age'] >= age_range[0]) & (data['Age'] <= age_range[1])]
st.write(f'Mostrando datos para edades entre {age_range[0]} y {age_range[1]}')
st.write(filtered_data)

# Descargar datos filtrados
st.download_button('Descargar Datos Filtrados', filtered_data.to_csv(index=False).encode('utf-8'), file_name='filtered_data.csv', mime='text/csv')

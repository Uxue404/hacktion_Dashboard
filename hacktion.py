import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos
file_path = 'Salary_Data.csv'
data = pd.read_csv(file_path)

st.title('Análisis de Datos de Salarios')

# Mostrar datos con data editor
st.subheader('Datos')
st.data_editor('Edita los datos aquí:', data)

# Filtros interactivos
st.sidebar.subheader('Filtros')
gender_filter = st.sidebar.multiselect('Filtrar por Género', options=data['Gender'].unique(), default=data['Gender'].unique())
education_filter = st.sidebar.multiselect('Filtrar por Nivel de Educación', options=data['Education Level'].unique(), default=data['Education Level'].unique())

filtered_data = data[(data['Gender'].isin(gender_filter)) & (data['Education Level'].isin(education_filter))]

# Visualización del Género
st.subheader('Distribución por Género')
fig, ax = plt.subplots()
sns.countplot(data=filtered_data, x='Gender', ax=ax)
st.pyplot(fig)

# Visualización del Nivel de Educación
st.subheader('Distribución por Nivel de Educación')
fig, ax = plt.subplots()
sns.countplot(data=filtered_data, x='Education Level', ax=ax)
st.pyplot(fig)

# Comparativa de Salario y Años de Experiencia por Género
st.subheader('Salario vs Años de Experiencia por Género')
fig, ax = plt.subplots()
sns.scatterplot(data=filtered_data, x='Years of Experience', y='Salary', hue='Gender', ax=ax)
st.pyplot(fig)

# Comparativa de Salario por Nivel de Educación
st.subheader('Salario por Nivel de Educación')
fig, ax = plt.subplots()
sns.boxplot(data=filtered_data, x='Education Level', y='Salary', ax=ax)
st.pyplot(fig)

# Comparativa de Años de Experiencia por Nivel de Educación
st.subheader('Años de Experiencia por Nivel de Educación')
fig, ax = plt.subplots()
sns.boxplot(data=filtered_data, x='Education Level', y='Years of Experience', ax=ax)
st.pyplot(fig)

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

# Color Picker
st.color_picker('Elige un color para la aplicación')

# Mostrar entrada de texto
st.text_input('Introduce algún texto aquí')
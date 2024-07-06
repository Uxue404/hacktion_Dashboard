import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos
file_path = 'Salary_Data.csv'
data = pd.read_csv(file_path)

st.title('Análisis de Datos de Salarios')

# Mostrar datos
st.subheader('Datos')
st.write(data)

# Visualización del Género
st.subheader('Distribución por Género')
fig, ax = plt.subplots()
sns.countplot(data=data, x='Gender', ax=ax)
st.pyplot(fig)

# Visualización del Nivel de Educación
st.subheader('Distribución por Nivel de Educación')
fig, ax = plt.subplots()
sns.countplot(data=data, x='Education Level', ax=ax)
st.pyplot(fig)

# Comparativa de Salario y Años de Experiencia por Género
st.subheader('Salario vs Años de Experiencia por Género')
fig, ax = plt.subplots()
sns.scatterplot(data=data, x='Years of Experience', y='Salary', hue='Gender', ax=ax)
st.pyplot(fig)

# Comparativa de Salario por Nivel de Educación
st.subheader('Salario por Nivel de Educación')
fig, ax = plt.subplots()
sns.boxplot(data=data, x='Education Level', y='Salary', ax=ax)
st.pyplot(fig)

# Comparativa de Años de Experiencia por Nivel de Educación
st.subheader('Años de Experiencia por Nivel de Educación')
fig, ax = plt.subplots()
sns.boxplot(data=data, x='Education Level', y='Years of Experience', ax=ax)
st.pyplot(fig)
import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts
import anthropic
#import fitz  # Biblioteca PyMuPDF para PDFs

# Sidebar para ingresar la clave de la API de Anthropic
with st.sidebar:
    anthropic_api_key = st.text_input("Anthropic API Key", key="anthropic_api_key", type="password")

# Título de la aplicación
st.title("Análisis de Datos de Salarios y Preguntas sobre Archivos")
st.write("Empieza a explorar y hacer preguntas...")

# Cargador de archivos
uploaded_file = st.file_uploader("Sube un archivo.", type=("txt", "md", "pdf", "csv"))

# Mostrar resumen de análisis de datos de salarios
if uploaded_file:
    st.subheader('Resumen de Análisis de Datos de Salarios')

    # Cargar datos dependiendo del tipo de archivo
    if uploaded_file.type == "text/csv":
        data = pd.read_csv(uploaded_file)
    elif uploaded_file.type == "application/pdf":
        pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        article = ""
        for page in pdf_doc:
            article += page.get_text()
        data = pd.DataFrame({'Text': [article]})
    else:
        data = pd.DataFrame({'Text': [uploaded_file.read().decode()]})

    # Limpiar datos: eliminar filas con valores NaN
    data = data.dropna()

    # Mostrar datos
    st.subheader('Datos del Archivo Cargado')
    st.write(data)

    # Filtros interactivos
    st.sidebar.subheader('Filtros para Análisis de Salarios')
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
            "radius": "60%",
            "data": [{"value": v, "name": k} for k, v in gender_counts.items()],
        }]
    }
    st_echarts(gender_options)

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

# Verificación de la clave de la API y archivos subidos para preguntas y respuestas
if uploaded_file and anthropic_api_key:
    question = st.text_input("Hazme una pregunta sobre el contenido del archivo.", "")

    if question:
        # Formatear el prompt para la API de Anthropic
        prompt = f"""{anthropic.HUMAN_PROMPT} Here's an article:\n\n<article>
        {data.to_string()}\n\n</article>\n\n{question}{anthropic.AI_PROMPT}"""

        # Llamar a la API de Anthropic
        client = anthropic.Client(api_key=anthropic_api_key)
        response = client.completions.create(
            prompt=prompt,
            stop_sequences=[anthropic.HUMAN_PROMPT],
            model="claude-2",
            max_tokens_to_sample=300,
        )

        # Mostrar la respuesta en la aplicación
        st.subheader("Respuesta a tu Pregunta")
        st.write(response.completion)
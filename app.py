import streamlit as st
import requests
import json

# Configuración de la página
st.set_page_config(page_title="Evaluación de Riesgo Crediticio", page_icon="💳", layout="wide")

# Título de la aplicación
st.title("Evaluación de Riesgo Crediticio utilizando IA")

# Instrucciones para el usuario
st.markdown("""
Esta aplicación evalúa el riesgo crediticio basado en varios criterios utilizando modelos de inteligencia artificial. Completa el formulario a continuación y obtén una evaluación del riesgo.
""")

# Ocultar API keys en los secrets de Streamlit
TOGETHER_API_KEY = st.secrets.get("TOGETHER_API_KEY")

# Función para hacer la solicitud a la API de Together
def evaluar_riesgo_crediticio(historial_credito, ingresos_mensuales, deudas_actuales, activos, dependientes, edad, comportamiento_financiero):
    # Crear el prompt basado en la entrada del usuario
    prompt = f"""
    Evaluar el riesgo crediticio de una persona con las siguientes características:

    - Historial de crédito: {historial_credito}
    - Ingresos mensuales: Q{ingresos_mensuales}
    - Deudas actuales: Q{deudas_actuales}
    - Activos: {activos}
    - Dependientes: {dependientes}
    - Edad: {edad} años
    - Comportamiento financiero: {comportamiento_financiero}

    Proporciona un análisis detallado de la probabilidad de que la persona cumpla con sus obligaciones crediticias, junto con recomendaciones para mejorar su perfil crediticio.
    """

    # Configuración de la solicitud a la API de Together
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        'Authorization': f'Bearer {TOGETHER_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2512,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "stop": ["<|eot_id|>"],
        "stream": False
    })

    # Hacer la solicitud POST
    response = requests.post(url, headers=headers, data=payload)

    # Procesar la respuesta
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "Error al procesar la solicitud. Por favor, inténtalo de nuevo."

# Crear el formulario para la entrada del usuario
st.header("Por favor, ingresa la siguiente información:")

# Entrada para el historial de crédito
historial_credito = st.selectbox("Historial de crédito", ["Excelente", "Bueno", "Regular", "Malo"])

# Entrada para los ingresos mensuales
ingresos_mensuales = st.number_input("Ingresos mensuales (Q)", min_value=0, value=10000, step=1000)

# Entrada para las deudas actuales
deudas_actuales = st.number_input("Deudas actuales (Q)", min_value=0, value=5000, step=1000)

# Entrada para los activos
activos = st.text_input("Activos (Ej. Propiedades, vehículos, cuentas de ahorro, etc.)")

# Entrada para los dependientes
dependientes = st.number_input("Número de dependientes", min_value=0, value=0, step=1)

# Entrada para la edad
edad = st.number_input("Edad", min_value=18, max_value=100, value=30)

# Entrada para el comportamiento financiero
comportamiento_financiero = st.text_area("Comportamiento financiero (Ej. Historial de pagos, bancarrotas, uso de crédito, etc.)")

# Botón para obtener la evaluación
if st.button("Evaluar riesgo crediticio"):
    with st.spinner("Evaluando el riesgo crediticio..."):
        resultado = evaluar_riesgo_crediticio(historial_credito, ingresos_mensuales, deudas_actuales, activos, dependientes, edad, comportamiento_financiero)
        st.success("Evaluación completada:")
        st.write(resultado)

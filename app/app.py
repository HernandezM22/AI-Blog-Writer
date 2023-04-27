import streamlit as st
import src.nlp_functions as nlp
import openai
from core.settings import settings

api_key = settings.OPENAI_API_KEY
openai.api_key = api_key

st.image("app/resources/images/logo.png")
st.title("Escritor de blogs con AI")

st.subheader("Etapa 1: Generación de prompts")

lang = st.radio(
    label="Idiomas disponibles",
    options=["English", "Español"]
)

st.subheader("Escribe una palabra clave en el idioma seleccionado")

keyword = st.text_input(
    label="Puede ser la que sea, pero escribe solo una. De preferencia un sustantivo o verbo conciso. Presiona enter cuando termines.",
    value="",
    key="keyword",
    help="Palabra clave que será usada para generar ideas de temas"
)

generate = st.button(
    label="Generar ideas",
    key="generate"
)

output_container = st.empty()

if "questions" not in st.session_state:
    st.session_state.questions = []

if generate:
    if lang == "English":
        st.session_state["questions"] = nlp.generate_prompts_from_word_en(keyword)
    elif lang == "Español":
        st.session_state["questions"] = nlp.generate_prompts_from_word_es(keyword)

if st.session_state["questions"]:
    st.write("Ideas generadas:")
    st.write(st.session_state["questions"])


st.subheader("Etapa 2: Generación de blogs")

prompt = st.text_input(
    label="Copia y pega uno de los prompts generados o introduce uno tu. (En el idioma seleccionado). Presiona enter cuando termines.",
    value="",
    key="Prompt",
    help="Pregunta que responderá el blog"
)

blog_generate = st.button(
    label="Generar blog"
)

if blog_generate:
    with st.spinner("Espera mientras se escribe el blog..."):
        if lang == "English":
            st.write(nlp.write_blogpost_from_prompt_en(prompt))
        elif lang == "Español":
            st.write(nlp.write_blogpost_from_prompt_es(prompt))
    st.success("Listo!")


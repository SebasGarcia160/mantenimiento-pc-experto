import streamlit as st
import json
import os

# configuracion inicial de la ventana del navegador
st.set_page_config(page_title="Asistente técnico maestro", page_icon="💻", layout="wide")

def cargar_conocimiento():
    # revisa si el archivo con las reglas de diagnostico existe en la carpeta
    if os.path.exists('conocimiento.json'):
        # abre el archivo con codificacion utf8 para evitar errores con tildes
        with open('conocimiento.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    # si el archivo no esta devuelve nada para activar la alerta de error
    return None

def main():
    # diseño de la cabecera usando html para centrar el titulo y dar color
    st.markdown("<h1 style='text-align: center; color: #0077B6; font-size: 50px;'>💻 Core-diagnostic pro</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: ##FFFFFF;'>Asistente de diagnóstico preventivo y correctivo para equipos de computo </h3>", unsafe_allow_html=True)
    st.divider()

    # intenta obtener los datos del archivo json
    datos = cargar_conocimiento()
    if not datos:
        st.error("error crítico: no se encontró la base de conocimiento.")
        return

    # bloque para mostrar las categorias de evaluacion
    st.subheader("1️⃣ Areas de evaluación técnica")
    descripciones = datos.get('descripciones_categorias', {})
    # extrae las categorias unicas de las reglas y las ordena
    categorias = sorted(list(set(r['categoria'] for r in datos['reglas'])))
    
    # crea columnas dinamicas segun la cantidad de categorias encontradas
    cols = st.columns(len(categorias))
    for i, cat in enumerate(categorias):
        with cols[i]:
            with st.container(border=True):
                st.markdown(f"**{cat}**")
                # muestra la descripcion breve de cada area
                st.caption(descripciones.get(cat, ""))

    # selector principal para que el usuario elija que quiere revisar
    cat_sel = st.selectbox("\n¿Cuál área desea diagnosticar?", [" seleccione una opción "] + categorias)

    # seccion de preguntas basada en la categoria seleccionada
    if cat_sel != " seleccione una opción ":
        st.divider()
        st.subheader(f"2️⃣ Análisis de síntomas detectados en: {cat_sel}")
        
        # filtra solo las reglas que pertenecen a la categoria elegida
        reglas_evaluar = [r for r in datos['reglas'] if r['categoria'] == cat_sel]
        # obtiene la lista de todos los sintomas posibles para esas reglas
        sintomas_relevantes = sorted(list(set(s for r in reglas_evaluar for s in r['sintomas'])))
        diccionario = datos.get('diccionario_sintomas', {})
        
        # formulario para agrupar las respuestas del usuario
        with st.form("form_diagnostico"):
            st.write("Seleccione los comportamientos inusuales que observa en su equipo:")
            respuestas = {}
            
            # organiza los sintomas en filas de 4 columnas para que se vea limpio
            for i in range(0, len(sintomas_relevantes), 4):
                cols_q = st.columns(4)
                for j in range(4):
                    if i + j < len(sintomas_relevantes):
                        s_key = sintomas_relevantes[i + j]
                        with cols_q[j]:
                            # guarda el estado (marcado o no) de cada sintoma
                            respuestas[s_key] = st.checkbox(diccionario.get(s_key, s_key), key=s_key)
            
            st.write("")
            submit = st.form_submit_button("🔍 Analizar y generar informe")

        # logica del motor de inferencia al enviar el formulario
        if submit:
            # crea una lista solo con los sintomas que el usuario marco
            hechos_usuario = [s for s, marcado in respuestas.items() if marcado]
            st.divider()
            
            if not hechos_usuario:
                st.warning("Debe seleccionar al menos un síntoma para que el sistema experto pueda inferir un resultado.")
            else:
                hallazgos = 0
                # recorre cada regla para ver si coincide con los sintomas del usuario
                for regla in reglas_evaluar:
                    sintomas_regla = set(regla['Sintomas'])
                    # encuentra la interseccion entre sintomas de la regla y los del usuario
                    coincidencias = sintomas_regla.intersection(set(hechos_usuario))
                    
                    if len(coincidencias) > 0:
                        hallazgos += 1
                        # calcula el porcentaje de certeza segun cuantos sintomas coinciden del total de la regla
                        certeza = int((len(coincidencias) / len(sintomas_regla)) * 100)
                        
                        # muestra el resultado del hallazgo con formato de error (rojo)
                        st.error(f"### 📍 Hallazgo técnico: {regla['falla'].upper()}")
                        st.write(f"**Confianza del diagnóstico:** {certeza}%")
                        st.progress(certeza / 100)
                        
                        # muestra la solucion sugerida
                        st.info(f"**🛠️ Acciones de mantenimiento:** {regla['accion']}")
                        
                        # explica por que el sistema llego a esa conclusion
                        with st.expander("Justificación del motor de inferencia"):
                            st.write(f"El sistema ha identificado patrones de falla basados en {len(coincidencias)} síntomas confirmados por el usuario.")
                            st.write(f"Indicadores analizados: {', '.join(list(coincidencias)).replace('_', ' ')}.")
                        st.write("---")
                
                # mensaje final decorativo
                st.success("Diagnóstico finalizado. se recomienda aplicar las acciones preventivas para evitar daños irreversibles.")
                st.balloons()
    else:
        # mensaje informativo que aparece antes de seleccionar una opcion
        st.divider()
        st.info("💡 Dato del experto: el mantenimiento preventivo regular puede ahorrarle hasta un 70% en costos de reparación a largo plazo.")

# punto de entrada para ejecutar la aplicacion
if __name__ == "__main__":
    main()
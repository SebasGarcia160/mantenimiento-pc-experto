import streamlit as st
import json
import os

# configuracion de la pagina de streamlit
st.set_page_config(page_title="Asistente Técnico Maestro", page_icon="💻", layout="wide")

def cargar_conocimiento():
    # verifica si el archivo json existe en el directorio
    if os.path.exists('conocimiento.json'):
        # abre el archivo con soporte para caracteres especiales
        with open('conocimiento.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def main():
    # renderizado del encabezado con estilos css
    st.markdown("<h1 style='text-align: center; color: #0077B6; font-size: 50px;'>💻 Core-Diagnostic Pro</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: ##FFFFFF;'>Asistente de diagnóstico preventivo y correctivo para equipos de computo </h3>", unsafe_allow_html=True)
    st.divider()

    # carga de la base de datos
    datos = cargar_conocimiento()
    if not datos:
        st.error("Error crítico: No se encontró la base de conocimiento.")
        return

    #  paso 1: áreas de evaluación 
    st.subheader("1️⃣ Áreas de Evaluación Técnica")
    descripciones = datos.get('descripciones_categorias', {})
    # extraccion de categorias unicas desde la lista de reglas
    categorias = sorted(list(set(r['categoria'] for r in datos['reglas'])))
    
    # despliegue visual de las categorias en columnas
    cols = st.columns(len(categorias))
    for i, cat in enumerate(categorias):
        with cols[i]:
            with st.container(border=True):
                st.markdown(f"**{cat}**")
                st.caption(descripciones.get(cat, ""))

    # menu de seleccion para el usuario
    cat_sel = st.selectbox("\n¿Cuál área desea diagnosticar?", ["-- Seleccione una opción --"] + categorias)

    # paso 2: cuestionario de 8 síntomas
    if cat_sel != "-- Seleccione una opción --":
        st.divider()
        st.subheader(f"2️⃣ Análisis de Síntomas Detectados en: {cat_sel}")
        
        # filtrado de reglas por la categoria seleccionada
        reglas_evaluar = [r for r in datos['reglas'] if r['categoria'] == cat_sel]
        # recopilacion de todos los sintomas posibles de esas reglas
        sintomas_relevantes = sorted(list(set(s for r in reglas_evaluar for s in r['sintomas'])))
        diccionario = datos.get('diccionario_sintomas', {})
        
        # inicio del formulario de diagnostico
        with st.form("form_diagnostico"):
            st.write("Seleccione los comportamientos inusuales que observa en su equipo:")
            respuestas = {}
            
            # distribucion de los sintomas en una rejilla de 4 columnas
            for i in range(0, len(sintomas_relevantes), 4):
                cols_q = st.columns(4)
                for j in range(4):
                    if i + j < len(sintomas_relevantes):
                        s_key = sintomas_relevantes[i + j]
                        with cols_q[j]:
                            # creacion de checkbox para cada sintoma usando el diccionario
                            respuestas[s_key] = st.checkbox(diccionario.get(s_key, s_key), key=s_key)
            
            st.write("")
            submit = st.form_submit_button("🔍 ANALIZAR Y GENERAR INFORME")

        # paso 3: motor de inferencia con nivel de confianza
        if submit:
            # identificacion de los sintomas seleccionados por el usuario
            hechos_usuario = [s for s, marcado in respuestas.items() if marcado]
            st.divider()
            
            if not hechos_usuario:
                st.warning("Debe seleccionar al menos un síntoma para que el sistema experto pueda inferir un resultado.")
            else:
                hallazgos = 0
                # evaluacion de cada regla contra los sintomas marcados
                for regla in reglas_evaluar:
                    sintomas_regla = set(regla['sintomas'])
                    # calculo de coincidencia entre conjuntos
                    coincidencias = sintomas_regla.intersection(set(hechos_usuario))
                    
                    if len(coincidencias) > 0:
                        hallazgos += 1
                        # calculo matematico del porcentaje de certeza
                        certeza = int((len(coincidencias) / len(sintomas_regla)) * 100)
                        
                        # muestra de los resultados de la falla
                        st.error(f"### 📍 HALLAZGO TÉCNICO: {regla['falla'].upper()}")
                        st.write(f"**Confianza del Diagnóstico:** {certeza}%")
                        st.progress(certeza / 100)
                        
                        # muestra de la accion recomendada
                        st.info(f"**🛠️ Acciones de Mantenimiento:** {regla['accion']}")
                        
                        # despliegue de la justificacion tecnica de la inferencia
                        with st.expander("Justificación del Motor de Inferencia"):
                            st.write(f"El sistema ha identificado patrones de falla basados en {len(coincidencias)} síntomas confirmados por el usuario.")
                            st.write(f"Indicadores analizados: {', '.join(list(coincidencias)).replace('_', ' ')}.")
                        st.write("---")
                
                # mensaje final tras procesar todas las reglas
                st.success("Diagnóstico finalizado. Se recomienda aplicar las acciones preventivas para evitar daños irreversibles.")
                st.balloons()
    else:
        # mensaje informativo por defecto
        st.divider()
        st.info("💡 **Dato del Experto:** El mantenimiento preventivo regular puede ahorrarle hasta un 70% en costos de reparación a largo plazo.")

# ejecucion del script principal
if __name__ == "__main__":
    main()
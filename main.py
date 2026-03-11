import streamlit as st
import json
import os

st.set_page_config(page_title="Asistente Técnico Maestro", page_icon="💻", layout="wide")

def cargar_conocimiento():
    if os.path.exists('conocimiento.json'):
        with open('conocimiento.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def main():
    st.markdown("<h1 style='text-align: center; color: #0077B6; font-size: 50px;'>💻 Sistema de soporte - Equipos de computo</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: ##FFFFFF;'>Asistente de Diagnóstico Preventivo y Correctivo</h3>", unsafe_allow_html=True)
    st.divider()

    datos = cargar_conocimiento()
    if not datos:
        st.error("Error crítico: No se encontró la base de conocimiento.")
        return

    # --- PASO 1: ÁREAS DE EVALUACIÓN ---
    st.subheader("1️⃣ Áreas de Evaluación Técnica")
    descripciones = datos.get('descripciones_categorias', {})
    categorias = sorted(list(set(r['categoria'] for r in datos['reglas'])))
    
    cols = st.columns(len(categorias))
    for i, cat in enumerate(categorias):
        with cols[i]:
            with st.container(border=True):
                st.markdown(f"**{cat}**")
                st.caption(descripciones.get(cat, ""))

    cat_sel = st.selectbox("\n¿Cuál área desea diagnosticar?", ["-- Seleccione una opción --"] + categorias)

    # --- PASO 2: CUESTIONARIO DE 8 SÍNTOMAS ---
    if cat_sel != "-- Seleccione una opción --":
        st.divider()
        st.subheader(f"2️⃣ Análisis de Síntomas Detectados en: {cat_sel}")
        
        reglas_evaluar = [r for r in datos['reglas'] if r['categoria'] == cat_sel]
        sintomas_relevantes = sorted(list(set(s for r in reglas_evaluar for s in r['sintomas'])))
        diccionario = datos.get('diccionario_sintomas', {})
        
        with st.form("form_diagnostico"):
            st.write("Seleccione los comportamientos inusuales que observa en su equipo:")
            respuestas = {}
            
            # Rejilla de 4 columnas para los 8 síntomas (2 filas de 4)
            for i in range(0, len(sintomas_relevantes), 4):
                cols_q = st.columns(4)
                for j in range(4):
                    if i + j < len(sintomas_relevantes):
                        s_key = sintomas_relevantes[i + j]
                        with cols_q[j]:
                            respuestas[s_key] = st.checkbox(diccionario.get(s_key, s_key), key=s_key)
            
            st.write("")
            submit = st.form_submit_button("🔍 ANALIZAR Y GENERAR INFORME")

        # --- PASO 3: MOTOR DE INFERENCIA CON NIVEL DE CONFIANZA ---
        if submit:
            hechos_usuario = [s for s, marcado in respuestas.items() if marcado]
            st.divider()
            
            if not hechos_usuario:
                st.warning("Debe seleccionar al menos un síntoma para que el sistema experto pueda inferir un resultado.")
            else:
                hallazgos = 0
                for regla in reglas_evaluar:
                    sintomas_regla = set(regla['sintomas'])
                    coincidencias = sintomas_regla.intersection(set(hechos_usuario))
                    
                    if len(coincidencias) > 0:
                        hallazgos += 1
                        certeza = int((len(coincidencias) / len(sintomas_regla)) * 100)
                        
                        st.error(f"### 📍 HALLAZGO TÉCNICO: {regla['falla'].upper()}")
                        st.write(f"**Confianza del Diagnóstico:** {certeza}%")
                        st.progress(certeza / 100)
                        
                        st.info(f"**🛠️ Acciones de Mantenimiento:** {regla['accion']}")
                        
                        with st.expander("Justificación del Motor de Inferencia"):
                            st.write(f"El sistema ha identificado patrones de falla basados en {len(coincidencias)} síntomas confirmados por el usuario.")
                            st.write(f"Indicadores analizados: {', '.join(list(coincidencias)).replace('_', ' ')}.")
                        st.write("---")
                
                st.success("Diagnóstico finalizado. Se recomienda aplicar las acciones preventivas para evitar daños irreversibles.")
                st.balloons()
    else:
        st.divider()
        st.info("💡 **Dato del Experto:** El mantenimiento preventivo regular puede ahorrarle hasta un 70% en costos de reparación a largo plazo.")

if __name__ == "__main__":
    main()
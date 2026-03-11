import streamlit as st
import json
import os

st.set_page_config(page_title="Asistente Técnico Pro", page_icon="💻", layout="wide")

def cargar_conocimiento():
    if os.path.exists('conocimiento.json'):
        with open('conocimiento.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def main():
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>💻 SISTEMA EXPERTO PARA EQUIPOS DE CÓMPUTO</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #4B5563;'>Diagnóstico Inteligente y Prevención de Fallas</h3>", unsafe_allow_html=True)
    st.divider()

    datos = cargar_conocimiento()
    if not datos:
        st.error("Error: Base de conocimiento no encontrada.")
        return

    # --- PASO 1: ÁREAS TÉCNICAS ---
    st.subheader("1️⃣ Áreas de Evaluación")
    descripciones = datos.get('descripciones_categorias', {})
    categorias = sorted(list(set(r['categoria'] for r in datos['reglas'])))
    
    cols = st.columns(len(categorias))
    for i, cat in enumerate(categorias):
        with cols[i]:
            with st.container(border=True):
                st.markdown(f"**{cat}**")
                st.caption(descripciones.get(cat, ""))

    cat_sel = st.selectbox("\n¿Qué área presenta anomalías?", ["-- Seleccione una opción --"] + categorias)

    # --- PASO 2: CUESTIONARIO DINÁMICO ---
    if cat_sel != "-- Seleccione una opción --":
        st.divider()
        st.subheader(f"2️⃣ Análisis de Síntomas: {cat_sel}")
        
        reglas_evaluar = [r for r in datos['reglas'] if r['categoria'] == cat_sel]
        sintomas_relevantes = sorted(list(set(s for r in reglas_evaluar for s in r['sintomas'])))
        diccionario = datos.get('diccionario_sintomas', {})
        
        with st.form("form_diagnostico"):
            st.write("Marque todos los síntomas observados:")
            respuestas = {}
            
            # Rejilla simétrica de 3 columnas
            for i in range(0, len(sintomas_relevantes), 3):
                cols_q = st.columns(3)
                for j in range(3):
                    if i + j < len(sintomas_relevantes):
                        s_key = sintomas_relevantes[i + j]
                        with cols_q[j]:
                            respuestas[s_key] = st.checkbox(diccionario.get(s_key, s_key), key=s_key)
            
            st.write("")
            submit = st.form_submit_button("🔍 GENERAR DIAGNÓSTICO AHORA")

        # --- PASO 3: MOTOR DE INFERENCIA SENSIBLE ---
        if submit:
            hechos_usuario = [s for s, marcado in respuestas.items() if marcado]
            st.divider()
            
            if not hechos_usuario:
                st.warning("⚠️ Seleccione al menos un síntoma para el análisis.")
            else:
                hallazgos = 0
                for regla in reglas_evaluar:
                    sintomas_regla = set(regla['sintomas'])
                    coincidencias = sintomas_regla.intersection(set(hechos_usuario))
                    
                    if len(coincidencias) > 0:
                        hallazgos += 1
                        # Cálculo de certeza
                        certeza = int((len(coincidencias) / len(sintomas_regla)) * 100)
                        
                        st.error(f"### 📍 DIAGNÓSTICO: {regla['falla'].upper()}")
                        
                        # Barra de progreso para la certeza
                        st.write(f"**Nivel de Certeza del Diagnóstico: {certeza}%**")
                        st.progress(certeza / 100)
                        
                        st.info(f"**🔧 Acción Sugerida:** {regla['accion']}")
                        
                        with st.expander("Detalles del Razonamiento"):
                            st.write(f"El sistema detectó {len(coincidencias)} de {len(sintomas_regla)} indicadores clave.")
                            st.write(f"Síntomas confirmados: *{', '.join(list(coincidencias)).replace('_', ' ')}*")
                        st.write("---")
                
                if hallazgos > 0:
                    st.success("Análisis completado. Siga las instrucciones para prevenir daños mayores.")
                else:
                    st.success("✅ No hay alertas críticas. Su equipo está en buen estado.")

    else:
        st.divider()
        st.info("💡 **Prevención:** Un equipo limpio y optimizado dura hasta 5 años más. ¡Empiece su diagnóstico arriba!")

if __name__ == "__main__":
    main()
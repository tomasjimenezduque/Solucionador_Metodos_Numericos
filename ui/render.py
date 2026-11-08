import streamlit as st

def mostrar_solucion(solucion: dict, plegar_pasos: bool = False) -> None:
    st.markdown(f"### 📊 {solucion['metodo']}")
    
    if solucion.get("pasos"):
        for paso in solucion["pasos"]:
            if plegar_pasos:
                with st.expander(paso["titulo"]):
                    st.latex(paso["latex"])
            else:
                st.markdown(f"**{paso['titulo']}**")
                st.latex(paso["latex"])
                
    st.markdown("#### Tabla de Iteraciones / Puntos")
    st.dataframe(solucion["tabla"], use_container_width=True)
    
    st.success(f"✨ **Resultado final aproximado:** `{solucion['resultado_final']:.6f}`")

def boton_descarga(solucion: dict, nombre_archivo: str) -> None:
    texto = f"Método: {solucion['metodo']}\n\nResultado Final: {solucion['resultado_final']}\n\nTabla:\n{solucion['tabla'].to_string()}"
    st.download_button("📥 Descargar reporte en texto", texto, file_name=nombre_archivo, mime="text/plain")
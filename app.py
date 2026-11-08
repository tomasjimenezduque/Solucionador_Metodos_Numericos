from __future__ import annotations
import streamlit as st

st.set_page_config(
    page_title="Solucionador de Métodos Numéricos",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

from core.parser import ErrorExpresion
from metodos import edos, integracion
from ui.render import boton_descarga, mostrar_solucion

FAMILIAS = {
    "📈 Ecuaciones Diferenciales (EDOs)": [
        "Método de Euler",
        "Euler Mejorado (Heun)",
        "Runge-Kutta 4 (RK4)",
    ],
    "📉 Integración Numérica": [
        "Trapecio Simple",
        "Simpson 1/3 Simple",
        "Simpson 3/8 Simple",
        "Trapecio Compuesto",
        "Simpson 1/3 Compuesto",
        "Cuadratura Gaussiana (2 Puntos)",
    ],
}

def resolver(funcion, *args, **kwargs):
    try:
        with st.spinner("Calculando solución paso a paso..."):
            return funcion(*args, **kwargs)
    except ErrorExpresion as exc:
        st.error(f"**Error en la expresión:** {exc}")
    except Exception as exc:
        st.error(f"**Error inesperado:** {exc}")
    return None

def main() -> None:
    with st.sidebar:
        st.markdown("## 📐 Métodos Numéricos")
        st.caption("Ecuaciones Diferenciales e Integración")
        familia = st.radio("Categoría", list(FAMILIAS), key="familia")
        metodo = st.selectbox("Método", FAMILIAS[familia], key="metodo")
        st.divider()
        plegar = st.toggle("Plegar los pasos", value=False, key="plegar")

    st.title("📐 Solucionador de Métodos Numéricos")
    
    solucion = None

    if familia == "📈 Ecuaciones Diferenciales (EDOs)":
        st.markdown(f"### {metodo}")
        with st.container(border=True):
            f_expr = st.text_input("Función f(x, y)", value="x - y", help="Ejemplo: x - y o 2*x*y")
            col1, col2, col3, col4 = st.columns(4)
            with col1: x0 = st.number_input("x₀ (Inicio)", value=0.0, step=0.1)
            with col2: y0 = st.number_input("y₀ (Condición inicial)", value=2.0, step=0.1)
            with col3: x_f = st.number_input("x_f (Valor final)", value=1.0, step=0.1)
            with col4: n = st.number_input("n (Subintervalos)", value=5, min_value=1, step=1)

        if st.button("🚀 Resolver EDO", type="primary", use_container_width=True):
            if metodo == "Método de Euler":
                solucion = resolver(edos.metodo_euler, f_expr, x0, y0, x_f, int(n))
            elif metodo == "Euler Mejorado (Heun)":
                solucion = resolver(edos.metodo_euler_mejorado, f_expr, x0, y0, x_f, int(n))
            elif metodo == "Runge-Kutta 4 (RK4)":
                solucion = resolver(edos.metodo_runge_kutta_4, f_expr, x0, y0, x_f, int(n))

    elif familia == "📉 Integración Numérica":
        st.markdown(f"### {metodo}")
        with st.container(border=True):
            f_expr = st.text_input("Función f(x)", value="2 + 3*x", help="Ejemplo: 2 + 3*x o sin(x)")
            col1, col2 = st.columns(2)
            with col1: a = st.number_input("Límite inferior (a)", value=0.0, step=0.5)
            with col2: b = st.number_input("Límite superior (b)", value=5.0, step=0.5)
            
            n = 4
            if "Compuesto" in metodo:
                n = st.number_input("Subintervalos n (par para Simpson 1/3)", value=4, min_value=2, step=2)

        if st.button("🚀 Calcular Integral", type="primary", use_container_width=True):
            if metodo == "Trapecio Simple":
                solucion = resolver(integracion.trapecio_simple, f_expr, a, b)
            elif metodo == "Simpson 1/3 Simple":
                solucion = resolver(integracion.simpson_1_3_simple, f_expr, a, b)
            elif metodo == "Simpson 3/8 Simple":
                solucion = resolver(integracion.simpson_3_8_simple, f_expr, a, b)
            elif metodo == "Trapecio Compuesto":
                solucion = resolver(integracion.trapecio_compuesto, f_expr, a, b, int(n))
            elif metodo == "Simpson 1/3 Compuesto":
                solucion = resolver(integracion.simpson_1_3_compuesto, f_expr, a, b, int(n))
            elif metodo == "Cuadratura Gaussiana (2 Puntos)":
                solucion = resolver(integracion.cuadratura_gaussiana_2, f_expr, a, b)

    if solucion:
        st.divider()
        mostrar_solucion(solucion, plegar_pasos=plegar)
        boton_descarga(solucion, f"{metodo.lower().replace(' ', '_')}.txt")

if __name__ == "__main__":
    main()
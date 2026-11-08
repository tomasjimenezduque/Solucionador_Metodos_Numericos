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

def aplicar_ejemplo(prefijos, valores: dict) -> None:
    """Limpia los widgets afectados de la sesión y carga los valores del ejemplo."""
    for clave in list(st.session_state.keys()):
        if any(str(clave).startswith(p) for p in prefijos):
            del st.session_state[clave]
    st.session_state.update(valores)
    st.rerun()

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

    # Si cambia de método, limpia la última solución mostrada
    seleccion = f"{familia}|{metodo}"
    if st.session_state.get("metodo_activo") != seleccion:
        st.session_state["metodo_activo"] = seleccion
        st.session_state.pop("ultima_solucion", None)

    st.title("📐 Solucionador de Métodos Numéricos")
    
    solucion = None

    if familia == "📈 Ecuaciones Diferenciales (EDOs)":
        st.markdown(f"### {metodo}")
        
        with st.container(border=True):
            if st.button("📋 Cargar ejemplo de clase", key="edo_ejemplo"):
                aplicar_ejemplo(["edo_"], {
                    "edo_expr": "x - y",
                    "edo_x0": 0.0,
                    "edo_y0": 2.0,
                    "edo_xf": 1.0,
                    "edo_n": 5
                })
            
            f_expr = st.text_input("Función f(x, y)", value=st.session_state.get("edo_expr", "x - y"), key="edo_expr", help="Ejemplo: x - y o 2*x*y")
            col1, col2, col3, col4 = st.columns(4)
            with col1: x0 = st.number_input("x₀ (Inicio)", value=float(st.session_state.get("edo_x0", 0.0)), step=0.1, key="edo_x0")
            with col2: y0 = st.number_input("y₀ (Condición inicial)", value=float(st.session_state.get("edo_y0", 2.0)), step=0.1, key="edo_y0")
            with col3: x_f = st.number_input("x_f (Valor final)", value=float(st.session_state.get("edo_xf", 1.0)), step=0.1, key="edo_xf")
            with col4: n = st.number_input("n (Subintervalos)", value=int(st.session_state.get("edo_n", 5)), min_value=1, step=1, key="edo_n")

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
            if st.button("📋 Cargar ejemplo de clase", key="int_ejemplo"):
                aplicar_ejemplo(["int_"], {
                    "int_expr": "2 + 3*x",
                    "int_a": 0.0,
                    "int_b": 5.0,
                    "int_n": 4
                })

            f_expr = st.text_input("Función f(x)", value=st.session_state.get("int_expr", "2 + 3*x"), key="int_expr", help="Ejemplo: 2 + 3*x o sin(x)")
            col1, col2 = st.columns(2)
            with col1: a = st.number_input("Límite inferior (a)", value=float(st.session_state.get("int_a", 0.0)), step=0.5, key="int_a")
            with col2: b = st.number_input("Límite superior (b)", value=float(st.session_state.get("int_b", 5.0)), step=0.5, key="int_b")
            
            n = 4
            if "Compuesto" in metodo:
                n = st.number_input("Subintervalos n (par para Simpson 1/3)", value=int(st.session_state.get("int_n", 4)), min_value=2, step=2, key="int_n")

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
        st.session_state["ultima_solucion"] = (solucion, metodo.lower().replace(" ", "_"))

    guardada = st.session_state.get("ultima_solucion")
    if guardada:
        sol, nombre_archivo = guardada
        st.divider()
        mostrar_solucion(sol, plegar_pasos=plegar)
        boton_descarga(sol, f"{nombre_archivo}.txt")

if __name__ == "__main__":
    main()
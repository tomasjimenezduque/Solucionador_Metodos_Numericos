from __future__ import annotations
import pandas as pd
from core.parser import evaluar_funcion

def metodo_euler(f_expr: str, x0: float, y0: float, x_f: float, n: int) -> dict:
    h = (x_f - x0) / n
    registros = []
    pasos = []
    
    pasos.append({
        "titulo": "Fórmula y Parámetros Iniciales",
        "latex": f"y_{{i+1}} = y_i + h \\cdot f(x_i, y_i) \\quad \\text{{con }} h = {h}"
    })

    x, y = x0, y0
    for i in range(n):
        f_val = evaluar_funcion(f_expr, {"x": x, "y": y})
        y_next = y + h * f_val
        registros.append({
            "Iter": i, "x_i": round(x, 4), "y_i": round(y, 4),
            "f(x_i, y_i)": round(f_val, 4), "y_{i+1}": round(y_next, 4)
        })
        x, y = x + h, y_next

    return {
        "metodo": "Método de Euler",
        "tabla": pd.DataFrame(registros),
        "resultado_final": y,
        "pasos": pasos
    }

def metodo_euler_mejorado(f_expr: str, x0: float, y0: float, x_f: float, n: int) -> dict:
    h = (x_f - x0) / n
    registros = []
    pasos = [{
        "titulo": "Fórmulas de Heun (Predictor - Corrector)",
        "latex": f"y^* = y_i + h \\cdot f(x_i, y_i), \\quad y_{{i+1}} = y_i + \\frac{{h}}{{{2}}} [f(x_i, y_i) + f(x_{{i+1}}, y^*)] \\quad (h = {h})"
    }]

    x, y = x0, y0
    for i in range(n):
        f_ini = evaluar_funcion(f_expr, {"x": x, "y": y})
        y_bar = y + h * f_ini
        x_sig = x + h
        f_pred = evaluar_funcion(f_expr, {"x": x_sig, "y": y_bar})
        y_next = y + (h / 2) * (f_ini + f_pred)
        
        registros.append({
            "Iter": i, "x_i": round(x, 4), "y_i": round(y, 4),
            "f_ini": round(f_ini, 4), "y_bar": round(y_bar, 4),
            "f_pred": round(f_pred, 4), "y_{i+1}": round(y_next, 4)
        })
        x, y = x_sig, y_next

    return {
        "metodo": "Método de Euler Mejorado / Heun",
        "tabla": pd.DataFrame(registros),
        "resultado_final": y,
        "pasos": pasos
    }

def metodo_runge_kutta_4(f_expr: str, x0: float, y0: float, x_f: float, n: int) -> dict:
    h = (x_f - x0) / n
    registros = []
    pasos = [{
        "titulo": "Fórmulas de Runge-Kutta de 4to Orden",
        "latex": f"y_{{i+1}} = y_i + \\frac{{h}}{{{6}}}(k_1 + 2k_2 + 2k_3 + k_4) \\quad (h = {h})"
    }]

    x, y = x0, y0
    for i in range(n):
        k1 = evaluar_funcion(f_expr, {"x": x, "y": y})
        k2 = evaluar_funcion(f_expr, {"x": x + 0.5 * h, "y": y + 0.5 * k1 * h})
        k3 = evaluar_funcion(f_expr, {"x": x + 0.5 * h, "y": y + 0.5 * k2 * h})
        k4 = evaluar_funcion(f_expr, {"x": x + h, "y": y + k3 * h})
        y_next = y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        
        registros.append({
            "Iter": i, "x_i": round(x, 4), "y_i": round(y, 4),
            "k1": round(k1, 4), "k2": round(k2, 4),
            "k3": round(k3, 4), "k4": round(k4, 4), "y_{i+1}": round(y_next, 4)
        })
        x, y = x + h, y_next

    return {
        "metodo": "Runge-Kutta 4 (RK4)",
        "tabla": pd.DataFrame(registros),
        "resultado_final": y,
        "pasos": pasos
    }
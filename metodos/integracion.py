from __future__ import annotations
import pandas as pd
from core.parser import evaluar_funcion

def trapecio_simple(f_expr: str, a: float, b: float) -> dict:
    h = b - a
    fa = evaluar_funcion(f_expr, {"x": a})
    fb = evaluar_funcion(f_expr, {"x": b})
    val = (h / 2) * (fa + fb)
    tabla = pd.DataFrame([
        {"Punto": "a (x0)", "x_i": a, "f(x_i)": fa},
        {"Punto": "b (x1)", "x_i": b, "f(x_i)": fb}
    ])
    return {"metodo": "Trapecio Simple", "tabla": tabla, "resultado_final": val, "pasos": []}

def simpson_1_3_simple(f_expr: str, a: float, b: float) -> dict:
    h = (b - a) / 2
    x0, x1, x2 = a, a + h, b
    fx0 = evaluar_funcion(f_expr, {"x": x0})
    fx1 = evaluar_funcion(f_expr, {"x": x1})
    fx2 = evaluar_funcion(f_expr, {"x": x2})
    val = (h / 3) * (fx0 + 4 * fx1 + fx2)
    tabla = pd.DataFrame([
        {"Punto": "x0", "x_i": x0, "f(x_i)": fx0},
        {"Punto": "x1", "x_i": x1, "f(x_i)": fx1},
        {"Punto": "x2", "x_i": x2, "f(x_i)": fx2}
    ])
    return {"metodo": "Simpson 1/3 Simple", "tabla": tabla, "resultado_final": val, "pasos": []}

def simpson_3_8_simple(f_expr: str, a: float, b: float) -> dict:
    h = (b - a) / 3
    x0, x1, x2, x3 = a, a + h, a + 2 * h, b
    fx0 = evaluar_funcion(f_expr, {"x": x0})
    fx1 = evaluar_funcion(f_expr, {"x": x1})
    fx2 = evaluar_funcion(f_expr, {"x": x2})
    fx3 = evaluar_funcion(f_expr, {"x": x3})
    val = ((3 * h) / 8) * (fx0 + 3 * fx1 + 3 * fx2 + fx3)
    tabla = pd.DataFrame([
        {"Punto": "x0", "x_i": x0, "f(x_i)": fx0},
        {"Punto": "x1", "x_i": x1, "f(x_i)": fx1},
        {"Punto": "x2", "x_i": x2, "f(x_i)": fx2},
        {"Punto": "x3", "x_i": x3, "f(x_i)": fx3}
    ])
    return {"metodo": "Simpson 3/8 Simple", "tabla": tabla, "resultado_final": val, "pasos": []}

def trapecio_compuesto(f_expr: str, a: float, b: float, n: int) -> dict:
    h = (b - a) / n
    registros = []
    suma = 0
    for i in range(n + 1):
        xi = a + i * h
        fxi = evaluar_funcion(f_expr, {"x": xi})
        coef = 1 if (i == 0 or i == n) else 2
        suma += coef * fxi
        registros.append({"i": i, "x_i": round(xi, 4), "f(x_i)": round(fxi, 4), "Coef": coef})
    val = (h / 2) * suma
    return {"metodo": f"Trapecio Compuesto (n={n})", "tabla": pd.DataFrame(registros), "resultado_final": val, "pasos": []}

def simpson_1_3_compuesto(f_expr: str, a: float, b: float, n: int) -> dict:
    if n % 2 != 0:
        raise ValueError("El número de subintervalos n debe ser par para Simpson 1/3 Compuesto.")
    h = (b - a) / n
    registros = []
    suma = 0
    for i in range(n + 1):
        xi = a + i * h
        fxi = evaluar_funcion(f_expr, {"x": xi})
        coef = 1 if (i == 0 or i == n) else (4 if i % 2 == 1 else 2)
        suma += coef * fxi
        registros.append({"i": i, "x_i": round(xi, 4), "f(x_i)": round(fxi, 4), "Coef": coef})
    val = (h / 3) * suma
    return {"metodo": f"Simpson 1/3 Compuesto (n={n})", "tabla": pd.DataFrame(registros), "resultado_final": val, "pasos": []}

def cuadratura_gaussiana_2(f_expr: str, a: float, b: float) -> dict:
    t1, t2, w1, w2 = -0.5773502692, 0.5773502692, 1.0, 1.0
    x1 = ((b - a) * t1 + (a + b)) / 2
    x2 = ((b - a) * t2 + (a + b)) / 2
    fx1 = evaluar_funcion(f_expr, {"x": x1})
    fx2 = evaluar_funcion(f_expr, {"x": x2})
    val = ((b - a) / 2) * (w1 * fx1 + w2 * fx2)
    tabla = pd.DataFrame([
        {"Punto": "P1", "t_i": t1, "x_i (Transformado)": round(x1, 4), "f(x_i)": round(fx1, 4)},
        {"Punto": "P2", "t_i": t2, "x_i (Transformado)": round(x2, 4), "f(x_i)": round(fx2, 4)}
    ])
    return {"metodo": "Cuadratura Gaussiana (2 Puntos)", "tabla": tabla, "resultado_final": val, "pasos": []}
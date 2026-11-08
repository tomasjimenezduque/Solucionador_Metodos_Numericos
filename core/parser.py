from __future__ import annotations
import math

class ErrorExpresion(Exception):
    """Error al interpretar o evaluar una expresión matemática."""
    pass

def evaluar_funcion(expr: str, variables: dict[str, float]) -> float:
    """Evalúa una expresión matemática de forma segura usando un diccionario de contexto."""
    contexto = {
        "sin": math.sin, "cos": math.cos, "tan": math.tan,
        "exp": math.exp, "log": math.log, "sqrt": math.sqrt,
        "pi": math.pi, "e": math.e, **variables
    }
    try:
        # Limpieza básica de sintaxis común
        expr_limpia = expr.replace("^", "**")
        return float(eval(expr_limpia, {"__builtins__": None}, contexto))
    except Exception as exc:
        raise ErrorExpresion(f"No se pudo evaluar la expresión '{expr}': {exc}")
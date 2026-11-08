# Métodos Numéricos: Solución de Ecuaciones Diferenciales Ordinarias e Integración Numérica

## 📄 Resumen Ejecutivo

Este repositorio contiene una suite computacional e interactiva orientada a la aproximación de soluciones de **Problemas de Valor Inicial (PVI)** en Ecuaciones Diferenciales Ordinarias (EDOs) de primer orden y al cálculo de **Integrales Definidas** mediante métodos numéricos clásicos y cuadraturas avanzadas.

El proyecto ha sido refactorizado bajo una **arquitectura modular estricta** desacoplando la lógica matemática del renderizado visual. Cuenta con una **interfaz web interactiva y reactiva desarrollada con Streamlit**, capaz de procesar expresiones matemáticas en tiempo de ejecución, desplegando el desarrollo paso a paso en notación $\LaTeX$, tablas interactivas con Pandas y opciones de exportación de reportes.

---

## 🏛️ Estructura del Repositorio

El código fuente se encuentra organizado por capas de responsabilidad para facilitar el mantenimiento y despliegue continuo:

```text
numericos/
├── core/
│   └── parser.py         # Evaluador y analizador sintáctico de funciones f(x) y f(x,y)
├── metodos/
│   ├── edos.py           # Solucionador PVI (Euler, Heun, Runge-Kutta 4)
│   └── integracion.py    # Integración Numérica (Newton-Cotes y Cuadratura Gaussiana)
├── ui/
│   └── render.py         # Componentes de renderizado LaTeX, tablas y exportación
├── app.py                # Orquestador principal de la aplicación Streamlit
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Documentación académica y guía de usuario
```

---

## 🧮 Fundamentación Matemática

### 1. Solución Numérica de Ecuaciones Diferenciales Ordinarias (PVI)

Dado un Problema de Valor Inicial formulado como:

$$
\begin{cases} 
\dfrac{dy}{dx} = f(x, y) \\ 
y(x_0) = y_0 
\end{cases}, \quad x \in [x_0, x_f]
$$

Se discretiza el intervalo $[x_0, x_f]$ mediante $n$ subintervalos equiespaciados de longitud $h = \frac{x_f - x_0}{n}$, generando los puntos del dominio $x_i = x_0 + i \cdot h$ para $i = 0, 1, \dots, n$.

#### 1.1. Método de Euler (Primer Orden)
Derivado de la truncación de la serie de Taylor a primer orden. Asume pendiente constante en cada subintervalo:

$$
y_{i+1} = y_i + h \cdot f(x_i, y_i)
$$

- **Error de Truncamiento Local:** $\mathcal{O}(h^2)$
- **Error Global:** $\mathcal{O}(h)$

#### 1.2. Método de Euler Mejorado / Heun (Segundo Orden)
Esquema de tipo **Predictor-Corrector** que promedia las pendientes evaluadas en los extremos inicial y final del subintervalo:

1. **Predicción (Euler):** $\bar{y}_{i+1} = y_i + h \cdot f(x_i, y_i)$
2. **Corrección:**

$$
y_{i+1} = y_i + \frac{h}{2} \left[ f(x_i, y_i) + f(x_{i+1}, \bar{y}_{i+1}) \right]
$$

- **Error Global:** $\mathcal{O}(h^2)$

#### 1.3. Método de Runge-Kutta de Cuarto Orden (RK4)
Combina cuatro evaluaciones discretas de la función de pendiente dentro del intervalo $[x_i, x_{i+1}]$ coincidiendo con los términos de la Serie de Taylor hasta orden 4 sin requerir cálculo explícito de derivadas superiores:

$$
y_{i+1} = y_i + \frac{h}{6} \left( k_1 + 2k_2 + 2k_3 + k_4 \right)
$$

Donde las pendientes ponderadas se definen como:

$$
\begin{aligned}
k_1 &= f(x_i, y_i) \\
k_2 &= f\left(x_i + \frac{h}{2}, y_i + \frac{h}{2}k_1\right) \\
k_3 &= f\left(x_i + \frac{h}{2}, y_i + \frac{h}{2}k_2\right) \\
k_4 &= f\left(x_i + h, y_i + h k_3\right)
\end{aligned}
$$

- **Error Global:** $\mathcal{O}(h^4)$

---

### 2. Métodos de Integración Numérica

Para estimar el área bajo la curva de una integral definida $I = \int_{a}^{b} f(x) \, dx$:

#### 2.1. Reglas de Newton-Cotes (Simples)

- **Trapecio Simple ($n=1$):** Aproximación lineal sobre $[a, b]$:

$$
I \approx \frac{b-a}{2} \left[ f(a) + f(b) \right]
$$

- **Simpson 1/3 Simple ($n=2$):** Interpolación polinómica cuadrática ($h = \frac{b-a}{2}$):

$$
I \approx \frac{h}{3} \left[ f(x_0) + 4f(x_1) + f(x_2) \right]
$$

- **Simpson 3/8 Simple ($n=3$):** Interpolación polinómica cúbica ($h = \frac{b-a}{3}$):

$$
I \approx \frac{3h}{8} \left[ f(x_0) + 3f(x_1) + 3f(x_2) + f(x_3) \right]
$$

#### 2.2. Reglas Compuestas (Subintervalos $n > 1$)

- **Trapecio Compuesto:**

$$
I \approx \frac{h}{2} \left[ f(x_0) + 2 \sum_{i=1}^{n-1} f(x_i) + f(x_n) \right]
$$

- **Simpson 1/3 Compuesto** (requiere $n$ par):

$$
I \approx \frac{h}{3} \left[ f(x_0) + 4 \sum_{i \text{ impar}}^{n-1} f(x_i) + 2 \sum_{i \text{ par}}^{n-2} f(x_i) + f(x_n) \right]
$$

#### 2.3. Cuadratura Gaussiana de 2 Puntos (Legendre)

Transforma el intervalo $[a, b]$ al dominio canónico $[-1, 1]$ mediante el cambio de variable lineal:

$$
x(t) = \frac{b-a}{2} t + \frac{a+b}{2}, \quad dx = \frac{b-a}{2} \, dt
$$

Aplicando pesos $W_1 = W_2 = 1.0$ y raíces del polinomio de Legendre $t_1, t_2 = \pm \frac{1}{\sqrt{3}} \approx \pm 0.5773502692$:

$$
I = \int_{a}^{b} f(x) \, dx = \frac{b-a}{2} \int_{-1}^{1} f(x(t)) \, dt \approx \frac{b-a}{2} \left[ f(x(t_1)) + f(x(t_2)) \right]
$$

---

## ⚙️ Especificación Técnica e Instalación

### Requisitos Prerequisito
- **Entorno Runtime:** Python 3.9 o superior.
- **Dependencias Principales:** `streamlit`, `pandas`, `numpy`.

### Instalación y Verificación

```powershell
# 1. Crear e ingresar a un entorno virtual (opcional pero recomendado)
python -m venv venv
.\venv\Scripts\Activate.ps1   # En Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Lanzar la aplicación web interactiva
streamlit run app.py
```

---

## 🚀 Guía de Uso Interactivo (Interfaz Web Streamlit)

La plataforma interactiva permite resolver y auditar cualquier ejercicio mediante los siguientes paneles:

### 1. Selección de Categoría y Método
A través de la barra lateral desplegable, el usuario selecciona el área de estudio (EDOs o Integración) y el algoritmo específico deseado. También cuenta con la opción de **"Plegar los pasos"** para ocultar/mostrar las derivaciones matemáticas según el interés pedagógico.

### 2. Evaluador Dinámico de Expresiones
Soporta expresiones matemáticas escritas en sintaxis nativa de Python / álgebra informal (se auto-reemplaza `^` por `**` automáticamente):
- **Operadores:** `+`, `-`, `*`, `/`, `**` (potencia).
- **Funciones Trascendentes:** `sin(x)`, `cos(x)`, `tan(x)`, `exp(x)`, `log(x)`, `sqrt(x)`.
- **Constantes:** `pi`, `e`.

### 3. Reportes Exportables
Al finalizar cada cálculo, el usuario puede descargar un archivo plano (`.txt`) con la tabla de resultados e iteraciones formateadas.

---

## 📊 Casos Límite y Análisis de Sensibilidad (Stress Testing)

Para comprobar la robustez y divergencia de los métodos ante condiciones extremas, se sugieren las siguientes pruebas de estrés:

| Dominio | Expresión $f(x, y)$ o $f(x)$ | Parámetros | Comportamiento Numérico a Observar |
| :--- | :--- | :--- | :--- |
| **EDO** | `y**2 - x` | $x_0=0, y_0=1, x_f=2, n=20$ | **Crecimiento Cuadrático Crítico:** Divergencia acentuada del método de Euler frente a la estabilidad del algoritmo RK4. |
| **EDO** | `sin(x) * y` | $x_0=0, y_0=1, x_f=5, n=10$ | **Rigidez Oscilatoria:** Muestra la amplificación del error en pasos gruesos ($h=0.5$). |
| **Integración** | `exp(x**2)` | $a=1, b=3, n=100$ | **Gradiente Extremo:** Evalúa la convergencia del método de Simpson compuesto en curvas exponenciales aceleradas. |

---

## 👥 Autoría y Créditos

- **Desarrollo del Software e Arquitectura en Python/Streamlit:** Desarrollador y colaboradores del Repositorio.
- **Base Teórica, Modelos Matemáticos y Diapositivas:** Prof. Carlos Alberto Márquez Fernández — *Universidad de San Buenaventura, Departamento de Ciencias Básicas y Matemáticas*.

---

## 📄 Licencia

Este proyecto está bajo la Licencia **MIT**. Eres libre de usar, modificar y redistribuir este código con fines educativos y académicos, siempre que se mantengan los reconocimientos de autoría correspondientes.
import streamlit as st
from fractions import Fraction

# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="LIM · FDP-01",
    page_icon="◩",
    layout="wide"
)

# =========================================================
# ESTILOS
# =========================================================

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .lim-code {
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        color: #38d45a;
    }

    .representaciones {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        margin-top: 18px;
        margin-bottom: 18px;
    }

    .representacion {
        border: 1px solid rgba(150, 160, 180, 0.35);
        border-radius: 14px;
        padding: 22px 18px;
        text-align: center;
    }

    .representacion-titulo {
        font-size: 0.95rem;
        opacity: 0.72;
        margin-bottom: 8px;
    }

    .representacion-valor {
        font-size: 2rem;
        font-weight: 750;
    }

    .cuadricula {
        display: grid;
        grid-template-columns: repeat(10, 1fr);
        gap: 5px;
        width: min(100%, 520px);
        margin: 22px auto;
    }

    .celda {
        aspect-ratio: 1 / 1;
        border-radius: 4px;
        border: 1px solid rgba(150, 160, 180, 0.42);
        background: rgba(120, 130, 150, 0.08);
    }

    .celda-activa {
        background: #38d45a;
        border-color: #38d45a;
    }

    .entero-label {
        text-align: center;
        opacity: 0.72;
        margin-top: 6px;
        font-size: 0.95rem;
    }

    .equivalencia {
        border: 1px solid rgba(150, 160, 180, 0.35);
        border-radius: 14px;
        padding: 18px 20px;
        margin-top: 16px;
    }

    @media (max-width: 700px) {
        .representaciones {
            grid-template-columns: 1fr;
        }

        .representacion-valor {
            font-size: 1.65rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# FUNCIONES
# =========================================================

def decimal_con_coma(valor):
    return f"{valor / 100:.2f}".replace(".", ",")


def fraccion_base(valor):
    return f"{valor}/100"


def fraccion_simplificada(valor):
    fraccion = Fraction(valor, 100)
    return fraccion.numerator, fraccion.denominator


def construir_cuadricula(valor):
    celdas = []

    for i in range(100):
        if i < valor:
            clase = "celda celda-activa"
        else:
            clase = "celda"

        celdas.append(f'<div class="{clase}"></div>')

    return (
        '<div class="cuadricula">'
        + "".join(celdas)
        + "</div>"
    )


# =========================================================
# ENCABEZADO
# =========================================================

st.markdown(
    '<div class="lim-code">FDP-01 &nbsp;|&nbsp; LIM · Laboratorio de Ideas Matemáticas</div>',
    unsafe_allow_html=True
)

st.title("Una cantidad, distintas escrituras")

st.subheader("Fracción, decimal y porcentaje")

st.write(
    """
Mové el control y observá cómo una misma cantidad puede
representarse de distintas maneras.
"""
)

st.divider()

# =========================================================
# MOMENTO 1 · MANIPULAR LA CANTIDAD
# =========================================================

st.header("1. Elegí cuánto querés representar")

valor = st.slider(
    "Cantidad representada",
    min_value=0,
    max_value=100,
    value=50,
    step=1,
    format="%d %%"
)

# Botones de cantidades especiales
st.write("También podés probar algunas cantidades:")

c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("25 %", use_container_width=True):
        valor = 25

with c2:
    if st.button("50 %", use_container_width=True):
        valor = 50

with c3:
    if st.button("75 %", use_container_width=True):
        valor = 75

with c4:
    if st.button("100 %", use_container_width=True):
        valor = 100

# =========================================================
# MOMENTO 2 · REPRESENTACIÓN VISUAL
# =========================================================

st.divider()

st.header("2. Mirá la cantidad")

st.write(
    f"Están representadas **{valor} de las 100 partes iguales** del entero."
)

st.markdown(
    construir_cuadricula(valor),
    unsafe_allow_html=True
)

st.markdown(
    '<div class="entero-label">El cuadrado completo representa 1 entero.</div>',
    unsafe_allow_html=True
)

# =========================================================
# MOMENTO 3 · TRES ESCRITURAS
# =========================================================

st.divider()

st.header("3. La misma cantidad, tres escrituras")

decimal = decimal_con_coma(valor)
fraccion = fraccion_base(valor)
porcentaje = f"{valor} %"

st.markdown(
    f"""
    <div class="representaciones">

        <div class="representacion">
            <div class="representacion-titulo">Fracción</div>
            <div class="representacion-valor">{fraccion}</div>
        </div>

        <div class="representacion">
            <div class="representacion-titulo">Número decimal</div>
            <div class="representacion-valor">{decimal}</div>
        </div>

        <div class="representacion">
            <div class="representacion-titulo">Porcentaje</div>
            <div class="representacion-valor">{porcentaje}</div>
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

st.info(
    "Las tres escrituras representan la misma cantidad que se muestra en la cuadrícula."
)

# =========================================================
# MOMENTO 4 · FRACCIONES EQUIVALENTES
# =========================================================

st.divider()

st.header("4. ¿Podemos escribir la fracción de otra manera?")

st.write(
    f"Por ahora escribimos la cantidad como **{valor}/100**."
)

mostrar_equivalente = st.checkbox(
    "Buscar una fracción equivalente con números más pequeños"
)

if mostrar_equivalente:

    numerador, denominador = fraccion_simplificada(valor)

    if denominador == 1:

        if numerador == 0:
            st.success(
                f"{valor}/100 representa 0."
            )
        else:
            st.success(
                f"{valor}/100 representa {numerador} entero."
            )

    elif numerador == valor and denominador == 100:

        st.write(
            "En este caso no encontramos una fracción equivalente "
            "con números enteros más pequeños."
        )

    else:

        st.markdown(
            f"""
            <div class="equivalencia">
                <strong>{valor}/100</strong>
                &nbsp; representa la misma cantidad que &nbsp;
                <strong>{numerador}/{denominador}</strong>.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write(
            "Volvé a mirar la cuadrícula: la cantidad representada no cambió."
        )

# =========================================================
# CIERRE
# =========================================================

st.divider()

st.subheader("Para seguir explorando")

st.write(
    """
Probá mover el control y buscá cantidades en las que puedas
reconocer relaciones entre la fracción, el decimal, el porcentaje
y la parte representada del entero.
"""
)

st.caption(
    "FDP-01 · Una cantidad, distintas escrituras · "
    "LIM – Laboratorio de Ideas Matemáticas · v0.1"
)

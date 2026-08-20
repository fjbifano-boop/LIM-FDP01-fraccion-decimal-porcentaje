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
# ESTADO
# =========================================================

if "cantidad" not in st.session_state:
    st.session_state.cantidad = 50


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

    .valor-grande {
        text-align: center;
        font-size: 2rem;
        font-weight: 750;
        padding: 8px 0 14px 0;
    }

    .equivalencia {
        border: 1px solid rgba(150, 160, 180, 0.35);
        border-radius: 14px;
        padding: 18px 20px;
        margin-top: 16px;
        font-size: 1.1rem;
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


def fijar_cantidad(valor):
    st.session_state.cantidad = valor


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
    '<div class="lim-code">'
    'FDP-01 &nbsp;|&nbsp; LIM · Laboratorio de Ideas Matemáticas'
    '</div>',
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
    step=1,
    key="cantidad",
    format="%d %%"
)

st.write("También podés probar algunas cantidades:")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.button(
        "25 %",
        on_click=fijar_cantidad,
        args=(25,),
        use_container_width=True
    )

with c2:
    st.button(
        "50 %",
        on_click=fijar_cantidad,
        args=(50,),
        use_container_width=True
    )

with c3:
    st.button(
        "75 %",
        on_click=fijar_cantidad,
        args=(75,),
        use_container_width=True
    )

with c4:
    st.button(
        "100 %",
        on_click=fijar_cantidad,
        args=(100,),
        use_container_width=True
    )

# Recuperamos el valor después de cualquier interacción
valor = st.session_state.cantidad


# =========================================================
# MOMENTO 2 · REPRESENTACIÓN VISUAL
# =========================================================

st.divider()

st.header("2. Mirá la cantidad")

st.write(
    f"Están representadas **{valor} de las 100 partes iguales** "
    f"del entero."
)

st.markdown(
    construir_cuadricula(valor),
    unsafe_allow_html=True
)

st.markdown(
    '<div class="entero-label">'
    'El cuadrado completo representa 1 entero.'
    '</div>',
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

col_frac, col_dec, col_por = st.columns(3)

with col_frac:
    with st.container(border=True):
        st.caption("Fracción")
        st.markdown(
            f'<div class="valor-grande">{fraccion}</div>',
            unsafe_allow_html=True
        )

with col_dec:
    with st.container(border=True):
        st.caption("Número decimal")
        st.markdown(
            f'<div class="valor-grande">{decimal}</div>',
            unsafe_allow_html=True
        )

with col_por:
    with st.container(border=True):
        st.caption("Porcentaje")
        st.markdown(
            f'<div class="valor-grande">{porcentaje}</div>',
            unsafe_allow_html=True
        )

st.info(
    "Las tres escrituras representan la misma cantidad "
    "que se muestra en la cuadrícula."
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

    if valor == 0:

        st.success(
            f"{valor}/100 representa 0."
        )

    elif denominador == 1:

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
            (
                '<div class="equivalencia">'
                f'<strong>{valor}/100</strong>'
                '&nbsp;&nbsp; representa la misma cantidad que '
                f'&nbsp;&nbsp;<strong>{numerador}/{denominador}</strong>.'
                '</div>'
            ),
            unsafe_allow_html=True
        )

        st.write(
            "Volvé a mirar la cuadrícula: "
            "la cantidad representada no cambió."
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

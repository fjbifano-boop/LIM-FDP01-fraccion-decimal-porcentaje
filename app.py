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
# FUNCIONES
# =========================================================

def fijar_cantidad(valor):
    st.session_state.cantidad = valor


def decimal_con_coma(valor):
    return f"{valor / 100:.2f}".replace(".", ",")


def fraccion_simplificada(valor):
    f = Fraction(valor, 100)
    return f.numerator, f.denominator


def alternar_celda(numero):
    """
    La cuadrícula representa una cantidad continua:
    al pulsar una celda, esa celda pasa a ser el nuevo límite
    de la cantidad representada.
    """
    st.session_state.cantidad = numero


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
        margin-bottom: 8px;
    }

    .valor-grande {
        text-align: center;
        font-size: 2rem;
        font-weight: 750;
        padding: 7px 0 12px 0;
    }

    .recta {
        position: relative;
        width: 92%;
        height: 80px;
        margin: 35px auto 10px auto;
    }

    .linea {
        position: absolute;
        top: 25px;
        left: 0;
        right: 0;
        height: 4px;
        background: #888;
        border-radius: 3px;
    }

    .marca {
        position: absolute;
        top: 16px;
        width: 4px;
        height: 22px;
        background: #ddd;
    }

    .marca0 {
        left: 0;
    }

    .marca1 {
        right: 0;
    }

    .punto {
        position: absolute;
        top: 17px;
        width: 20px;
        height: 20px;
        background: #38d45a;
        border-radius: 50%;
        transform: translateX(-50%);
    }

    .etiqueta-punto {
        position: absolute;
        top: 48px;
        transform: translateX(-50%);
        font-weight: 700;
        color: #38d45a;
    }

    .numero0 {
        position: absolute;
        top: 48px;
        left: 0;
        transform: translateX(-50%);
    }

    .numero1 {
        position: absolute;
        top: 48px;
        right: 0;
        transform: translateX(50%);
    }

    div[data-testid="stButton"] > button {
        min-height: 42px;
    }

    </style>
    """,
    unsafe_allow_html=True
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

st.title("Una cantidad, distintas representaciones")

st.subheader("Fracción, decimal y porcentaje")

st.write(
    """
Cambiá la cantidad de distintas maneras y observá qué ocurre
con sus diferentes representaciones.
"""
)

st.divider()

# =========================================================
# 1. CONTROL DE LA CANTIDAD
# =========================================================

st.header("1. Elegí una cantidad")

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

valor = st.session_state.cantidad

st.divider()

# =========================================================
# 2. CUADRÍCULA MANIPULABLE
# =========================================================

st.header("2. También podés cambiar la cantidad desde la cuadrícula")

st.write(
    "Tocá un cuadrado para cambiar la cantidad representada."
)

# Cuadrícula 10 x 10.
# Cada botón representa una centésima.

for fila in range(10):

    columnas = st.columns(10, gap="small")

    for columna in range(10):

        numero = fila * 10 + columna + 1
        activa = numero <= valor

        with columnas[columna]:

            if activa:
                etiqueta = "■"
            else:
                etiqueta = "□"

            st.button(
                etiqueta,
                key=f"celda_{numero}",
                on_click=alternar_celda,
                args=(numero,),
                use_container_width=True,
                type="primary" if activa else "secondary"
            )

st.caption(
    f"Están representadas {valor} de las 100 partes iguales del entero."
)

st.divider()

# =========================================================
# 3. REPRESENTACIONES NUMÉRICAS
# =========================================================

st.header("3. La misma cantidad, tres escrituras")

decimal = decimal_con_coma(valor)
fraccion = f"{valor}/100"
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

st.divider()

# =========================================================
# 4. RECTA NUMÉRICA
# =========================================================

st.header("4. ¿Dónde está esta cantidad entre 0 y 1?")

posicion = valor
decimal_recta = decimal_con_coma(valor)

recta_html = f"""
<style>
.recta-fdp {{
    position: relative;
    width: 92%;
    height: 90px;
    margin: 30px auto 5px auto;
}}

.recta-fdp .linea-fdp {{
    position: absolute;
    top: 26px;
    left: 0;
    right: 0;
    height: 4px;
    background: #888;
    border-radius: 3px;
}}

.recta-fdp .marca-fdp {{
    position: absolute;
    top: 17px;
    width: 3px;
    height: 22px;
    background: currentColor;
}}

.recta-fdp .marca-cero {{
    left: 0;
}}

.recta-fdp .marca-uno {{
    right: 0;
}}

.recta-fdp .punto-fdp {{
    position: absolute;
    top: 17px;
    left: {posicion}%;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #38d45a;
    transform: translateX(-50%);
}}

.recta-fdp .etiqueta-fdp {{
    position: absolute;
    top: 51px;
    left: {posicion}%;
    transform: translateX(-50%);
    font-weight: 700;
    color: #38d45a;
}}

.recta-fdp .cero-fdp {{
    position: absolute;
    top: 50px;
    left: 0;
}}

.recta-fdp .uno-fdp {{
    position: absolute;
    top: 50px;
    right: 0;
}}
</style>

<div class="recta-fdp">
    <div class="linea-fdp"></div>

    <div class="marca-fdp marca-cero"></div>
    <div class="marca-fdp marca-uno"></div>

    <div class="punto-fdp"></div>
    <div class="etiqueta-fdp">{decimal_recta}</div>

    <div class="cero-fdp">0</div>
    <div class="uno-fdp">1</div>
</div>
"""

st.html(recta_html)

st.write(
    "El punto representa en la recta la misma cantidad "
    "que aparece en la cuadrícula."
)

st.divider()

# =========================================================
# 5. FRACCIONES EQUIVALENTES
# =========================================================

st.header("5. ¿Podemos escribir la fracción de otra manera?")

st.write(
    f"La cuadrícula permite verla como **{valor}/100**."
)

mostrar_equivalente = st.checkbox(
    "Buscar una fracción equivalente con números más pequeños"
)

if mostrar_equivalente:

    numerador, denominador = fraccion_simplificada(valor)

    if valor == 0:

        st.success("0/100 representa 0.")

    elif denominador == 1:

        st.success(
            f"{valor}/100 representa {numerador} entero."
        )

    elif numerador == valor and denominador == 100:

        st.info(
            "En este caso no encontramos una fracción equivalente "
            "con números enteros más pequeños."
        )

    else:

        st.success(
            f"{valor}/100 representa la misma cantidad que "
            f"{numerador}/{denominador}."
        )

        st.write(
            "La escritura cambió, pero la cantidad representada "
            "en la cuadrícula y su posición en la recta permanecen iguales."
        )

st.divider()

# =========================================================
# CIERRE
# =========================================================

st.subheader("Para seguir explorando")

st.write(
    """
Probá cambiar la cantidad desde el control y desde la cuadrícula.
Observá cómo se modifican simultáneamente la fracción, el número
decimal, el porcentaje y la posición en la recta.
"""
)

st.caption(
    "FDP-01 · Una cantidad, distintas representaciones · "
    "LIM – Laboratorio de Ideas Matemáticas · v0.2"
)

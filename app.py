import streamlit as st
from fractions import Fraction
from decimal import Decimal

# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="LIM · FDP-02",
    page_icon="↔",
    layout="wide"
)

# =========================================================
# ESTADO
# =========================================================

if "valor" not in st.session_state:
    st.session_state.valor = Decimal("0.50")

if "salto" not in st.session_state:
    st.session_state.salto = Decimal("0.10")

if "historial" not in st.session_state:
    st.session_state.historial = []

if "ultimo_movimiento" not in st.session_state:
    st.session_state.ultimo_movimiento = None


# =========================================================
# FUNCIONES
# =========================================================

def decimal_a_texto(valor):
    """
    Conserva una escritura decimal adecuada al valor:
    0.50 -> 0,5
    0.25 -> 0,25
    0.01 -> 0,01
    """

    valor = Decimal(valor)

    if valor == valor.quantize(Decimal("1")):
        return str(int(valor))

    if valor == valor.quantize(Decimal("0.1")):
        return f"{valor:.1f}".replace(".", ",")

    return f"{valor:.2f}".replace(".", ",")


def fijar_salto(valor):
    st.session_state.salto = Decimal(valor)


def fijar_valor(valor):
    st.session_state.valor = Decimal(valor)
    st.session_state.historial = []
    st.session_state.ultimo_movimiento = None


def denominador_del_salto(salto):
    """
    Elegimos una unidad fraccionaria vinculada con
    el tamaño del salto.
    """

    salto = abs(Decimal(salto))

    if salto == Decimal("0.50"):
        return 2

    if salto == Decimal("0.25"):
        return 4

    if salto == Decimal("0.10"):
        return 10

    if salto == Decimal("0.01"):
        return 100

    return 100


def como_fraccion_con_denominador(valor, denominador):
    """
    Expresa el valor usando el denominador elegido.
    """

    valor = Decimal(valor)

    numerador = int(
        valor * Decimal(denominador)
    )

    return numerador, denominador


def mover(direccion):

    anterior = st.session_state.valor
    salto = st.session_state.salto

    desplazamiento = salto * Decimal(direccion)
    nuevo = anterior + desplazamiento

    # Evitamos salir de la recta 0-2
    if nuevo < Decimal("0"):
        nuevo = Decimal("0")

    if nuevo > Decimal("2"):
        nuevo = Decimal("2")

    desplazamiento_real = nuevo - anterior

    if nuevo != anterior:

        movimiento = {
            "desde": anterior,
            "hasta": nuevo,
            "desplazamiento": desplazamiento_real,
            "salto_elegido": salto
        }

        st.session_state.historial.append(movimiento)
        st.session_state.ultimo_movimiento = movimiento

    st.session_state.valor = nuevo


def reiniciar():
    st.session_state.valor = Decimal("0.50")
    st.session_state.salto = Decimal("0.10")
    st.session_state.historial = []
    st.session_state.ultimo_movimiento = None


# =========================================================
# ESTILOS
# =========================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1180px;
        padding-top: 4rem;
        padding-bottom: 3rem;
    }

    .lim-code {
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        color: #38d45a;
        margin-bottom: 8px;
    }

    .valor-central {
        text-align: center;
        font-size: 3rem;
        font-weight: 750;
        padding: 8px 0;
    }

    .valor-grande {
        text-align: center;
        font-size: 1.9rem;
        font-weight: 700;
        padding: 8px 0 12px 0;
    }

    .operacion {
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
        padding: 16px 4px;
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
    'FDP-02 &nbsp;|&nbsp; LIM · Laboratorio de Ideas Matemáticas'
    '</div>',
    unsafe_allow_html=True
)

st.title("Recorrer la unidad")

st.write(
    """
Movete sobre la recta dando saltos de distinto tamaño.
Observá qué ocurre con la cantidad cuando avanzás o retrocedés.
"""
)

st.divider()


# =========================================================
# 1. PUNTO DE PARTIDA
# =========================================================

st.header("1. Elegí un punto de partida")

c1, c2, c3, c4, c5 = st.columns(5)

puntos = [
    ("0", "0"),
    ("0,25", "0.25"),
    ("0,5", "0.50"),
    ("0,75", "0.75"),
    ("1", "1")
]

columnas_puntos = [c1, c2, c3, c4, c5]

for indice, (columna, (etiqueta, valor_punto)) in enumerate(
    zip(columnas_puntos, puntos)
):
    with columna:
        st.button(
            etiqueta,
            key=f"punto_partida_{indice}",
            on_click=fijar_valor,
            args=(valor_punto,),
            use_container_width=True
        )


# =========================================================
# 2. RECTA
# =========================================================

st.divider()

st.header("2. Tu posición en la recta")

valor = st.session_state.valor
texto_decimal = decimal_a_texto(valor)

# Recta de 0 a 2
posicion = float(valor / Decimal("2")) * 100


recta_html = f"""
<style>

.recta-fdp2 {{
    position: relative;
    width: 92%;
    height: 125px;
    margin: 35px auto 5px auto;
}}

.recta-fdp2 .linea {{
    position: absolute;
    top: 28px;
    left: 0;
    right: 0;
    height: 4px;
    background: #888;
    border-radius: 3px;
}}

.recta-fdp2 .marca {{
    position: absolute;
    top: 19px;
    width: 2px;
    height: 22px;
    background: #888;
    transform: translateX(-50%);
}}

.recta-fdp2 .etiqueta {{
    position: absolute;
    top: 50px;
    transform: translateX(-50%);
    color: #999;
    font-size: 0.9rem;
}}

.recta-fdp2 .punto {{
    position: absolute;
    top: 18px;
    left: {posicion}%;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: #38d45a;
    transform: translateX(-50%);
    z-index: 3;
}}

.recta-fdp2 .actual {{
    position: absolute;
    top: 80px;
    left: {posicion}%;
    transform: translateX(-50%);
    color: #38d45a;
    font-size: 1.15rem;
    font-weight: 750;
}}

</style>

<div class="recta-fdp2">

    <div class="linea"></div>

    <div class="marca" style="left:0%;"></div>
    <div class="marca" style="left:12.5%;"></div>
    <div class="marca" style="left:25%;"></div>
    <div class="marca" style="left:37.5%;"></div>
    <div class="marca" style="left:50%;"></div>
    <div class="marca" style="left:75%;"></div>
    <div class="marca" style="left:100%;"></div>

    <div class="etiqueta" style="left:0%;">0</div>
    <div class="etiqueta" style="left:12.5%;">0,25</div>
    <div class="etiqueta" style="left:25%;">0,5</div>
    <div class="etiqueta" style="left:37.5%;">0,75</div>
    <div class="etiqueta" style="left:50%;">1</div>
    <div class="etiqueta" style="left:75%;">1,5</div>
    <div class="etiqueta" style="left:100%;">2</div>

    <div class="punto"></div>
    <div class="actual">{texto_decimal}</div>

</div>
"""

st.html(recta_html)


# =========================================================
# 3. ELEGIR EL SALTO
# =========================================================

st.header("3. Elegí el tamaño del salto")

s1, s2, s3, s4 = st.columns(4)

saltos = [
    ("0,5", "0.50"),
    ("0,25", "0.25"),
    ("0,1", "0.10"),
    ("0,01", "0.01")
]

columnas_saltos = [s1, s2, s3, s4]

for indice, (columna, (etiqueta, valor_salto)) in enumerate(
    zip(columnas_saltos, saltos)
):
    with columna:

        st.button(
            etiqueta,
            key=f"salto_{indice}",
            on_click=fijar_salto,
            args=(valor_salto,),
            use_container_width=True,
            type=(
                "primary"
                if st.session_state.salto == Decimal(valor_salto)
                else "secondary"
            )
        )

st.write(
    "Tamaño del salto elegido: "
    f"**{decimal_a_texto(st.session_state.salto)}**"
)


# =========================================================
# 4. MOVERSE
# =========================================================

st.subheader("Movete sobre la recta")

izquierda, centro, derecha = st.columns([2, 2, 2])

with izquierda:

    st.button(
        "← Retroceder",
        key="boton_retroceder",
        on_click=mover,
        args=(-1,),
        use_container_width=True,
        disabled=st.session_state.valor <= Decimal("0")
    )

with centro:

    st.markdown(
        f'<div class="valor-central">'
        f'{decimal_a_texto(st.session_state.valor)}'
        f'</div>',
        unsafe_allow_html=True
    )

with derecha:

    st.button(
        "Avanzar →",
        key="boton_avanzar",
        on_click=mover,
        args=(1,),
        use_container_width=True,
        disabled=st.session_state.valor >= Decimal("2")
    )


# =========================================================
# 5. REPRESENTACIONES DE LA POSICIÓN ACTUAL
# =========================================================

st.divider()

st.header("4. La cantidad a la que llegaste")

valor = st.session_state.valor

fraccion_simplificada = Fraction(valor)

col_frac, col_dec = st.columns(2)

with col_dec:

    with st.container(border=True):

        st.caption("Número decimal")

        st.markdown(
            f'<div class="valor-grande">'
            f'{decimal_a_texto(valor)}'
            f'</div>',
            unsafe_allow_html=True
        )


with col_frac:

    with st.container(border=True):

        st.caption("Fracción")

        st.markdown(
            f'<div class="valor-grande">'
            f'{fraccion_simplificada.numerator}/'
            f'{fraccion_simplificada.denominator}'
            f'</div>',
            unsafe_allow_html=True
        )


# =========================================================
# 6. OPERACIÓN OPCIONAL
# =========================================================

if st.session_state.ultimo_movimiento is not None:

    st.divider()

    mostrar_operacion = st.checkbox(
        "Mostrar cómo puede escribirse el desplazamiento",
        key="mostrar_operacion"
    )

    if mostrar_operacion:

        st.header("5. Escribimos el desplazamiento")

        movimiento = st.session_state.ultimo_movimiento

        desde = movimiento["desde"]
        hasta = movimiento["hasta"]
        desplazamiento = movimiento["desplazamiento"]

        if desplazamiento > 0:
            signo = "+"
        else:
            signo = "−"

        magnitud = abs(desplazamiento)

        # -------------------------------------------------
        # OPERACIÓN DECIMAL
        # -------------------------------------------------

        st.subheader("Con números decimales")

        operacion_decimal = (
            f"{decimal_a_texto(desde)} "
            f"{signo} "
            f"{decimal_a_texto(magnitud)} "
            f"= "
            f"{decimal_a_texto(hasta)}"
        )

        with st.container(border=True):

            st.markdown(
                f'<div class="operacion">'
                f'{operacion_decimal}'
                f'</div>',
                unsafe_allow_html=True
            )

        # -------------------------------------------------
        # OPERACIÓN FRACCIONARIA
        # -------------------------------------------------

        st.subheader("Con fracciones")

        denominador = denominador_del_salto(
            movimiento["salto_elegido"]
        )

        num_desde, den = como_fraccion_con_denominador(
            desde,
            denominador
        )

        num_salto, _ = como_fraccion_con_denominador(
            magnitud,
            denominador
        )

        num_hasta, _ = como_fraccion_con_denominador(
            hasta,
            denominador
        )

        operacion_fraccion = (
            f"{num_desde}/{den} "
            f"{signo} "
            f"{num_salto}/{den} "
            f"= "
            f"{num_hasta}/{den}"
        )

        with st.container(border=True):

            st.markdown(
                f'<div class="operacion">'
                f'{operacion_fraccion}'
                f'</div>',
                unsafe_allow_html=True
            )

        # -------------------------------------------------
        # EQUIVALENCIA OPCIONAL
        # -------------------------------------------------

        resultado_simplificado = Fraction(hasta)

        if (
            resultado_simplificado.denominator != den
            or resultado_simplificado.numerator != num_hasta
        ):

            mostrar_equivalente = st.checkbox(
                "Mostrar también la fracción equivalente simplificada",
                key="mostrar_equivalente"
            )

            if mostrar_equivalente:

                st.info(
                    f"{num_hasta}/{den} representa la misma cantidad "
                    f"que "
                    f"{resultado_simplificado.numerator}/"
                    f"{resultado_simplificado.denominator}."
                )


# =========================================================
# 7. HISTORIAL OPCIONAL
# =========================================================

if st.session_state.historial:

    st.divider()

    mostrar_historial = st.checkbox(
        "Ver los desplazamientos que hice",
        key="mostrar_historial"
    )

    if mostrar_historial:

        st.subheader("Mi recorrido")

        for numero, paso in enumerate(
            st.session_state.historial,
            start=1
        ):

            desde = decimal_a_texto(paso["desde"])
            hasta = decimal_a_texto(paso["hasta"])

            desplazamiento = paso["desplazamiento"]

            signo = "+" if desplazamiento > 0 else "−"

            magnitud = decimal_a_texto(
                abs(desplazamiento)
            )

            st.write(
                f"**{numero}.** "
                f"{desde} → {hasta} "
                f"({signo}{magnitud})"
            )


# =========================================================
# REINICIAR
# =========================================================

st.divider()

st.button(
    "↺ Reiniciar el recorrido",
    key="boton_reiniciar",
    on_click=reiniciar
)

st.caption(
    "FDP-02 · Recorrer la unidad · "
    "LIM – Laboratorio de Ideas Matemáticas · v0.2"
)

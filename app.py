import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

st.set_page_config(
    page_title="Simulador de Campos y Señales - UdeC",
    page_icon="⚡",
    layout="wide"
)

# ==============================================================================
# PORTADA INSTITUCIONAL
# ==============================================================================
st.title("⚡ Simulador Interactivo de Campos y Señales")
st.markdown("**CADI Matemáticas Especiales — Universidad de Cundinamarca** | **Gestor:** Mgtr. Arley Rodríguez")
st.markdown("**Integrantes:** Daniel Felipe Virguez Mateus • Sheccid Avila Rojas • Daniel Enrique Castro Vargas • Jimmy Andres Nivia Castillo")
st.caption("Acoplamiento matemático paso a paso entre plano complejo, ecuaciones armónicas y síntesis espectral de Fourier.")

# ==============================================================================
# ZONA INTERACTIVA SUPERIOR PARA EL DOCENTE
# ==============================================================================
st.info("👨‍🏫 **Entrada Interactiva:** Ingresa un número complejo z = x + iy (ejemplos: `2+1.5j`, `-3+4i`, `1-2j`) y selecciona la función de mapeo.")

col_in1, col_in2, col_in3 = st.columns([1.5, 1.5, 1])

with col_in1:
    entrada_z = st.text_input("✍️ Número complejo z = x + iy:", value="2 + 1.5j")

with col_in2:
    funcion_mapeo = st.selectbox(
        "🔄 Función compleja de mapeo w = f(z):",
        [
            "Cuadrática: f(z) = z²",
            "Lineal: f(z) = (1 + i)z + (1 - i)",
            "Cúbica: f(z) = z³",
            "Exponencial compleja: f(z) = e^z"
        ]
    )

with col_in3:
    mostrar_malla = st.checkbox("Mostrar vecindad (90°)", value=True)

try:
    texto_limpio = entrada_z.replace(" ", "").replace("i", "j").replace("I", "j").replace("J", "j")
    z_val = complex(texto_limpio)
    x_val, y_val = z_val.real, z_val.imag
except ValueError:
    st.error("⚠️ Formato inválido. Usa la forma `x + yj` (ejemplo: `2 + 1.5j`).")
    z_val = complex(2.0, 1.5)
    x_val, y_val = 2.0, 1.5

st.divider()

# ==============================================================================
# PESTAÑAS DE LOS 3 MÓDULOS + SUSTENTACIÓN
# ==============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "1️⃣ Números Complejos y Mapeo Conforme",
    "2️⃣ Verificación Armónica y Líneas de Flujo",
    "3️⃣ Síntesis de Fourier",
    "🔗 Acoplamiento Matemático (Sustentación)"
])

# ------------------------------------------------------------------------------
# MÓDULO 1: NÚMEROS COMPLEJOS Y MAPEO CONFORME
# ------------------------------------------------------------------------------
with tab1:
    st.subheader("Módulo 1: Transformación Geométrica y Procedimiento Analítico")

    def aplicar_f(z_in):
        if "z²" in funcion_mapeo:
            return z_in ** 2
        elif "Lineal" in funcion_mapeo:
            return (1 + 1j) * z_in + (1 - 1j)
        elif "z³" in funcion_mapeo:
            return z_in ** 3
        else:
            return np.exp(z_in)

    w_val = aplicar_f(z_val)

    r_z = abs(z_val)
    theta_z_rad = np.angle(z_val)
    theta_z_deg = np.degrees(theta_z_rad)

    r_w = abs(w_val)
    theta_w_rad = np.angle(w_val)
    theta_w_deg = np.degrees(theta_w_rad)

    m1, m2, m3, m4 = st.columns(4)
    signo_z = "+" if y_val >= 0 else "-"
    signo_w = "+" if w_val.imag >= 0 else "-"

    m1.metric("Binómica z", f"{x_val:.2f} {signo_z} i{abs(y_val):.2f}")
    m2.metric("Polar de z", f"{r_z:.3f} ∠ {theta_z_deg:.2f}°")
    m3.metric("Imagen w = f(z)", f"{w_val.real:.2f} {signo_w} i{abs(w_val.imag):.2f}")
    m4.metric("Polar de w", f"{r_w:.3f} ∠ {theta_w_deg:.2f}°")

    st.markdown("### 📝 Procedimiento Matemático Paso a Paso")
    
    if "z²" in funcion_mapeo:
        desarrollo_w = (
            f"w = z² = (x² - y²) + i(2xy)\n"
            f"w = [({x_val:.2f})² - ({y_val:.2f})²] + i[2({x_val:.2f})({y_val:.2f})]\n"
            f"w = {w_val.real:.4f} {signo_w} i{abs(w_val.imag):.4f}\n"
            f"Por De Moivre: w = r² · e^(i·2θ) = ({r_z:.3f})² · e^(i·{2*theta_z_rad:.4f}) = {r_w:.4f} · e^(i·{theta_w_rad:.4f})"
        )
    elif "Lineal" in funcion_mapeo:
        desarrollo_w = (
            f"w = (1 + i)z + (1 - i)\n"
            f"w = (1 + i)({x_val:.2f} {signo_z} i{abs(y_val):.2f}) + (1 - i)\n"
            f"w = {w_val.real:.4f} {signo_w} i{abs(w_val.imag):.4f}"
        )
    elif "z³" in funcion_mapeo:
        desarrollo_w = (
            f"w = z³ = (x³ - 3xy²) + i(3x²y - y³)\n"
            f"w = {w_val.real:.4f} {signo_w} i{abs(w_val.imag):.4f}\n"
            f"Por De Moivre: w = r³ · e^(i·3θ) = {r_w:.4f} · e^(i·{theta_w_rad:.4f})"
        )
    else:
        desarrollo_w = (
            f"w = e^z = e^x · (cos(y) + i·sin(y))\n"
            f"w = e^({x_val:.2f}) · (cos({y_val:.2f}) + i·sin({y_val:.2f}))\n"
            f"w = {w_val.real:.4f} {signo_w} i{abs(w_val.imag):.4f}"
        )

    texto_pasos_m1 = f"""
PASO 1: Cálculo del Módulo (r) y Argumento (θ) de z = {x_val:.2f} {signo_z} i{abs(y_val):.2f}
  • r = √(x² + y²) = √(({x_val:.2f})² + ({y_val:.2f})²) = √({x_val**2 + y_val**2:.4f}) = {r_z:.4f}
  • θ = atan2(y, x) = atan2({y_val:.2f}, {x_val:.2f}) = {theta_z_rad:.4f} rad  ({theta_z_deg:.2f}°)

PASO 2: Forma Polar y Exponencial (Fórmula de Euler)
  • Forma Polar:       z = {r_z:.4f} · [cos({theta_z_deg:.2f}°) + i·sin({theta_z_deg:.2f}°)]
  • Forma Exponencial: z = {r_z:.4f} · e^(i · {theta_z_rad:.4f})

PASO 3: Evaluación de la Transformación w = f(z)
{desarrollo_w}
"""
    st.code(texto_pasos_m1, language="text")

    col_z, col_w = st.columns(2)
    delta = 0.5
    t_lado = np.linspace(-delta, delta, 40)
    borde1 = (x_val + t_lado) + 1j * (y_val - delta)
    borde2 = (x_val + delta) + 1j * (y_val + t_lado)
    borde3 = (x_val - t_lado) + 1j * (y_val + delta)
    borde4 = (x_val - delta) + 1j * (y_val - t_lado)
    cuadro_z = np.concatenate([borde1, borde2, borde3, borde4])
    cuadro_w = aplicar_f(cuadro_z)

    with col_z:
        fig_z, ax_z = plt.subplots(figsize=(5.5, 4.2))
        lim_z = max(r_z * 1.4, 4.0)
        ax_z.axhline(0, color='black', lw=1)
        ax_z.axvline(0, color='black', lw=1)
        ax_z.quiver(0, 0, x_val, y_val, angles='xy', scale_units='xy', scale=1, color='#1f77b4', lw=2.5, label='Vector z')
        if mostrar_malla:
            ax_z.plot(cuadro_z.real, cuadro_z.imag, 'g--', lw=1.8, label='Vecindad original (90°)')
        ax_z.set_xlim(-lim_z, lim_z)
        ax_z.set_ylim(-lim_z, lim_z)
        ax_z.set_title("Plano Original Z (x, y)")
        ax_z.set_xlabel("Re(z) = x")
        ax_z.set_ylabel("Im(z) = y")
        ax_z.grid(True, alpha=0.4)
        ax_z.legend(loc='upper left')
        st.pyplot(fig_z)

    with col_w:
        fig_w, ax_w = plt.subplots(figsize=(5.5, 4.2))
        lim_w = max(r_w * 1.4, np.max(np.abs(cuadro_w)) * 1.2, 4.0)
        ax_w.axhline(0, color='black', lw=1)
        ax_w.axvline(0, color='black', lw=1)
        ax_w.quiver(0, 0, w_val.real, w_val.imag, angles='xy', scale_units='xy', scale=1, color='#d62728', lw=2.5, label='Vector w = f(z)')
        if mostrar_malla:
            ax_w.plot(cuadro_w.real, cuadro_w.imag, 'm-', lw=2, label='Vecindad transformada (Conserva 90°)')
        ax_w.set_xlim(-lim_w, lim_w)
        ax_w.set_ylim(-lim_w, lim_w)
        ax_w.set_title("Plano Transformado W (u, v)")
        ax_w.set_xlabel("Re(w) = u(x,y)")
        ax_w.set_ylabel("Im(w) = v(x,y)")
        ax_w.grid(True, alpha=0.4)
        ax_w.legend(loc='upper left')
        st.pyplot(fig_w)

# ------------------------------------------------------------------------------
# MÓDULO 2: VERIFICACIÓN ARMÓNICA Y LÍNEAS DE FLUJO
# ------------------------------------------------------------------------------
with tab2:
    st.subheader("Módulo 2: Ecuaciones de Cauchy-Riemann, Armonicidad y Curvas de Nivel")

    x_s, y_s = sp.symbols('x y', real=True)
    z_s = x_s + sp.I * y_s

    if "z²" in funcion_mapeo:
        f_sym = z_s ** 2
    elif "Lineal" in funcion_mapeo:
        f_sym = (1 + sp.I) * z_s + (1 - sp.I)
    elif "z³" in funcion_mapeo:
        f_sym = z_s ** 3
    else:
        f_sym = sp.exp(z_s)

    u_sym = sp.expand(sp.re(f_sym))
    v_sym = sp.expand(sp.im(f_sym))

    ux = sp.diff(u_sym, x_s)
    uy = sp.diff(u_sym, y_s)
    vx = sp.diff(v_sym, x_s)
    vy = sp.diff(v_sym, y_s)

    uxx = sp.diff(ux, x_s)
    uyy = sp.diff(uy, y_s)
    vxx = sp.diff(vx, x_s)
    vyy = sp.diff(vy, y_s)

    lap_u = sp.simplify(uxx + uyy)
    lap_v = sp.simplify(vxx + vyy)

    cumple_cr = (sp.simplify(ux - vy) == 0) and (sp.simplify(uy + vx) == 0)
    es_armonica = (lap_u == 0) and (lap_v == 0)

    col_cr1, col_cr2 = st.columns([1.15, 1.25])

    with col_cr1:
        st.markdown("### 📝 Procedimiento Algebraico Paso a Paso")
        texto_pasos_m2 = f"""
PASO 1: Separación en Parte Real u(x,y) e Imaginaria v(x,y)
  • u(x,y) = {u_sym}
  • v(x,y) = {v_sym}

PASO 2: Derivadas Parciales de Primer Orden (Cauchy-Riemann)
  • ∂u/∂x = {ux}    |    ∂v/∂y = {vy}   --> ¿Iguales? {sp.simplify(ux - vy) == 0}
  • ∂u/∂y = {uy}    |   -∂v/∂x = {-vx}  --> ¿Iguales? {sp.simplify(uy + vx) == 0}
  => CONCLUSIÓN: Cumple Cauchy-Riemann = {cumple_cr} (Función Analítica)

PASO 3: Segundas Derivadas y Ecuación de Laplace (∇²u = 0, ∇²v = 0)
  • ∂²u/∂x² = {uxx}   y   ∂²u/∂y² = {uyy}
  • ∇²u = ({uxx}) + ({uyy}) = {lap_u}

  • ∂²v/∂x² = {vxx}   y   ∂²v/∂y² = {vyy}
  • ∇²v = ({vxx}) + ({vyy}) = {lap_v}
  => CONCLUSIÓN: Funciones Armónicas Conjugadas = {es_armonica}
"""
        st.code(texto_pasos_m2, language="text")

    with col_cr2:
        st.markdown("### Curvas de Nivel: Campo Potencial vs. Líneas de Flujo")
        grid = np.linspace(-3, 3, 300)
        X, Y = np.meshgrid(grid, grid)
        u_func = sp.lambdify((x_s, y_s), u_sym, 'numpy')
        v_func = sp.lambdify((x_s, y_s), v_sym, 'numpy')

        fig_cr, ax_cr = plt.subplots(figsize=(6.2, 4.8))
        ax_cr.contour(X, Y, u_func(X, Y), levels=14, colors='#1f77b4', linestyles='solid', linewidths=1.3)
        ax_cr.contour(X, Y, v_func(X, Y), levels=14, colors='#ff7f0e', linestyles='dashed', linewidths=1.3)

        ax_cr.scatter([x_val], [y_val], color='red', s=70, zorder=5, label=f'Punto z = ({x_val:.1f}, {y_val:.1f})')
        ax_cr.plot([], [], color='#1f77b4', linestyle='solid', label='u(x,y) = c (Equipotencial)')
        ax_cr.plot([], [], color='#ff7f0e', linestyle='dashed', label='v(x,y) = k (Líneas de Flujo)')

        ax_cr.set_title("Red Ortogonal de Campo Armónico (Cruce a 90°)")
        ax_cr.set_xlabel("x")
        ax_cr.set_ylabel("y")
        ax_cr.grid(True, alpha=0.3)
        ax_cr.legend(loc='upper right', fontsize=8.5)
        st.pyplot(fig_cr)

# ------------------------------------------------------------------------------
# MÓDULO 3: SÍNTESIS DE FOURIER
# ------------------------------------------------------------------------------
with tab3:
    st.subheader("Módulo 3: Reconstrucción Espectral mediante Series de Fourier")

    col_f1, col_f2, col_f3 = st.columns([1.2, 1.5, 1])
    with col_f1:
        tipo_onda = st.selectbox(
            "Selecciona la señal periódica:",
            ["Onda Cuadrada", "Diente de Sierra", "Onda Triangular"]
        )
    with col_f2:
        N_armonicos = st.slider("Número de armónicos (N):", min_value=1, max_value=60, value=7, step=1)
    with col_f3:
        amplitud = st.number_input("Amplitud A:", min_value=1.0, max_value=10.0, value=1.0, step=0.5)

    t = np.linspace(-np.pi, np.pi, 1500)
    f_reconstruida = np.zeros_like(t)
    armonicos_freq = []
    armonicos_amp = []
    terminos_str = []

    if tipo_onda == "Onda Cuadrada":
        f_original = amplitud * np.sign(np.sin(t))
        for n in range(1, N_armonicos + 1):
            if n % 2 != 0:
                bn = (4 * amplitud) / (n * np.pi)
                f_reconstruida += bn * np.sin(n * t)
                armonicos_freq.append(n)
                armonicos_amp.append(abs(bn))
                if len(terminos_str) < 4:
                    terminos_str.append(f"({4*amplitud:.1f}/{n}π)·sin({n}t)")
            else:
                armonicos_freq.append(n)
                armonicos_amp.append(0)
        paso_integral = (
            f"bn = (2/π) · ∫[0 a π] {amplitud:.1f}·sin(nt) dt = ({2*amplitud:.1f}/nπ)·(1 - (-1)^n)\n"
            f"  • Para n par:   bn = 0\n"
            f"  • Para n impar: bn = {4*amplitud:.1f} / (n·π)"
        )

    elif tipo_onda == "Diente de Sierra":
        f_original = (amplitud / np.pi) * t
        for n in range(1, N_armonicos + 1):
            bn = (2 * amplitud * ((-1) ** (n + 1))) / (n * np.pi)
            f_reconstruida += bn * np.sin(n * t)
            armonicos_freq.append(n)
            armonicos_amp.append(abs(bn))
            if len(terminos_str) < 4:
                signo_t = "+" if bn >= 0 else "-"
                terminos_str.append(f"{signo_t} ({2*amplitud:.1f}/{n}π)·sin({n}t)")
        paso_integral = (
            f"bn = (2/π) · ∫[0 a π] ({amplitud:.1f}·t/π)·sin(nt) dt\n"
            f"  • Para todo n: bn = {2*amplitud:.1f} · (-1)^(n+1) / (n·π)"
        )

    else:
        f_original = (2 * amplitud / np.pi) * np.arcsin(np.sin(t))
        for n in range(1, N_armonicos + 1):
            if n % 2 != 0:
                bn = (8 * amplitud * ((-1) ** ((n - 1) // 2))) / ((n * np.pi) ** 2)
                f_reconstruida += bn * np.sin(n * t)
                armonicos_freq.append(n)
                armonicos_amp.append(abs(bn))
                if len(terminos_str) < 4:
                    signo_t = "+" if bn >= 0 else "-"
                    terminos_str.append(f"{signo_t} ({8*amplitud:.1f}/{n**2}π²)·sin({n}t)")
            else:
                armonicos_freq.append(n)
                armonicos_amp.append(0)
        paso_integral = (
            f"bn = (2/π) · ∫[0 a π] (2·{amplitud:.1f}·t/π)·sin(nt) dt\n"
            f"  • Para n impar: bn = {8*amplitud:.1f} · (-1)^((n-1)/2) / (n²·π²)"
        )

    rmse = np.sqrt(np.mean((f_original - f_reconstruida) ** 2))

    st.markdown("### 📝 Desarrollo Analítico de la Serie de Fourier (Paso a Paso)")
    serie_armada = " + ".join(terminos_str).replace("+ -", "- ")
    texto_pasos_m3 = f"""
PASO 1: Análisis de Simetría en [-π, π]
  • Como f(-t) = -f(t) (Simetría Impar), los coeficientes cosenoidales son cero: a0 = 0 y an = 0.

PASO 2: Cálculo Integral de los Coeficientes bn
  • {paso_integral}

PASO 3: Sumatoria Parcial Reconstruida (N = {N_armonicos} armónicos)
  • f_{N_armonicos}(t) = {serie_armada} + ...
  • Error Cuadrático Medio (RMSE) = {rmse:.5f}
"""
    st.code(texto_pasos_m3, language="text")

    g_fourier1, g_fourier2 = st.columns([1.4, 1])

    with g_fourier1:
        fig_f1, ax_f1 = plt.subplots(figsize=(6.5, 4))
        ax_f1.plot(t, f_original, 'k-', lw=1.8, alpha=0.6, label='Señal Original')
        ax_f1.plot(t, f_reconstruida, color='#e6550d', lw=2, label=f'Síntesis de Fourier (N={N_armonicos})')
        ax_f1.set_title(f"Dominio del Tiempo: {tipo_onda}")
        ax_f1.set_xlabel("Tiempo / Fase (rad)")
        ax_f1.set_ylabel("Amplitud")
        ax_f1.grid(True, alpha=0.4)
        ax_f1.legend()
        st.pyplot(fig_f1)

    with g_fourier2:
        fig_f2, ax_f2 = plt.subplots(figsize=(5.5, 4))
        ax_f2.stem(armonicos_freq, armonicos_amp, basefmt=" ")
        ax_f2.set_title("Espectro de Amplitudes |bₙ|")
        ax_f2.set_xlabel("Armónico (n)")
        ax_f2.set_ylabel("Magnitud")
        ax_f2.grid(True, alpha=0.4)
        st.pyplot(fig_f2)

# ------------------------------------------------------------------------------
# PESTAÑA 4: ACOPLAMIENTO MATEMÁTICO PARA SUSTENTACIÓN
# ------------------------------------------------------------------------------
with tab4:
    st.subheader("¿Cómo se conectan los 3 módulos matemáticamente?")
    st.markdown("""
    El puente matemático que une todo el simulador es la **Fórmula de Euler** ($e^{i\\theta} = \\cos\\theta + i\\sin\\theta$):
    1. **Plano Complejo y Mapeo Conforme:** Un número $z = x + iy = r e^{i\\theta}$ representa amplitud y fase. Al aplicar una función analítica $w = f(z)$, se conservan los ángulos locales (90°) y se deforman las regiones del plano.
    2. **Ecuaciones Armónicas (Cauchy-Riemann):** Porque $f(z) = u(x,y) + iv(x,y)$ es analítica, sus componentes satisfacen Cauchy-Riemann y la **Ecuación de Laplace** ($\\nabla^2 u = 0, \\nabla^2 v = 0$), generando campos físicos ortogonales (potencial y flujo).
    3. **Síntesis de Fourier:** Cuando un fasor complejo gira en el tiempo ($z(t) = c_n e^{i n \\omega_0 t}$), su proyección sobre los ejes real e imaginario genera las funciones armónicas $\\cos(n\\omega_0 t)$ y $\\sin(n\\omega_0 t)$ que reconstruyen cualquier señal periódica.
    """)
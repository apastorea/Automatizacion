from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


ROOT = Path(__file__).resolve().parent
MAT = ROOT / "Matlab" / "Laboratorio 5"
SIM = MAT / "resultados_puntos_1_2"
DATA = MAT / "datos_experimentales"
OUT = ROOT / "Informe_Lab5_Automatizacion_Pastore.docx"

FOLDERS = {
    "ts1o": DATA / "lab5_identificado_TS1_oscillatory_50mV_zerocorr_final_20261121_174827",
    "ts1d": DATA / "lab5_identificado_TS1_deadbeat_50mV_zerocorr_final_20261121_175752",
    "ts2o": DATA / "lab5_identificado_TS2_oscillatory_50mV_zerocorr_scopefinal_20261121_180202",
    "ts2d": DATA / "lab5_identificado_TS2_deadbeat_50mV_zerocorr_final_20261121_180423",
}

GRAY = "E7E6E6"


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_columns(section, count=2, space_twips=360):
    sect_pr = section._sectPr
    cols = sect_pr.find(qn("w:cols"))
    if cols is None:
        cols = OxmlElement("w:cols")
        sect_pr.append(cols)
    cols.set(qn("w:num"), str(count))
    cols.set(qn("w:space"), str(space_twips))


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run()
    fld_char1 = OxmlElement("w:fldChar")
    fld_char1.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    fld_char2 = OxmlElement("w:fldChar")
    fld_char2.set(qn("w:fldCharType"), "end")
    run._r.extend([fld_char1, instr, fld_char2])


def remove_table_borders(table):
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.find(qn("w:tblBorders"))
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tbl_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        tag = qn(f"w:{edge}")
        element = borders.find(tag)
        if element is None:
            element = OxmlElement(f"w:{edge}")
            borders.append(element)
        element.set(qn("w:val"), "nil")


def configure_footer(section, sdg_position=None, linked=True, reset=False):
    footer = section.footer
    footer.is_linked_to_previous = linked
    if reset:
        for child in list(footer._element):
            footer._element.remove(child)
        footer._element.append(OxmlElement("w:p"))
    if len(footer.tables) == 0:
        table = footer.add_table(rows=1, cols=3, width=Inches(7.25))
        table.autofit = False
        remove_table_borders(table)
        widths = (2.4, 2.45, 2.4)
        for cell, width in zip(table.rows[0].cells, widths):
            cell.width = Inches(width)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        left, center, right = table.rows[0].cells
        add_page_number(center.paragraphs[0])
        right.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        if sdg_position in {"left", "right"}:
            cell = left if sdg_position == "left" else right
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if sdg_position == "left" else WD_ALIGN_PARAGRAPH.RIGHT
            r = p.add_run("SDG")
            r.font.name = "Times New Roman"
            r.font.size = Pt(8)
    footer.paragraphs[0].paragraph_format.space_after = Pt(0)


def configure_section(section, columns=1):
    section.top_margin = Inches(0.55)
    section.bottom_margin = Inches(0.55)
    section.left_margin = Inches(0.62)
    section.right_margin = Inches(0.62)
    section.header_distance = Inches(0.22)
    section.footer_distance = Inches(0.22)
    set_columns(section, columns)
    configure_footer(section)


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def no_split(row):
    tr_pr = row._tr.get_or_add_trPr()
    cant_split = OxmlElement("w:cantSplit")
    tr_pr.append(cant_split)


def add_heading(doc, text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(5 if level == 1 else 3)
    p.paragraph_format.space_after = Pt(2)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if level == 1 else WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(text)
    r.bold = False
    r.font.name = "Times New Roman"
    r.font.size = Pt(9.6 if level == 1 else 9.1)
    r.font.color.rgb = RGBColor.from_string("000000")
    if level == 1:
        r.font.small_caps = True
    else:
        r.italic = True
    return p


def add_body(doc, text, first_indent=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.line_spacing = 1.0
    if first_indent:
        p.paragraph_format.first_line_indent = Inches(0.16)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(8.8)
    return p


def math_run(text):
    run = OxmlElement("m:r")
    value = OxmlElement("m:t")
    value.text = text
    run.append(value)
    return run


def math_fraction(numerator, denominator):
    frac = OxmlElement("m:f")
    num = OxmlElement("m:num")
    num.append(math_run(numerator))
    den = OxmlElement("m:den")
    den.append(math_run(denominator))
    frac.extend([num, den])
    return frac


def add_equation(doc, expression, number, width=None):
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    remove_table_borders(table)
    eq_cell, num_cell = table.rows[0].cells
    eq_cell.width = Inches(2.95)
    num_cell.width = Inches(0.32)
    p = eq_cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    math_para = OxmlElement("m:oMathPara")
    math_para_pr = OxmlElement("m:oMathParaPr")
    justification = OxmlElement("m:jc")
    justification.set(qn("m:val"), "center")
    math_para_pr.append(justification)
    math_para.append(math_para_pr)
    equation = OxmlElement("m:oMath")
    for kind, value in expression:
        if kind == "text":
            equation.append(math_run(value))
        elif kind == "frac":
            equation.append(math_fraction(value[0], value[1]))
    math_para.append(equation)
    p._p.append(math_para)
    p = num_cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p.add_run(f"({number})")
    r.font.name = "Times New Roman"
    r.font.size = Pt(8.8)
    return table


def add_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_together = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(7.8)
    return p


def add_figure(doc, path, caption, width=3.35):
    if not Path(path).exists():
        raise FileNotFoundError(path)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_together = True
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(0)
    p.add_run().add_picture(str(path), width=Inches(width))
    add_caption(doc, caption)


def add_full_width_section(doc):
    section = doc.add_section(WD_SECTION.CONTINUOUS)
    configure_section(section, columns=1)
    return section


def add_two_column_section(doc):
    section = doc.add_section(WD_SECTION.CONTINUOUS)
    configure_section(section, columns=2)
    return section


def add_table(doc, headers, rows, widths=None, font_size=7.4):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    hdr = table.rows[0]
    set_repeat_table_header(hdr)
    for i, h in enumerate(headers):
        cell = hdr.cells[i]
        cell.text = h
        set_cell_shading(cell, "FFFFFF")
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        for r in cell.paragraphs[0].runs:
            r.bold = True
            r.font.color.rgb = RGBColor(0, 0, 0)
            r.font.name = "Times New Roman"
            r.font.size = Pt(font_size)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for ridx, row_data in enumerate(rows):
        row = table.add_row()
        no_split(row)
        for i, value in enumerate(row_data):
            cell = row.cells[i]
            cell.text = str(value)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            set_cell_shading(cell, "FFFFFF")
            for para in cell.paragraphs:
                para.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for r in para.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(font_size)
        if widths:
            for i, w in enumerate(widths):
                row.cells[i].width = Inches(w)
                hdr.cells[i].width = Inches(w)
    return table


doc = Document()
configure_section(doc.sections[0], columns=1)

styles = doc.styles
styles["Normal"].font.name = "Times New Roman"
styles["Normal"].font.size = Pt(8.8)
styles["Normal"].paragraph_format.space_after = Pt(1.5)
styles["Normal"].paragraph_format.line_spacing = 1.0

# Encabezado de artículo, coherente con el informe del Laboratorio 4.
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(4)
r = p.add_run("Síntesis directa de Truxal–Ragazzini para una planta analógica")
r.font.name = "Times New Roman"
r.font.size = Pt(19)
r.bold = False
r.font.color.rgb = RGBColor.from_string("000000")

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(1)
r = p.add_run("Aldo Pastore")
r.font.name = "Times New Roman"
r.font.size = Pt(11)
r.bold = False

for line in [
    "Automatización – Ingeniería Electrónica",
    "Facultad de Ciencias y Tecnología",
    "Universidad Católica ‘Nuestra Señora de la Asunción’ – Asunción, Paraguay",
    "aldo.pastore@uc.edu.py",
]:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    rr = p.add_run(line)
    rr.font.name = "Times New Roman"
    rr.font.size = Pt(8.8)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p.paragraph_format.space_before = Pt(7)
p.paragraph_format.space_after = Pt(3)
r = p.add_run("Resumen—")
r.bold = True
r.font.name = "Times New Roman"
r.font.size = Pt(8.8)
r = p.add_run(
    "Se diseñaron e implementaron cuatro controladores digitales por síntesis directa para la planta analógica identificada en el laboratorio anterior. Se emplearon dos períodos de muestreo, 5,750 ms y 1,920 ms, y en cada caso se comparó la respuesta de tiempo mínimo F(z)=z⁻¹ con una formulación deadbeat que incorpora el cero estable de la planta para eliminar la cola alternante del mando. Los cuatro ensayos utilizaron el mismo escalón físico de 50 mV. La implementación en un PSoC 5LP conservó 256 muestras por ejecución, 32 de ellas de pretrigger, y aplicó una corrección de cero calculada antes de cerrar el lazo. Los RMSE de salida respecto del modelo identificado quedaron entre 2,705 y 3,194 mV, sin banderas de saturación, temporización o rango ADC. Al reducir Tₛ, el controlador oscilatorio elevó el pico de mando hasta 0,415 V y el osciloscopio mostró excursiones continuas entre −0,144 y 0,456 V; la alternativa deadbeat redujo el pico aplicado a 0,277 V y evitó la alternancia determinista. Los resultados confirman que una respuesta exacta en los instantes de muestreo no garantiza un comportamiento continuo aceptable entre muestras."
)
r.font.name = "Times New Roman"
r.font.size = Pt(8.8)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p.paragraph_format.space_after = Pt(5)
r = p.add_run("Palabras clave—")
r.bold = True
r = p.add_run("síntesis directa, Truxal–Ragazzini, deadbeat, oscilación intramuestra, control digital, PSoC.")
for rr in p.runs:
    rr.font.name = "Times New Roman"
    rr.font.size = Pt(8.8)

add_two_column_section(doc)

add_heading(doc, "I. OBJETIVOS Y ALCANCE")
add_body(doc, "El objetivo fue diseñar un controlador digital por el método analítico de Truxal–Ragazzini, obtener una respuesta de tiempo mínimo y estudiar qué ocurre entre instantes de muestreo. La consigna exige dos períodos de muestreo y, para cada uno, un controlador que impone F(z)=z⁻¹ y otro que satisface las condiciones de respuesta deadbeat sin oscilaciones intramuestra.")
add_body(doc, "La aclaración posterior de la cátedra confirmó que debían implementarse las cuatro configuraciones. También indicó que el seguimiento debía evaluarse con referencia escalón, que el diseño debía basarse en el mejor modelo identificado y que la comparación entre MATLAB y el montaje debía conservar la misma amplitud. En consecuencia, todos los resultados de este informe corresponden a un escalón de 50 mV, sin reescalar curvas para hacerlas coincidir.")

add_heading(doc, "II. MODELO DE LA PLANTA")
add_heading(doc, "II-A. Modelo continuo identificado", 2)
add_body(doc, "La planta está formada por dos etapas inversoras pasabajos. El modelo nominal se conservó como referencia, pero el diseño se realizó con los parámetros identificados y validados en el Laboratorio 4: K=1,002941, τ₁=9,06915 ms y τ₂=0,774399 ms.")
add_equation(doc, [("text", "G(s)="), ("frac", ("1,002941", "(1+0,00906915s)(1+0,000774399s)"))], 1)
add_body(doc, "Al desarrollar el denominador se obtiene G(s)=142805,198/(s²+1401,588s+142386,440). Sus polos están en −110,264 y −1291,324 rad/s. El ancho de banda es 109,216 rad/s, equivalente a 17,382 Hz; la planta es estable, estrictamente propia y sin ceros finitos.")

add_heading(doc, "II-B. Selección de los períodos de muestreo", 2)
add_body(doc, "Se adoptaron frecuencias de muestreo de aproximadamente diez y treinta veces el ancho de banda. Los valores ideales se ajustaron al reloj de 100 kHz disponible en el PSoC. Así se obtuvieron Tₛ₁=5,750 ms (173,913 Hz) y Tₛ₂=1,920 ms (520,833 Hz), con registros Period iguales a 574 y 191, respectivamente.")
add_table(doc, ["Caso", "Criterio", "Tₛ (ms)", "fₛ (Hz)", "Period"], [
    ["TS1", "10 fB", "5,750", "173,913", "574"],
    ["TS2", "30 fB", "1,920", "520,833", "191"],
], font_size=7.2)
add_caption(doc, "Tabla I. Períodos de muestreo implementados.")

add_heading(doc, "III. SÍNTESIS DIRECTA")
add_heading(doc, "III-A. Relación fundamental", 2)
add_body(doc, "Para realimentación unitaria, la función de transferencia de lazo cerrado es F(z)=C(z)Gd(z)/[1+C(z)Gd(z)]. Despejando el controlador se obtiene la expresión de síntesis directa:")
add_equation(doc, [("text", "C(z)="), ("frac", ("F(z)", "G_d(z)[1−F(z)]"))], 2)
add_body(doc, "La elección de F(z) debe respetar causalidad, estabilidad y realizabilidad. También debe impedir que la inversión de Gd(z) introduzca polos inestables o una acción de control que continúe alternando una vez alcanzada la salida deseada.")

add_heading(doc, "III-B. Respuesta de una muestra con oscilación intramuestra", 2)
add_body(doc, "La primera elección fue Fosc(z)=z⁻¹. En las muestras, la salida alcanza exactamente el valor final después de un retardo. Sin embargo, el cero de la planta discreta queda en el denominador de U(z)/R(z). Como ese cero es negativo, el mando presenta una cola alternante. El retenedor mantiene cada valor durante Tₛ y la planta continua evoluciona dentro de cada intervalo; por eso la salida física puede oscilar aun cuando y[k] parezca ideal.")
add_equation(doc, [("text", "F_osc(z)=z⁻¹")], 3)

add_heading(doc, "III-C. Restricción deadbeat", 2)
add_body(doc, "Para eliminar la alternancia se incorporó el numerador estable de Gd(z) en la respuesta deseada. Si el numerador de la planta es b₁z+b₂, se eligió:")
add_equation(doc, [("text", "F_db(z)="), ("frac", ("b₁z+b₂", "(b₁+b₂)z²"))], 4)
add_body(doc, "Con esta estructura, Fdb(z)/Gd(z) no conserva el cero de planta en el denominador y el mando se vuelve constante en tiempo finito para una referencia escalón ideal. La respuesta ya no es exactamente z⁻¹, pero desaparece el mecanismo que produce el rizado determinista entre muestras.")

add_heading(doc, "IV. CONTROLADORES OBTENIDOS")
add_body(doc, "Los cuatro controladores se expresaron en una estructura racional de segundo orden:")
add_equation(doc, [("text", "C(z)="), ("frac", ("b₀+b₁z⁻¹+b₂z⁻²", "1+a₁z⁻¹+a₂z⁻²"))], 5)
add_body(doc, "Con e[k]=r[k]−y[k], la implementación se realizó mediante la ecuación en diferencias:")
add_equation(doc, [("text", "u[k]=−a₁u[k−1]−a₂u[k−2]+b₀e[k]+b₁e[k−1]+b₂e[k−2]")], 6)

add_full_width_section(doc)
add_table(doc,
    ["Diseño", "b₀", "b₁", "b₂", "a₁", "a₂"],
    [
        ["TS1 oscilatorio", "2,373542", "−1,260476", "0,000751", "−0,882907", "−0,117093"],
        ["TS1 deadbeat", "2,124749", "−1,128353", "0,000672", "−0,895181", "−0,104819"],
        ["TS2 oscilatorio", "8,101351", "−7,234509", "0,549351", "−0,579642", "−0,420358"],
        ["TS2 deadbeat", "5,703740", "−5,093441", "0,386769", "−0,704048", "−0,295952"],
    ], font_size=8.0)
add_caption(doc, "Tabla II. Coeficientes con la precisión utilizada en la implementación.")

add_two_column_section(doc)
add_body(doc, "Las simulaciones se realizaron con el mismo escalón de 50 mV empleado en el montaje. En TS1, el diseño oscilatorio presentó 7,653 % de sobrepaso y 118,7 mV de pico de mando; el deadbeat anuló el sobrepaso y redujo el pico previsto a 106,2 mV. En TS2, la mayor frecuencia de muestreo permitió una respuesta más rápida, pero F(z)=z⁻¹ exigió 405,1 mV y generó un mínimo de −126,9 mV. La variante deadbeat redujo el máximo previsto a 285,2 mV.")

add_figure(doc, SIM / "respuesta_Ts1_oscilatorio.png", "Figura 1. Simulación continua y muestras para TS1, diseño oscilatorio.")
add_figure(doc, SIM / "respuesta_Ts1_deadbeat.png", "Figura 2. Simulación para TS1 con restricción deadbeat.")
add_figure(doc, SIM / "respuesta_Ts2_oscilatorio.png", "Figura 3. Simulación para TS2: la respuesta muestreada oculta la excursión intramuestra.")
add_figure(doc, SIM / "respuesta_Ts2_deadbeat.png", "Figura 4. Simulación para TS2 con eliminación del rizado determinista.")

add_heading(doc, "IV-A. Polos y ceros", 2)
add_body(doc, "Los diagramas se exportaron individualmente, con límites ajustados y etiquetas de mayor tamaño. Esta presentación evita superponer las cuatro configuraciones en una sola figura. Los polos de lazo cerrado permanecen dentro del círculo unidad; los ceros negativos de las plantas discretas, −0,1171 para TS1 y −0,4204 para TS2, explican la alternancia que aparece al invertir la planta sin imponer la condición deadbeat.")
add_figure(doc, SIM / "pz_lazo_Ts1_oscilatorio.png", "Figura 5. Polos y ceros del lazo cerrado, TS1 oscilatorio.")
add_figure(doc, SIM / "pz_lazo_Ts1_deadbeat.png", "Figura 6. Polos y ceros del lazo cerrado, TS1 deadbeat.")
add_figure(doc, SIM / "pz_lazo_Ts2_oscilatorio.png", "Figura 7. Polos y ceros del lazo cerrado, TS2 oscilatorio.")
add_figure(doc, SIM / "pz_lazo_Ts2_deadbeat.png", "Figura 8. Polos y ceros del lazo cerrado, TS2 deadbeat.")

add_heading(doc, "V. IMPLEMENTACIÓN EN PSoC")
add_body(doc, "Se duplicó el proyecto del Laboratorio 4 con etiquetas Lab5 y se conservó el esquema de adquisición y actuación ya calibrado. No se utilizó ADC_SAR_Seq, ya que ese periférico corresponde a una práctica posterior. La lectura se realiza con el SAR existente y el mando se genera mediante las dos ramas del VDAC y sus acondicionamientos analógicos.")
add_body(doc, "El temporizador selecciona 575 o 192 cuentas, según el caso. Cada ejecución almacena 256 muestras; las primeras 32 se utilizan como pretrigger. La referencia permanece en cero durante ese intervalo y luego cambia a 50 mV. El algoritmo registra las señales solicitada y aplicada, las cuentas del ADC, el tiempo de interrupción, el intervalo entre muestras y banderas de rango, saturación, cálculo e incumplimiento temporal.")
add_body(doc, "El límite conservador del mando fue ±1 V. Ninguna de las cuatro configuraciones lo alcanzó. Al concluir la captura, el firmware lleva la salida a cero. La última compilación Release ocupó 9704 bytes de Flash (3,7 %) y 11817 bytes de SRAM (18,0 %), con 2048 bytes de pila y 128 bytes de heap.")

add_heading(doc, "V-A. Calibración y tratamiento del cero", 2)
add_body(doc, "La conversión del ADC se mantuvo explícita: y=(VADC−2,353802)/0,210252. La caracterización del actuador fue J5=0,98171u+0,017209 V, con RMSE de 0,967 mV. No se normalizaron las curvas experimentales ni se ajustó su amplitud después de adquirirlas.")
add_body(doc, "Antes de activar cada controlador se promediaron las 32 muestras de pretrigger. Ese promedio se restó de y durante el control, pero se conservó en el encabezado de la captura. Los cuatro ceros medidos fueron 0,469; 4,844; −4,219 y −49,938 mV. La corrección afecta el origen de seguimiento, no la amplitud: tanto MATLAB como el PSoC reciben un incremento de referencia de 50 mV. El caso TS2 deadbeat presentó el mayor desplazamiento y por ello se informa de manera separada, en lugar de ocultarlo mediante una normalización gráfica.")

add_heading(doc, "VI. PROCEDIMIENTO EXPERIMENTAL")
add_body(doc, "El canal 1 del RIGOL DS1202Z-E se conectó a J5 para medir el mando físico u(t), y el canal 2 a J7 para observar la salida continua y(t). Las sondas se mantuvieron en 10×, con acoplamiento DC y límite de ancho de banda. MATLAB armó el osciloscopio después del mensaje de inicio del PSoC y esperó el escalón programado tres segundos más tarde. Cada ensayo guardó la pantalla, las dos trazas del osciloscopio y las 256 muestras UART.")
add_body(doc, "Las comparaciones modelo–experimento se efectuaron con el modelo identificado, el período realmente implementado y el escalón de 50 mV. El osciloscopio muestra el comportamiento continuo; la telemetría corresponde a los instantes kTₛ. Esta distinción es esencial para evaluar las oscilaciones intramuestra solicitadas por la práctica.")

add_heading(doc, "VII. RESULTADOS")
add_full_width_section(doc)
add_table(doc,
    ["Diseño", "Cero previo (mV)", "Pico y (mV)", "Valor final (mV)", "Pico |u| (mV)", "RMSE y (mV)", "Banderas"],
    [
        ["TS1 oscilatorio", "0,469", "54", "49,984", "123", "3,194", "0"],
        ["TS1 deadbeat", "4,844", "60", "49,984", "123", "2,705", "0"],
        ["TS2 oscilatorio", "−4,219", "59", "49,953", "415", "2,724", "0"],
        ["TS2 deadbeat", "−49,938", "61", "50,156", "277", "2,759", "0"],
    ], font_size=7.8)
add_caption(doc, "Tabla III. Resultados experimentales con referencia común de 50 mV.")

add_two_column_section(doc)
add_body(doc, "Los valores finales difieren de la referencia entre −0,047 y +0,156 mV. Los RMSE de salida permanecen alrededor de 3 mV, magnitud compatible con la resolución efectiva y el ruido ya observados en la cadena de lectura. No se registró ninguna bandera de saturación, intervalo, tiempo de CPU, rango ADC o cálculo numérico.")
add_body(doc, "En TS1, ambos controladores aplicaron un máximo cuantizado de 123 mV. La diferencia principal apareció en el sobrepaso y en la persistencia del rizado: el deadbeat redujo el pico a 60 mV y el recorrido estacionario pico a pico de 17 a 11 mV. El modelo y el experimento conservaron el mismo escalón; por ello la comparación del esfuerzo de control no depende de una normalización.")
add_body(doc, "En TS2, la diferencia fue más marcada. El diseño oscilatorio solicitó una acción inicial próxima a 0,405 V y aplicó 0,415 V; el RIGOL midió −0,144 a 0,456 V en J5. El deadbeat aplicó 0,277 V y el RIGOL registró −0,008 a 0,312 V. Así, la restricción deadbeat redujo 33,3 % el pico aplicado medido por el PSoC y 29,8 % la excursión positiva observada en J5.")

for pair_index, pair in enumerate([
    [("ts1o", 9, "TS1 oscilatorio"), ("ts1d", 10, "TS1 deadbeat")],
    [("ts2o", 11, "TS2 oscilatorio"), ("ts2d", 12, "TS2 deadbeat")],
]):
    add_full_width_section(doc)
    for key, fig_no, title in pair:
        add_figure(doc, FOLDERS[key] / "comparacion_matlab_experimento_completa.png",
                   f"Figura {fig_no}. Comparación MATLAB–experimento para {title}. La referencia común es 50 mV; se muestran la salida y el mando solicitado y aplicado.", width=4.35)
    if pair_index == 0:
        doc.add_page_break()
    else:
        add_two_column_section(doc)

add_heading(doc, "VII-A. Evidencia continua de oscilación intramuestra", 2)
add_body(doc, "Las Figuras 9–12 comparan valores muestreados y, por sí solas, no describen todo lo que sucede entre kTₛ. La captura del osciloscopio aporta esa información. En TS2 oscilatorio, CH1 recorrió 0,600 V entre mínimo y máximo, mientras CH2 alcanzó 76 mV aun cuando las muestras del PSoC convergieron a 49,953 mV. En TS2 deadbeat, la excursión de CH1 se redujo a 0,320 V y CH2 alcanzó 69,6 mV. El resultado coincide con la finalidad didáctica de la práctica: F(z)=z⁻¹ cumple la trayectoria en las muestras, pero no controla por sí sola el comportamiento continuo del montaje.")
add_figure(doc, FOLDERS["ts2o"] / "pantalla.png", "Figura 13. Osciloscopio, TS2 oscilatorio: CH1/J5 en amarillo y CH2/J7 en cian.")
add_figure(doc, FOLDERS["ts2d"] / "pantalla.png", "Figura 14. Osciloscopio, TS2 deadbeat bajo las mismas condiciones.")

add_heading(doc, "VII-B. Alcance de los tiempos de establecimiento", 2)
add_body(doc, "Los tiempos teóricos de establecimiento, entre 3,128 y 10,435 ms, describen el modelo lineal. En las capturas digitales, una banda estricta del 10 % resulta sensible a la cuantización de la salida: los recorridos estacionarios pico a pico son de 5 a 17 mV para una referencia de 50 mV. Por ese motivo, el algoritmo de evaluación reporta tiempos aparentes de 0,255 a 1,259 s. Estos valores no representan un transitorio lento de la planta; indican que la resolución experimental no permite permanecer de manera continua dentro de una banda estrecha. El pico, el promedio final y el RMSE son métricas más representativas para esta escala de ensayo.")

section = doc.add_section(WD_SECTION.NEW_PAGE)
configure_section(section, columns=2)
configure_footer(section, sdg_position="right", linked=False, reset=True)

add_heading(doc, "VIII. DISCUSIÓN")
add_body(doc, "El efecto del período de muestreo no puede resumirse como ‘más rápido es mejor’. TS2 ofrece una trayectoria muestreada más veloz, pero obliga a invertir con mayor intensidad la dinámica discreta. En el diseño oscilatorio, el coeficiente b₀ crece de 2,374 a 8,101 y el pico experimental de mando pasa de 123 a 415 mV. La misma aceleración hace más visible la dinámica intermuestreo.")
add_body(doc, "La formulación deadbeat no elimina el rizado causado por cuantización y ruido, pero sí la cola alternante determinista asociada al cero negativo de la planta. Esto explica que el experimento no produzca una línea perfectamente lisa y, al mismo tiempo, que el esfuerzo máximo de TS2 caiga de 415 a 277 mV. La mejora se verifica tanto en la telemetría como en la señal continua de J5.")
add_body(doc, "La corrección de cero merece una separación conceptual. Se utilizó para definir y=0 antes del escalón en cada ejecución, no para modificar después las curvas o su ganancia. Los valores originales permanecen documentados y las simulaciones emplean exactamente 50 mV. De este modo, las comparaciones de salida y esfuerzo de control responden a condiciones equivalentes, atendiendo las dos observaciones formuladas en la corrección del informe de referencia.")
add_body(doc, "La principal limitación sigue siendo la resolución de la medición referida a la salida. Con escalones pequeños, una cuenta del ADC representa una fracción importante de la banda de establecimiento. Aumentar la referencia mejoraría la relación señal–ruido, pero también elevaría el mando de TS2 oscilatorio; por eso se mantuvo 50 mV para los cuatro casos y se evitó introducir una segunda amplitud que invalidara la comparación.")

add_heading(doc, "IX. CONCLUSIONES")
add_body(doc, "El método de síntesis directa permitió construir cuatro controladores estables a partir del modelo identificado G(s). Los períodos de 5,750 y 1,920 ms representan aproximadamente diez y treinta muestras por ciclo asociado al ancho de banda. En ambos casos, F(z)=z⁻¹ alcanzó la referencia en los instantes de muestreo, pero conservó una cola alternante en el mando. La incorporación del cero estable de la planta en Fdb(z) eliminó ese mecanismo y produjo una respuesta deadbeat de control.")
add_body(doc, "Las cuatro implementaciones siguieron el mismo escalón de 50 mV y finalizaron sin banderas. Los valores estacionarios quedaron entre 49,953 y 50,156 mV, y los RMSE de salida entre 2,705 y 3,194 mV. En TS2, donde la diferencia es más evidente, el mando aplicado disminuyó de 0,415 V a 0,277 V al imponer la restricción deadbeat; simultáneamente, la excursión continua medida en J5 se redujo de 0,600 V a 0,320 V. La alternativa oscilatoria alcanzó 76 mV en la salida continua, aunque las muestras convergían prácticamente a 50 mV.")
add_body(doc, "El ensayo confirma que el cumplimiento de una función de transferencia discreta no basta para juzgar el comportamiento físico. La respuesta entre muestras, el cero de la planta y el esfuerzo de control condicionan la elección final. Para este montaje, el deadbeat con Tₛ=1,920 ms ofrece el compromiso más favorable: conserva la rapidez asociada al mayor muestreo, reduce alrededor de un tercio el pico de mando respecto del diseño oscilatorio y evita las oscilaciones deterministas que motivan la práctica. La corrección de cero por pretrigger fue necesaria —entre 0,469 y −49,938 mV según el reinicio— y quedó registrada sin alterar la amplitud común de las comparaciones.")

add_heading(doc, "REFERENCIAS")
refs = [
    "[1] K. Ogata, Sistemas de control en tiempo discreto, 2.ª ed. Prentice Hall, 1996.",
    "[2] G. F. Franklin, J. D. Powell y M. L. Workman, Digital Control of Dynamic Systems, 3rd ed. Addison-Wesley, 1998.",
]
for ref in refs:
    p = add_body(doc, ref, first_indent=False)
    p.paragraph_format.left_indent = Inches(0.14)
    p.paragraph_format.first_line_indent = Inches(-0.14)

# Metadatos del documento.
doc.core_properties.title = "Síntesis directa de Truxal–Ragazzini para una planta analógica"
doc.core_properties.subject = "Práctica de Laboratorio N.º 5 de Automatización"
doc.core_properties.author = "Aldo Pastore"
doc.core_properties.keywords = "síntesis directa, deadbeat, PSoC, control digital"
doc.core_properties.comments = "Informe generado a partir de los scripts, capturas y métricas verificadas del Laboratorio 5."

doc.save(OUT)
print(OUT)

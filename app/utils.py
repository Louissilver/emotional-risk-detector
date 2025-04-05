from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    Table,
    TableStyle,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    KeepTogether,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io


def gerar_pdf_respostas(df):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20,
        leftMargin=20,
        topMargin=40,
        bottomMargin=20,
    )
    elements = []

    title_style = getSampleStyleSheet()["Title"]
    elements.append(
        Paragraph("Histórico de Respostas - Detector de Burnout Oculto", title_style)
    )

    # Estilo com wrap forçado
    cell_style = ParagraphStyle(
        name="TableCell",
        fontSize=8,
        leading=10,
        wordWrap="CJK",  # força quebra de linha
        spaceAfter=4,
    )

    headers = list(df.columns)
    data = [[Paragraph(h, cell_style) for h in headers]]  # cabeçalhos

    for _, row in df.iterrows():
        formatted_row = []
        for col, val in zip(headers, row):
            text = str(val)
            formatted_row.append(Paragraph(text, cell_style))
        data.append(formatted_row)

    # FORÇAR largura mais estreita na coluna 'message'
    col_widths = []
    for col in headers:
        if col == "message":
            col_widths.append(150)
        elif col == "input":
            col_widths.append(120)
        elif col == "timestamp":
            col_widths.append(70)
        elif col == "emotion":
            col_widths.append(50)
        elif col == "risco_emocional":
            col_widths.append(60)
        elif col == "similarity_score":
            col_widths.append(40)
        else:
            col_widths.append(70)

    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ]
        )
    )

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer


def gerar_pdf_recomendacao(texto: str, emocao: str, risco: str):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=50,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    title = styles["Title"]
    subtitle = ParagraphStyle("Subtitle", parent=normal, fontSize=10, spaceAfter=8)

    elements = []
    elements.append(Paragraph("📄 Recomendação Personalizada", title))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<b>Emoção mais frequente:</b> {emocao}", subtitle))
    elements.append(
        Paragraph(f"<b>Nível de risco emocional predominante:</b> {risco}", subtitle)
    )
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<b>Mensagem gerada pela IA:</b>", subtitle))

    # Divide o texto por quebras de parágrafo e adiciona individualmente
    paragrafos = texto.strip().split("\n\n")
    for p in paragrafos:
        elements.append(Paragraph(p.strip(), normal))
        elements.append(Spacer(1, 8))

    doc.build(elements)
    buffer.seek(0)
    return buffer

from io import BytesIO
from docx import Document
from docx.shared import Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import asyncio
import html

def add_page_border(doc):
    section = doc.sections[0]
    sectPr = section._sectPr

    pgBorders = OxmlElement('w:pgBorders')
    pgBorders.set(qn('w:offsetFrom'), 'page')

    for border in ["top", "left", "bottom", "right"]:
        element = OxmlElement(f'w:{border}')
        element.set(qn('w:val'), 'single')  # simple line
        element.set(qn('w:sz'), '12')       # thickness
        element.set(qn('w:space'), '24')    # spacing
        element.set(qn('w:color'), '000000')  # black color
        pgBorders.append(element)

    sectPr.append(pgBorders)

async def word_generator(type, mavzu, univer, name, user_id, rejalar: list, theme_text: dict):
    name = html.unescape(name)
    univer = html.unescape(univer)

    loop = asyncio.get_event_loop()
    doc = await loop.run_in_executor(None, Document, "Referal.docx")

    # >>> RAMKA QO'SHISH <<<
    add_page_border(doc)

    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            if "TypeType" in run.text:
                run.text = run.text.replace("TypeType", type.upper())
                run.font.name = 'Times New Roman'
                run.font.size = Pt(54)
                run.bold = True
            if "UNIVER,UNIVER,UNIVER,UNIVER" in run.text:
                run.text = run.text.replace("UNIVER,UNIVER,UNIVER,UNIVER", univer.upper())
                run.font.name = 'Times New Roman'
                run.font.size = Pt(16)
            if "ThemeTheme" in run.text:
                run.text = run.text.replace("ThemeTheme", mavzu.title())
                run.font.name = 'Times New Roman'
                run.font.size = Pt(14)
            if "namenamename" in run.text:
                run.text = run.text.replace("namenamename", name.title())
                run.font.name = 'Times New Roman'
                run.font.size = Pt(14)

    def add_new_page(doc):
        doc.add_page_break()

    add_new_page(doc)

    # Rejalar
    reja_heading = doc.add_paragraph("Rejalar")
    for run in reja_heading.runs:
        run.font.name = 'Times New Roman'
        run.font.bold = True
        run.font.size = Pt(14)

    for reja in rejalar:
        p = doc.add_paragraph(reja)
        for run in p.runs:
            run.font.name = 'Times New Roman'
            run.italic = True
            run.font.size = Pt(14)

    doc.add_page_break()
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    # Mavzular va matnlar
    for mavzu, text in theme_text.items():
        mavzu_text = doc.add_paragraph(mavzu)
        mavzu_text.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for run in mavzu_text.runs:
            run.font.name = 'Times New Roman'
            run.bold = True
            run.font.size = Pt(14)

        teks_text = doc.add_paragraph(f"     {text}")
        teks_text.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for run in teks_text.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(14)

        if list(theme_text.keys())[-1] != mavzu:
            doc.add_page_break()

    # Return file
    file_stream = BytesIO()
    await loop.run_in_executor(None, doc.save, file_stream)
    file_stream.seek(0)
    return file_stream

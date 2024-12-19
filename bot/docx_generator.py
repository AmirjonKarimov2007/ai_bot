from io import BytesIO
from docx import Document
from docx.shared import Pt
from docx.oxml import OxmlElement
from aiogram.types import InputFile

async def word_generator(type, mavzu, univer, name, user_id, rejalar: list, theme_text: dict):
    # Word hujjatini yaratish
    doc = Document("Referal.docx")

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

    # Yangi sahifa qo'shish
    def add_new_page(doc):
        paragraph = doc.add_paragraph()
        run = paragraph.add_run()
        run._r.addnext(OxmlElement('w:br'))

    add_new_page(doc)

    # "Rejalar" sarlavhasi va rejalar qo'shish
    reja_heading = doc.add_paragraph("Rejalar")
    for run in reja_heading.runs:
        run.font.name = 'Times New Roman'
        run.font.bold = True
        run.font.size = Pt(14)

    for reja in rejalar:
        rejalar_ = doc.add_paragraph(reja)
        for run in rejalar_.runs:
            run.font.name = 'Times New Roman'
            run.italic = True
            run.font.size = Pt(14)

    rejalar_ = doc.add_page_break()

    # Mavzu va matnlar qo'shish
    for mavzu, text in theme_text.items():
        mavzu_text = doc.add_paragraph(mavzu)
        for run in mavzu_text.runs:
            run.font.name = 'Times New Roman'
            run.bold = True
            run.font.size = Pt(14)

        teks_text = doc.add_paragraph(text)
        for run in teks_text.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(14)
        teks_text = doc.add_page_break()

    # Faylni BytesIO obyektiga yozish
    file_stream = BytesIO()
    doc.save(file_stream)  
    file_stream.seek(0)  
    return file_stream

# Foydalanuvchiga faylni yuborish
async def send_document(msg, user_id, file_stream):
    await msg.answer_document(InputFile(file_stream, filename=f"{user_id}.docx"))

from docx import Document
from docx.shared import Pt
from docx.oxml import OxmlElement

# Hujjatni yuklash
doc = Document("Referal.docx")

# Hujjat tarkibini o'qish va tahrirlash
for paragraph in doc.paragraphs:
    print(paragraph.text)  # Hozirgi matnni chiqaradi
    # "TypeType" matnini almashtirish va formatlash
    for run in paragraph.runs:
        if "TypeType" in run.text:
            run.text = run.text.replace("TypeType", "MUSTAQIL ISH")
            run.font.name = 'Times New Roman'
            run.font.size = Pt(54)
            run.bold = True
        # "UNIVER" matnini almashtirish va formatlash
        if "UNIVER,UNIVER,UNIVER,UNIVER" in run.text:
            run.text = run.text.replace("UNIVER,UNIVER,UNIVER,UNIVER", "DAVLAT UNIVERSITETI")
            run.font.name = 'Times New Roman'
            run.font.size = Pt(16)

# Yangi sahifa qo'shish funksiyasi
def add_new_page(doc):
    paragraph = doc.add_paragraph()
    run = paragraph.add_run()
    run._r.addnext(OxmlElement('w:br'))  # Sahifa ajratuvchi qo'shish

# Yangi sahifa qo'shish
add_new_page(doc)

# Yangi sahifaga "Hello World" matnini qo'shish
new_paragraph = doc.add_paragraph("Hello World")

# "Hello World" matnini faqat Times New Roman va 14px qilish
for run in new_paragraph.runs:
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)

# Hujjatni saqlash
doc.save("referat_tahrirlangan.docx")

print("Hujjatga yangi sahifa qo'shildi va 'Hello World' matni Times New Roman, 14px formatida yozildi.")

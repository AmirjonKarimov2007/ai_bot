from pptx import Presentation
from pptx.util import Inches
from pptx.util import Pt



def slayd_generator(mavzu, ism, rejalars, matnlar):
    input_file = "bot/slaydlar/shablon_1.pptx"
    output_file = "edited_shablon.pptx"
    presentation = Presentation(input_file)

    # Birinchi slaydda mavzu va tayyorlovchini yangilash
    first_slide = presentation.slides[0]
    for shape in first_slide.shapes:
        if shape.has_text_frame:
            for paragraph in shape.text_frame.paragraphs:
                if "Mavzu:MavzuMavzu" == paragraph.text:
                    paragraph.text = f"Mavzu: {mavzu}"
                elif "Tayyorladi:" == paragraph.text:
                    paragraph.text = f"Tayyorladi: {ism}"

    # Ikkinchi slayd uchun rejalarni yangilash
    reja_slide = presentation.slides[1]
    for shape in reja_slide.shapes:
        if shape.has_text_frame and "RejalarRejalarRejalar" in shape.text_frame.text:
            text_frame = shape.text_frame
            text_frame.clear()
            for reja in rejalars:
                text_frame.add_paragraph().text = reja

    # Har bir reja uchun yangi slayd yaratish va matn qo'shish
    for reja, matn in matnlar.items():
        slide_layout = presentation.slide_layouts[1]  # Sarlavha va matn uchun slayd
        new_slide = presentation.slides.add_slide(slide_layout)
        
        # Sarlavha joylashtirish
        title = new_slide.shapes.title
        title.text = reja
        title.text_frame.paragraphs[0].font.size = Pt(14)  # Sarlavha uchun shrift o'lchami

        # Matn joylashtirish
        content = new_slide.placeholders[1]
        content.text = matn
        for paragraph in content.text_frame.paragraphs:
            paragraph.font.size = Pt(14)

    # Taqdimotni saqlash
    presentation.save(output_file)
    return output_file

# Rejalar va matnlar ro'yxati
rejalar = [
    "1. Birinchi Reja",
    "2. Ikkinchi Reja",
    "3. Uchinchi Reja"
]
matnlar = {
    "1. Birinchi Reja": "llakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljsk",
    "2. Ikkinchi Reja": "llakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljsk",
    "3. Uchinchi Reja": "llakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljskllakjdlakjsdaljsk"
}

output_file = slayd_generator(mavzu="Yangi taqdimot", ism="Amirjon Karimov", rejalars=rejalar, matnlar=matnlar)
print(f"Tahrir qilingan taqdimot '{output_file}' nomi bilan saqlandi.")

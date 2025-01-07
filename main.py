from pptx import Presentation



def slayd_generator(mavzu,ism,rejalars):
    input_file = "bot/slaydlar/shablon_1.pptx"
    output_file = "edited_shablon.pptx"
    presentation = Presentation(input_file)

    first_slide = presentation.slides[0]
    rejalar = presentation.slides[1]

    for shape in first_slide.shapes:
        if shape.has_text_frame:  
            for paragraph in shape.text_frame.paragraphs:
                old_title = "Mavzu:Avtomobil yo’llarni ta’mirlash va texnik xizmat ko’rsatishning texnik qoidalari"
                old_description = "Tayyorladi:"
                if old_title==paragraph.text:
                    paragraph.text = f"Mavzu: {mavzu}"  # Matnni yangilash
                elif old_description==paragraph.text:
                    paragraph.text=f"Tayyorladi: {ism}"
    for reja in rejalar.shapes:
        if reja.has_text_frame:  
            for r in rejalars:
                for paragraph in reja.text_frame.paragraphs:
                    old_title = "Reja:"
                    if old_description!=paragraph.text:
                        print(paragraph.text)
                        paragraph.text=f"{r}"
    presentation.save(output_file)
    return output_file
rejalar = {
    "1. Birinchi Reja",
    "2. Birinchi Reja",
    "3. Birinchi Reja"
}
output_file = slayd_generator(mavzu="Yangi taqdimot",ism="Amirjon Karimov",rejalars=rejalar)
print(f"Tahrir qilingan taqdimot '{output_file}' nomi bilan saqlandi.")

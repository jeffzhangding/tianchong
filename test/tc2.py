from docxtpl import DocxTemplate

doc = DocxTemplate("黄浦投资意见书.docx")
sd = doc.new_subdoc('sub.docx')

context = {
        't1': 'tttttttttttttt1',
        't2': 'tttttttttttttt2',
        'sub': sd,
    }
doc.render(context)
doc.save("generated_doc.docx")



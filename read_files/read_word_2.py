from docx import Document
#from docx import opendocx

document = Document('D:\\Pavan\\New folder\\word_read_write.docx')
print(document)


Dictionary = {'sea':'ocean'}

sections = document.sections
for section in sections:
    print(section.start_type)

#Now, I would like to navigate, focus on, get to, whatever to the section that has my
#single line of text and execute a find/replace using the dictionary above.
#then save the document in the usual way.

document.save('D:\\Pavan\\New folder\\word_read_write1.docx')
import openpyxl
book = openpyxl.load_workbook('D:/LV/read_excel.xlsx')

sheet = book.active
#print sheet
cells = sheet['A2': 'B50']
excel_values = {}
#print cells
for c1, c2 in cells:
    excel_values[c1.value] = c2.value
    # if excel_values[c1.value] == 'None':
    #     excel_values.pop('None')

print excel_values


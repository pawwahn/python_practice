import xlrd

workbook = xlrd.open_workbook('Z:/files/Book1.xlsx')
sheet = workbook.sheet_by_index(0)
sheet1 = workbook.sheet_by_name('Sheet1')
print  sheet1.nrows
print sheet1.ncols
print workbook.sheet_names()
workbook.nsheets
# for col in range(sheet1.ncols):
#     print col
#
# for rows in range(sheet1.nrows):
#     print rows

data = [[sheet1.cell_value(r,c) for r in range(sheet1.nrows)] for c in range(sheet1.ncols)]
print data

datas = [[sheet1.cell_value(r,c) for c in range(sheet1.ncols)] for r in range(sheet1.nrows)]
print datas

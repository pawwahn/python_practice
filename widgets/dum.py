exc_descp = ['tibs','tip', 'tip']
exc_set_amt = ['10.00','12.00','15.00']
exc_set_date = ['16-11-2021','14-11-2021','15-10-2021']

sipp_data = [('tibs', '10.00', '16-11-2021'), ('tip', '12.00', '15-11-2021'), ('tip', '15.00', '15-10-2021'),('tibs','20.00','13-10-2020')]
#excel_data = [['tibs', '10.00', '16-11-2021'], ['tip', '12.00', '14-11-2021'], ['tip', '15.00', '15-10-2021']]
excel_data = []

for i in range(len(exc_descp)):
    exl_data = []
    exl_data.append(exc_descp[i])
    exl_data.append(exc_set_amt[i])
    exl_data.append(exc_set_date[i])
    excel_data.append(exl_data)

print(excel_data)
print("above is excel data")

for i in excel_data:
    for j in sipp_data:
        if ((i[0]==j[0]) and (i[1]==j[1]) and (i[2]==j[2])):
            print(i)
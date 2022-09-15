ims = ['brewin','schoder']

trans_amt = ['100','']

set_dates = ['10/10/2021','19/10/2021']

new_lst = []
cnt = 0
for i in range(0,len(ims)):
    excel_dict = {}
    excel_dict['description'] = ims[i]
    excel_dict['trans_amt'] = trans_amt[i]
    excel_dict['set_date'] = set_dates[i]
    new_lst.append(excel_dict)
    #print(new_lst)

#print(excel_dict)
print(new_lst)
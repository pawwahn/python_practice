#from datetime import datetime
import datetime
val_rec = [
{'Investment_ID': '252690', 'Investment_Type': 'T', 'Description': 'Smoothed Pension, 80031770, NMPTL Client 604743, Royal Bank of Scot, Current', 'Valuation': '0.0000', 'Unitholder_ID': 'None', 'valuation_date': '2020-12-31 00:00:00'},
{'Investment_ID': '252890', 'Investment_Type': 'T', 'Description': 'Smoothed Pension, 80031720, NMPTL Client 604743, Royal Bank of Scot, Current', 'Valuation': '0.0000', 'Unitholder_ID': 'None', 'valuation_date': '2021-12-31 00:00:00'},
{'Investment_ID': '252840', 'Investment_Type': 'T', 'Description': 'Smoothed Pension, 80031740, NMPTL Client 604743, Royal Bank of Scot, Current', 'Valuation': '0.0000', 'Unitholder_ID': 'None', 'valuation_date': '2020-08-31 00:00:00'},
{'Investment_ID': '252698', 'Investment_Type': 'T', 'Description': 'Liverpool Victoria Financial Services Limited, N60474350, UID N60474350', 'Valuation': '115034.4000', 'Unitholder_ID': 'N60474350', 'valuation_date': '2021-10-30 00:00:00'},
{'Investment_ID': '252703', 'Investment_Type': 'T', 'Description': 'Liverpool Victoria Financial Services Limited, T60474351, UID T60474351', 'Valuation': '139828.7500', 'Unitholder_ID': 'T60474351', 'valuation_date': '2021-11-01 00:00:00'},
{'Investment_ID': '252763', 'Investment_Type': 'T', 'Description': 'Liverpool Victoria Financial Services Limited, T63474351, UID T60474351', 'Valuation': '139828.7500', 'Unitholder_ID': 'T60474351', 'valuation_date': '2020-11-01 00:00:00'}]

d1_smp = datetime.datetime(1800,1,1)
d1_lv = datetime.datetime(1800,1,1)
new_dict = {}

for i in val_rec:
    d2 = datetime.datetime(int(i['valuation_date'][0:4]), int(i['valuation_date'][5:7]), int(i['valuation_date'][8:10]))
    if 'Smoothed Pension' in i['Description']:

        if d1_smp < d2:
            new_date_smp = d2
            d1_smp = new_date_smp
    elif 'Liverpool Victoria' in i['Description']:
        if d1_lv < d2:
            new_date_lv = d2
            d1_lv = new_date_lv
print(d1_smp)
print(d1_lv)

new_obj = []
for i in val_rec:
    if 'Smoothed Pension' in i['Description']:
        if str(d1_smp) in str(i['valuation_date']):
            print(i)
            new_obj.append(i)
    elif 'Liverpool Victoria' in i['Description']:
        if str(d1_lv) in str(i['valuation_date']):
            print(i)
            new_obj.append(i)
print("=========")
print(new_obj)




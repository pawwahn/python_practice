tv_tvu_usp,emr_reg, mem_reg = {}, {}, {}
# emr_reg = {}
# mem_reg = {}

dd = [{'Premium_id': '133534', 'payment_date': '2016-04-06 00:00:00', 'amount': '80737.0000', 'partner_id': 'None',
       'Premium_type': 'TV - TVU', 'currency_code': 'GBP', 'description': 'Single', '': '51.3846201200',
       'end_date': 'None', 'frequency_code': 'S', 'carry_back_year': 'None', 'carry_back_amount': 'None',
       'unpaid_premium': 'False', 'carry_forward_year': 'None', 'Fund_Prop_Reliable': 'True',
       'Description': 'Primary SIPP Fund', 'Tax_Free_Cash_Certificate': '0.0000',
       'Date_Of_Tax_Free_Certificate': '1899-12-30 00:00:00', 'Sub_Fund_ID': '66002', 'Total_Segments': '1000',
       'Unvested_Fund_Prop': '0E-10'},
      {'Premium_id': '133535', 'payment_date': '2016-04-06 00:00:00', 'amount': '7125.0700', 'partner_id': 'None',
       'Premium_type': 'TV - USP', 'currency_code': 'GBP', 'description': 'Single', '': '100.0000000000',
       'end_date': 'None', 'frequency_code': 'S', 'carry_back_year': 'None', 'carry_back_amount': 'None',
       'unpaid_premium': 'False', 'carry_forward_year': 'None', 'Fund_Prop_Reliable': 'True',
       'Description': 'Fund Pot 11', 'Tax_Free_Cash_Certificate': '0.0000',
       'Date_Of_Tax_Free_Certificate': '1899-12-30 00:00:00', 'Sub_Fund_ID': '79963', 'Total_Segments': '1000',
       'Unvested_Fund_Prop': '0E-10'},
      {'Premium_id': '133550', 'payment_date': '2016-04-06 00:00:00', 'amount': '7365.4100', 'partner_id': 'None',
       'Premium_type': 'EMR', 'currency_code': 'GBP', 'description': 'Single', '': '100.0000000000',
       'end_date': 'None', 'frequency_code': 'S', 'carry_back_year': 'None', 'carry_back_amount': 'None',
       'unpaid_premium': 'False', 'carry_forward_year': 'None', 'Fund_Prop_Reliable': 'True',
       'Description': 'Fund Pot 7', 'Tax_Free_Cash_Certificate': '0.0000',
       'Date_Of_Tax_Free_Certificate': '1899-12-30 00:00:00', 'Sub_Fund_ID': '79959', 'Total_Segments': '1000',
       'Unvested_Fund_Prop': '0E-10'},
      {'Premium_id': '145719', 'payment_date': '2016-04-06 00:00:00', 'amount': '53352.8100', 'partner_id': 'None',
       'Premium_type': 'MEMBER', 'currency_code': 'GBP', 'description': 'Single', '': '48.6153798800',
       'end_date': 'None', 'frequency_code': 'S', 'carry_back_year': 'None', 'carry_back_amount': 'None',
       'unpaid_premium': 'False', 'carry_forward_year': 'None', 'Fund_Prop_Reliable': 'True',
       'Description': 'Primary SIPP Fund', 'Tax_Free_Cash_Certificate': '0.0000',
       'Date_Of_Tax_Free_Certificate': '1899-12-30 00:00:00', 'Sub_Fund_ID': '66002', 'Total_Segments': '1000',
       'Unvested_Fund_Prop': '0E-10'}]

start_date = '23-10-2010'   #excel_date

import datetime
tv_amt,mem_amt,emr_amt = 0,0,0
# mem_amt = 0
# emr_amt = 0

for i in dd:
    if i['payment_date'] and i['frequency_code'] in ['s','S']:
        dd, mm, yyyy = i['payment_date'][8:10], i['payment_date'][5:7], i['payment_date'][:4]
        print(dd, mm, yyyy)
        d1 = datetime.datetime(int(yyyy), int(mm), int(dd))
        d2 = datetime.datetime(int(start_date[6:]), int(start_date[3:5]), int(start_date[0:2]))
        if d1 > d2:
            if i['Premium_type'].lower() in ['tv - tvu', 'tv - usp', 'tv - asp']:
                print("transfer satisfied")
                tv_amt = tv_amt+round(float(i['amount']), 2)
                tv_tvu_usp['amount'] = round(tv_amt,2)
                tv_tvu_usp['premium_type'] = 'Transfer Value'
            if i['Premium_type'].lower() in ['emr']:
                print("emr satisfied")
                emr_amt = emr_amt+round(float(i['amount']), 2)
                emr_reg['amount'] = round(emr_amt,2)
                emr_reg['premium_type'] = 'Employer Single payments'
            if i['Premium_type'].lower() in ['member']:
                print("member satisfied")
                mem_amt = mem_amt+round(float(i['amount']), 2)
                mem_reg['amount'] = round(mem_amt,2)
                mem_reg['premium_type'] = 'Member Single payments'

print(tv_tvu_usp)
print(emr_reg)
print(mem_reg)
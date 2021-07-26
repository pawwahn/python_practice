dd = {'Field_name': 'Value', 'Policy_number': 40447, 'Surname': 'TESTTHEAEEH', 'Payment_amount': 2000, 'Sale_date': '24/04/2021', 'Tax_code': '1250L', 'Adhoc_fee': 100, 'Encashment': 'D40447000', 'Fund_code-1': 1248, 'Split-1': 100, 'CTC_product_type': 'FTA PP Min AMC', 'Account_name': 'Testtheaeeh', 'Account_surname': 'TESTTHEAEEH', 'Account_number': 123.45, 'Sort_code': '77-48-14', 'Risk_warnings_required?': 'No', 'Correspondence_to_be_sent_to': 'Member', 'Member_email_address\n': 'Member@lv.com', 'Adviser_email_address': None, 'AML_check': 'Yes'}


for i,k in dd.items():
    if 'Member_email_address' in i.rstrip("\n"):
        print i, k


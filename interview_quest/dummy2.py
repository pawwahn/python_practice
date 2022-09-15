smf_rv_data = [['DFM', 'Brewin Dolphin Limited', '£\n50,300.00', '20', None], ['DFM', 'Schroder & Co Ltd', '50,300.00', '20', None]]

sipp_im_invests_data = [
{'Investment_ID': '40684', 'Investment_Type': 'I', 'Description': 'Brewin Dolphin Limited, LIVER0032', 'Valuation': '1774468.1500', 'Unitholder_ID': ''},
{'Investment_ID': '40732', 'Investment_Type': 'I', 'Description': 'Schroder & Co Ltd, 714438', 'Valuation': '1162060.4100', 'Unitholder_ID': ''},
{'Investment_ID': '248874', 'Investment_Type': 'I', 'Description': 'Rathbone Investment Management Limited, 274937', 'Valuation': '1319916.6300', 'Unitholder_ID': ''}
]

common_rv_sipp_ims = []
for i in smf_rv_data:
    for j in sipp_im_invests_data:
        if i[1] in j['Description']:
            j['amount'] = i[2][2:].replace(',', '')
            j['income'] = i[4]
            j['acc_ref'] = j['Description'].split(',')[1]
            common_rv_sipp_ims.append(j)
print(common_rv_sipp_ims)

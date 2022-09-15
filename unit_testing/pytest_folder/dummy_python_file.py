a = """Hi Team,


Exception Type: Business

Exception 1: Traceback (most recent call last): File "C:\Automaton\Var\TestsResult\17\2022-05-05\2022-05-05_09-27-52.108390.Ym90X3VubWF0Y2hlZF9vcmlnb19qYW1idXV1dQ==.salooja\SubTE0.py", line 212, in definition exception_list ,queue_processing_list = [] ValueError: not enough values to unpack (expected 2, got 0)
Exception 2: C:\Automaton\Var\TestsResult\17\2022-05-05\2022-05-05_09-27-52.108390.Ym90X3VubWF0Y2hlZF9vcmlnb19qYW1idXV1dQ==.salooja

Exception Date & time: 05-05-2022 09:27:59


Regards,
Automation Team
Support email ID: CIOApplicationManagementLifeRSAutomatON@lv.com"""

new_a = a.replace('Regards','Note: Do not reply to this email. \n \nRegards')
print(new_a)

#print(a)
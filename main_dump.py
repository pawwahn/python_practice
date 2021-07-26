import xmltodict
import pprint
import json
#import dump2


def convert(k):
    k = k.replace('@', '')
    return k

def change_keys(obj, convert):
    """
    Recursivly goes through the dictionnary obj and replaces keys with the convert function.
    """
    if isinstance(obj, dict):
        new = {}
        for k, v in obj.items():
            new[convert(k)] = change_keys(v, convert)
    elif isinstance(obj, list):
        new = []
        for v in obj:
            new.append(change_keys(v, convert))
    else:
        return obj
    return new

xml_val = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
   <soapenv:Header/>
   <SOAP-ENV:Body xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns4="urn:idu" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      <ns0:verificationResponse xmlns:ns0="http://www.lv.com/rs/middleware/verification">
         <ns0:message>
            <ns0:m_control>
               <ns0:control_timestamp>2021-03-31T08:10:13.647+01:00</ns0:control_timestamp>
               <ns0:system_source>RetirementView</ns0:system_source>
               <ns0:publisher>?</ns0:publisher>
               <ns0:Request_Ref/>
               <ns0:user_ID>?</ns0:user_ID>
               <ns0:scorecard>IDU default</ns0:scorecard>
            </ns0:m_control>
            <ns2:services_response xmlns:ns2="http://www.lv.com/rs/middleware/verification">
               <ns2:status>REFER</ns2:status>
               <ns2:message>
                  <Errors xsi:type="ns4:ErrorPart" xsi:nil="true"/>
               </ns2:message>
               <ns2:evidence_of_age>
                  <ns2:status>FAIL</ns2:status>
                  <ns2:message>
                     <DOB>
                        <TracesmartDOB xsi:type="xsd:int">0</TracesmartDOB>
                        <EquifaxDOB xsi:type="xsd:int">-1</EquifaxDOB>
                        <EquifaxDOBStatus xsi:type="xsd:string">-1</EquifaxDOBStatus>
                     </DOB>
                     <CreditActive>
                        <InsightAccounts xsi:type="xsd:int">-1</InsightAccounts>
                        <InsightLenders xsi:type="xsd:int">-1</InsightLenders>
                        <CAISLenders xsi:type="xsd:int">0</CAISLenders>
                     </CreditActive>
                  </ns2:message>
               </ns2:evidence_of_age>
               <ns2:anti_money_laundering>
                  <ns2:status>FAIL</ns2:status>
                  <ns2:message>
                     <Address>
                        <Forename xsi:type="xsd:string">GEB</Forename>
                        <MiddleName xsi:type="xsd:string">JOHN</MiddleName>
                        <Surname xsi:type="xsd:string">AUTOMATE TEST</Surname>
                        <DOB xsi:type="xsd:string">1961-03-12</DOB>
                        <MatchType xsi:type="xsd:string"/>
                        <ForenameAppended xsi:type="xsd:boolean">false</ForenameAppended>
                        <MiddleNameAppended xsi:type="xsd:boolean">false</MiddleNameAppended>
                        <DOBAppended xsi:type="xsd:boolean">false</DOBAppended>
                        <Telephone xsi:type="xsd:string">Unavailable</Telephone>
                        <Telephonename xsi:type="xsd:string"/>
                        <Phonematch xsi:type="SOAP-ENC:Array" SOAP-ENC:arrayType="xsd:string[0]" xsi:nil="true"/>
                        <GoneAway xsi:type="xsd:string">N</GoneAway>
                        <Source xsi:type="xsd:string"/>
                        <Recency xsi:type="xsd:string"/>
                        <Occupants xsi:type="SOAP-ENC:Array" SOAP-ENC:arrayType="ns4:OccupantPart[0]" xsi:nil="true"/>
                        <Property xsi:type="SOAP-ENC:Array" SOAP-ENC:arrayType="ns4:PropertyPart[1]">
                           <PropertySale xsi:type="ns4:PropertyPart">
                              <Type xsi:type="xsd:string"/>
                              <Tenure xsi:type="xsd:string"/>
                              <Date xsi:type="xsd:string"/>
                              <Price xsi:type="xsd:string"/>
                              <Silhouette xsi:type="xsd:string">B33</Silhouette>
                           </PropertySale>
                        </Property>
                        <AddressValidated xsi:type="xsd:boolean">true</AddressValidated>
                     </Address>
                     <Deathscreen xsi:type="SOAP-ENC:Array" SOAP-ENC:arrayType="ns4:DeathscreenResult[0]" xsi:nil="true"/>
                     <DOB>
                        <TracesmartDOB xsi:type="xsd:int">0</TracesmartDOB>
                        <EquifaxDOB xsi:type="xsd:int">-1</EquifaxDOB>
                        <EquifaxDOBStatus xsi:type="xsd:string">-1</EquifaxDOBStatus>
                     </DOB>
                     <Sanction xsi:type="SOAP-ENC:Array" SOAP-ENC:arrayType="ns4:SanctionPart[0]" xsi:nil="true"/>
                     <Insolvency xsi:type="SOAP-ENC:Array" SOAP-ENC:arrayType="ns4:InsolvencyResult[0]" xsi:nil="true"/>
                     <Crediva>
                        <FullER xsi:type="xsd:boolean">false</FullER>
                     </Crediva>
                     <Ccj xsi:type="SOAP-ENC:Array" SOAP-ENC:arrayType="ns4:CcjResult[0]" xsi:nil="true"/>
                     <CreditActive>
                        <InsightAccounts xsi:type="xsd:int">-1</InsightAccounts>
                        <InsightLenders xsi:type="xsd:int">-1</InsightLenders>
                        <CAISLenders xsi:type="xsd:int">0</CAISLenders>
                     </CreditActive>
                  </ns2:message>
               </ns2:anti_money_laundering>
               <ns2:bank_account>
                  <ns2:status>true</ns2:status>
                  <ns2:message>
                     <Bankmatch>
                        <BankAccountValid xsi:type="xsd:boolean">true</BankAccountValid>
                        <BankName xsi:type="xsd:string">LLOYDS BANK PLC</BankName>
                        <BranchDetails xsi:type="xsd:string">ST ALBANS (309725)</BranchDetails>
                        <BACSPayments xsi:type="xsd:boolean">true</BACSPayments>
                        <CHAPSPayments xsi:type="xsd:boolean">true</CHAPSPayments>
                        <FasterPayments xsi:type="xsd:boolean">true</FasterPayments>
                        <DirectDebit xsi:type="xsd:boolean">true</DirectDebit>
                     </Bankmatch>
                  </ns2:message>
               </ns2:bank_account>
               <ns2:bank_match_live>
                  <ns2:status/>
                  <ns2:message>
                     <BankmatchLive>
                        <Sortcode xsi:type="xsd:string"/>
                        <AccountNumber xsi:type="xsd:string"/>
                        <AccountName xsi:type="xsd:string"/>
                        <AccountAddress xsi:type="xsd:string"/>
                        <AccountStatus xsi:type="xsd:string"/>
                        <ErrorCode xsi:type="xsd:string"/>
                     </BankmatchLive>
                  </ns2:message>
               </ns2:bank_match_live>
               <ns2:company_director>
                  <ns2:status>
                     <ns2:status>FAIL</ns2:status>
                  </ns2:status>
                  <ns2:message>
                     <CompanyDirector xsi:type="SOAP-ENC:Array" SOAP-ENC:arrayType="ns4:CompanyDirectorPart[0]" xsi:nil="true"/>
                  </ns2:message>
               </ns2:company_director>
            </ns2:services_response>
         </ns0:message>
      </ns0:verificationResponse>
   </SOAP-ENV:Body>
</soapenv:Envelope>"""

#my_xml = dump2.xml_val
my_dict = xmltodict.parse(xml_val)
# print type(my_dict)

dic = dict(my_dict)

data1= change_keys(my_dict, convert)

bank_account_status = data1.get("soapenv:Envelope").get("SOAP-ENV:Body").get("ns0:verificationResponse").get("ns0:message").get("ns2:services_response").get("ns2:bank_account").get("ns2:status")
address_status = data1.get("soapenv:Envelope").get("SOAP-ENV:Body").get("ns0:verificationResponse").get('ns0:message').get('ns2:services_response').get('ns2:anti_money_laundering').get('ns2:message').get('Address').get('AddressValidated').get('#text')
service_response = data1.get("soapenv:Envelope").get("SOAP-ENV:Body").get("ns0:verificationResponse").get('ns0:message').get("ns2:services_response").get("ns2:status")
bank_match_live = data1.get("soapenv:Envelope").get("SOAP-ENV:Body").get("ns0:verificationResponse").get('ns0:message').get('ns2:services_response').get("ns2:anti_money_laundering").get("ns2:bank_match_live")#.get("ns2:status")
print bank_account_status
print address_status
print service_response
print bank_match_live
#print(res['ns2:status'])


from tests.suites.network_access.common.common_utils import *
from tests.suites.network_access.uplift_test.na_uplift_helper import UI_methods as UiLib
import tests.suites.network_access.uplift_test.uplift_constants as NAUplift_Constants
from tests.suites.network_access.uplift_test.pez_helper import PezHelper as Pezlib
import utilities.third_party.ad2016.ad2016 as AD2016

AD_ATTRIBUTES = ["sAMAccountName", "userPrincipalName"]
AUTH_CONDITIONS = ['Tnt5205712c_New_Authorization_Rule_1', 'Tnt5205712c_New_Authorization_Rule_2']
RELATIVE_CONDITION = 'EQUALS'
ATTRIBUTE_VALUE = ['testsuite1', 'testsuite1@demo.local']  # ['ISE','ISE@demo.local']
AUTHORIZATION_RULE_NAME = 'Authorization Rule'
AUTHORIZATION_POLICY_PROFILE = 'PermitAccess'
SECURITY_GROUP = 'Unknown'
DEFAULT_VALUE_AUTHENTICATION = 'Internal Users'
LIVE_LOGS_SECTION = 'Other Attributes'
POLICY_SET_PROTOCOL = 'Default Network Access'
POLICY_SET = 'Policy Set 1'
CONDITIONS = ['Tnt5205712c_Policy_Set_Condition', 'Tnt5205712c_Authorization_Condition']

NAS_FOLDER = "/volume1/vms/local/session_api/selenium_record"

class Commonsetup(aetest.CommonSetup):
    @aetest.subsection
    def setup_start(self):
        pass


class US356257_Tnt5205712c_SAM_PLUS_CN_EAP_TLS(aetest.Testcase):
    @aetest.setup
    def setup(self):
        self.nad_ip = cfg.te.get_PEZ().get_ip()
        UiLib.check_app_up(cfg.te.get_POSITRON()[0].get_ip())
        self.selenium_url = cfg.te.get_WIN_CLIENT().get_internal_selenium()
        s_log.info("###### SELENIUM URL ######## {} ".format(self.selenium_url))

        self.iseIP = cfg.te.get_POSITRON()[0].get_ip()
        s_log.info("###### ISE IP ######## {} ".format(self.iseIP))

        self.iseUrl = "https://" + self.iseIP + "/"
        s_log.info("###### ISE URL ######## {} ".format(self.iseUrl))

        self.iseUser = cfg.te.get_POSITRON()[0].get_login()
        s_log.info("###### ISE User ######## {} ".format(self.iseUser))

        self.isePassword = cfg.te.get_POSITRON()[0].get_password()
        s_log.info("###### ISE Password ######## {} ".format(self.isePassword))

        self.homeDir = automationDir()

        # Preconfigure Settings
        UiLib.bindFunction(self, UiLib.delete_all_policy_sets, [])
        UiLib.bindFunction(self, UiLib.delete_library_conditions_with_prefix, ['Tnt'])
        UiLib.bindFunction(self, UiLib.remove_all_identity_source_from_sequence, ['All_User_ID_Stores', 'default'])
        UiLib.bindFunction(self, UiLib.config_certificate_authprofile,
                           [NAUplift_Constants.CER_NAME,
                            NAUplift_Constants.CER_NAME,
                            NAUplift_Constants.CER_DESCRIPTION,
                            NAUplift_Constants.CER_ATTRIBUTE,
                            '[not applicable]',
                            NAUplift_Constants.MATCH_CLIENT_CERT_ENABLE]
                           )
        UiLib.bindFunction(self, UiLib.trustedCertificates_deleteTrustedCertificate,
                           [NAUplift_Constants.FRIENDLYNAME_ISE_TRUSTED_CERT])
        #
        funcs = [self.delete_all_policy_sets,
                 self.delete_library_conditions_with_prefix,
                 self.remove_all_identity_source_from_sequence,
                 self.config_certificate_authprofile,
                 self.trustedCertificates_deleteTrustedCertificate
                 ]

        retries = 3
        runFunctionsInOrderV2(funcs, self, retries, recordingDir=NAS_FOLDER)

    @aetest.test
    def Tnt5205712c(self):
        AD_DOMAIN_NAME = "demo.local" #cfg.suite.get_AD()[0].get_hostname()
        AD_ADMIN_USERNAME = cfg.suite.get_AD()[0].get_login()
        AD_ADMIN_PASSWORD = cfg.suite.get_AD()[0].get_password()

        attribute_check_map = {'sAMAccountName': NAUplift_Constants.ADD_USER,
                               'userPrincipalName': NAUplift_Constants.ADD_USER + '@' + AD_DOMAIN_NAME}

        AD_USERNAME = 'testsuite1'
        AD_USER_PASSWORD = 'Lab@123'
        AD_USER_ATTRS = '-samid testsuite1 -upn testsuite1@demo.local -memberof "cn=Administrators,cn=Builtin,dc=demo,dc=local"'

        AD2016.add_user_with_attr(userToAdd=AD_USERNAME,
                                      userPwd=AD_USER_PASSWORD,
                                      domain=AD_DOMAIN_NAME,
                                      attributeDetails=AD_USER_ATTRS)

        cert_path= NAUplift_Constants.strPath + "tests/suites/network_access/uplift_test/test_data/eap_tls_cert/" + \
                                NAUplift_Constants.ISE_TRUSTED_CERT

        cert=NAUplift_Constants.ClientSystemCerts

        AD2016.add_cert_to_user(certname=NAUplift_Constants.ClientSystemCerts,
                                certpath=cert_path,
                                user=AD_USERNAME,
                                certificatePath="C:\\Users\\Administrator\\{}".format(cert))

        UiLib.bindFunction(self, UiLib.securitySetting_setCheckbox, ['SHA1', True])
        UiLib.bindFunction(self, UiLib.create_active_directory_with_any_mode,
                           [NAUplift_Constants.AD_NAME,
                            AD_DOMAIN_NAME,
                            AD_ADMIN_USERNAME,
                            AD_ADMIN_PASSWORD,
                            False,
                            None,
                            None,
                            AD_ATTRIBUTES,
                            NAUplift_Constants.ADD_USER  # NAUplift_Constants.AD_SHORT_USER
                            ])

        self.certificate_file = NAUplift_Constants.strPath + "resources/CommonCriteria/" + \
                                NAUplift_Constants.ISE_TRUSTED_CERT
        s_log.info("CERTIFICATE FILE PATH: {}".format(self.certificate_file))

        UiLib.bindFunction(self, UiLib.trustedCertificates_setTrustedCert,
                           [self.certificate_file,
                            NAUplift_Constants.FRIENDLYNAME_ISE_TRUSTED_CERT])

        UiLib.bindFunction(self, UiLib.config_network_device, [NAUplift_Constants.NETWORK_DEVICE_NAME,
                                                               self.nad_ip,
                                                               NAUplift_Constants.SHARED_SECRET])

        funcs = [self.securitySetting_setCheckbox,
                 self.create_active_directory_with_any_mode,
                 self.trustedCertificates_setTrustedCert,
                 self.config_network_device,
                 ]

        retries = 3
        runFunctionsInOrderV2(funcs, self, retries,recordingDir=NAS_FOLDER)

        UiLib.bindFunction(self, UiLib.create_simple_library_condition, [CONDITIONS[0],
                                                                         'Network Access',
                                                                         'Protocol',
                                                                         'EQUALS',
                                                                         'RADIUS'])

        UiLib.bindFunction(self, UiLib.create_policy_set, [POLICY_SET, CONDITIONS[0], POLICY_SET_PROTOCOL])

        funcs = [self.create_simple_library_condition,
                 self.create_policy_set
                 ]

        retries = 3
        runFunctionsInOrderV2(funcs, self, retries, record=False, killPreviousFF=False)

        UiLib.bindFunction(self, UiLib.create_library_condition, [NAUplift_Constants.AD_NAME,
                                                                  AD_ATTRIBUTES,
                                                                  ATTRIBUTE_VALUE,
                                                                  AUTH_CONDITIONS,
                                                                  CONDITIONS[1]])


        # Configuring the policy in authorization policy
        UiLib.bindFunction(self, UiLib.create_authorization_rule_for_simple_condition,
                           [POLICY_SET,AUTHORIZATION_RULE_NAME,
                            CONDITIONS[1],
                            AUTHORIZATION_POLICY_PROFILE,
                            SECURITY_GROUP])

        UiLib.bindFunction(self, UiLib.config_certificate_authprofile,
                           [NAUplift_Constants.CER_NAME,
                            NAUplift_Constants.CER_NAME,
                            NAUplift_Constants.CER_DESCRIPTION,
                            NAUplift_Constants.CER_ATTRIBUTE,
                            NAUplift_Constants.AD_NAME,
                            NAUplift_Constants.MATCH_CLIENT_CERT_ENABLE])

        funcs = [self.create_library_condition,
                 self.create_authorization_rule_for_simple_condition,
                 self.config_certificate_authprofile
                 ]

        retries = 3
        runFunctionsInOrderV2(funcs, self, retries, record=False, killPreviousFF=False)


        # PEZ Authentication Flow
        s_log.info("---------------- PEZ AUTHENTICATION FLOW -----------")
        self.pezlib = Pezlib()

        # Copy Certificates to PEZ
        self.pezlib.copy_cert_pez(root_path=NAUplift_Constants.strPath,
                                  ise_trusted_cert=NAUplift_Constants.ISE_TRUSTED_CERT,
                                  client_certificate=NAUplift_Constants.ClientSystemCerts,
                                  client_key=NAUplift_Constants.ClientSystemKeys)

        # # Run EAP-TLS Authentication
        self.pezlib.run_eap_tls(root_path=NAUplift_Constants.strPath,
                                ise_trust_cert=NAUplift_Constants.ISE_TRUSTED_CERT,
                                client_sys_cert=NAUplift_Constants.ClientSystemCerts,
                                client_sys_key=NAUplift_Constants.ClientSystemKeys,
                                internal_user=NAUplift_Constants.ADD_USER,
                                ise_ip=self.iseIP)

        # self.app.run()
        # self.app = self.uilib.login_into_ise()
        # Add Validation Steps
        UiLib.bindFunction(self, UiLib.compare_attributes_from_live_logs, [attribute_check_map])

        retries = 3

        functs = [self.compare_attributes_from_live_logs]
        runFunctionsInOrderV2(functs, self, retries, record=False, killPreviousFF=False)

    @aetest.cleanup
    def cleanup(self):
        pass
        UiLib.bindFunction(self, UiLib.trustedCertificates_deleteTrustedCertificate,
                           [NAUplift_Constants.FRIENDLYNAME_ISE_TRUSTED_CERT])

        UiLib.bindFunction(self, UiLib.config_certificate_authprofile,
                           [NAUplift_Constants.CER_NAME, NAUplift_Constants.CER_NAME,
                            NAUplift_Constants.CER_DESCRIPTION,
                            NAUplift_Constants.CER_ATTRIBUTE, '[not applicable]',
                            NAUplift_Constants.MATCH_CLIENT_CERT_ENABLE])

        UiLib.bindFunction(self, UiLib.delete_policy_set, [[POLICY_SET]])

        # Delete Library Conditions
        UiLib.bindFunction(self, UiLib.delete_multiple_library_condition,
                           [CONDITIONS])

        UiLib.bindFunction(self, UiLib.delete_network_device,
                           [NAUplift_Constants.NETWORK_DEVICE_NAME])

        funcs = [self.trustedCertificates_deleteTrustedCertificate,
                 self.config_certificate_authprofile,
                 self.delete_policy_set,
                 self.delete_multiple_library_condition,
                 self.delete_network_device
                 ]
        retries = 3
        runFunctionsInOrderV2(funcs, self, retries, record=False, killPreviousFF=False)

        UiLib.bindFunction(self, UiLib.delete_multiple_library_condition,
                           [AUTH_CONDITIONS])

        UiLib.bindFunction(self, UiLib.deleting_ad, [NAUplift_Constants.AD_NAME])

        funcs = [self.delete_multiple_library_condition,
                 self.deleting_ad
                 ]
        retries = 3
        runFunctionsInOrderV2(funcs, self, retries, record=False, killPreviousFF=False)



class TestCaseCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def commoncleanup(self):
        pass


if __name__ == '__main__':
    aetest.main()  # REQUIRED LINE
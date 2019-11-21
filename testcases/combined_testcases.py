from tests.suites.network_access.common.common_utils import *
from tests.suites.network_access.uplift_test.na_uplift_helper import UI_methods as UiLib
from tests.suites.network_access.uplift_test.na_uplift_helper import *
import tests.suites.network_access.uplift_test.uplift_constants as NAUplift_Constants
from tests.suites.network_access.uplift_test.pez_helper import PezHelper as Pezlib
import utilities.third_party.ad2016.ad2016 as ad2016
#from corelib.base.JobBaseTestCase import *

record_option = False
NAS_FOLDER = "/volume1/vms/local/session_api/selenium_record"

AD_DOMAIN_NAME = cfg.suite.get_AD()[0].get_domain()
AD_ADMIN_USERNAME = cfg.suite.get_AD()[0].get_login()
AD_ADMIN_PASSWORD = cfg.suite.get_AD()[0].get_password()
SELECT_GROUP_AD = AD_DOMAIN_NAME + "/Builtin/Administrators"

POLICY_SET = 'Policy Set 1'
POLICY_SET_PROTOCOL = 'Default Network Access'

AUTH_COND_NAME = ['Tnt_peap_eap_test_cases', 'Tnt5753124c_AD_CONDITION','Tnt5988327c_peap_condition']
DICT_NAME = ['Network Access', NAUplift_Constants.AD_NAME,'Network Access']
ATTRIBUTE = ['Protocol', 'ExternalGroups','EapTunnel']
ATTRIBUTE_VALUE = ['RADIUS', SELECT_GROUP_AD,'PEAP']

AUTHZ_POLICY_NAME = ['Authorization_policy_1','Authorization_policy_2']
AUTH_PROFILE = 'PermitAccess'

AUTHENTICATION_POLICY="new_auth_policy"
IDENTITY_SEQUENCE_NAME="New_identity_sequence"
AD_ATTRIBUTES = ["userPrincipalName","name"]

RETRIES = 3

# To get the Positron Details
def get_device_attributes(obj):

    obj.nad_ip = cfg.te.get_PEZ().get_ip()
    UiLib.check_app_up(cfg.te.get_POSITRON()[0].get_ip())
    obj.selenium_url = cfg.te.get_WIN_CLIENT().get_internal_selenium()
    s_log.info("###### SELENIUM URL ######## {} ".format(obj.selenium_url))
    obj.iseIP = cfg.te.get_POSITRON()[0].get_ip()
    # obj.iseIP = '10.197.88.215'
    s_log.info("###### ISE IP ######## {} ".format(obj.iseIP))
    obj.iseUrl = "https://" + obj.iseIP + "/"
    s_log.info("###### ISE URL ######## {} ".format(obj.iseUrl))
    obj.iseUser = cfg.te.get_POSITRON()[0].get_login()
    s_log.info("###### ISE User ######## {} ".format(obj.iseUser))
    obj.isePassword = cfg.te.get_POSITRON()[0].get_password()
    s_log.info("###### ISE Password ######## {} ".format(obj.isePassword))
    obj.homeDir = automationDir()


def set_peap_eap_tests_common_settting(obj):

    AD_USERNAME = 'testsuite1'
    AD_USER_PASSWORD = 'Lab@123'
    AD_USER_ATTRS = '-upn testsuite1@demo.local -memberof "cn=Administrators,cn=Builtin,dc=demo,dc=local"'

    ad2016.add_user_with_attr(userToAdd=AD_USERNAME,
                              userPwd=AD_USER_PASSWORD,
                              domain=AD_DOMAIN_NAME,
                              attributeDetails=AD_USER_ATTRS)

    AD_SPL_ATR = '-memberof "cn=Administrators,cn=Builtin,dc=demo,dc=local" -mustchpwd yes'
    ad2016.add_user_with_attr(userToAdd=NAUplift_Constants.AD_VAR_LEN_USER,
                              userPwd=NAUplift_Constants.AD_VAR_LEN_PWD,
                              domain=AD_DOMAIN_NAME,
                              attributeDetails=AD_SPL_ATR)

    ad2016.add_utf_user(userToAdd=NAUplift_Constants.AD_UTF_USER,
                        userPassword=NAUplift_Constants.AD_USER_PASSWORD,
                        domain= AD_DOMAIN_NAME,
                        attributeDetails='-memberof "cn=Administrators,cn=Builtin,dc=demo,dc=local"')

    UiLib.bindFunction(obj, UiLib.securitySetting_setCheckbox, ['SHA1', True])

    # ---Active Directory:
    # Connect\join to AD server:
    # Navigate to Administration > Identity Management > External Identity Sources > AD
    # Enter the AD Name and Identity Store Name, and click Join.
    # Enter the credentials of the AD account that can add and make changes to computer objects, and click Save Configuration.
    #Retrieve groups and attributes

    UiLib.bindFunction(obj, UiLib.create_active_directory_with_any_mode,
                       [NAUplift_Constants.AD_NAME,
                        AD_DOMAIN_NAME,
                        AD_ADMIN_USERNAME,
                        AD_ADMIN_PASSWORD,
                        True,
                        NAUplift_Constants.AD_SCOPE1,
                        SELECT_GROUP_AD,
                        AD_ATTRIBUTES,
                        NAUplift_Constants.ADD_USER
                        ])

    UiLib.bindFunction(obj, UiLib.identities_add_simple_user, [NAUplift_Constants.ADD_USER_SPECIAL,
                                                               NAUplift_Constants.ADD_EMAIL,
                                                               NAUplift_Constants.ADD_PASSWORD])

    UiLib.bindFunction(obj, UiLib.disable_lower_upper_in_pswdpolicy, [])

    # Configure an Internal User "UTF8-user-name" where the username is in UTF-8 characters
    UiLib.bindFunction(obj, UiLib.identities_add_simple_user, [NAUplift_Constants.ADD_UTF8USER,
                                                               NAUplift_Constants.ADD_EMAIL,
                                                               NAUplift_Constants.ADD_PASSWORD])

    UiLib.bindFunction(obj, UiLib.enable_inner_checkbox_password_policy, [])

    # Step3: enable Peap GTC in allowed protocols
    UiLib.bindFunction(obj, UiLib.enable_peap_gtc_in_allowed_protocol, [])

    UiLib.bindFunction(obj, UiLib.config_network_device, [NAUplift_Constants.NETWORK_DEVICE_NAME,
                                                          obj.nad_ip,
                                                          NAUplift_Constants.SHARED_SECRET])
    funcs = [
        obj.securitySetting_setCheckbox,
        obj.create_active_directory_with_any_mode,
        obj.identities_add_simple_user,
        obj.disable_lower_upper_in_pswdpolicy,
        obj.identities_add_simple_user,
        obj.enable_inner_checkbox_password_policy,
        obj.enable_peap_gtc_in_allowed_protocol,
        obj.config_network_device
       ]

    runFunctionsInOrderV2(funcs, obj, RETRIES,
                          resumeLastSession=True,
                          killFFWhenFinished=True,
                          record=record_option
                        )

    internal_user = [NAUplift_Constants.ADD_USER,
                     "user_nxtlgn_pwdchng"]

    for index in range(len(internal_user)):

        # enable "change password" next logging.
        UiLib.bindFunction(obj, UiLib.create_user_with_passwdchange_in_next_login, [internal_user[index],
                                                                                    NAUplift_Constants.ADD_EMAIL,
                                                                                    NAUplift_Constants.ADD_PASSWORD,
                                                                                    True])
        funcs = [obj.create_user_with_passwdchange_in_next_login]
        runFunctionsInOrderV2(funcs, obj, RETRIES,
                              resumeLastSession=True,
                              killFFWhenFinished=True,
                              record=record_option
                              )

    for index in range(len(AUTH_COND_NAME)):

        UiLib.bindFunction(obj, UiLib.create_simple_library_condition, [AUTH_COND_NAME[index],
                                                                        DICT_NAME[index],
                                                                        ATTRIBUTE[index],
                                                                        'EQUALS',
                                                                        ATTRIBUTE_VALUE[index]])
        funcs = [obj.create_simple_library_condition]
        runFunctionsInOrderV2(funcs, obj, RETRIES,
                              resumeLastSession=True,
                              killFFWhenFinished=True,
                              record=record_option
                       )

    UiLib.bindFunction(obj, UiLib.create_policy_set, [POLICY_SET,
                                                      AUTH_COND_NAME[0],
                                                      POLICY_SET_PROTOCOL])

    UiLib.bindFunction(obj, UiLib.edit_identity_source_in_default_policy, [NAUplift_Constants.AD_NAME,
                                                                           POLICY_SET])

    UiLib.bindFunction(obj, UiLib.create_authorization_rule_for_simple_condition, [POLICY_SET,
                                                                                   AUTHZ_POLICY_NAME[0],
                                                                                   AUTH_COND_NAME[0],
                                                                                   AUTH_PROFILE,
                                                                                   None])
    funcs = [ obj.create_policy_set,
              obj.edit_identity_source_in_default_policy,
              obj.create_authorization_rule_for_simple_condition
                ]

    runFunctionsInOrderV2(funcs, obj, RETRIES,
                              resumeLastSession=True,
                              killFFWhenFinished=True,
                              record=record_option
                           )

peap_eap_cfg_data = {'SIMPLE_USER_peap.py': {'internal_user': NAUplift_Constants.AD_SIMPLE_USER + '@' + AD_DOMAIN_NAME,
                                             'int_usr_pwd': NAUplift_Constants.AD_SIMPLE_USER_PASSWORD,
                                             'int_usr_new_pwd': NAUplift_Constants.AD_SIMPLE_USER_CHN_PASSWORD,
                                             'utf8': False
                                             },
                     'USER_peap.py': {'internal_user': NAUplift_Constants.ADD_USER,
                                      'int_usr_pwd' :NAUplift_Constants.ADD_PASSWORD,
                                      'int_usr_new_pwd': NAUplift_Constants.ADD_NEWPASSWORD,
                                      'utf8':False
                                      },
                     'USER_SPECIAL_peap.py': {'internal_user': NAUplift_Constants.ADD_USER_SPECIAL,
                                              'int_usr_pwd': NAUplift_Constants.ADD_PASSWORD,
                                              'int_usr_new_pwd': NAUplift_Constants.ADD_NEWPASSWORD,
                                              'utf8':False
                                              },
                     'VAR_LEN_PWD_peap.py': {'internal_user': NAUplift_Constants.AD_VAR_LEN_USER,
                                             'int_usr_pwd': NAUplift_Constants.AD_VAR_LEN_PWD,
                                             'int_usr_new_pwd': NAUplift_Constants.AD_VAR_LEN_CHN_PWD,
                                             'utf8':False
                                             },
                     'UTF_USER_peap.py': {'internal_user': NAUplift_Constants.AD_UTF_USER,
                                          'int_usr_pwd': NAUplift_Constants.AD_USER_PASSWORD,
                                          'int_usr_new_pwd': NAUplift_Constants.ADD_NEWPASSWORD,
                                          'utf8': True
                                          }
                     }

peap_mschapv2_cfg_data = {'SIMPLE_USER_peapms.py': {'internal_user': NAUplift_Constants.AD_SIMPLE_USER + '@' + AD_DOMAIN_NAME,
                                                    'int_usr_pwd': NAUplift_Constants.AD_SIMPLE_USER_PASSWORD,
                                                    'int_usr_new_pwd': NAUplift_Constants.AD_SIMPLE_USER_CHN_PASSWORD,
                                                    'peap_ciphers' :"AES128-SHA",
                                                    'utf8': False
                                                    },
                          'USER_peapms.py': {'internal_user': NAUplift_Constants.ADD_USER,
                                             'int_usr_pwd' :NAUplift_Constants.ADD_PASSWORD,
                                             'int_usr_new_pwd': NAUplift_Constants.ADD_NEWPASSWORD,
                                             'peap_ciphers' :"AES128-SHA",
                                             'utf8':False
                                             },
                          'user_nxtlgn_pwdcng_peapms.py': {'internal_user':'user_nxtlgn_pwdchng',
                                                           'int_usr_pwd':NAUplift_Constants.ADD_PASSWORD,
                                                           'int_usr_new_pwd':  NAUplift_Constants.ADD_NEWPASSWORD,
                                                           'peap_ciphers' :"AES128-SHA",
                                                           'utf8': False
                                                           },
                          'UTF8USER_peapms.py': {'internal_user': NAUplift_Constants.ADD_UTF8USER,
                                                 'int_usr_pwd': NAUplift_Constants.ADD_PASSWORD,
                                                 'int_usr_new_pwd': NAUplift_Constants.ADD_NEWPASSWORD,
                                                 'peap_ciphers' :"AES128-SHA",
                                                 'utf8': True
                                                  },
                          'SIMPLE_USER_peapms_md5.py': {'internal_user': NAUplift_Constants.AD_SIMPLE_USER + '@' + AD_DOMAIN_NAME,
                                                    'int_usr_pwd': NAUplift_Constants.AD_SIMPLE_USER_PASSWORD,
                                                    'int_usr_new_pwd': NAUplift_Constants.AD_SIMPLE_USER_CHN_PASSWORD,
                                                    'peap_ciphers' : NAUplift_Constants.MD5,
                                                    'utf8': False
                                                    },
                          }

def copy_pez_files(obj):

    pez_config_file_peap = "utilities/simulators/pez/pez_config_files/" \
                      "protocols/peap_gtc_working.py"

    pez_config_file_mschapv2 = "utilities/simulators/pez/pez_config_files/" \
                      "protocols/peap_eap_mschapv2.py"


    obj.pezlib = Pezlib()
    obj.pezlib.create_directory(dirname='/tmp/peap_eap_gtc')
    obj.pezlib.create_directory(dirname='/tmp/peap_mschapv2')

    #peap_eap_cfg_data
    for key in peap_eap_cfg_data:

        obj.changes_peap_gtc = {"radius:host": "{}".format(obj.iseIP),
                                "radius:attributes:User-Name": "{}".format(peap_eap_cfg_data[key]['internal_user']),
                                "radius:attributes:User-Password": "{}".format(peap_eap_cfg_data[key]['int_usr_pwd']),
                                "peap:eap_gtc:Change Password": "{}".format(peap_eap_cfg_data[key]['int_usr_new_pwd']),
                                "peap:eap_gtc:Password": "{}".format(peap_eap_cfg_data[key]['int_usr_pwd']),
                                "eap:inner_identity": "{}".format(peap_eap_cfg_data[key]['internal_user']),
                                "radius:secret": "acsi"}

        obj.pezlib.copy_pez_cfg_folder_test(root_path=NAUplift_Constants.strPath,
                                            config_file_path=pez_config_file_peap,
                                            changable_value=obj.changes_peap_gtc,
                                            local_path='/tmp/peap_eap_gtc' + '/' + key,
                                            utf8=peap_eap_cfg_data[key]['utf8']
                                            )

    obj.pezlib.copy_config_folder('/tmp/peap_eap_gtc')

    #peap_mschapv2_cfg_data
    for key in peap_mschapv2_cfg_data:

        obj.changes_mschapv2 = {"ciphers": "{}".format(peap_mschapv2_cfg_data[key]['peap_ciphers']),
                       "peap:eap_ms_chapv2:name": "{}".format(peap_mschapv2_cfg_data[key]['internal_user']),
                       "peap:eap_ms_chapv2:password": "{}".format(peap_mschapv2_cfg_data[key]['int_usr_pwd']),
                       "peap:eap_ms_chapv2:new_password": "{}".format(peap_mschapv2_cfg_data[key]['int_usr_new_pwd']),
                       "eap:inner_identity": "{}".format(peap_mschapv2_cfg_data[key]['internal_user']),
                       "radius:host": "{}".format(obj.iseIP),
                       "radius:secret": "acsi",
                       "radius:attributes:User-Name": "{}".format(peap_mschapv2_cfg_data[key]['internal_user']),
                       "radius:attributes:User-Password": "{}".format(peap_mschapv2_cfg_data[key]['int_usr_pwd'])  }

        obj.pezlib.copy_pez_cfg_folder_test(root_path=NAUplift_Constants.strPath,
                                            config_file_path=pez_config_file_mschapv2,
                                            changable_value=obj.changes_mschapv2,
                                            local_path='/tmp/peap_mschapv2' + '/' + key,
                                            utf8=peap_mschapv2_cfg_data[key]['utf8']
                                            )
    obj.pezlib.copy_config_folder('/tmp/peap_mschapv2')

class Commonsetup(aetest.CommonSetup):
    @aetest.subsection
    def commonsetup(self):

        get_device_attributes(self)
        s_log.info(" ********* PEAP_EAP_TESTS Common Setting **********")
        set_peap_eap_tests_common_settting(self)
        pez_utils.start_pez_docker_image(docker_image="dockerhub.cisco.com/isepy-release-docker/pez-executer",
                                         docker_image_version="v4")

        copy_pez_files(self)

#Policy AD
class US342239_Tnt5212325c_PEAP_GTC_AD_Change_password(aetest.Testcase):
    @aetest.setup
    def setup(self):
        get_device_attributes(self)

    @aetest.test
    def Tnt5212325c(self):
        # pez_utils.start_pez_docker_image(docker_image="dockerhub.cisco.com/isepy-release-docker/pez-executer",
        #                                  docker_image_version="v4")

        # PEZ Authentication Flow
        s_log.info("---------------- PEZ AUTHENTICATION FLOW  -----------")
        self.pezlib = Pezlib()

        # Run EAP-TLS Authentication
        self.pezlib.run_and_verify_pezcmd('/tmp/' + 'SIMPLE_USER_peap.py',
                                          tls_config=False,
                                          negative_test=False)
        # Add Validation Steps
        UiLib.bindFunction(self, UiLib.radius_live_logs, [NAUplift_Constants.AD_SIMPLE_USER + "@" + AD_DOMAIN_NAME,
                                                          None])

        functs=[self.radius_live_logs]
        runFunctionsInOrderV2(functs, self, RETRIES,
                              resumeLastSession=True,
                              killFFWhenFinished=True,
                              record=record_option
                              )
    @aetest.cleanup
    def cleanup(self):
        pass

class US342271_Tnt5214193c_Authentication_with_passwords_of_various_lengths(aetest.Testcase):

    @aetest.setup
    def setup(self):
        get_device_attributes(self)

    @aetest.test
    def Tnt5214193c(self):

        # PEZ Authentication Flow
        s_log.info("---------------- PEZ AUTHENTICATION FLOW  -----------")
        self.pezlib = Pezlib()

        self.pezlib.run_and_verify_pezcmd('/tmp/' + 'VAR_LEN_PWD_peap.py',
                                          tls_config=False,
                                          negative_test=False)

        # Add Validation Steps
        UiLib.bindFunction(self, UiLib.radius_live_logs, [NAUplift_Constants.AD_VAR_LEN_USER,
                                                          AD_DOMAIN_NAME])
        functs=[self.radius_live_logs]
        runFunctionsInOrderV2(functs, self, RETRIES,
                              killFFWhenFinished=True,
                              record=record_option
                              )
    @aetest.cleanup
    def cleanup(self):
        pass

class US342254_Tnt5212069c_Authentication_with_UTF8(aetest.Testcase):

    @aetest.setup
    def setup(self):
        get_device_attributes(self)

    @aetest.test
    def Tnt5212069c(self):

        # PEZ Authentication Flow
        s_log.info("---------------- PEZ AUTHENTICATION FLOW  -----------")
        self.pezlib = Pezlib()

        # Run PEAP-GTC Authentication
        self.pezlib.run_and_verify_pezcmd('/tmp/' + 'UTF_USER_peap.py',
                                          tls_config=False,
                                          negative_test=False)
        # Add Validation Steps
        UiLib.bindFunction(self, UiLib.radius_live_logs, [NAUplift_Constants.AD_UTF_USER, AD_DOMAIN_NAME])

        functs=[self.radius_live_logs]
        runFunctionsInOrderV2(functs, self, RETRIES,
                              killFFWhenFinished=True,
                              record=record_option
                              )
    @aetest.cleanup
    def cleanup(self):
        pass

class US353137_Tnt5211328c_PEAP_MSCHAPv2_against_AD(aetest.Testcase):

    @aetest.setup
    def setup(self):
        get_device_attributes(self)

    @aetest.test
    def Tnt5211328c(self):
        UiLib.bindFunction(self, UiLib.Enable_Peap_Eap_Mschap, [])

        functs = [self.Enable_Peap_Eap_Mschap]
        runFunctionsInOrderV2(functs, self, RETRIES,
                              resumeLastSession=True,
                              killFFWhenFinished=True,
                              record=record_option
                              )

        # PEZ Authentication Flow
        s_log.info("---------------- PEZ AUTHENTICATION FLOW  -----------")
        self.pezlib = Pezlib()

        self.pezlib.run_and_verify_pezcmd('/tmp/' + 'SIMPLE_USER_peapms.py',
                                          tls_config=False,
                                          negative_test=False)

        # Add Validation Steps
        UiLib.bindFunction(self, UiLib.radius_live_logs, [NAUplift_Constants.AD_SIMPLE_USER + '@' + AD_DOMAIN_NAME,
                                                          None])
        functs=[self.radius_live_logs  ]
        runFunctionsInOrderV2(functs, self, RETRIES,
                              killFFWhenFinished=True,
                              record=record_option
                              )
    @aetest.cleanup
    def cleanup(self):
        pass

# Internal Users Next login
class US342269_Tnt5213050c_Change_user_password_against_internal_identity_store(aetest.Testcase):
    @aetest.setup
    def setup(self):
        get_device_attributes(self)

    @aetest.test
    def Tnt5213050c(self):
        UiLib.bindFunction(self, UiLib.edit_identity_source_in_default_policy, ["Internal Users", POLICY_SET])
        funcs = [self.edit_identity_source_in_default_policy]

        runFunctionsInOrderV2(funcs, self, RETRIES,
                              resumeLastSession=True,
                              killFFWhenFinished=True,
                              record=record_option
                              )

        # PEZ Authentication Flow
        s_log.info("---------------- PEZ AUTHENTICATION FLOW  -----------")
        self.pezlib = Pezlib()

        ## Run EAP-TLS Authentication
        self.pezlib.run_and_verify_pezcmd('/tmp/' + 'USER_peap.py',
                                          tls_config=False,
                                          negative_test=False)

        # Add Validation Steps
        UiLib.bindFunction(self, UiLib.radius_live_logs, [NAUplift_Constants.ADD_USER, None])
        functs=[self.radius_live_logs]

        runFunctionsInOrderV2(functs, self, RETRIES,
                              resumeLastSession=True,
                              killFFWhenFinished=True,
                              record=record_option
                              )
    @aetest.cleanup
    def cleanup(self):
        pass

#Internal Users Next login
class US341330_Tnt5048856c_Change_internal_user_password(aetest.Testcase):
    @aetest.setup
    def setup(self):
        get_device_attributes(self)

    @aetest.test
    def Tnt5048856c(self):

        # # PEZ Authentication Flow
        s_log.info("---------------- PEZ AUTHENTICATION FLOW  -----------")
        self.pezlib = Pezlib()

        # Run Peap EAP MSCHAPV2 Authentication
        self.pezlib.run_and_verify_pezcmd('/tmp/' + 'user_nxtlgn_pwdcng_peapms.py',
                                          tls_config=False,
                                          negative_test=False)

        # Add Validation Steps
        UiLib.bindFunction(self, UiLib.radius_live_logs, ["user_nxtlgn_pwdchng",
                                                               None])
        functs=[self.radius_live_logs]

        runFunctionsInOrderV2(functs, self, RETRIES,
                              resumeLastSession=True,
                              killFFWhenFinished=True,
                              record=record_option
                              )
    @aetest.cleanup
    def cleanup(self):
        pass

class US357385_Tnt5213065c_Auth_with_special_characters_PEAP_GTC(aetest.Testcase):
    @aetest.setup
    def setup(self):
        get_device_attributes(self)

    @aetest.test
    def Tnt5213065c(self):

        # PEZ Authentication Flow
        s_log.info("---------------- PEZ AUTHENTICATION FLOW  -----------")
        self.pezlib = Pezlib()

        # Run PEAP-GTC Authentication
        self.pezlib.run_and_verify_pezcmd('/tmp/' + 'USER_SPECIAL_peap.py',
                                          tls_config=False,
                                          negative_test=False)

        # Add Validation Steps
        UiLib.bindFunction(self, UiLib.radius_live_logs, [NAUplift_Constants.ADD_USER_SPECIAL, None])
        functs=[self.radius_live_logs]
        runFunctionsInOrderV2(functs, self, RETRIES,
                              resumeLastSession=True,
                              killFFWhenFinished=True,
                              record=record_option
                              )
    @aetest.cleanup
    def cleanup(self):
        pass

class US341331_Tnt5048980c_Change_internal_user_password_when_user_define_with_UTF_8(aetest.Testcase):
    @aetest.setup
    def setup(self):
        get_device_attributes(self)

    @aetest.test
    def Tnt5048980c(self):

        UiLib.bindFunction(self, UiLib.identities_add_simple_user, [NAUplift_Constants.ADD_USER,
                                                                    NAUplift_Constants.ADD_EMAIL,
                                                                    NAUplift_Constants.ADD_PASSWORD])

        functs = [ self.identities_add_simple_user]
        runFunctionsInOrderV2(functs, self, RETRIES,
                              resumeLastSession=True,
                              killFFWhenFinished=True,
                              record=record_option
                              )

        # PEZ Authentication Flow
        s_log.info("---------------- PEZ AUTHENTICATION FLOW  -----------")
        self.pezlib = Pezlib()

        self.pezlib.run_and_verify_pezcmd('/tmp/' + 'UTF8USER_peapms.py',
                                          tls_config=False,
                                          negative_test=False)

        # Add Validation Steps
        UiLib.bindFunction(self, UiLib.radius_live_logs, [NAUplift_Constants.ADD_UTF8USER, None])
        functs=[self.radius_live_logs]
        runFunctionsInOrderV2(functs, self, RETRIES,
                              resumeLastSession=True,
                              killFFWhenFinished=True,
                              record=record_option
                              )
    @aetest.cleanup
    def cleanup(self):
        pass

class US342270_Tnt5213718c_Fast_reconnect(aetest.Testcase):
    @aetest.setup
    def setup(self):
        get_device_attributes(self)

    @aetest.test
    def Tnt5213718c(self):


        # PEZ Authentication Flow
        s_log.info("---------------- PEZ AUTHENTICATION FLOW  -----------")
        self.pezlib = Pezlib()

        self.pezlib.run_and_verify_pezcmd('/tmp/' + 'USER_peap.py',
                                          tls_config=False,
                                          negative_test=False)

        # Add Validation Steps
        UiLib.bindFunction(self, UiLib.radius_live_logs, [NAUplift_Constants.ADD_USER, None])
        functs=[self.radius_live_logs]

        runFunctionsInOrderV2(functs, self, RETRIES,
                              resumeLastSession=True,
                              killFFWhenFinished=True,
                              record=record_option
                              )
    @aetest.cleanup
    def cleanup(self):
        pass

class US359233_Tnt5281274c_Verify_authentication_when_2nd_Shared_Secret_key_maching(aetest.Testcase):

    @aetest.setup
    def setup(self):
        get_device_attributes(self)

    @aetest.test
    def Tnt5281274c(self):
        # pez_utils.start_pez_docker_image(docker_image="dockerhub.cisco.com/isepy-release-docker/pez-executer",
        #                                  docker_image_version="v4")

        UiLib.bindFunction(self, UiLib.networkDevices_create_with_range_and_two_secret,
                           [NAUplift_Constants.NETWORK_DEVICE_NAME,
                            self.nad_ip,
                            NAUplift_Constants.SHARED_SECRET, 'asci', '32'])

        functs = [self.networkDevices_create_with_range_and_two_secret]
        runFunctionsInOrderV2(functs, self, RETRIES,
                              resumeLastSession=True,
                              killFFWhenFinished=True,
                              record=record_option
                              )

        # PEZ Authentication Flow
        s_log.info("---------------- PEZ AUTHENTICATION FLOW  -----------")
        self.pezlib = Pezlib()

        self.pezlib.run_and_verify_pezcmd('/tmp/' + 'USER_peapms.py',
                                          tls_config=False,
                                          negative_test=False)

        # Add Validation Steps
        UiLib.bindFunction(self, UiLib.radius_live_logs, [NAUplift_Constants.ADD_USER,
                                                          None])
        functs=[self.radius_live_logs]
        runFunctionsInOrderV2(functs, self, RETRIES,
                              killFFWhenFinished=True,
                              record=record_option
                              )
    @aetest.cleanup
    def cleanup(self):
        pass

class US342251_Tnt5753124c_Authentication_using_Active_Directory_groups_and_attributes(aetest.Testcase):
    @aetest.setup
    def setup(self):
        get_device_attributes(self)

    @aetest.test
    def Tnt5753124c(self):
        # pez_utils.start_pez_docker_image(docker_image="dockerhub.cisco.com/isepy-release-docker/pez-executer",
        #                                  docker_image_version="v4")

        UiLib.bindFunction(self, UiLib.config_network_device, [NAUplift_Constants.NETWORK_DEVICE_NAME,
                                                              self.nad_ip,
                                                              NAUplift_Constants.SHARED_SECRET])
        UiLib.bindFunction(self, UiLib.edit_identity_source_in_default_policy, [NAUplift_Constants.AD_NAME,
                                                                               POLICY_SET])
        UiLib.bindFunction(self, UiLib.create_authorization_rule_for_simple_condition, [POLICY_SET,
                                                                                        AUTHZ_POLICY_NAME[1],
                                                                                       AUTH_COND_NAME[1],
                                                                                       AUTH_PROFILE,
                                                                                       None])

        functs = [self.config_network_device,
                  self.edit_identity_source_in_default_policy,
                  self.create_authorization_rule_for_simple_condition
                  ]
        runFunctionsInOrderV2(functs, self, RETRIES,
                              resumeLastSession=True,
                              killFFWhenFinished=True,
                              #record=record_option
                              record=True
                              )

        # PEZ Authentication Flow
        s_log.info("---------------- PEZ AUTHENTICATION FLOW  -----------")
        self.pezlib = Pezlib()

        # Run PEAP-GTC Authentication
        self.pezlib.run_and_verify_pezcmd('/tmp/' + 'SIMPLE_USER_peap.py',
                                          tls_config=False,
                                          negative_test=False)

        # Add Validation Steps
        UiLib.bindFunction(self, UiLib.radius_live_logs,
                           [NAUplift_Constants.AD_SIMPLE_USER + '@' + AD_DOMAIN_NAME, None])
        functs=[self.radius_live_logs]
        runFunctionsInOrderV2(functs, self, RETRIES,
                              resumeLastSession=True,
                              killFFWhenFinished=True,
                              record=record_option,
                              recordingDir=NAS_FOLDER
                             )
    @aetest.cleanup
    def cleanup(self):
        pass

class Tnt5121851c_Change_User_password_against_domain_in_the_Authentication_domain(aetest.Testcase):
    @aetest.setup
    def setup(self):
        get_device_attributes(self)

    @aetest.test
    def Tnt5121851c(self):
        # step2:
        # Enable domain in the Authentication domain
        UiLib.bindFunction(self, UiLib.domain_authentication_enable, [NAUplift_Constants.AD_SCOPE1,
                                                                      NAUplift_Constants.AD_NAME,
                                                                      AD_DOMAIN_NAME])

        funcs = [self.domain_authentication_enable]

        runFunctionsInOrderV2(funcs, self, RETRIES,
                              resumeLastSession=True,
                              killFFWhenFinished=True,
                              record=record_option
                              )

        # PEZ Authentication Flow
        s_log.info("---------------- PEZ AUTHENTICATION FLOW  -----------")
        self.pezlib = Pezlib()

        # Run EAP-TLS Authentication
        self.pezlib.run_and_verify_pezcmd('/tmp/' + 'SIMPLE_USER_peap.py',
                                          tls_config=False,
                                          negative_test=False)
        # Add Validation Steps
        UiLib.bindFunction(self, UiLib.radius_live_logs, [NAUplift_Constants.AD_SIMPLE_USER + "@" + AD_DOMAIN_NAME,
                                                          None])

        functs=[self.radius_live_logs]
        runFunctionsInOrderV2(functs, self, RETRIES,
                              resumeLastSession=True,
                              killFFWhenFinished=True,
                              record=record_option
                              )
    @aetest.cleanup
    def cleanup(self):
        pass

class US377894_Tnt5988327c_PEAP_MSCHAPv2_authentication_using_PEZ(aetest.Testcase):

    @aetest.setup
    def setup(self):
        get_device_attributes(self)

    @aetest.test
    def Tnt5988327c(self):

        UiLib.bindFunction(self, UiLib.delete_user_identity, [NAUplift_Constants.ADD_USER])

        # create new identity source sequence
        UiLib.bindFunction(self, UiLib.create_identity_source_sequence, [IDENTITY_SEQUENCE_NAME,
                                                                         ["Internal Users",
                                                                          NAUplift_Constants.AD_NAME]])

        UiLib.bindFunction(self, UiLib.create_authentication_rule_for_simple_condition,
                           [POLICY_SET, AUTHENTICATION_POLICY, AUTH_COND_NAME[2], IDENTITY_SEQUENCE_NAME])

        functs = [self.delete_user_identity,
                  self.create_identity_source_sequence,
                  self.create_authentication_rule_for_simple_condition]

        runFunctionsInOrderV2(functs, self, RETRIES,
                              resumeLastSession=True,
                              killFFWhenFinished=True,
                              record=record_option
                              )

        # PEZ Authentication Flow
        s_log.info("---------------- PEZ AUTHENTICATION FLOW  -----------")
        self.pezlib = Pezlib()

        self.pezlib.run_and_verify_pezcmd('/tmp/' + 'USER_peapms.py',
                                          tls_config=False,
                                          negative_test=False)

        # Add Validation Steps
        UiLib.bindFunction(self, UiLib.radius_live_logs, [NAUplift_Constants.ADD_USER,
                                                          None])
        functs=[self.radius_live_logs]
        runFunctionsInOrderV2(functs, self, RETRIES,
                              killFFWhenFinished=True,
                              record=record_option
                              )
    @aetest.cleanup
    def cleanup(self):
        pass


class US353137_Tnt5995039c_PEAP_MSCHAPv2_Turn_On_Weak_Cipher(aetest.Testcase):

    @aetest.setup
    def setup(self):
        get_device_attributes(self)

    @aetest.test
    def Tnt5995039c(self):
        UiLib.bindFunction(self, UiLib.Enable_Peap_Eap_Mschap, [])
        UiLib.bindFunction(self, UiLib.Enable_Weak_Ciphers, [])

        functs = [self.Enable_Peap_Eap_Mschap,
                  self.Enable_Weak_Ciphers
                  ]

        runFunctionsInOrderV2(functs, self, RETRIES,
                              resumeLastSession=True,
                              killFFWhenFinished=True,
                              record=record_option
                              )

        # PEZ Authentication Flow
        s_log.info("---------------- PEZ AUTHENTICATION FLOW  -----------")
        self.pezlib = Pezlib()

        self.pezlib.run_and_verify_pezcmd('/tmp/' + 'SIMPLE_USER_peapms_md5.py',
                                          tls_config=False,
                                          negative_test=False)

        # Add Validation Steps
        UiLib.bindFunction(self, UiLib.radius_live_logs, [NAUplift_Constants.AD_SIMPLE_USER + '@' + AD_DOMAIN_NAME,
                                                          None])
        functs=[self.radius_live_logs]
        runFunctionsInOrderV2(functs, self, RETRIES,
                              killFFWhenFinished=True,
                              record=record_option
                              )
    @aetest.cleanup
    def cleanup(self):
        pass

class US377906_Tnt5994926c_PEAP_MSCHAPv2_authentication_FIPS_mode_using_PEZ(aetest.Testcase):

    @aetest.setup
    def setup(self):
        get_device_attributes(self)

    @aetest.test
    def Tnt5994926c(self):

        UiLib.bindFunction(self, UiLib.Disable_Weak_Ciphers, [])

        # Setup for FIPS mode, removing the default protocols
        UiLib.bindFunction(self, UiLib.edit_default_allowed_protocols, [NAUplift_Constants.DEFAULT_POLICY_SET,
                                                                        False])

        # Setup the allowed protocols for FIPS mode.
        # Enable FIPS mode under Administration->Settings
        UiLib.bindFunction(self, UiLib.fips_mode_enabling_and_disabling, ["Enabled"])
        funcs = [self.Disable_Weak_Ciphers,
                 self.edit_default_allowed_protocols,
                 self.fips_mode_enabling_and_disabling
                 ]
        runFunctionsInOrderV2(funcs, self, RETRIES,
                              record=record_option,
                              killFFWhenFinished=True)

        time.sleep(100)
        s_log.info("Waited first 100 seconds")
        time.sleep(100)
        s_log.info("Waited second 100 seconds")
        time.sleep(100)
        s_log.info("Waited third 100 seconds")
        time.sleep(100)
        s_log.info("Waited fourth 100 seconds")
        time.sleep(100)
        s_log.info("Waited fifth 100 seconds")
        time.sleep(100)
        s_log.info("Waited sixth 100 seconds")
        time.sleep(100)
        s_log.info("Waited seventh 100 seconds")
        time.sleep(100)
        s_log.info("Waited eighth 100 seconds")
        time.sleep(100)
        s_log.info("Waited ninth 100 seconds")
        time.sleep(100)
        s_log.info("Waited tenth 100 seconds")
        time.sleep(100)
        s_log.info("Waited eleventh 100 seconds")

        # Creating New Protocol
        UiLib.bindFunction(self, UiLib.new_allowed_protocol,["Peap_allowed_protocol"])

        UiLib.bindFunction(self, UiLib.edit_default_policy_set,
                           ["Peap_allowed_protocol",POLICY_SET])

        funcs = [self.new_allowed_protocol,
                 self.edit_default_policy_set]

        runFunctionsInOrderV2(funcs, self, RETRIES,
                              record=record_option,
                              killFFWhenFinished=True)

        # PEZ Authentication Flow
        s_log.info("---------------- PEZ AUTHENTICATION FLOW  -----------")
        self.pezlib = Pezlib()

        self.pezlib.run_and_verify_pezcmd('/tmp/' + 'USER_peapms.py',
                                          tls_config=False,
                                          negative_test=False)

        # Add Validation Steps
        UiLib.bindFunction(self, UiLib.radius_live_logs, [NAUplift_Constants.ADD_USER,
                                                          None])
        functs=[self.radius_live_logs]
        runFunctionsInOrderV2(functs, self, RETRIES,
                              killFFWhenFinished=True,
                              record=record_option
                              )
    @aetest.cleanup
    def cleanup(self):
        pass

class TestCaseCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def commoncleanup(self):
        pass

if __name__ == '__main__':
    aetest.main()  # REQUIRED LINE


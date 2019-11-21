from tests.suites.network_access.common.common_utils import *
from tests.suites.network_access.uplift_test.na_uplift_helper import UI_methods as UiLib
from tests.suites.network_access.uplift_test.na_uplift_helper import *
import tests.suites.network_access.uplift_test.uplift_constants as NAUplift_Constants
from tests.suites.network_access.uplift_test.pez_helper import PezHelper as Pezlib

AUTHZ_COND_NAME = 'Tnt5121584c_Authz_condtn_'
# Policy set
POLICY_SET = 'Policy Set 1'
POLICY_SET_PROTOCOL = 'Default Network Access'
POLICY_SET_COND_NAME = 'Tnt5121584c_Access Protocol'
retries = 3
NAS_FOLDER = "/volume1/vms/local/session_api/selenium_record"

class Commonsetup(aetest.CommonSetup):
    @aetest.subsection
    def setup_start(self):
        pass

class US356286_Tnt5121584c_Get_attribute_name_contain_spl_char(aetest.Testcase):
    @aetest.setup
    def setup(self):
        s_log.info('Logging into the ISE')
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

        UiLib.check_app_up(self.iseIP)
        self.nad_ip = cfg.te.get_PEZ().get_ip()
        self.homeDir = automationDir()
        # Preconfigure Settings
        UiLib.bindFunction(self, UiLib.delete_all_policy_sets, [])
        UiLib.bindFunction(self, UiLib.delete_library_conditions_with_prefix, ['Tnt'])
        UiLib.bindFunction(self, UiLib.remove_all_identity_source_from_sequence, ['All_User_ID_Stores', 'default'])
        #
        funcs = [self.delete_all_policy_sets,
                 self.delete_library_conditions_with_prefix,
                 self.remove_all_identity_source_from_sequence
                 ]

        retries = 3
        runFunctionsInOrderV2(funcs, self, retries, recordingDir=NAS_FOLDER)

    @aetest.test
    def Tnt5121584c(self):
        # Constants from CLOUD file
        AD_DOMAIN_NAME = cfg.suite.get_AD()[0].get_hostname()
        AD_ADMIN_USERNAME = cfg.suite.get_AD()[0].get_login()
        AD_ADMIN_PASSWORD = cfg.suite.get_AD()[0].get_password()
        GROUP_AD = AD_DOMAIN_NAME + "/Builtin/Administrators"

        # Enabling Scope mode and creating AD, joining in the group.
        UiLib.bindFunction(self, UiLib.create_active_directory_with_any_mode,
                           [NAUplift_Constants.AD_NAME,
                            AD_DOMAIN_NAME,
                            AD_ADMIN_USERNAME,
                            AD_ADMIN_PASSWORD,
                            True,
                            NAUplift_Constants.AD_SCOPE1,
                            GROUP_AD,
                            NAUplift_Constants.INFO,
                            AD_ADMIN_USERNAME
                            ])

        # Adding ad in the identity sequence stores
        UiLib.bindFunction(self, UiLib.adding_id_source,[NAUplift_Constants.AD_NAME])

        UiLib.bindFunction(self, UiLib.edit_identity_source_in_default_policy,
                           [NAUplift_Constants.AD_SCOPE1, POLICY_SET])

        UiLib.bindFunction(self, UiLib.config_network_device,
                           [NAUplift_Constants.NETWORK_DEVICE_NAME,
                            self.nad_ip,
                            NAUplift_Constants.SHARED_SECRET])

        UiLib.bindFunction(self, UiLib.create_simple_library_condition, [POLICY_SET_COND_NAME,
                                                                         'Network Access',
                                                                         'Protocol',
                                                                         'Equals',
                                                                         'RADIUS'])
        UiLib.bindFunction(self, UiLib.create_policy_set, [POLICY_SET, POLICY_SET_COND_NAME, POLICY_SET_PROTOCOL])


        funcs = [
                self.create_active_directory_with_any_mode,
                self.adding_id_source,
                self.config_network_device,
                self.create_simple_library_condition,
                self.create_policy_set,
                self.edit_identity_source_in_default_policy,
                ]

        runFunctionsInOrderV2(funcs, self, retries, resumeLastSession=True, recordingDir=NAS_FOLDER)

        UiLib.bindFunction(self, UiLib.create_simple_library_condition, [AUTHZ_COND_NAME,
                                                                         NAUplift_Constants.AD_NAME,
                                                                         NAUplift_Constants.INFO,
                                                                         'Equals',
                                                                         NAUplift_Constants.SPL_CHARACTERS])

        UiLib.bindFunction(self, UiLib.create_authorization_rule_for_simple_condition,
                           [POLICY_SET,
                            'Authz_rule_1',
                            AUTHZ_COND_NAME,
                            'PermitAccess',
                            None])

        funcs = [
                 self.create_simple_library_condition,
                 self.create_authorization_rule_for_simple_condition
                 ]
        runFunctionsInOrderV2(funcs, self, retries, resumeLastSession=True, recordingDir=NAS_FOLDER, killFFWhenFinished=True)

        # Pez authorization
        s_log.info("---------------- PEZ AUTHENTICATION FLOW  -----------")
        pez = Pezlib()
        status = []
        try:
            s_log.info("Running for {}".format(AD_ADMIN_USERNAME))
            pez.run_pap_via_pez(1, NAUplift_Constants.strPath,
                                self.iseIP,
                                AD_ADMIN_USERNAME,
                                AD_ADMIN_PASSWORD,
                                NAUplift_Constants.SHARED_SECRET,
                                "10.0.10.151",
                                "00:05:02:00:00:01"
                                )
            status.append(True)
        except Exception as e:
            status.append(False)
            s_log.error(e)
        if not all(status):
            self.failed("Authentication failed or username is not as expected. Please check the logs above.")


    @aetest.cleanup
    def cleanup(self):
        # Deleting  PolicySet
        # Deleting  Policy
        UiLib.bindFunction(self, UiLib.delete_policy_set, [[POLICY_SET]])

        # Delete Library Conditions
        UiLib.bindFunction(self, UiLib.delete_multiple_library_condition,
                           [[POLICY_SET_COND_NAME, AUTHZ_COND_NAME]])

        # removing ad in the identity sequence stores
        UiLib.bindFunction(self, UiLib.removing_id_source, [NAUplift_Constants.AD_NAME])

        # Deleting AD
        UiLib.bindFunction(self, UiLib.delete_ad_in_scope,
                           [NAUplift_Constants.AD_SCOPE1, NAUplift_Constants.AD_NAME])

        # Delete Scope
        UiLib.bindFunction(self, UiLib.delete_scope,
                           [NAUplift_Constants.AD_SCOPE1])
        # Exit from Scope
        UiLib.bindFunction(self, UiLib.exit_scope_mode,
                           [])


        #
        funcs = [
            self.delete_policy_set,
            self.delete_multiple_library_condition,
            self.removing_id_source,
            self.delete_ad_in_scope,
            self.delete_scope,
            self.exit_scope_mode

        ]
        runFunctionsInOrderV2(funcs, self, retries, recordingDir=NAS_FOLDER, killFFWhenFinished=True)


class TestCaseCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def commoncleanup(self):
        pass

if __name__ == '__main__':
    aetest.main()  # REQUIRED LINE
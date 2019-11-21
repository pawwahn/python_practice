from tests.suites.network_access.uplift_test.na_uplift_utils import *
from tests.suites.network_access.uplift_test.na_uplift_helper import UI_methods as UiLib
# from tests.suites.network_access.uplift_test.na_uplift_helper import *
import tests.suites.network_access.uplift_test.uplift_constants as NAUplift_Constants
from tests.suites.network_access.uplift_test.pez_helper import PezHelper as Pezlib

retries = 3

AUTH_COND_NAME = "Tnt5212445c_AccessProtocol"
POLICY_SET = 'Policy Set 1'
POLICY_SET_PROTOCOL = 'Default Network Access'


class Commonsetup(aetest.CommonSetup):
    @aetest.subsection
    def setup_start(self):
        pass


class US355292_Tnt5212445c_Proxy_Authentication_using_EAP_TLS(aetest.Testcase):
    @aetest.setup
    def setup(self):
        s_log.info('Logging into the ISE')
        try:
            self.selenium_url = cfg.te.get_WIN_CLIENT().get_internal_selenium()
            s_log.info("###### SELENIUM URL ######## {} ".format(self.selenium_url))

            self.iseIP = cfg.te.get_POSITRON()[0].get_ip()
            s_log.info("###### ISE IP ######## {} ".format(self.iseIP))

            self.iseLoginurl = "https://" + self.iseIP + "/"
            s_log.info("###### ISE URL ######## {} ".format(self.iseLoginurl))

            self.iseUser = cfg.te.get_POSITRON()[0].get_login()
            s_log.info("###### ISE User ######## {} ".format(self.iseUser))

            self.isePassword = cfg.te.get_POSITRON()[0].get_password()
            s_log.info("###### ISE Password ######## {} ".format(self.isePassword))

            # RAD SERVER DETAILS
            self.iseIP_radserver = cfg.te.get_POSITRON()[1].get_ip()
            s_log.info("###### Radius IP ######## {} ".format(self.iseIP_radserver))

            self.iseUrl_radserver = "https://" + self.iseIP_radserver + "/"
            s_log.info("###### Radius URL ######## {} ".format(self.iseUrl_radserver))

            self.iseUser_radserver = cfg.te.get_POSITRON()[1].get_login()
            s_log.info("###### Radius User ######## {} ".format(self.iseUser))

            self.isePassword_radserver = cfg.te.get_POSITRON()[1].get_password()
            s_log.info("###### Radius Password ######## {} ".format(self.isePassword))

            UiLib.check_app_up(cfg.te.get_POSITRON()[0].get_ip())

            self.homeDir = automationDir()
            self.uilib = UiLib(
                self,
                seleniumUrl=self.selenium_url,
                iseUrl=self.iseLoginurl,
                logger=s_log,
                iseUser=self.iseUser,
                isePass=self.isePassword
            )

            self.app = self.uilib.login_into_ise()

            UiLib.bindFunction(self, UiLib.delete_network_device,
                               [NAUplift_Constants.NETWORK_DEVICE_NAME])

            UiLib.bindFunction(self, UiLib.delete_all_policy_sets, [])
            # Delete Library Conditions
            UiLib.bindFunction(self, UiLib.delete_library_conditions_with_prefix, ['Tnt'])

            UiLib.bindFunction(self, UiLib.delete_user_identity,
                               [NAUplift_Constants.ADD_USER])

            UiLib.bindFunction(self, UiLib.delete_radius_server_sequence,
                               [NAUplift_Constants.RADIUS_SEQUENCE_NAME])

            UiLib.bindFunction(self, UiLib.delete_rad_server,
                               [NAUplift_Constants.RADIUS_SERVER_NAME])

            UiLib.bindFunction(self, UiLib.remove_all_identity_source_from_sequence, ['All_User_ID_Stores', 'default'])

            UiLib.bindFunction(self, UiLib.trustedCertificates_deleteTrustedCertificate,
                               [NAUplift_Constants.FRIENDLYNAME_ISE_TRUSTED_CERT])

            funcs = [
                self.delete_network_device,
                self.delete_all_policy_sets,
                self.delete_library_conditions_with_prefix,
                self.delete_user_identity,
                self.delete_radius_server_sequence,
                self.delete_rad_server,
                self.remove_all_identity_source_from_sequence,
                self.trustedCertificates_deleteTrustedCertificate
            ]

            retries = 3
            runFunctionsInOrderV2(funcs, self, retries, record=False, killPreviousFF=False)
            time.sleep(5)

            self.app.quit()
            self.app.run()

            UiLib.bindFunction(self, UiLib.login_different_ise,
                               [self.iseUrl_radserver,
                                self.iseUser_radserver,
                                self.isePassword_radserver
                                ]
                               )

            UiLib.bindFunction(self, UiLib.delete_all_policy_sets, [])
            UiLib.bindFunction(self, UiLib.delete_library_conditions_with_prefix, ['Tnt'])
            UiLib.bindFunction(self, UiLib.delete_user_identity,
                               [NAUplift_Constants.ADD_USER])
            UiLib.bindFunction(self, UiLib.delete_network_device,
                               [NAUplift_Constants.NETWORK_DEVICE_NAME])

            UiLib.bindFunction(self, UiLib.trustedCertificates_deleteTrustedCertificate,
                               [NAUplift_Constants.FRIENDLYNAME_ISE_TRUSTED_CERT])

            funcs = [
                self.login_different_ise,
                self.delete_all_policy_sets,
                self.delete_library_conditions_with_prefix,
                self.delete_user_identity,
                self.delete_network_device,
                self.trustedCertificates_deleteTrustedCertificate
            ]

            retries = 3
            runFunctionsInOrderV2(funcs, self, retries, record=False, killPreviousFF=False)
            time.sleep(5)

            self.app.quit()
            self.app.run()

            self.app = self.uilib.login_into_ise()

        except Exception as E:
            s_log.error("Failed to Login to ISE - {}".format(E))
            assert False

    @aetest.test
    def Tnt5212445c(self):

        # Step 1:
        # - Configure Radius Server
        UiLib.bindFunction(self, UiLib.rad_server,
                           [NAUplift_Constants.RADIUS_SERVER_NAME,
                            self.iseIP_radserver,
                            NAUplift_Constants.SHARED_SECRET])
        # Step 2:
        # - Configure Radius Server Sequence
        UiLib.bindFunction(self, UiLib.configure_radius_server_sequence,
                           [NAUplift_Constants.RADIUS_SEQUENCE_NAME,
                            [NAUplift_Constants.RADIUS_SERVER_NAME]])
        # # Step 3:
        # # - Configure Authentication Proxy - Forward all
        # UiLib.bindFunction(self, UiLib.edit_default_policy_set,
        #                    [NAUplift_Constants.RADIUS_SEQUENCE_NAME])
        UiLib.bindFunction(self, UiLib.create_simple_library_condition, [AUTH_COND_NAME,
                                                                         'Network Access',
                                                                         'Protocol',
                                                                         'EQUALS',
                                                                         'RADIUS'])

        # Step 6:
        # create new policy set
        UiLib.bindFunction(self, UiLib.create_policy_set,
                           [POLICY_SET, AUTH_COND_NAME, NAUplift_Constants.RADIUS_SEQUENCE_NAME])

        nad_ip = cfg.te.get_PEZ().get_ip()
        UiLib.bindFunction(self, UiLib.config_network_device,
                           [NAUplift_Constants.NETWORK_DEVICE_NAME,
                            nad_ip,
                            NAUplift_Constants.SHARED_SECRET])
        # Step 4
        # Add Internal User
        UiLib.bindFunction(self, UiLib.identities_add_simple_user,
                           [NAUplift_Constants.ADD_USER,
                            NAUplift_Constants.ADD_EMAIL,
                            NAUplift_Constants.ADD_NEWPASSWORD])

        self.certificate_file = NAUplift_Constants.strPath + "resources/CommonCriteria/" + \
                                NAUplift_Constants.ISE_TRUSTED_CERT
        s_log.info("CERTIFICATE FILE PATH: {}".format(self.certificate_file))

        # step 7:
        # import root certificate on ISE:
        # Navigate to System > Certificate Operations > Trust Certificates,
        # import root certificate
        UiLib.bindFunction(self, UiLib.trustedCertificates_setTrustedCert,
                           [self.certificate_file,
                            NAUplift_Constants.FRIENDLYNAME_ISE_TRUSTED_CERT])

        retries = 3
        funcs = [self.rad_server,
                 self.configure_radius_server_sequence,
                 self.create_simple_library_condition,
                 self.create_policy_set,
                 self.config_network_device,
                 self.identities_add_simple_user,
                 self.trustedCertificates_setTrustedCert,

                 ]

        runFunctionsInOrderV2(funcs, self, retries, record=False, killPreviousFF=False)

        self.app.quit();
        self.app.run()

        # Configuration of RADIUS SERVER
        UiLib.bindFunction(self, UiLib.login_different_ise,
                           [self.iseUrl_radserver,
                            self.iseUser_radserver,
                            self.isePassword_radserver
                            ])

        # Step 09: Add user in RADIUS SERVER
        UiLib.bindFunction(self, UiLib.identities_add_simple_user,
                           [NAUplift_Constants.ADD_USER,
                            NAUplift_Constants.ADD_EMAIL,
                            NAUplift_Constants.ADD_NEWPASSWORD])

        UiLib.bindFunction(self, UiLib.config_network_device,
                           [NAUplift_Constants.NETWORK_DEVICE_NAME,
                            self.iseIP,
                            NAUplift_Constants.SHARED_SECRET])

        # step 11:
        # import root certificate on ISE to Radius Server:
        # Navigate to System > Certificate Operations > Trust Certificates, import root certificate

        UiLib.bindFunction(self, UiLib.trustedCertificates_setTrustedCert,
                           [self.certificate_file,
                            NAUplift_Constants.FRIENDLYNAME_ISE_TRUSTED_CERT])

        funcs = [
            self.login_different_ise,
            self.identities_add_simple_user,
            self.config_network_device,
            self.trustedCertificates_setTrustedCert,
        ]

        runFunctionsInOrderV2(funcs, self, retries, record=False, killPreviousFF=False)

        # PEZ Authentication Flow
        s_log.info("---------------- PEZ AUTHENTICATION FLOW -----------")
        self.pezlib = Pezlib()

        # Copy Certificates to PEZ
        self.pezlib.copy_cert_pez(root_path=NAUplift_Constants.strPath,
                                  ise_trusted_cert=NAUplift_Constants.ISE_TRUSTED_CERT,
                                  client_certificate=NAUplift_Constants.ClientSystemCerts,
                                  client_key=NAUplift_Constants.ClientSystemKeys)

        # Run EAP-TLS Authentication
        self.pezlib.run_eap_tls(root_path=NAUplift_Constants.strPath,
                                ise_trust_cert=NAUplift_Constants.ISE_TRUSTED_CERT,
                                client_sys_cert=NAUplift_Constants.ClientSystemCerts,
                                client_sys_key=NAUplift_Constants.ClientSystemKeys,
                                ise_ip=self.iseIP)

        # Validation Steps in Radius Server
        UiLib.bindFunction(self, UiLib.radius_live_logs, [NAUplift_Constants.ADD_USER, None])
        functs = [self.radius_live_logs,
                  ]
        runFunctionsInOrderV2(functs, self, retries, record=False, killPreviousFF=False)

        self.app.quit();
        self.app.run()

        # Validation in ISE
        UiLib.bindFunction(self, UiLib.login_different_ise,
                           [self.iseLoginurl,
                            self.iseUser,
                            self.isePassword
                            ])

        UiLib.bindFunction(self,
                           UiLib.radius_live_logs,
                           [NAUplift_Constants.ADD_USER, None])

        functs = [self.login_different_ise,
                  self.radius_live_logs]

        runFunctionsInOrderV2(functs,
                              self,
                              retries,
                              record=False,
                              killPreviousFF=False)
        self.app.quit();
        self.app.run()


    @aetest.cleanup
    def cleanup(self):
        time.sleep(5)

        # Validation in ISE
        UiLib.bindFunction(self, UiLib.login_different_ise,
                           [self.iseLoginurl,
                            self.iseUser,
                            self.isePassword
                            ])

        UiLib.bindFunction(self, UiLib.trustedCertificates_deleteTrustedCertificate,
                           [NAUplift_Constants.FRIENDLYNAME_ISE_TRUSTED_CERT])

        UiLib.bindFunction(self, UiLib.delete_user_identity,
                           [NAUplift_Constants.ADD_USER])

        UiLib.bindFunction(self, UiLib.delete_network_device,
                           [NAUplift_Constants.NETWORK_DEVICE_NAME])

        UiLib.bindFunction(self, UiLib.delete_policy_set, [[POLICY_SET]])
        # Delete Library Conditions
        UiLib.bindFunction(self, UiLib.delete_multiple_library_condition, [[AUTH_COND_NAME]])

        #
        UiLib.bindFunction(self, UiLib.delete_radius_server_sequence,
                           [NAUplift_Constants.RADIUS_SEQUENCE_NAME])

        UiLib.bindFunction(self, UiLib.delete_rad_server,
                           [NAUplift_Constants.RADIUS_SERVER_NAME])



        funcs = [self.login_different_ise,
                 self.trustedCertificates_deleteTrustedCertificate,
                 self.delete_user_identity,
                 self.delete_network_device,
                 self.delete_policy_set,
                 self.delete_multiple_library_condition,
                 self.delete_radius_server_sequence,
                 self.delete_rad_server
                 ]

        retries = 3
        runFunctionsInOrderV2(funcs, self, retries, record=False, killPreviousFF=False)
        time.sleep(5)

        self.app.quit();
        self.app.run()

        # Confiuration to Radius Server
        # LOGIN to Ise
        UiLib.bindFunction(self, UiLib.login_different_ise,
                           [self.iseUrl_radserver,
                            self.iseUser_radserver,
                            self.isePassword_radserver
                            ]
                           )

        UiLib.bindFunction(self, UiLib.trustedCertificates_deleteTrustedCertificate,
                           [NAUplift_Constants.FRIENDLYNAME_ISE_TRUSTED_CERT])

        UiLib.bindFunction(self, UiLib.delete_user_identity, [NAUplift_Constants.ADD_USER])

        UiLib.bindFunction(self, UiLib.delete_network_device,
                           [NAUplift_Constants.NETWORK_DEVICE_NAME])


        funcs = [self.login_different_ise,
                 self.trustedCertificates_deleteTrustedCertificate,
                 self.delete_user_identity,
                 self.delete_network_device
                 ]

        retries = 3
        runFunctionsInOrderV2(funcs, self, retries, record=False, killPreviousFF=False)
        time.sleep(5)

        self.app.quit()


class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def cleanup_section(self):
        pass

if __name__ == '__main__':
    aetest.main()  # REQUIRED LINE
from tests.suites.network_access.uplift_test.na_uplift_utils import killPreviousFireFox, appCleanup
##### @@@@@ REQUIRED LINE - DON'T DELETE @@@@@@@@@@@@@ ##########
from corelib.base.BaseTestCase import *
# from corelib.base.JobBaseTestCase import *
##### EOF - @@@@@ REQUIRED LINE - DON'T DELETE @@@@@@@@@@@@@ ##########
from utilities.simulators.pez import pez_utils
import utilities.mgmt_utils.mgmt_utils as mgmt_utils
from tests.suites.network_access import protocols_utils
# import corelib.global_variables.config as cfg

import time, types
from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import *
from corelib.selenium.selenium_ui_base_page import BasePage
from tests.configurations.ise.ui.policy.policy_elements.conditions.library_conditions import LibraryConditions
from tests.configurations.ise.ui.policy.policy_sets.new_policy_sets import RadPolicySets


class UI_methods():

    def __init__(self, testObj, seleniumUrl,
                 iseUrl, logger, iseUser,
                 isePass, save_to_disk=None
                 ):

        self.testObj = testObj
        self.seleniumUrl = seleniumUrl
        self.iseUrl = iseUrl
        self.logger = logger
        self.iseUser = iseUser
        self.isePass = isePass
        self.save_to_disk = save_to_disk
        self.cloud = cfg.env.get('cloud')
        self.argsQueue = []

    def login_into_ise(self):
        if self.cloud == True:
            selenium_ip = self.seleniumUrl.split("http://")[1].split(':')[0]
            killPreviousFireFox(ip=selenium_ip, user="seluser", pwd="secret")
        else:
            killPreviousFireFox()
        from corelib.selenium.selenium_ui_app import App
        from tests.configurations.ise.ui.login_page import Login
        self.app = App(self.seleniumUrl, default_save_to_disk=self.save_to_disk)
        page = Login(self.app, self.logger, self.iseUrl)
        page.navigate_to_page()
        page.login(self.iseUser, self.isePass, timeout=7)
        time.sleep(1)
        return self.app

    @staticmethod
    def bindFunction(obj, funcToBind, argList):
        functionName = funcToBind.__name__
        exec("obj.{} = types.MethodType({},{})".format(functionName, "funcToBind", "obj"))

        # is self.args exist?
        if not (hasattr(obj, 'args')):
            obj.args = {}

        # is self.args[functionName] exists?
        if not (functionName in obj.args):
            obj.args[functionName] = []

        for arg in argList:
            obj.args[functionName].append(arg)

    @staticmethod
    def remove_binded_args_after_run(obj, func_name, args_count):
        """
        :param obj: object of the test script class (most commonly self)
        :param args_count: number of args that needs to be deleted
        :return: removes the args mapped to a function during bindFunction
        """
        s_log.info("Removing binded attributes...")
        for _ in range(args_count):
            obj.args[func_name].pop(0)

    # verified
    def itentities_deleteAllUsers(self):
        from tests.configurations.ise.ui.administration.identity_management import identities
        identitiesPage = identities.Identities(self.app, self.logger)
        identitiesPage.navigate_to_page()
        identitiesPage.delete_all_user()
        time.sleep(1)

    # verified
    def systemCertificates_deleteSystemEapAuthenticationCertificate(self):
        from tests.configurations.ise.ui.administration.system.certificates.system_certificates import \
            SystemCertificates
        systemCertificatesPage = SystemCertificates(self.app, self.logger)
        systemCertificatesPage.navigate_to_page()
        systemCertificatesPage.delete_eap_authentication_certificate()
        time.sleep(1)

    # verified
    def systemCertificates_deleteSystemDTLSAuthenticationCertificate(self):
        from tests.configurations.ise.ui.administration.system.certificates.system_certificates import \
            SystemCertificates
        systemCertificatesPage = SystemCertificates(self.app, self.logger)
        systemCertificatesPage.navigate_to_page()
        systemCertificatesPage.delete_DTLS_authentication_certificate()
        time.sleep(1)

        # verified

    def systemCertificates_generateSystemCertificate(self):
        from tests.configurations.ise.ui.administration.system.certificates.system_certificates import \
            SystemCertificates
        from tests.suites.network_access import protocols_utils
        from tests.suites.certificates.ca_certmgmt_constants import CertRole

        systemCertificatesPage = SystemCertificates(self.app, self.logger)
        systemCertificatesPage.navigate_to_page()

        friendly_name = self.args['systemCertificates_generateSystemCertificate'][0]
        key_type = self.args['systemCertificates_generateSystemCertificate'][1]
        digest = self.args['systemCertificates_generateSystemCertificate'][2]
        hostname = self.args['systemCertificates_generateSystemCertificate'][3]
        subj = protocols_utils.Subject()
        subj.cn = hostname

        systemCertificatesPage.generate_self_signed_cert_long_api(CertRole.EAP.value, subj, False, friendly_name,
                                                                  key_type,
                                                                  digest)
        for i in range(0, 4):
            self.args['systemCertificates_generateSystemCertificate'].pop(0)

    # verified
    def trustedCertificates_deleteTrustedCertificate(self):
        from tests.configurations.ise.ui.administration.system.certificates.trusted_certificates import \
            TrustedCertificates
        trustedCertificatePage = TrustedCertificates(self.app, self.logger)

        trustedCertificate = self.args['trustedCertificates_deleteTrustedCertificate'][0]

        trustedCertificatePage.navigate_to_page()
        time.sleep(10)

        if trustedCertificatePage.certcheckbox(trustedCertificate).is_displayed():
            try:
                success_msg, success_alert = trustedCertificatePage.delete_trusted_certificate(trustedCertificate,
                                                                                               ver="2.3")
                if success_msg is None:
                    raise Exception("Trusted Certificate is not deleted - {}".format(success_alert))
                else:
                    s_log.info("#### Trusted Added Successfully ### - **** {}  ****".format(success_msg))

            except Exception as e:
                assert False, "Deletion of Trust certificate Failed - {0}".format(e)

        for i in range(0, 1):
            self.args['trustedCertificates_deleteTrustedCertificate'].pop(0)

    @appCleanup
    def trustedCertificates_setTrustedCert(self):
        from tests.configurations.ise.ui.administration.system.certificates import trusted_certificates
        trustedCertificatesPage = trusted_certificates.TrustedCertificates(self.app, self.logger)

        cert_path = self.args['trustedCertificates_setTrustedCert'][0]
        friendly_name = self.args['trustedCertificates_setTrustedCert'][1]

        trustedCertificatesPage.navigate_to_page()
        time.sleep(10)
        trustedCertificatesPage.import_trusted_certificate(
            cert_path=cert_path,
            friendly_name=friendly_name, trust_auth_ise=True, trust_client_auth=True,
            trust_auth_cisco_services=True)
        time.sleep(1)

        for i in range(0, 2):
            self.args['trustedCertificates_setTrustedCert'].pop(0)

    # verified
    def networkDevices_setDefaultDevice(self):
        from tests.configurations.ise.ui.administration.network_resources import network_device
        networkDevicePage = network_device.NetworkDevice(self.app, self.logger)
        networkDevicePage.driver.execute_script(
            'window.location.hash = "#administration/administration_networkresources/administration_networkresources_devices"')
        time.sleep(10)
        networkDeviceSecret = self.args['networkDevices_setDefaultDevice'][0]

        # networkDevicePage.navigate_to_page()
        time.sleep(10)
        networkDevicePage.enable_radius_on_default_device(networkDeviceSecret)
        time.sleep(10)

        self.args['networkDevices_setDefaultDevice'].pop(0)

    def networkDevices_setDefaultDevice_with2secret(self):
        from tests.configurations.ise.ui.administration.network_resources import network_device
        networkDevicePage = network_device.NetworkDevice(self.app, self.logger)
        networkDevicePage.driver.execute_script(
            'window.location.hash = "#administration/administration_networkresources/administration_networkresources_devices"')
        time.sleep(10)

        networkDeviceSecret1 = self.args['networkDevices_setDefaultDevice_with2secret'][0]
        networkDeviceSecret2 = self.args['networkDevices_setDefaultDevice_with2secret'][1]

        # networkDevicePage.navigate_to_page()
        networkDevicePage.enable_radius_on_default_device_with_2_ss(networkDeviceSecret1, networkDeviceSecret2)
        time.sleep(1)

        self.args['networkDevices_setDefaultDevice_with2secret'].pop(0)

    def sgacls_deleteAll(self):

        from tests.configurations.ise.ui.workcenters.trustsec.components.security_group_acl import \
            security_group_acl
        security_group_acl_page = security_group_acl(self.app, self.logger)

        security_group_acl_page.navigate_to_page()
        security_group_acl_page.delete_all_sgacls()
        time.sleep(1)

    def matrixPolicy_deleteAll(self):
        from tests.configurations.ise.ui.workcenters.trustsec.trustesc_policy.matrix import matrix
        matrix_page = matrix(self.app, self.logger)
        matrix_page.navigate_to_page()
        time.sleep(7)
        matrix_page.delete_all_policies()
        time.sleep(1)

    def networkDevices_setDTLSDefaultDevice(self):
        from tests.configurations.ise.ui.administration.network_resources import network_device
        networkDevicePage = network_device.NetworkDevice(self.app, self.logger)
        networkDevicePage.driver.execute_script(
            'window.location.hash = "#administration/administration_networkresources/administration_networkresources_devices"')
        time.sleep(10)
        # networkDevicePage.navigate_to_page()
        networkDevicePage.enable_radius_on_default_device('', dtls=True)

    def networkDevices_deleteAll(self):
        from tests.configurations.ise.ui.administration.network_resources import network_device
        networkDevicePage = network_device.NetworkDevice(self.app, self.logger)
        networkDevicePage.driver.execute_script(
            'window.location.hash = "#administration/administration_networkresources/administration_networkresources_devices"')
        time.sleep(10)

        # networkDevicePage.navigate_to_page()
        networkDevicePage.delete_all_devices()
        time.sleep(1)

    def networkDevices_disableRadiusOnDefaultDevice(self):
        from tests.configurations.ise.ui.administration.network_resources import network_device
        networkDevicePage = network_device.NetworkDevice(self.app, self.logger)
        networkDevicePage.driver.execute_script(
            'window.location.hash = "#administration/administration_networkresources/administration_networkresources_devices"')
        time.sleep(10)

        # networkDevicePage.navigate_to_page()
        networkDevicePage.disable_radius_on_default_device()
        time.sleep(1)

    def networkDevices_create_with_range_and_two_secret(self):
        from tests.configurations.ise.ui.administration.network_resources import network_device
        networkDevicePage = network_device.NetworkDevice(self.app, self.logger)
        networkDevicePage.driver.execute_script(
            'window.location.hash = "#administration/administration_networkresources/administration_networkresources_devices"')
        time.sleep(10)
        # networkDevicePage.navigate_to_page()
        time.sleep(2)
        nadWithRange = self.args['networkDevices_create_with_range_and_two_secret'][0]
        nadIPwithRange = self.args['networkDevices_create_with_range_and_two_secret'][1]
        networkDeviceSecret1 = self.args['networkDevices_create_with_range_and_two_secret'][2]
        networkDeviceSecret2 = self.args['networkDevices_create_with_range_and_two_secret'][3]
        nadMASK = self.args['networkDevices_create_with_range_and_two_secret'][4]
        if networkDevicePage.nad_by_name(nad_name=nadWithRange):
            networkDevicePage.delete_network_device(name1=nadWithRange)
        time.sleep(5)
        networkDevicePage.add_network_device_second_shared_secret(nadWithRange, nadIPwithRange,
                                                                  networkDeviceSecret1,
                                                                  second_shared_secret=networkDeviceSecret2,
                                                                  mask=nadMASK)
        time.sleep(2)
        for i in range(0, 5):
            self.args['networkDevices_create_with_range_and_two_secret'].pop(0)

    # verified
    def systemCertificates_setSystemCert(self):
        from tests.configurations.ise.ui.administration.system.certificates import system_certificates
        systemCertificatesPage = system_certificates.SystemCertificates(self.app, self.logger)

        Node = self.args['systemCertificates_setSystemCert'][0]
        cert_path = self.args['systemCertificates_setSystemCert'][1]
        key_file_path = self.args['systemCertificates_setSystemCert'][2]
        cert_password = self.args['systemCertificates_setSystemCert'][3]
        friendly_name = self.args['systemCertificates_setSystemCert'][4]
        eap_usage = self.args['systemCertificates_setSystemCert'][5]

        # 3. install system cert of ISE
        systemCertificatesPage.navigate_to_page()
        systemCertificatesPage.import_system_certificate(Node,
                                                         cert_path=cert_path,
                                                         key_file_path=key_file_path,
                                                         cert_password=cert_password,
                                                         friendly_name=friendly_name,
                                                         eap_usage=eap_usage)
        time.sleep(1)

        for i in range(0, 6):
            self.args['systemCertificates_setSystemCert'].pop(0)

    # verified
    def systemCertificates_setSystemCertDTLS(self):
        from tests.configurations.ise.ui.administration.system.certificates import system_certificates
        systemCertificatesPage = system_certificates.SystemCertificates(self.app, self.logger)

        Node = self.args['systemCertificates_setSystemCertDTLS'][0]
        cert_path = self.args['systemCertificates_setSystemCertDTLS'][1]
        key_file_path = self.args['systemCertificates_setSystemCertDTLS'][2]
        cert_password = self.args['systemCertificates_setSystemCertDTLS'][3]
        friendly_name = self.args['systemCertificates_setSystemCertDTLS'][4]

        # 3. install system cert of ISE
        systemCertificatesPage.navigate_to_page()
        systemCertificatesPage.import_system_certificate(Node,
                                                         cert_path=cert_path,
                                                         key_file_path=key_file_path,
                                                         cert_password=cert_password,
                                                         friendly_name=friendly_name,
                                                         radius_usage=True)
        time.sleep(1)

        for i in range(0, 5):
            self.args['systemCertificates_setSystemCertDTLS'].pop(0)

    # verified
    def identities_addUser(self):
        from tests.configurations.ise.ui.administration.identity_management import identities
        identitiesPage = identities.Identities(self.app, self.logger)

        testUser = self.args['identities_addUser'][0]
        testEmail = self.args['identities_addUser'][1]
        testPassword = self.args['identities_addUser'][2]

        identitiesPage.navigate_to_page()
        identitiesPage.add_user(testUser, testEmail, testPassword)
        time.sleep(1)

        for i in range(0, 3):
            self.args['identities_addUser'].pop(0)

    def ers_enable(self):
        from tests.configurations.ise.ui.administration.system.settings.ers_settings import ErsSettings
        self.page = ErsSettings(self.app, self.logger)
        self.page.navigate_to_page()
        self.page.short_enable_ers_settings()

    def securityGroup_import(self):
        from tests.configurations.ise.ui.workcenters.trustsec.components.security_group import Security_Groups
        self.securityGroupPage = Security_Groups(self.app, self.logger)

        fileToImport = self.args['securityGroup_import'][0]
        maxOperationTimeMinutes = self.args['securityGroup_import'][1]

        self.securityGroupPage.navigate_to_page()
        self.securityGroupPage.import_sgt_from_file(fileToImport, maxOperationTimeMinutes)

        for i in range(0, 2):
            self.args['securityGroup_import'].pop(0)

    def securityGroup_addSgt(self):
        from tests.configurations.ise.ui.workcenters.trustsec.components.security_group import Security_Groups

        # def add_sgt(self, sgt, num):
        security_group_page = Security_Groups(self.app, self.logger)

        sgt = self.args['securityGroup_addSgt'][0]
        num = self.args['securityGroup_addSgt'][1]
        icon = self.args['securityGroup_addSgt'][2]

        security_group_page.navigate_to_page()
        security_group_page.add_sgt(sgt, num, icon)

        for i in range(0, 3):
            self.args['securityGroup_addSgt'].pop(0)

    def securityGroup_deleteAll(self):
        from tests.configurations.ise.ui.workcenters.trustsec.components.security_group import Security_Groups
        security_group_page = Security_Groups(self.app, self.logger)

        maxOperationTimeMinutes = self.args['securityGroup_deleteAll'][0]

        security_group_page.navigate_to_page()
        security_group_page.deleteAllSgts(maxOperationTimeMinutes)

        self.args['securityGroup_deleteAll'].pop(0)

    def identities_dummyEditUser(self):
        from tests.configurations.ise.ui.administration.identity_management import identities
        identitiesPage = identities.Identities(self.app, self.logger)

        testUser = self.args['identities_dummyEditUser'][0]
        testEmail = self.args['identities_dummyEditUser'][1]

        identitiesPage.navigate_to_page()
        identitiesPage.edit_user(testUser, testUser, testEmail)
        time.sleep(1)

        for i in range(0, 2):
            self.args['identities_dummyEditUser'].pop(0)

    # verified
    def securitySetting_setCheckbox(self):
        from tests.configurations.ise.ui.administration.system.settings import security_settings
        securitySettingPage = security_settings.securitySettings(self.app, self.logger)

        checkbox = self.args['securitySetting_setCheckbox'][0]
        checkBox_value = self.args['securitySetting_setCheckbox'][1]

        securitySettingPage.navigate_to_page()
        securitySettingPage.select_checkBox(checkbox, checkBox_value)
        time.sleep(1)

        for i in range(0, 2):
            self.args['securitySetting_setCheckbox'].pop(0)

    def securitySetting_setTwoCheckbox(self):
        from tests.configurations.ise.ui.administration.system.settings import security_settings
        securitySettingPage = security_settings.securitySettings(self.app, self.logger)

        checkbox1 = self.args['securitySetting_setTwoCheckbox'][0]
        checkBox1_value = self.args['securitySetting_setTwoCheckbox'][1]
        checkbox2 = self.args['securitySetting_setTwoCheckbox'][2]
        checkBox2_value = self.args['securitySetting_setTwoCheckbox'][3]

        securitySettingPage.navigate_to_page()
        securitySettingPage.select_two_checkBoxes(checkbox1, checkbox2, checkBox1_value, checkBox2_value)
        time.sleep(1)

        for i in range(0, 4):
            self.args['securitySetting_setCheckbox'].pop(0)

    def securitySetting_setAllCheckboxs(self):
        from tests.configurations.ise.ui.administration.system.settings import security_settings
        securitySettingPage = security_settings.securitySettings(self.app, self.logger)

        securitySettingPage.navigate_to_page()
        securitySettingPage.select_all_checkbox()
        time.sleep(1)

    @appCleanup
    def logging_changeLogLevel(self):
        from tests.configurations.ise.ui.administration.system.logging import logging as loggingUI
        loggingPage = loggingUI.Logging(self.app, self.logger)

        nodeNamde = self.args['logging_changeLogLevel'][0]
        log = self.args['logging_changeLogLevel'][1]
        logLevel = self.args['logging_changeLogLevel'][2]

        loggingPage.navigate_to_page()
        loggingPage.changeLogLevel_debugLogConfiguration(nodeNamde, log, logLevel)

        for i in range(0, 3):
            self.args['logging_changeLogLevel'].pop(0)

    def trustedCertificates_downloadCrl(self):
        from tests.configurations.ise.ui.administration.system.certificates import trusted_certificates
        trustedCertificatesPage = trusted_certificates.TrustedCertificates(self.app, self.logger)

        trustedCert = self.args['trustedCertificates_downloadCrl'][0]
        serverIp = self.args['trustedCertificates_downloadCrl'][1]
        serverPort = self.args['trustedCertificates_downloadCrl'][2]
        usedServerProtocol = self.args['trustedCertificates_downloadCrl'][3]

        trustedCertificatesPage.navigate_to_page()
        trustedCertificatesPage.download_crl(trustedCert, serverIp, serverPort, usedServerProtocol)

        for i in range(0, 4):
            self.args['trustedCertificates_downloadCrl'].pop(0)

    def trustedCertificates_dummyAction(self):
        from tests.configurations.ise.ui.administration.system.certificates import trusted_certificates
        trustedCertificatesPage = trusted_certificates.TrustedCertificates(self.app, self.logger)

        trustedCert = self.args['trustedCertificates_dummyAction'][0]

        trustedCertificatesPage.navigate_to_page()
        trustedCertificatesPage.dummyAction(trustedCert)

        self.args['trustedCertificates_dummyAction'].pop(0)

    def sxpService_enable(self):
        from tests.configurations.ise.ui.administration.system import deployment
        deploymentPage = deployment.Deployment(self.app, self.logger)

        persona = self.args['sxpService_enable'][0]

        deploymentPage.navigate_to_page()
        deploymentPage.edit_node_personas("Positron", enable_pan_persona=True, enable_mnt_persona=True,
                                          enable_pxgrid_persona=False,
                                          enable_psn_persona=True, enable_sxp=True)

        self.args['sxpService_enable'].pop(0)

    def sxpDevices_addDevice(self):
        from tests.configurations.ise.ui.workcenters.trustsec.sxp import sxp_devices
        sxpDevicesPage = sxp_devices.SxpDevices(self.app, self.logger)

        deviceName = self.args['sxpDevices_addDevice'][0]
        deviceIP = self.args['sxpDevices_addDevice'][1]
        devicePsn = self.args['sxpDevices_addDevice'][2]
        roleName = self.args['sxpDevices_addDevice'][3]
        sxpDevicesPage.navigate_to_page()
        sxpDevicesPage.add_sxp_device(name_text=deviceName, ip_address=deviceIP, psn=devicePsn, peer_role=roleName)

        for i in range(0, 4):
            self.args['sxpDevices_addDevice'].pop(0)

    def sxpSettings_setGlobalPwd(self):
        from tests.configurations.ise.ui.workcenters.trustsec.settings import sxp_settings
        sxpGlobalPage = sxp_settings.SxpSettings(self.app, self.logger)

        globalpwd = self.args['sxpSettings_setGlobalPwd'][0]
        retry_period = self.args['sxpSettings_setGlobalPwd'][1]
        sxpGlobalPage.navigate_to_page()
        sxpGlobalPage.edit_sxp_settings(global_password=globalpwd, retry_period=retry_period)

        self.args['sxpSettings_setGlobalPwd'].pop(0)

    def logging_setRemoteLogging(self):
        from tests.configurations.ise.ui.administration.system.logging import logging as loggingUI

        targetName = self.args['logging_setRemoteLogging'][0]
        syslogIp = self.args['logging_setRemoteLogging'][1]
        syslogPort = self.args['logging_setRemoteLogging'][2]
        syslogCert = self.args['logging_setRemoteLogging'][3]
        loggingPage = loggingUI.Logging(self.app, self.logger)
        loggingPage.navigate_to_page()
        loggingPage.add_remote_logging_target(targetName, syslogIp, syslogPort, syslogCert)
        loggingPage.add_remote_logging_server_to_category(targetName)  # todo config cert

        for i in range(0, 4):
            self.args['logging_setRemoteLogging'].pop(0)

    def logging_deleteRemoteLoggingTarget(self):
        from tests.configurations.ise.ui.administration.system.logging import logging as loggingUI
        targetName = self.args['logging_deleteRemoteLoggingTarget'][0]
        loggingPage = loggingUI.Logging(self.app, self.logger)
        loggingPage.navigate_to_page()
        loggingPage.delete_remote_logging_target(targetName)

        self.args['logging_deleteRemoteLoggingTarget'].pop(0)

    @staticmethod
    def pez_runPez():
        from utilities.simulators.pez import pez_utils
        from tests.suites.network_access.common.common_utils import isAccepted

        runPez_Result, stdOut = pez_utils.runPezCommand(device=cfg.te.get_PEZ().get_ip(),
                                                        username=cfg.te.get_PEZ().get_login(),
                                                        password=cfg.te.get_PEZ().get_password(),
                                                        pez_config_file_path="/tmp/pez.py",
                                                        port=int(cfg.te.get_PEZ().get_ssh_port()),
                                                        useSSL=True)
        if not runPez_Result:
            raise Exception("Error in applying PEZ command on the given Device")

        Authentication_result = isAccepted(stdOut)
        return Authentication_result, stdOut \
 \
               @ staticmethod

    def pez_runPezDTLS():
        from utilities.simulators.pez import pez_utils
        from tests.suites.network_access.common.common_utils import isAccepted

        runPez_Result, stdOut = pez_utils.runPezCommand(device=cfg.te.get_PEZ().get_ip(),
                                                        username=cfg.te.get_PEZ().get_login(),
                                                        password=cfg.te.get_PEZ().get_password(),
                                                        pez_config_file_path="/tmp/pez.py",
                                                        port=int(cfg.te.get_PEZ().get_ssh_port()),
                                                        useSSL=True,
                                                        pezType="dtls")
        if not runPez_Result:
            raise Exception("Error in applying PEZ command on the given Device")

        Authentication_result = isAccepted(stdOut)
        return Authentication_result, stdOut

    @staticmethod
    def pez_changePezConfig_sendPezMachine(changes, pez_template):
        from utilities.simulators.pez import pez_utils
        from tests.suites.network_access.common.common_utils import automationDir

        # Opens pez template config file and places arguments from changes dictionary to $$ markers in template file -> output is pez_config_dict
        s_log.info("running change multipe changes Once")
        pez_config_file = automationDir() + pez_template
        pez_configuration_dict = pez_utils.changeMultipleVariablesInPizConfig("file", pez_config_file, changes, True)

        s_log.info("dump the configuration file to remote or local device")
        pezConfigFile_RemotePath = "/tmp/pez.py"
        pez_utils.dumpConfigurationFile(device=cfg.te.get_PEZ().get_ip(),
                                        pez_configuration_dict=pez_configuration_dict,
                                        username_remote=cfg.te.get_PEZ().get_login(),
                                        password=cfg.te.get_PEZ().get_password(),
                                        local_path="/tmp/pez.py",
                                        remote_path=pezConfigFile_RemotePath,
                                        port=int(cfg.te.get_PEZ().get_ssh_port()))

    def configure_radius_tokens(self):
        from tests.configurations.ise.ui.administration.identity_management.radius_token import RadiusToken
        radtoken = RadiusToken(self.app, self.logger)

        name = self.args['configure_radius_tokens'][0]
        IP = self.args['configure_radius_tokens'][1]
        shared_secret = self.args['configure_radius_tokens'][2]
        time.sleep(5)
        radtoken.navigate_to_page()

        time.sleep(5)

        connection_msg, connection_alert = radtoken.config_radius_token(name=name, IP=IP, shared_secret=shared_secret)

        # Verify the Radius Token is added
        if connection_msg is None:
            assert False, "********* Radius Token is not added successfully - ****".format(
                connection_alert)
        else:
            s_log.info("********* Radius Token is added successfully ****")
            s_log.info("********* Server response : {}".format(connection_msg))
        time.sleep(10)

        for i in range(0, 3):
            self.args['configure_radius_tokens'].pop(0)

    def delete_radius_tokens(self):
        from tests.configurations.ise.ui.administration.identity_management.radius_token import RadiusToken
        radtoken = RadiusToken(self.app, self.logger)

        name = self.args['delete_radius_tokens'][0]
        time.sleep(5)
        radtoken.navigate_to_page()
        time.sleep(5)
        try:
            radtoken.delete_radius_token(name=name)
        except Exception as e:
            s_log.info("<-- Radius Token is not found-->")
        for i in range(0, 1):
            self.args['delete_radius_tokens'].pop(0)

    def edit_identity_source_sequences(self):
        from tests.configurations.ise.ui.administration.identity_management.identity_source_sequences import \
            IdentitySourceSequences
        identity = IdentitySourceSequences(self.app, self.logger)

        identity_source = self.args['edit_identity_source_sequences'][0]
        sequence = self.args['edit_identity_source_sequences'][1]
        time.sleep(5)
        connection_msg, connection_alert = identity.add_identity_source_to_sequence_authstores(
            identity_source=identity_source,
            sequence=sequence)

        # Verify the Identity Source Sequeuce is edited
        if connection_msg is None:
            assert False, "********* Identity Source Sequence is not edited successfully - ****".format(
                connection_alert)
        else:
            s_log.info("********* Identity Source Sequence is added successfully ****")
            s_log.info("********* Server response : {}".format(connection_msg))
        time.sleep(10)

        for i in range(0, 2):
            self.args['edit_identity_source_sequences'].pop(0)

    def create_active_directory(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        activedirectory = ActiveDirectory(self.app, self.logger)

        ad_name = self.args['create_active_directory'][0]
        domain_name = self.args['create_active_directory'][1]
        ad_admin_user_name = self.args['create_active_directory'][2]
        ad_admin_pass = self.args['create_active_directory'][3]
        time.sleep(5)
        activedirectory.navigate_to_page()
        time.sleep(5)
        activedirectory.create_AD_instance(adname=ad_name, domainName=domain_name, username=ad_admin_user_name,
                                           password=ad_admin_pass, post_validatename="", pre_validatename="")

        for i in range(0, 4):
            self.args['create_active_directory'].pop(0)

    def import_AD_groups(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        activedirectory = ActiveDirectory(self.app, self.logger)
        scope_ad = self.args['import_AD_groups'][0]
        group_name = self.args['import_AD_groups'][1]
        activedirectory.navigate_to_page()
        time.sleep(10)
        activedirectory.select_Ad_group(scope_ad=scope_ad, group_name=group_name)
        time.sleep(2)

        for i in range(0, 2):
            self.args['import_AD_groups'].pop(0)

    def change_admin_password_authentication(self):
        from tests.configurations.ise.ui.administration.system.admin_access.authentication.authentication import \
            Authentication
        authentication = Authentication(app=self.app, logger=s_log)
        option = self.args['change_admin_password_authentication'][0]
        authentication.navigate_to_page()
        # authentication.password_based.click()
        # time.sleep(5)
        # authentication.popup_ok_button.click()
        # time.sleep(2)
        authentication.change_identity_source(option=option)
        time.sleep(2)

        for i in range(0, 1):
            self.args['change_admin_password_authentication'].pop(0)

    def add_admin_with_external_group(self):
        from tests.configurations.ise.ui.administration.system.admin_access.administrators.admin_groups import \
            AdminGroups
        admingroups = AdminGroups(app=self.app, logger=s_log)
        admin_group_name = self.args['add_admin_with_external_group'][0]
        group_description = self.args['add_admin_with_external_group'][1]
        select_group = self.args['add_admin_with_external_group'][2]
        admingroups.navigate_to_page()
        try:
            admingroups.create_admin_group_with_external_group_mapped(group_name=admin_group_name,
                                                                      group_description=group_description,
                                                                      external_group_name=select_group)
            assert True
            s_log.info("Able to retrive group from AD")
        except:
            s_log.info("Not able to retrive group from AD")
            assert False
        for i in range(0, 3):
            self.args['add_admin_with_external_group'].pop(0)

    def create_ldap(self):
        from tests.configurations.ise.ui.administration.identity_management.ldap import Ldap
        ldap = Ldap(app=self.app, logger=s_log)
        ldap_name = self.args['create_ldap'][0]
        description = self.args['create_ldap'][1]
        schema = self.args['create_ldap'][2]
        hostname_ip = self.args['create_ldap'][3]
        primary_server_port = self.args['create_ldap'][4]
        admin_dn = self.args['create_ldap'][5]
        admin_password = self.args['create_ldap'][6]
        subject_search_base_input = self.args['create_ldap'][7]
        group_search_base_input = self.args['create_ldap'][8]
        select_group = self.args['create_ldap'][9]
        time.sleep(5)
        ldap.navigate_to_page()
        time.sleep(5)
        if ldap.delete_ldap_if_exists(ldap_name=ldap_name):
            assert False, "Failed to delete Ldap, ldap may be referred to some policy... "
        ldap.add_ldap_with_primary_server(name=ldap_name,
                                          description=description,
                                          schema=schema,
                                          primary_server_host_or_ip=hostname_ip,
                                          primary_server_port=primary_server_port,
                                          primary_admin_dn=admin_dn,
                                          primary_admin_password=admin_password,
                                          subject_search_base=subject_search_base_input,
                                          group_search_base=group_search_base_input,
                                          ldap_group=select_group)

        for i in range(0, 10):
            self.args['create_ldap'].pop(0)

    def add_authorization_policy_in_admin_access(self):
        from tests.configurations.ise.ui.administration.system.admin_access.authorization.policy import Policy
        policy = Policy(app=self.app, logger=s_log)
        policy_name = self.args['add_authorization_policy_in_admin_access'][0]
        admin_group_name = self.args['add_authorization_policy_in_admin_access'][1]
        menu_access = self.args['add_authorization_policy_in_admin_access'][2]
        data_access = self.args['add_authorization_policy_in_admin_access'][3]
        policy.navigate_to_page()
        time.sleep(5)
        policy.create_new_policy(policy_name=policy_name, group_name=admin_group_name, menu_access=menu_access,
                                 data_access=data_access)

        for i in range(0, 4):
            self.args['add_authorization_policy_in_admin_access'].pop(0)

    def logout(self):
        from tests.configurations.ise.ui.login_page import Login
        self.cloud = cfg.env.get('cloud')
        print("CLOUD INSIDE logout {}".format(self.cloud))
        if self.cloud == True:
            login = Login(app=self.app, logger=s_log, url=self.iseUrl)
        else:
            login = Login(app=self.app, logger=s_log)
        login.logout_using_button()

    def login(self):
        from tests.configurations.ise.ui.login_page import Login
        login = Login(app=self.app, logger=s_log)
        username = self.args['login'][0]
        password = self.args['login'][1]
        time_out = self.args['login'][2]
        s_log.info("LOGIN to verify ldap login")
        try:
            login.login(username_text=username, password_text=password, timeout=time_out)
            s_log.info("Logged in Successfully")
            assert True
        except:
            s_log.info("Not able to login into ise with these credentials")
            assert False
        for i in range(0, 3):
            self.args['login'].pop(0)

    def verify_ldap_added_sucessfully_or_not(self):
        from tests.configurations.ise.ui.administration.identity_management.ldap import Ldap
        ldap = Ldap(app=self.app, logger=s_log)
        ldap_name = self.args['verify_ldap_added_sucessfully_or_not'][0]
        time.sleep(5)
        ldap.navigate_to_page()
        time.sleep(5)
        if ldap.select_ldap(ldap_name).is_displayed():
            assert True
            s_log.info("ldap added succuessfully")
        else:
            s_log.info("failed to add ldap")
            assert False

        for i in range(0, 1):
            self.args['verify_ldap_added_sucessfully_or_not'].pop(0)

    def verify_ldap_group_added_sucessfully_or_not(self):
        from tests.configurations.ise.ui.administration.identity_management.ldap import Ldap
        ldap_name = self.args['verify_ldap_group_added_sucessfully_or_not'][0]
        select_group = self.args['verify_ldap_group_added_sucessfully_or_not'][1]
        ldap = Ldap(app=self.app, logger=s_log)
        ldap.select_ldap(ldap_name).click()
        ldap.groups_tab.click()
        if ldap.added_group_by_name(groupname=select_group).is_displayed():
            assert True
            s_log.info("group added successfully")
        else:
            s_log.info("group not added")
            assert False

        for i in range(0, 2):
            self.args['verify_ldap_group_added_sucessfully_or_not'].pop(0)

    def verify_ad_added_sucessfully_or_not(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        activedirectory = ActiveDirectory(app=self.app, logger=s_log)
        ad_name = self.args['verify_ad_added_sucessfully_or_not'][0]

        activedirectory.navigate_to_page()
        if activedirectory.selecting_AD(ad_name).is_displayed():
            assert True
            s_log.info("AD added succuessfully")
        else:
            s_log.info("failed to add AD")
            assert False

        for i in range(0, 1):
            self.args['verify_ad_added_sucessfully_or_not'].pop(0)

    def verify_ad_group_added_sucessfully_or_not(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        ad_name = self.args['verify_ad_group_added_sucessfully_or_not'][0]
        select_group = self.args['verify_ad_group_added_sucessfully_or_not'][1]
        activedirectory = ActiveDirectory(app=self.app, logger=s_log)
        activedirectory.selecting_AD(ad_name).click()
        time.sleep(7)
        activedirectory.groups_tab.click()
        time.sleep(5)
        if activedirectory.added_group_by_name(group_name=select_group).is_displayed():
            assert True
            s_log.info("group added successfully")
        else:
            s_log.info("group not added")
            assert False

        for i in range(0, 2):
            self.args['verify_ad_group_added_sucessfully_or_not'].pop(0)

    def config_certificate_authprofile(self):
        from tests.configurations.ise.ui.administration.identity_management.certificate_authentication_profile import \
            CertificateAuthenticationProfile
        certificate_authentication = CertificateAuthenticationProfile(self.app, self.logger)
        certificate_authentication.navigate_to_page()
        time.sleep(5)
        certificate_name = self.args['config_certificate_authprofile'][0]
        name = self.args['config_certificate_authprofile'][1]
        description = self.args['config_certificate_authprofile'][2]
        certificate_attribute = self.args['config_certificate_authprofile'][3]
        ad_name = self.args['config_certificate_authprofile'][4]
        enable_name = self.args['config_certificate_authprofile'][5]
        certificate_authentication.cert_auth_profile_edit(cert_auth_profile_name=certificate_name, name_text=name,
                                                          description_text=description,
                                                          certificate_attribute=certificate_attribute,
                                                          identity_store_option=ad_name, enable_name=enable_name)
        time.sleep(10)
        for i in range(0, 6):
            self.args['config_certificate_authprofile'].pop(0)

    def basic_chap_authenticaton(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allow_protocol_chap = AllowedProtocols(app=self.app, logger=None)
        allow_protocol_chap.navigate_to_page()
        allow_protocol_chap.check_basic_chap_protocol()

    def EAP_TLS_session_resume_enable(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowedprotocols = AllowedProtocols(self.app, self.logger)
        allowedprotocols.navigate_to_page()
        allowedprotocols.enable_EAP_TLS_session_resume()
        time.sleep(2)

    def EAP_TLS_session_resume_disable(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowedprotocols = AllowedProtocols(self.app, self.logger)
        allowedprotocols.navigate_to_page()
        allowedprotocols.uncheck_EAP_TLS_session_resume()
        time.sleep(2)

    def identities_add_simple_user(self):
        from tests.configurations.ise.ui.administration.identity_management import identities
        identitiesPage = identities.Identities(self.app, self.logger)

        testUser = self.args['identities_add_simple_user'][0]
        testEmail = self.args['identities_add_simple_user'][1]
        testPassword = self.args['identities_add_simple_user'][2]
        identitiesPage.navigate_to_page()
        time.sleep(5)
        if identitiesPage.user_checkbox(testUser).is_displayed():
            identitiesPage.delete_user(name1=testUser)
        identitiesPage.add_simple_user(name=testUser, email=testEmail, password=testPassword)
        time.sleep(1)

        for i in range(0, 3):
            self.args['identities_add_simple_user'].pop(0)

    def trusted_certificate_download_crl(self):
        from tests.configurations.ise.ui.administration.system.certificates import trusted_certificates
        trustedCertificates = trusted_certificates.TrustedCertificates(self.app, self.logger)

        cert_name = self.args['trusted_certificate_download_crl'][0]
        crl_url = self.args['trusted_certificate_download_crl'][1]
        time_format = self.args['trusted_certificate_download_crl'][2]
        value = self.args['trusted_certificate_download_crl'][3]

        trustedCertificates.navigate_to_page()
        trustedCertificates.enter_download_crl_config(cert_name=cert_name, crl_url=crl_url, time_format=time_format,
                                                      value=value)

        for i in range(0, 4):
            self.args['trusted_certificate_download_crl'].pop(0)

    def trusted_certificate_hour_download_crl(self):
        from tests.configurations.ise.ui.administration.system.certificates import trusted_certificates
        trustedCertificates = trusted_certificates.TrustedCertificates(self.app, self.logger)

        cert_name = self.args['trusted_certificate_hour_download_crl'][0]
        crl_url = self.args['trusted_certificate_hour_download_crl'][1]
        time_format = self.args['trusted_certificate_hour_download_crl'][2]
        value = self.args['trusted_certificate_hour_download_crl'][3]

        trustedCertificates.navigate_to_page()
        trustedCertificates.enter_download_crl_hour_config(cert_name=cert_name, crl_url=crl_url,
                                                           time_format=time_format, value=value)

        for i in range(0, 4):
            self.args['trusted_certificate_hour_download_crl'].pop(0)

    def trusted_certificate_crl_config(self):
        from tests.configurations.ise.ui.administration.system.certificates import trusted_certificates
        trusted_certificate = trusted_certificates.TrustedCertificates(self.app, self.logger)

        cert_name = self.args['trusted_certificate_crl_config'][0]
        time1 = self.args['trusted_certificate_crl_config'][1]
        time2 = self.args['trusted_certificate_crl_config'][2]

        trusted_certificate.navigate_to_page()
        trusted_certificate.add_retrive_checkbox(cert_name=cert_name, time1=time1, time2=time2)

        for i in range(0, 3):
            self.args['trusted_certificate_crl_config'].pop(0)

    def change_authentication_as_internal(self):
        from tests.configurations.ise.ui.administration.system.admin_access.authentication.authentication import \
            Authentication
        change_authentication = Authentication(self.app, self.logger)

        option = self.args['change_authentication_as_internal'][0]

        change_authentication.navigate_to_page()
        change_authentication.change_identity_source(option=option)

        for i in range(0, 1):
            self.args['change_authentication_as_internal'].pop(0)

    def deleting_ad(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        active_directory = ActiveDirectory(app=self.app, logger=self.logger)
        ad_name = self.args['deleting_ad'][0]
        active_directory.navigate_to_page()
        time.sleep(10)
        active_directory.delete_active_directory(ad_name=ad_name)
        for i in range(0, 1):
            self.args['deleting_ad'].pop(0)

    def exiting_scope_and_deleting_ad(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        active_directory = ActiveDirectory(app=self.app, logger=self.logger)
        ad_name = self.args['exiting_scope_and_deleting_ad'][0]
        active_directory.navigate_to_page()
        active_directory.exit_scope_mode_ad(ad_name=ad_name)
        for i in range(0, 1):
            self.args['exiting_scope_and_deleting_ad'].pop(0)

    def deleting_ldap(self):
        from tests.configurations.ise.ui.administration.identity_management.ldap import Ldap
        ldap = Ldap(app=self.app, logger=self.logger)
        ldap_name = self.args['deleting_ldap'][0]
        ldap.navigate_to_page()
        ldap.delete_ldap(name=ldap_name)
        for i in range(0, 1):
            self.args['deleting_ldap'].pop(0)

    def deleting_RBAC_policy(self):
        from tests.configurations.ise.ui.administration.system.admin_access.authorization.policy import Policy
        policy = Policy(app=self.app, logger=self.logger)
        policy_name = self.args['deleting_RBAC_policy'][0]
        policy.navigate_to_page()
        policy.delete_policy_by_policy_name(policy_name=policy_name)
        for i in range(0, 1):
            self.args['deleting_RBAC_policy'].pop(0)

    def login_with_identity_source(self):
        from tests.configurations.ise.ui.login_page import Login
        login = Login(app=self.app, logger=self.logger)
        username = self.args['login_with_identity_source'][0]
        password = self.args['login_with_identity_source'][1]
        identity_source = self.args['login_with_identity_source'][2]
        login.login_with_identity_source(username_text=username,
                                         password_text=password,
                                         identity_source=identity_source)
        for i in range(0, 3):
            self.args['login_with_identity_source'].pop(0)

    def deleting_admin_group_by_name(self):
        from tests.configurations.ise.ui.administration.system.admin_access.administrators.admin_groups import \
            AdminGroups
        admin_group = AdminGroups(app=self.app, logger=self.logger)
        group_name = self.args['deleting_admin_group_by_name'][0]
        admin_group.navigate_to_page()
        admin_group.delete_admin_group(group_name=group_name)
        for i in range(0, 1):
            self.args['deleting_admin_group_by_name'].pop(0)

    def identities_add_user_change_password(self):
        from tests.configurations.ise.ui.administration.identity_management import identities
        identitiesPage = identities.Identities(self.app, self.logger)

        testUser = self.args['identities_add_user_change_password'][0]
        testEmail = self.args['identities_add_user_change_password'][1]
        testPassword = self.args['identities_add_user_change_password'][2]
        user_group = self.args['identities_add_user_change_password'][3]
        enable_password_change = self.args['identities_add_user_change_password'][4]
        identitiesPage.navigate_to_page()
        identitiesPage.add_user_to(name=testUser, email=testEmail, password=testPassword, usrgrp=user_group,
                                   passwdchange=enable_password_change)
        time.sleep(1)

        for i in range(0, 5):
            self.args['identities_add_user_change_password'].pop(0)

    def delete_user_identity(self):
        from tests.configurations.ise.ui.administration.identity_management.identities import Identities
        users = Identities(app=self.app, logger=self.logger)
        user_name = self.args['delete_user_identity'][0]
        users.navigate_to_page()
        time.sleep(10)
        users.delete_user(name1=user_name)
        time.sleep(5)

        for i in range(0, 1):
            self.args['delete_user_identity'].pop(0)

    def disable_Eap_Tls_In_New_Allowed_Protocol(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowedprotocols = AllowedProtocols(self.app, self.logger)
        name = self.args['disable_Eap_Tls_In_New_Allowed_Protocol'][0]
        description = self.args['disable_Eap_Tls_In_New_Allowed_Protocol'][1]
        allowedprotocols.navigate_to_page()
        allowedprotocols.Add_New_Allowed_Protocol_EAP_TLS_disabled(name=name, description=description)
        time.sleep(5)

        for i in range(0, 2):
            self.args['disable_Eap_Tls_In_New_Allowed_Protocol'].pop(0)

    def delete_New_Allowed_Protocol(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowedprotocols = AllowedProtocols(self.app, self.logger)
        protocolname = self.args['delete_New_Allowed_Protocol'][0]
        allowedprotocols.navigate_to_page()
        allowedprotocols.delete_allowed_prtocol(protocolname=protocolname)
        time.sleep(5)

        for i in range(0, 1):
            self.args['delete_New_Allowed_Protocol'].pop(0)

    def pez_start(self):
        # pez_utils.start_pez_docker_image(docker_image="dockerhub.cisco.com/isepy-release-docker/pez-executer",
        #                          docker_image_version="v4")

        value = pez_utils.get_pez_docker_ipv4()
        print("PEZ VALUE: {}".format(value))
        host = "10.0.0.18"
        username = "root"
        password = "Lab@123"
        ssh_to_td = SSH(hostname=host,
                        username=username,
                        password=password,
                        port=22, timeout=5, logger=logging)
        pez_utils.validate_docker_image_state(docker_image="dockerhub.cisco.com/isepy-release-docker/pez-executer",
                                              docker_image_version="v4",
                                              host_connection=ssh_to_td,
                                              check_state="Exited"
                                              )

    ###### CODE ADDED TO RUN PEZ ########
    def copy_files_device(self, root_path,
                          client_trusted_cert,
                          ise_sys_cert,
                          ise_sys_key,
                          ise_trust_cert
                          ):
        s_log.info(" =====  Copy_certificates Start ===== ")
        s_log.info("Copying Client Trusted Certificate")
        # certName = 'rootCA_OCSP_Users.cer'
        certDir = root_path + "resources/CommonCriteria/{}".format(client_trusted_cert)
        if not protocols_utils.copy_certificate_into_device(logger=s_log,
                                                            local_path=certDir,
                                                            remote_path="/home/root/certs/{}".format(
                                                                client_trusted_cert),
                                                            # equivalent win dir is C:\\Users\\root\\certs\\....
                                                            node_ip=cfg.te.get_WIN_CLIENT().get_ip(),
                                                            user=cfg.te.get_WIN_CLIENT().get_login(),
                                                            password=cfg.te.get_WIN_CLIENT().get_password()):
            raise Exception("Error on copy file")

        # certName = 'PorcoRossoServer.cer'
        certDir = root_path + "resources/CommonCriteria/{}".format(ise_sys_cert)
        if not protocols_utils.copy_certificate_into_device(logger=s_log,
                                                            local_path=certDir,
                                                            remote_path="/home/root/certs/{}".format(
                                                                ise_sys_cert),
                                                            # equivalent win dir is C:\\Users\\root\\certs\\....
                                                            node_ip=cfg.te.get_WIN_CLIENT().get_ip(),
                                                            user=cfg.te.get_WIN_CLIENT().get_login(),
                                                            password=cfg.te.get_WIN_CLIENT().get_password()):
            raise Exception("Error on copy file")

        # certName = 'PorcoRossoServer.pvk'
        certDir = root_path + "resources/CommonCriteria/{}".format(ise_sys_key)
        if not protocols_utils.copy_certificate_into_device(logger=s_log,
                                                            local_path=certDir,
                                                            remote_path="/home/root/certs/{}".format(
                                                                ise_sys_key),
                                                            # equivalent win dir is C:\\Users\\root\\certs\\....
                                                            node_ip=cfg.te.get_WIN_CLIENT().get_ip(),
                                                            user=cfg.te.get_WIN_CLIENT().get_login(),
                                                            password=cfg.te.get_WIN_CLIENT().get_password()):
            raise Exception("Error on copy file")

        # certName = 'PorcoRossoServerCA.cer'
        certDir = root_path + "resources/CommonCriteria/{}".format(ise_trust_cert)
        if not protocols_utils.copy_certificate_into_device(logger=s_log,
                                                            local_path=certDir,
                                                            remote_path="/home/root/certs/{}".format(
                                                                ise_trust_cert),
                                                            # equivalent win dir is C:\\Users\\root\\certs\\....
                                                            node_ip=cfg.te.get_WIN_CLIENT().get_ip(),
                                                            user=cfg.te.get_WIN_CLIENT().get_login(),
                                                            password=cfg.te.get_WIN_CLIENT().get_password()):
            raise Exception("Error on copy file")

        # copy certs to client
        # certName = 'PorcoRossoServerCA.cer'
        certDir = root_path + "resources/CommonCriteria/{}".format(ise_trust_cert)
        mgmt_utils.sendFileUsingSsh(cfg.te.get_PEZ().get_ip(),
                                    cfg.te.get_PEZ().get_login(),
                                    cfg.te.get_PEZ().get_password(),
                                    certDir,
                                    "/tmp/{}".format(ise_trust_cert),
                                    int(cfg.te.get_PEZ().get_ssh_port()))

    def disable_mschap_v2_authentication_protocol(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowed_protocols = AllowedProtocols(app=self.app, logger=self.logger)
        allowed_protocols.navigate_to_page()
        time.sleep(5)
        allowed_protocols.default_network_access.click()
        time.sleep(2)
        allowed_protocols.mschap_v2.deselect()
        time.sleep(2)
        allowed_protocols.submit_button.scroll_to_element()
        allowed_protocols.submit_button.click()
        time.sleep(5)

    def disable_mschap_v1_authentication_protocol(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowed_protocols = AllowedProtocols(app=self.app, logger=self.logger)
        allowed_protocols.navigate_to_page()
        time.sleep(5)
        allowed_protocols.default_network_access.click()
        time.sleep(2)
        allowed_protocols.mschap_v1.deselect()
        time.sleep(2)
        allowed_protocols.submit_button.scroll_to_element()
        allowed_protocols.submit_button.click()
        time.sleep(5)

    def mschap_v2_allowed_protocol_authentication(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowed_protocol = AllowedProtocols(app=self.app, logger=s_log)
        allowed_protocol.navigate_to_page()
        allowed_protocol.default_network_access.click()
        time.sleep(5)
        allowed_protocol.mschap_v2.select()
        time.sleep(5)
        allowed_protocol.save.scroll_to_element()
        allowed_protocol.save.click()
        s_log.info("Saved the changes")
        time.sleep(5)

    def tacacs_live_logs(self):
        from tests.configurations.ise.ui.operations.tacacs.live_logs import Livelogs
        live_logs = Livelogs(app=self.app, logger=self.logger)
        username = self.args['tacacs_live_logs'][0]
        live_logs.navigate_to_page()
        live_logs.tacacs_live_logs_quick_filter(username=username)
        time.sleep(5)
        for i in range(0, 1):
            self.args['tacacs_live_logs'].pop(0)

    def radius_live_logs(self):
        from tests.configurations.ise.ui.operations.radius.live_logs import Livelogs
        live_logs = Livelogs(app=self.app, logger=self.logger)
        username = self.args['radius_live_logs'][0]
        domain_name = self.args['radius_live_logs'][1]
        live_logs.navigate_to_page()
        time.sleep(10)
        live_logs.radius_live_logs_quick_filter(username=username, domain_name=domain_name)
        for i in range(0, 2):
            self.args['radius_live_logs'].pop(0)

    def radius_live_logs_section_result(self):
        from tests.configurations.ise.ui.operations.radius.live_logs import Livelogs
        live_logs = Livelogs(app=self.app, logger=self.logger)
        username = self.args['radius_live_logs_section_result'][0]
        section_name = self.args['radius_live_logs_section_result'][1]
        key_value_attributes_list = self.args['radius_live_logs_section_result'][2]
        live_logs.navigate_to_page()
        time.sleep(15)
        self.logger.info("---> {},{},{}".format(username, section_name, key_value_attributes_list))
        print("DEBUG:##############")
        # print(dir(live_logs))
        live_logs.radius_live_logs_quick_filter_section_data(username=username, section_name=section_name,
                                                             key_value_attributes_list=key_value_attributes_list)
        for i in range(0, 3):
            self.args['radius_live_logs_section_result'].pop(0)

    def negative_radius_live_logs(self):
        from tests.configurations.ise.ui.operations.radius.live_logs import Livelogs
        live_logs = Livelogs(app=self.app, logger=self.logger)
        username = self.args['negative_radius_live_logs'][0]
        domain_name = self.args['negative_radius_live_logs'][1]
        negative_test = self.args['negative_radius_live_logs'][2]
        live_logs.navigate_to_page()
        live_logs.radius_live_logs_quick_filter(username=username, domain_name=domain_name, negative_test=negative_test)
        for i in range(0, 2):
            self.args['negative_radius_live_logs'].pop(0)

    def check_mschapv2_protocol(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        ms_chapv2_enable = AllowedProtocols(self.app, self.logger)
        ms_chapv2_enable.navigate_to_page()
        ms_chapv2_enable.check_basic_mschapv2_protocol()
        time.sleep(5)

    def disable_mschap_v2_authentication_protocol(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowed_protocols = AllowedProtocols(app=self.app, logger=self.logger)
        allowed_protocols.navigate_to_page()
        time.sleep(5)
        allowed_protocols.default_network_access.click()
        time.sleep(2)
        allowed_protocols.mschap_v2.deselect()
        time.sleep(5)
        allowed_protocols.submit_button.scroll_to_element()
        allowed_protocols.submit_button.click()
        time.sleep(10)

    def delete_user_identity(self):
        from tests.configurations.ise.ui.administration.identity_management.identities import Identities
        users = Identities(app=self.app, logger=self.logger)
        user_name = self.args['delete_user_identity'][0]
        users.navigate_to_page()
        users.delete_user(name1=user_name)
        for i in range(0, 1):
            self.args['delete_user_identity'].pop(0)

    def verify_crl_config(self):
        from tests.configurations.ise.ui.administration.system.certificates.trusted_certificates import \
            TrustedCertificates
        verify_config = TrustedCertificates(self.app, logger=s_log)
        cert_name = self.args['verify_crl_config'][0]
        url = self.args['verify_crl_config'][1]
        value = self.args['verify_crl_config'][2]
        time_format = self.args['verify_crl_config'][3]
        verify_config.navigate_to_page()
        time.sleep(5)
        verify_config.one_trusted_certificate_checkbox(cert_name).select()
        verify_config.edit_button.click()
        if verify_config.download_crl_checkbox_click.is_enabled():
            s_log.info('download crl is enabled')
        else:
            s_log.logger('download crl is not enabled')
            assert False
        # verifying url is entered or not
        if url == verify_config.CRL_Distribution_URL.get_attribute_value('value'):
            assert True
            s_log.info("url added succuessfully")
        else:
            s_log.error("failed to add url")
            assert False
        # verifying crl valu time is correct or not
        if value == verify_config.retrieve_crl_5min.get_attribute_value('value'):
            assert True
            s_log.info("crl value time is correctly entered")
        else:
            s_log.info("crl value time is not correct")
            assert False
        # verifying crl valu time format is correct or not
        if time_format == verify_config.retrieve_crl_value.get_attribute_value('value'):
            assert True
            s_log.info("crl time format is in minutes")
        else:
            s_log.info("crl time format is not in minutes")
            assert False
        # verify crl_authentication checkbox ix enabled or not
        if verify_config.validating_crl_before_receiving.is_enabled():
            assert True
            s_log.info("authenticating clr is enabled")
        else:
            s_log.info("authenticating clr is disabled")
            assert False

        for i in range(0, 4):
            self.args['verify_crl_config'].pop(0)
        time.sleep(2)

    def verify_crl_changed_config(self):
        from tests.configurations.ise.ui.administration.system.certificates.trusted_certificates import \
            TrustedCertificates
        verify_new_config = TrustedCertificates(self.app, logger=s_log)
        cert_name = self.args['verify_crl_changed_config'][0]
        url_1 = self.args['verify_crl_changed_config'][1]
        value_2 = self.args['verify_crl_changed_config'][2]
        time_format_3 = self.args['verify_crl_changed_config'][3]

        verify_new_config.navigate_to_page()
        time.sleep(5)
        verify_new_config.one_trusted_certificate_checkbox(cert_name).select()
        verify_new_config.edit_button.click()
        if verify_new_config.download_crl_checkbox_click.is_enabled():
            s_log.info('download crl is enabled')
        else:
            s_log.logger('download crl is not enabled')
            assert False

        url_value = verify_new_config.CRL_Distribution_URL.get_attribute_value('value')
        if url_1 == url_value:
            assert True
            s_log.info("url added succuessfully")
        else:
            s_log.info("failed to add url")
            assert False

        value_v = verify_new_config.retrive_crl_onehour.get_attribute_value('value')
        if value_2 == value_v:
            assert True
            s_log.info("crl value time is correctly entered")
        else:
            s_log.info("crl value time is not correct")
            assert False

        time_format_v = verify_new_config.retrieve_crl_dropdown.get_attribute_value('value')
        if time_format_3 == time_format_v:
            assert True
            s_log.info("crl time format is in minutes")
        else:
            s_log.info("crl time format is not in minutes")
            assert False

        if verify_new_config.ignore_crl_not_received.is_enabled():
            assert True
            s_log.info("authenticating clr is enabled")
        else:
            s_log.info("authenticating clr is disabled")
            assert False

        for i in range(0, 4):
            self.args['verify_crl_changed_config'].pop(0)

    def verify_Download_crl_disable_or_not(self):
        from tests.configurations.ise.ui.administration.system.certificates.trusted_certificates import \
            TrustedCertificates
        verify_Download_crl = TrustedCertificates(self.app, logger=s_log)
        cert_name = self.args['verify_Download_crl_disable_or_not'][0]
        verify_Download_crl.navigate_to_page()
        verify_Download_crl.verify_download_crl_disabled(cert_name=cert_name)
        time.sleep(2)

        for i in range(0, 1):
            self.args['verify_Download_crl_disable_or_not'].pop(0)

    def disable_download_crl(self):
        from tests.configurations.ise.ui.administration.system.certificates.trusted_certificates import \
            TrustedCertificates
        disable_crl = TrustedCertificates(self.app, logger=s_log)
        cert_name = self.args['disable_download_crl'][0]
        disable_crl.navigate_to_page()
        disable_crl.disable_crl_config(cert_name=cert_name)
        time.sleep(2)

        for i in range(0, 1):
            self.args['disable_download_crl'].pop(0)

    def password_policy_check(self):
        from tests.configurations.ise.ui.administration.identity_management.settings.settings import \
            IdentityManagementSettings
        from tests.configurations.ise.ui.administration.identity_management.user_auth_settings import user_auth_settings
        settings_page = IdentityManagementSettings(app=self.app, logger=s_log)
        settings_page.navigate_to_page()
        authpage = user_auth_settings(app=self.app, logger=s_log)
        suspend_list = ["10", "1460"]
        disable_user_account_list = ["-1", "-4"]
        display_reminder_list = ["-1", "-5"]
        s_log.info("Input Values tested: {},{},{}".format(suspend_list,
                                                          disable_user_account_list, display_reminder_list))
        time.sleep(2)
        # identitiesPage.navigate_to_page()
        # time.sleep(5)
        authpage.identities_password_policy_setting(suspend_list, disable_user_account_list, display_reminder_list)

    def set_user_auth_def(self):
        from tests.configurations.ise.ui.administration.identity_management.settings.settings import \
            IdentityManagementSettings
        from tests.configurations.ise.ui.administration.identity_management.user_auth_settings import user_auth_settings
        settings_page = IdentityManagementSettings(app=self.app, logger=s_log)
        settings_page.navigate_to_page()
        authpage = user_auth_settings(app=self.app, logger=s_log)
        authpage.set_user_authentication_default()

    def authentication_policy(self):
        from tests.configurations.ise.ui.policy.policy_sets.new_policy_sets import RadPolicySets
        new_policy = RadPolicySets(app=self.app, logger=s_log)
        new_policy.navigate_policy.click()
        new_policy.navigate_policy_sets.click()
        new_policy.open_set_view.click()
        new_policy.authentication_policy_expand.wait_for_enable()
        new_policy.authentication_policy_expand.click()
        new_policy.authen_plus.click()
        time.sleep(3)
        new_policy.create_authentication_policy("policy1", auth_policy_name_list=['MAB'],
                                                source_drag_name_list_of_list=[['Wired_MAB', 'Wireless_MAB']],
                                                cond_studio_name_list=["WirelessMAB"], use_val='ISE_AD',
                                                cond_name='Network Access',
                                                attr_val='Protocol', comp_cond_name='NETWORK_PROTOCOL', cond_value=None)
        s_log.info("**** Successfully policy set and auth policy has created... ****")
        time.sleep(3)

    def delete_new_policy_with_AD(self):
        from tests.configurations.ise.ui.policy.policy_sets.new_policy_sets import RadPolicySets
        new_policy = RadPolicySets(app=self.app, logger=self.logger)
        row = self.args['delete_new_policy_with_AD'][0]
        new_policy.navigate_policy.click()
        new_policy.navigate_policy_sets.click()
        new_policy.open_set_view.click()
        new_policy.authentication_policy_expand.wait_for_enable()
        new_policy.authentication_policy_expand.click()
        time.sleep(5)
        new_policy.delete_policy_set(row=row)
        time.sleep(5)

        for i in range(0, 1):
            self.args['delete_new_policy_with_AD'].pop(0)

    def mschap_allowed_protocol_authentication(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        ui_lib = AllowedProtocols(app=self.app, logger=s_log)
        ui_lib.navigate_to_page()
        ui_lib.default_network_access.click()
        time.sleep(5)
        ui_lib.mschapv2.select()
        # time.sleep(5)
        ui_lib.save.wait_for_ui_element(timeout=30)
        # BasePage.wait_for_loader([ui_lib.save.click()])
        ui_lib.save.click()
        s_log.info("Saved the changes")
        time.sleep(5)

    def eap_ttls_mschap_allowed_protocol_authentication(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        ui_lib = AllowedProtocols(app=self.app, logger=s_log)
        ui_lib.navigate_to_page()
        ui_lib.default_network_access.click()
        time.sleep(5)
        check_outer_ttls = ui_lib.eap_ttls.is_enabled()
        check_inner_ttls_mschap = ui_lib.eapttlseapmschap.is_enabled()

        if not check_outer_ttls:
            ui_lib.eap_ttls.select()
        else:
            s_log.info("Outer Champ is enabled")
        time.sleep(5)

        if not check_inner_ttls_mschap:
            ui_lib.eapttlseapmschap.select()
        else:
            s_log.info("Inner chap is enabled")

        time.sleep(5)
        ui_lib.save.click()
        s_log.info("Saved the changes")
        time.sleep(5)

    def configure_ocsp_profile(self):
        from tests.configurations.ise.ui.administration.system.certificates.ocsp_client_profile import OCSPClientProfile
        ocspclientprofile = OCSPClientProfile(self.app, self.logger)

        name = self.args['configure_ocsp_profile'][0]
        description = self.args['configure_ocsp_profile'][1]
        url = self.args['configure_ocsp_profile'][2]
        ttl = self.args['configure_ocsp_profile'][3]
        ocspclientprofile.navigate_to_page()

        try:
            ocspclientprofile.delete_ocsp_client(key=name)
        except:
            s_log.info("ocsp profile given does not exist.")

        try:
            success_msg, alert = ocspclientprofile.add_ocsp_client(name=name, description=description,
                                                                   url=url, ttl=ttl)

            if success_msg is None:
                raise Exception("ocsp server not saved - {}".format(alert))
        except Exception as e:
            assert False, "creation of ocsp server Failed - {0}".format(e)

        for i in range(0, 4):
            self.args['configure_ocsp_profile'].pop(0)

    def certificate_to_check_against_ocsp(self):
        from tests.configurations.ise.ui.administration.system.certificates.trusted_certificates import \
            TrustedCertificates
        trustedCertificatePage = TrustedCertificates(self.app, self.logger)

        key = self.args['certificate_to_check_against_ocsp'][0]
        name = self.args['certificate_to_check_against_ocsp'][1]
        desp = self.args['certificate_to_check_against_ocsp'][2]
        option = self.args['certificate_to_check_against_ocsp'][3]
        unknown = self.args['certificate_to_check_against_ocsp'][4]

        trustedCertificatePage.navigate_to_page()
        time.sleep(5)

        try:
            success_msg, success_alert = trustedCertificatePage.validate_against_ocsp(key=key, name=name,
                                                                                      desp=desp, option=option,
                                                                                      unknown=unknown)

            if success_msg is None:
                raise Exception("certificate changes not saved - {}".format(success_msg))
        except Exception as e:
            assert False, "editing trustedcert Failed - {0}".format(e)

        for i in range(0, 5):
            self.args['certificate_to_check_against_ocsp'].pop(0)

    def delete_ocsp_client_profile(self):
        from tests.configurations.ise.ui.administration.system.certificates.ocsp_client_profile import OCSPClientProfile
        ocspclientprofile = OCSPClientProfile(self.app, self.logger)

        key = self.args['delete_ocsp_client_profile'][0]

        ocspclientprofile.navigate_to_page()
        time.sleep(5)
        if ocspclientprofile.ocsp_profile_checkbox(key=key).is_displayed():
            ocspclientprofile.delete_ocsp_client(key=key)

        for i in range(0, 1):
            self.args['delete_ocsp_client_profile'].pop(0)

    def adding_new_allowed_protocols(self):
        allow_protocol_chap = AllowedProtocols(app=self.app, logger=None)
        allow_protocol_chap.navigate_to_page()
        # allow_protocol_chap.check_basic_chap_protocol()
        allow_protocol_chap.policy_add_button.click()
        allow_protocol_chap.add_new_allowed_protocol("Test", process_host_lookup=True, pap_ascii=True, auth_chap=False,
                                                     mschapv1=False, mschap_v2=False,
                                                     eap_md5=True, eap_tls=True, auth_eaptls_expired_certs=False,
                                                     eap_tls_session_resume=False, allow_leap=False,
                                                     allow_peap=True, peap_eap_ms_chap=True, peap_eapgtc=False,
                                                     peap_eap_tls=True,
                                                     auth_cryptobinding=False,
                                                     allowpeapv0=False)

    def enable_allowed_protocol_eap_fast_inner_method_eaptls_only(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowedprotocols = AllowedProtocols(self.app, self.logger)
        allowedprotocols.navigate_to_page()
        allowedprotocols.eap_fast_tls_client_cert()
        time.sleep(2)

    def disable_allowed_protocol_eap_fast_inner_method_eaptls_only(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowedprotocols = AllowedProtocols(self.app, self.logger)
        allowedprotocols.navigate_to_page()
        allowedprotocols.delete_eap_fast_tls_client_cert()
        time.sleep(2)

    def Disable_Eap_Fast_Inner_functions_Allowed_Protocol(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowedprotocols = AllowedProtocols(self.app, self.logger)
        allowedprotocols.navigate_to_page()
        allowedprotocols.eap_fast_mschap_disable()
        time.sleep(2)

    def Enable_Eap_Fast_Inner_method_mschapv2(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowedprotocols = AllowedProtocols(self.app, self.logger)
        allowedprotocols.navigate_to_page()
        allowedprotocols.Eap_Fast_inner_methods_enable()
        time.sleep(2)

    def enable_require_message_authenticator(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowedprotocols = AllowedProtocols(self.app, self.logger)
        allowedprotocols.navigate_to_page()
        allowedprotocols.enable_require_message_authenticaion()
        time.sleep(2)

    def disable_require_message_authenticator(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowedprotocols = AllowedProtocols(self.app, self.logger)
        allowedprotocols.navigate_to_page()
        allowedprotocols.disable_require_message_authenticaion()
        time.sleep(2)

    def edit_identity_source_in_default_policy(self):
        from tests.configurations.ise.ui.policy.policy_sets.new_policy_sets import RadPolicySets
        edit_policy = RadPolicySets(app=self.app, logger=s_log)
        fname = 'edit_identity_source_in_default_policy'
        use_value = self.args[fname][0]
        if len(self.args[fname]) > 1:
            policy_set = self.args[fname][1]
        else:
            policy_set = 'Default'
        edit_policy.navigate_policy.click()
        time.sleep(15)
        edit_policy.navigate_policy_sets.click()
        time.sleep(15)
        edit_policy.enter_policy_set_view_by_name(name=policy_set)
        time.sleep(15)
        edit_policy.authentication_policy_expand.wait_for_enable()
        edit_policy.authentication_policy_expand.click()
        time.sleep(20)
        edit_policy.Default_auth_policy_identity_use_change(use_val=use_value)
        time.sleep(15)

        for i in range(len(self.args[fname])):
            self.args[fname].pop(0)

    def add_ldap_to_user_identity(self):
        from tests.configurations.ise.ui.administration.identity_management.identity_source_sequences import \
            IdentitySourceSequences

        ldap = IdentitySourceSequences(app=self.app, logger=s_log)
        ldap.navigate_to_page()
        ldap.add_ldap_to_all_user_id_store()

    def deselect_ldap_from_identity_store(self):
        from tests.configurations.ise.ui.administration.identity_management.identity_source_sequences import \
            IdentitySourceSequences
        ldap = IdentitySourceSequences(self.app, self.logger)
        selected_id_source = self.args['deselect_ldap_from_identity_store'][0]
        sequence = self.args['deselect_ldap_from_identity_store'][1]
        ldap.navigate_to_page()
        ldap.select_All_Users_id_store.click()
        ldap.diselect_identity_source_from_sequence_authstores(selected_id_source=selected_id_source, sequence=sequence)

        for i in range(0, 2):
            self.args['deselect_ldap_from_identity_store'].pop(0)
        time.sleep(2)

    def secondary_server_enable_in_ldap(self):
        from tests.configurations.ise.ui.administration.identity_management.ldap import Ldap
        ldap = Ldap(app=self.app, logger=s_log)
        ldap_name = self.args['secondary_server_enable_in_ldap'][0]
        hostname_ip = self.args['secondary_server_enable_in_ldap'][1]
        secondary_server_port = self.args['secondary_server_enable_in_ldap'][2]
        admin_dn = self.args['secondary_server_enable_in_ldap'][3]
        admin_password = self.args['secondary_server_enable_in_ldap'][4]
        ldap.navigate_to_page()
        ldap.enable_secondary_server_in_ldap(ldap_name=ldap_name,
                                             secondary_server_host_or_ip=hostname_ip,
                                             secondary_server_port=secondary_server_port,
                                             secondary_admin_dn=admin_dn,
                                             secondary_admin_password=admin_password)
        time.sleep(2)

        for i in range(0, 5):
            self.args['secondary_server_enable_in_ldap'].pop(0)

    def create_user_with_passwdchange_in_next_login(self):

        from tests.configurations.ise.ui.administration.identity_management import identities
        identitiesPage = identities.Identities(self.app, self.logger)

        name = self.args['create_user_with_passwdchange_in_next_login'][0]
        email = self.args['create_user_with_passwdchange_in_next_login'][1]
        password = self.args['create_user_with_passwdchange_in_next_login'][2]
        passwdchange = self.args['create_user_with_passwdchange_in_next_login'][3]
        identitiesPage.navigate_to_page()
        time.sleep(5)
        if identitiesPage.user_checkbox(name).is_displayed():
            identitiesPage.delete_user(name1=name)
        try:
            success_msg, alert = identitiesPage.create_user_identity(name=name, email=email, password=password,
                                                                     passwdchange=passwdchange)

            if success_msg is None:
                raise Exception("Success Message is not Displayed - {}".format(success_msg))

        except Exception as e:
            assert False, "***** Addin User Failed *****"

        time.sleep(1)

        for i in range(0, 4):
            self.args['create_user_with_passwdchange_in_next_login'].pop(0)

    def enable_peap_gtc_in_allowed_protocol(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowedprotocols = AllowedProtocols(self.app, self.logger)
        allowedprotocols.navigate_to_page()
        allowedprotocols.PEAP_GTC_enable()
        time.sleep(2)

    def add_authentication_policy(self):
        from tests.configurations.ise.ui.policy.policy_sets.new_policy_sets import RadPolicySets
        new_policy = RadPolicySets(app=self.app, logger=s_log)
        policy_name = self.args['add_authentication_policy'][0]
        use_val = self.args['add_authentication_policy'][1]
        cond_name = self.args['add_authentication_policy'][2]
        attr_val = self.args['add_authentication_policy'][3]
        comp_cond_name = self.args['add_authentication_policy'][4]
        cond_value = self.args['add_authentication_policy'][5]

        new_policy.navigate_policy.click()
        time.sleep(5)
        new_policy.navigate_policy_sets.click()
        time.sleep(5)
        new_policy.open_set_view.click()
        time.sleep(5)
        new_policy.authentication_policy_expand.wait_for_enable()
        new_policy.authentication_policy_expand.click()
        time.sleep(5)
        new_policy.authen_plus.click()
        time.sleep(3)
        new_policy.create_authentication_policy(policy_name=policy_name,
                                                auth_policy_name_list="",
                                                source_drag_name_list_of_list=""
                                                , cond_studio_name_list="", use_val=use_val,
                                                cond_name=cond_name, attr_val=attr_val,
                                                comp_cond_name=comp_cond_name,
                                                cond_value=cond_value)
        s_log.info("**** Successfully policy set and auth policy has created... ****")
        time.sleep(3)

        for i in range(0, 6):
            self.args['add_authentication_policy'].pop(0)

    def edit_default_policy_set(self):
        from tests.configurations.ise.ui.policy.policy_sets.new_policy_sets import RadPolicySets
        new_policy = RadPolicySets(app=self.app, logger=s_log)
        fname = 'edit_default_policy_set'
        use_value = self.args[fname][0]
        if len(self.args[fname]) > 1:
            policy_set = self.args[fname][1]
        else:
            policy_set = 'Default'
        new_policy.navigate_policy.click()
        time.sleep(15)
        new_policy.navigate_policy_sets.click()
        time.sleep(15)
        new_policy.enter_policy_set_view_by_name(name=policy_set)
        time.sleep(15)
        new_policy.change_allowed_protocol_in_default_policy_set(use_val=use_value)
        s_log.info("**** Successfully edited default policy set... ****")
        time.sleep(3)

        for i in range(len(self.args[fname])):
            self.args['edit_default_policy_set'].pop(0)

    def eap_fast_configuration_pac_based_authentication(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols as All_Prot

        ui_lib = All_Prot(app=self.app, logger=s_log)
        policy_name = self.args['eap_fast_configuration_pac_based_authentication'][0]
        description = self.args['eap_fast_configuration_pac_based_authentication'][1]
        ui_lib.navigate_to_page()
        ui_lib.Enable_EAP_Fast_in_new_allowed_protocol(policy_name=policy_name, desp=description)
        for i in range(0, 2):
            self.args['eap_fast_configuration_pac_based_authentication'].pop(0)

    def eap_authorization_policy(self):
        from tests.configurations.ise.ui.policy.policy_sets.new_policy_sets import RadPolicySets

        auth_policy = RadPolicySets(app=self.app, logger=s_log)
        rule_name = self.args['eap_authorization_policy'][0]
        rule_line_num = self.args['eap_authorization_policy'][1]
        dict_name = self.args['eap_authorization_policy'][2]
        # attribute = self.args['eap_authorization_policy'][4]
        attribute_value = self.args['eap_authorization_policy'][3]
        true_false = self.args['eap_authorization_policy'][4]
        profiles = self.args['eap_authorization_policy'][5]
        if len(self.args['eap_authorization_policy']) > 6:
            policy_set = self.args['eap_authorization_policy'][6]
        else:
            policy_set = 'Default'
        auth_policy.navigate_policy.click()
        time.sleep(5)
        auth_policy.navigate_policy_sets.click()
        time.sleep(5)
        auth_policy.enter_policy_set_view_by_name(name=policy_set)
        time.sleep(5)
        auth_policy.authorization_policy_expand.wait_for_enable()
        auth_policy.authorization_policy_expand.click()
        time.sleep(5)
        auth_policy.create_new_authorization_policy_rule_3(rule_name=rule_name, rule_line_num=rule_line_num,
                                                           dict_name=dict_name,
                                                           attribute_value=attribute_value,
                                                           true_false=true_false, profiles=profiles)

        for i in range(0, 6):
            self.args['eap_authorization_policy'].pop(0)

    # Tnt5212445c_Tnt5210671c
    def rad_server(self):
        # Adding External radius servers
        s_log.info("<-- Inside rad_server function -->")
        from tests.configurations.ise.ui.administration.network_resources.external_RADIUS_servers import \
            externalRadiusServers
        ui_lib = externalRadiusServers(app=self.app, logger=s_log)
        time.sleep(5)
        ui_lib.navigate_to_page()
        time.sleep(5)
        rad_server = self.args['rad_server'][0]
        rad_server_ip = self.args['rad_server'][1]
        rad_server_secret = self.args['rad_server'][2]
        try:
            success_msg, sucess_alert = ui_lib.add_external_RADIUS_server(name=rad_server, hostIP=rad_server_ip,
                                                                          shared_secret=rad_server_secret)
            if success_msg is None:
                raise Exception("Success Message is not Displayed - {}".format(success_msg))

        except Exception as e:
            s_log.info("Not able to add Radius server : {}".format(e))
            assert False, "***** Add Radius server failed *****"

        for i in range(0, 3):
            self.args['rad_server'].pop(0)

    # Tnt5212445c_Tnt5210671c
    def configure_radius_server_sequence(self):
        s_log.info("<-- Inside configure_radius_server_sequence function -->")
        time.sleep(5)
        from tests.configurations.ise.ui.administration.network_resources.RADIUS_server_sequences import \
            RADIUSserverSequences
        server_sequence = RADIUSserverSequences(app=self.app, logger=s_log)
        server_sequence.navigate_to_page()
        rad_server_seq = self.args['configure_radius_server_sequence'][0]
        rad_server = self.args['configure_radius_server_sequence'][1]
        s_log.info("<-- rad_server_value --> {} ".format(rad_server))
        server_sequence.add_radius_server_sequence(name=rad_server_seq, radiusServerNames=rad_server)

        for i in range(0, 2):
            self.args['configure_radius_server_sequence'].pop(0)

    # Tnt5212445c_Tnt5210671c
    def select_proxy_seq(self):
        s_log.info("<-- Inside select_proxy_seq function -->")
        time.sleep(5)
        from tests.configurations.ise.ui.policy.policy_sets.new_policy_sets import RadPolicySets
        new_policy = RadPolicySets(app=self.app, logger=s_log)
        ##new_policy.navigate_to_page()
        time.sleep(5)
        use_val = self.args['select_proxy_seq'][0]
        new_policy.navigate_policy.click()
        time.sleep(5)
        new_policy.navigate_policy_sets.click()
        time.sleep(5)
        new_policy.open_set_view.click()
        time.sleep(5)
        new_policy.change_allowed_protocol_in_default_policy_set(use_val=use_val)
        s_log.info("**** Successfully edited default policy set... ****")
        time.sleep(3)

        for i in range(0, 1):
            self.args['edit_default_policy_set'].pop(0)

    # Tnt5212445c_Tnt5210671c
    def config_network_device(self):
        fname = 'config_network_device'
        s_log.info("<-- Inside config_network_device function -->")
        time.sleep(5)
        from tests.configurations.ise.ui.administration.network_resources.network_device import NetworkDevice
        ui_lib = NetworkDevice(app=self.app, logger=s_log)
        ui_lib.driver.execute_script(
            'window.location.hash = "#administration/administration_networkresources/administration_networkresources_devices"')
        time.sleep(10)

        # ui_lib.navigate_to_page()
        time.sleep(5)
        name = self.args[fname][0]
        ip = self.args[fname][1]
        secret = self.args[fname][2]
        additional_params = {}
        if len(self.args[fname]) > 3:
            additional_params = self.args[fname][3]
        mask = additional_params.get('mask', 32)

        time.sleep(3)
        if ui_lib.nad_by_name(nad_name=name):
            ui_lib.delete_network_device(name1=name)
        time.sleep(3)
        ui_lib.add_network_device(name=name, ip_address=ip,
                                  shared_secret=secret,
                                  mask=mask)
        UI_methods.remove_binded_args_after_run(obj=self,
                                                func_name=fname,
                                                args_count=len(self.args[fname]),
                                                )

    # Tnt5212445c_Tnt5210671c
    def internal_user(self):
        s_log.info("<-- Inside internal_user function -->")
        time.sleep(5)
        from tests.configurations.ise.ui.administration.identity_management.identities import \
            Identities
        ui_iden = Identities(app=self.app, logger=s_log)
        ui_iden.navigate_to_page()
        time.sleep(5)
        username = self.args['internal_user'][0]
        email = self.args['internal_user'][1]
        password = self.args['internal_user'][2]
        ui_iden.add_user(name=username, email=email,
                         password=password)

        for i in range(0, 3):
            self.args['internal_user'].pop(0)

    # Tnt5212445c_Tnt5210671c
    def delete_internal_user(self):
        from tests.configurations.ise.ui.administration.identity_management.identities import \
            Identities
        ui_iden = Identities(app=self.app, logger=s_log)
        ui_iden.navigate_to_page()
        username = self.args['delete_internal_user'][0]
        version = self.args['delete_internal_user'][1]
        ui_iden.delete_user(name1=username, version=version)

        for i in range(0, 2):
            self.args['delete_internal_user'].pop(0)

    # Tnt5212445c_Tnt5210671c
    def delete_network_device(self):
        from tests.configurations.ise.ui.administration.network_resources.network_device import \
            NetworkDevice
        ui_lib = NetworkDevice(app=self.app, logger=s_log)
        ui_lib.driver.execute_script(
            'window.location.hash = "#administration/administration_networkresources/administration_networkresources_devices"')
        time.sleep(10)

        # ui_lib.navigate_to_page()
        name = self.args['delete_network_device'][0]
        ui_lib.delete_network_device(name1=name)

        for i in range(0, 1):
            self.args['delete_network_device'].pop(0)

    # Tnt5212445c_Tnt5210671c
    def deselect_proxy_seq(self):
        from tests.configurations.ise.ui.policy.policy_sets.new_policy_sets import RadPolicySets
        new_policy = RadPolicySets(app=self.app, logger=s_log)
        value = self.args['deselect_proxy_seq'][1]
        new_policy.navigate_policy.click()
        new_policy.navigate_policy_sets.click()
        # new_policy.open_set_view.click()
        new_policy.change_allowed_protocol_in_default_policy_set(use_val=value)
        new_policy.save_button.click()
        s_log.info("**** Successfully edited default policy set... ****")
        time.sleep(3)

        for i in range(0, 1):
            self.args['deselect_proxy_seq'].pop(0)

    # Tnt5212445c_Tnt5210671c
    def delete_radius_server_sequence(self):
        from tests.configurations.ise.ui.administration.network_resources.RADIUS_server_sequences import \
            RADIUSserverSequences
        server_sequence = RADIUSserverSequences(app=self.app, logger=s_log)
        server_sequence.navigate_to_page()
        rad_server_seq = self.args['delete_radius_server_sequence'][0]
        server_sequence.delete_radius_server_sequence(rad_server_seq)

        for i in range(0, 1):
            self.args['delete_radius_server_sequence'].pop(0)

    # Tnt5212445c_Tnt5210671c
    def delete_rad_server(self):
        from tests.configurations.ise.ui.administration.network_resources.external_RADIUS_servers import \
            externalRadiusServers
        ui_lib = externalRadiusServers(app=self.app, logger=s_log)
        ui_lib.navigate_to_page()
        rad_server = self.args['delete_rad_server'][0]
        ui_lib.delete_external_radius_server(rad_server)

        for i in range(0, 1):
            self.args['delete_rad_server'].pop(0)

    def login_different_ise(self):
        from tests.configurations.ise.ui.login_page import Login
        ise_url = self.args['login_different_ise'][0]
        username = self.args['login_different_ise'][1]
        password = self.args['login_different_ise'][2]
        login = Login(app=self.app, logger=s_log, url=ise_url)
        s_log.info("Login into different ISE")
        try:
            login.navigate_to_page()
            login.login(username, password)
            # login.login(username_text=username, password_text=password, timeout=time_out)
            s_log.info("Logged in Successfully")
            assert True
        except Exception as e:
            s_log.info("Not able to login into ise : {}".format(e))
            assert False
        for i in range(0, 3):
            self.args['login_different_ise'].pop(0)

    def disable_lower_upper_in_pswdpolicy(self):
        from tests.configurations.ise.ui.administration.identity_management.settings.user_authentication_settings import \
            UserAuthenticationSettings
        pswdpolicy = UserAuthenticationSettings(self.app, self.logger)
        pswdpolicy.navigate_to_page()
        pswdpolicy.edit_password_policy()
        time.sleep(2)

    def enable_inner_checkbox_password_policy(self):
        from tests.configurations.ise.ui.administration.identity_management.settings.user_authentication_settings import \
            UserAuthenticationSettings
        pswdpolicy = UserAuthenticationSettings(self.app, self.logger)
        pswdpolicy.navigate_to_page()
        pswdpolicy.enable_inner_checkbox_password_policy()
        time.sleep(2)

    def create_new_allowed_protocol_with_eap_fast(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowedprotocols = AllowedProtocols(app=self.app, logger=s_log)
        protocol_name = self.args['create_new_allowed_protocol_with_eap_fast'][0]
        desp = self.args['create_new_allowed_protocol_with_eap_fast'][1]
        time_str = self.args['create_new_allowed_protocol_with_eap_fast'][2]
        format = self.args['create_new_allowed_protocol_with_eap_fast'][3]
        percentage = self.args['create_new_allowed_protocol_with_eap_fast'][4]
        allowedprotocols.navigate_to_page()
        time.sleep(5)
        if allowedprotocols.select_protocol_by_name(protocol_name).is_displayed():
            allowedprotocols.delete_allowed_prtocol(protocol_name)
        allowedprotocols.create_eap_fast_protocol(protocol_name=protocol_name,
                                                  desp=desp,
                                                  time_str=time_str,
                                                  format=format,
                                                  percentage=percentage)
        for i in range(0, 5):
            self.args['create_new_allowed_protocol_with_eap_fast'].pop(0)

    def create_new_authorization_policy_ad(self,
                                           cond_name='new_ad', attr_val='ExternalGroups', comp_cond_name='na_uplift_grp'
                                           ):
        from tests.configurations.ise.ui.policy.policy_sets.new_policy_sets import RadPolicySets
        new_policy_set = RadPolicySets(app=self.app, logger=s_log)
        new_policy_set.wait_for_loader([new_policy_set.new_authorization_policy])
        new_policy_set.new_authorization_policy.click()
        # new_policy_set.enter_authorization_section.click()
        # new_policy_set.authorization_profile_textbox_test.send_text(profiles)
        time.sleep(4)
        # new_policy_set.authorization_profile_textbox_test.send_enter()
        new_policy_set.author_open_conditions.click()
        time.sleep(3)
        # click to add an attribute
        new_policy_set.logger.info("waiting for Add Codition button...")
        new_policy_set.wait_for_loader([new_policy_set.add_condition_attribute])
        time.sleep(5)
        new_policy_set.logger.info("Adding Policy Condition Rule...")
        new_policy_set.add_condition_attribute.click()
        # if not new_policy_set.select_attr_condition_text.is_displayed():
        #     new_policy_set.logger.info("select attribute condition text is not visible, clicking again...")
        #     new_policy_set.add_condition_attribute.click()
        time.sleep(5)
        # click on dictionary dropdown
        new_policy_set.wait_for_loader([new_policy_set.select_attr_for_condition])
        new_policy_set.select_attr_for_condition.click()
        time.sleep(3)
        # self.select_attr_for_condition.select_option_by_value(cond_name)
        new_policy_set.select_attr_for_condition.select_option(cond_name)
        time.sleep(2)
        # select attr value
        new_policy_set.logger.info("Selecting Attribute Value from ...")
        new_policy_set.select_attr_val(attr_val).scroll_to_element()
        new_policy_set.wait_for_loader([new_policy_set.select_attr_val(attr_val)])
        new_policy_set.select_attr_val(attr_val).click()
        new_policy_set.select_attr_val(attr_val).click()
        time.sleep(5)
        new_policy_set.select_attribute.click()
        time.sleep(10)
        new_policy_set.select_condition_studio_attribute(attr_val).click()
        new_policy_set.select_condition_studio_attribute(attr_val).click()
        time.sleep(3)
        new_policy_set.wait_for_loader([new_policy_set.save_library_condition_button])
        new_policy_set.save_library_condition_button.click()
        new_policy_set.wait_for_loader([new_policy_set.save_as_new_library])
        new_policy_set.logger.info("Saving a New Library ")
        new_policy_set.save_as_new_library.click()
        new_policy_set.wait_for_loader([new_policy_set.insert_condition_name])
        new_policy_set.insert_condition_name.click()
        new_policy_set.insert_condition_name.send_text(comp_cond_name)
        new_policy_set.save_condition_button.click()
        time.sleep(2)
        new_policy_set.wait_for_loader([new_policy_set.use_button])
        new_policy_set.use_button.click()
        time.sleep(2)
        new_policy_set.logger.info("Saving the Authorization Policy ...")
        new_policy_set.save_button.click()
        time.sleep(5)

    def scope_function(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        scope_meth = ActiveDirectory(app=self.app, logger=s_log)
        scope_meth.navigate_to_page()
        time.sleep(5)
        scope_meth.create_scope_with_multiple_ad_instance("trial_scope", "new_ad", "b1.com", "acsadmin",
                                                          "acS100%", "na_uplift_grp")

    def check_user_name(self, username):
        from tests.configurations.ise.ui.operations.radius.live_logs import Livelogs
        live_logs = Livelogs(app=self.app, logger=s_log)
        live_logs.navigate_to_page()
        usr = live_logs.live_log_details_get_attributes(['Username'])
        s_log.info("***********************")
        s_log.info(usr)
        if not usr.get('Username') == username:
            s_log.info("***********************")
            s_log.info("Username is not as expected")
            s_log.info("***********************")

    def Enable_Peap_Eap_Mschap(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowedprotocols = AllowedProtocols(self.app, self.logger)
        allowedprotocols.navigate_to_page()
        allowedprotocols.PEAP_EAP_MSCHAPv2_enable()
        time.sleep(2)

    def Enable_Weak_Ciphers(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowedprotocols = AllowedProtocols(self.app, self.logger)
        allowedprotocols.navigate_to_page()
        allowedprotocols.Enable_weak_ciphers()
        time.sleep(2)

    def Disable_Weak_Ciphers(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowedprotocols = AllowedProtocols(self.app, self.logger)
        allowedprotocols.navigate_to_page()
        allowedprotocols.Disable_weak_ciphers()
        time.sleep(2)

    def Genarate_PAC_configuration(self):
        from tests.configurations.ise.ui.administration.system.settings.Protocols.protocols import EAPFAST
        generatepac = EAPFAST(self.app, self.logger)
        identity_name = self.args['Genarate_PAC_configuration'][0]
        encryption_key = self.args['Genarate_PAC_configuration'][1]
        ttl = self.args['Genarate_PAC_configuration'][2]
        ttl_period = self.args['Genarate_PAC_configuration'][3]
        generatepac.navigate_to_page()
        time.sleep(5)
        generatepac.generate_tunnel_and_machine_pac_multiple_inputs(identity=identity_name, key=encryption_key,
                                                                    ttl=ttl, ttl_period=ttl_period)

        for i in range(0, 4):
            self.args['Genarate_PAC_configuration'].pop(0)

    def delete_authorization_rule(self):
        from tests.configurations.ise.ui.policy.policy_sets.new_policy_sets import RadPolicySets
        new_policy = RadPolicySets(app=self.app, logger=s_log)
        new_policy.navigate_to_policy_set_page()
        time.sleep(5)
        policy_name = self.args['delete_authorization_rule'][0]
        time.sleep(10)
        new_policy.delete_authorization_by_policy_name(policy_name=policy_name)
        time.sleep(10)

    """++++++++++++++++++++++++++++++++++++++Library Condition+++++++++++++++++++++++++++++++++++++++++++++++++++++++"""

    def change_operator_value_and_save_as_existing_condition(self):
        from tests.configurations.ise.ui.policy.policy_elements.conditions.library_conditions import LibraryConditions
        LC = LibraryConditions(self.app, self.logger)
        UI_methods.retry_now(self, LC.navigate_to_page)
        LC.load_library_condition()
        LC.search_conditions_library(self.args['change_operator_value_and_save_as_existing_condition'][0])
        LC.drag_and_drop(LC.conditions_studio_library_condition(self.args['change_operator_value_and_save_as_existing_'
                                                                          'condition'][0]).element, '')
        LC.edit_library_condition()
        LC.edit_operator_attribute(self.args['change_operator_value_and_save_as_existing_condition'][1])
        LC.scroll_to_top()
        LC.save_editor.click()
        LC.save_condition.click()
        LC.navigate_to_page()
        LC.load_library_condition()
        LC.search_conditions_library(self.args['change_operator_value_and_save_as_existing_condition'][0])
        LC.drag_and_drop(LC.conditions_studio_library_condition(self.args['change_operator_value_and_save_'
                                                                          'as_existing_condition'][0]).element, '')
        LC.edit_library_condition()
        operator_attribute_value = Button(By.XPATH, "//option[@selected='selected']", self.app.driver).get_text()
        if operator_attribute_value == self.args['change_operator_value_and_save_as_existing_condition'][1]:
            s_log.info("Library condition failed to save.")
            assert False
        else:
            s_log.info("Library condition successfully saved.")

    def revert_change_operator_value_and_save_as_existing_condition(self):
        from tests.configurations.ise.ui.policy.policy_elements.conditions.library_conditions import LibraryConditions
        LC = LibraryConditions(self.app, self.logger)
        UI_methods.retry_now(self, LC.navigate_to_page)
        LC.load_library_condition()
        LC.search_conditions_library(self.args['revert_change_operator_value_and_save_as_existing_condition'][0])
        LC.drag_and_drop(LC.conditions_studio_library_condition(self.args['revert_change_operator_value_and_save_'
                                                                          'as_existing_condition'][0]).element,
                         '')
        LC.edit_library_condition()
        LC.edit_operator_attribute(self.args['revert_change_operator_value_and_save_as_existing_condition'][1])
        LC.scroll_to_top()
        LC.save_editor.click()
        LC.save_condition.click()
        LC.navigate_to_page()
        LC.load_library_condition()
        LC.search_conditions_library(self.args['revert_change_operator_value_and_save_as_existing_condition'][0])
        LC.drag_and_drop(LC.conditions_studio_library_condition(self.args['revert_change_operator_value_and_save_'
                                                                          'as_existing_condition'][0]).element,
                         '')
        LC.edit_library_condition()
        operator_attribute_value = Button(By.XPATH, "//option[@selected='selected']", self.app.driver).get_text()
        if operator_attribute_value == self.args['revert_change_operator_value_and_save_as_existing_condition'][1]:
            s_log.info("Library condition failed to save and original value is not reverted back.")
        else:
            s_log.info("Library condition successfully saved and reverted back to original value.")

    def rename_library_condition(self):
        from tests.configurations.ise.ui.policy.policy_elements.conditions.library_conditions import LibraryConditions
        LC = LibraryConditions(self.app, s_log)
        UI_methods.retry_now(self, LC.navigate_to_page)
        LC.load_library_condition()
        LC.drag_and_drop(LC.conditions_studio_library_condition(self.args['rename_library_condition'][0]).element, '')
        LC.edit_library_condition()
        LC.save_editor.click()
        if LC.rename_library_condition(self.args['rename_library_condition'][0],
                                       self.args['rename_library_condition'][1]):
            s_log.info("Library condition successfully renamed.")
        else:
            s_log.info("Library condition could not be renamed. No provision to enter the new name.")
            # assert False
        element_id = LC.find_condition(self.args['rename_library_condition'][1])
        if element_id.wait_for_element():
            s_log.info("Renamed library condition available in library condition table.")
        else:
            s_log.info("Renamed library condition is not available in the table.")

    def add_conditions_with_block(self):
        from tests.configurations.ise.ui.policy.policy_elements.conditions.library_conditions import LibraryConditions
        LC = LibraryConditions(self.app, s_log)
        name_of_policy = self.args['add_conditions_with_block'][0]
        name_of_condition = self.args['add_conditions_with_block'][1]
        match_attribute = self.args['add_conditions_with_block'][2]  # "OR" ,"AND" etc..
        UI_methods.retry_now(self, LC.navigate_to_page)
        try:
            LC.library_condition_select_or_block.click()
            time.sleep(3)
            for condition in name_of_condition:
                LC.drag_and_drop(LC.conditions_studio_library_condition(condition).element, '')
                time.sleep(5)
            LC.save_editor.click(do_move=False)
            LC.save_as_new.click()
            time.sleep(3)
            LC.condition_name.send_text(name_of_policy)
            time.sleep(3)
            LC.save_condition.click()
            time.sleep(3)
            LC.navigate_to_page()
            LC.load_library_condition()
            LC.search_conditions_library(name_of_policy)
            LC.drag_and_drop(LC.conditions_studio_library_condition(name_of_policy).element, '')
            time.sleep(3)
            LC.edit_library_condition()
            time.sleep(3)
            value = LC.library_condition_type_selected.get_text()
            if not value == match_attribute:
                assert False

        except Exception as e:
            s_log.info("Exception as {}".format(e))
            assert False
        for i in range(0, 3):
            self.args['add_conditions_with_block'].pop(0)

    def remove_condition_from_library(self):
        from tests.configurations.ise.ui.policy.policy_elements.conditions.library_conditions import LibraryConditions
        LC = LibraryConditions(self.app, s_log)
        name_of_condition = self.args['remove_condition_from_library'][0]
        UI_methods.retry_now(self, LC.navigate_to_page)
        LC.load_library_condition()
        LC.search_conditions_library(name_of_condition)
        LC.delete_condition(name_of_condition)
        s_log.info("Policy condition has been deleted.")
        time.sleep(3)
        for i in range(0, 1):
            self.args['remove_condition_from_library'].pop(0)

    """"++++++++++++++++++++++++++++++++++++++Library Condition++++++++++++++++++++++++++++++++++++++++++++++++++++++"""

    def compare_attributes_from_live_logs(self):
        from tests.configurations.ise.ui.operations.radius.live_logs import Livelogs
        fname = 'compare_attributes_from_live_logs'
        attribute_map = self.args[fname][0]
        live_logs = Livelogs(app=self.app, logger=s_log)
        live_logs.navigate_to_page()
        dict_returned = live_logs.live_log_details_get_attributes(list(attribute_map.keys()))
        s_log.info("************Dictionary Obtained is as follows***********")
        s_log.info(dict_returned)
        for attribute in attribute_map:
            if dict_returned[attribute] != attribute_map[attribute]:
                assert False, "Expected value for attribute '{}' is '{}', but '{}' was returned".format(attribute,
                                                                                                        attribute_map[
                                                                                                            attribute],
                                                                                                        dict_returned[
                                                                                                            attribute],
                                                                                                        )
            s_log.info("Expected value for attribute '{}' is '{}', got '{}' as expected".format(attribute,
                                                                                                attribute_map[
                                                                                                    attribute],
                                                                                                dict_returned[
                                                                                                    attribute],
                                                                                                ))
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=1)

    def ldap_retrieve_attributes(self):
        from tests.configurations.ise.ui.administration.identity_management.ldap import Ldap
        ldap_nav = Ldap(self.app, s_log)
        ldap_nav.navigate_to_page()
        time.sleep(5)
        name = self.args['ldap_retrieve_attributes'][0]
        username = self.args['ldap_retrieve_attributes'][1]
        if not ldap_nav.ldap_retrieve_attr(name=name, username=username):
            s_log.info("Attributes not found for the username provided")
            ldap_nav.popup_cancel_button.click()
            aetest.Testcase().failed("Attributes not found for the username provided")
        ldap_nav.popup_cancel_button.click()
        for i in range(0, 2):
            self.args['ldap_retrieve_attributes'].pop(0)

    def check_error_message_displayed(self, page_object, message):
        if page_object.read_popup_text.is_displayed():
            error_message = page_object.read_popup_text.get_text()
            page_object.popup_ok_button.click()
            s_log.error("Pop up message encountered is: '{}'".format(error_message))
            page_object.navigate_to_page()
            page_object.popup_ok_button.click()
            if message not in error_message:
                aetest.Testcase().failed("Error message is not as expected")

    def verify_ad_group_deletion(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        ad = ActiveDirectory(app=self.app, logger=s_log)
        ad.navigate_to_page()
        time.sleep(5)
        ad_name = self.args['verify_ad_group_deletion'][0]
        group_name = self.args['verify_ad_group_deletion'][1]
        action_result = self.args['verify_ad_group_deletion'][2]
        message_expected = self.args['verify_ad_group_deletion'][3]
        # Consider ad_name paramter to be a dictionary
        scope_name = ad_name.get('scope')
        ad_instance = ad_name.get('ad')
        if scope_name is not None:
            ad.select_ad(scope_name)
            ad.wait_for_loader([ad.testuser_test_button], timeout=60)
        if len(set([ad.delete_ad_group(ad_instance, group_name), action_result])) != 1:
            if ad.read_popup_text.is_element_displayed():
                s_log.error(
                    "There was a popup alert with the following message.\n {}".format(ad.read_popup_text.get_text()))
                ad.popup_ok_button.click()
            ad.navigate_to_page()
            if ad.popup_ok_button.is_element_displayed():
                ad.popup_ok_button.click()
            aetest.Testcase().failed("The deletion result was not as expected")
        UI_methods.check_error_message_displayed(self, ad, message_expected)

    def test_user_authentication(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        activedirectory = ActiveDirectory(self.app, self.logger)
        ad_name = self.args['test_user_authentication'][0]
        username = self.args['test_user_authentication'][1]
        password = self.args['test_user_authentication'][2]
        authentypename = self.args['test_user_authentication'][3]
        group_name = self.args['test_user_authentication'][4]
        attribute_value = self.args['test_user_authentication'][5]
        # Consider ad_name paramter to be a dictionary
        scope_name = ad_name.get('scope')
        ad_instance = ad_name.get('ad')
        activedirectory.navigate_to_page()
        time.sleep(10)
        if scope_name is not None:
            activedirectory.select_ad(scope_name)
            activedirectory.wait_for_loader([activedirectory.testuser_test_button], timeout=60)
            activedirectory.ad_in_scope_mode(ad_instance).click()
        else:
            activedirectory.select_ad(ad_name=ad_instance)
        time.sleep(10)
        activedirectory.user_authentication_test(username=username, password=password, authentypename=authentypename,
                                                 group_name=group_name, attribute_value=attribute_value)
        time.sleep(2)

        for i in range(0, 6):
            self.args['test_user_authentication'].pop(0)

    def create_simple_library_condition(self):
        fname = 'create_simple_library_condition'
        library_condtion_page = LibraryConditions(self.app, s_log)
        condition_name = self.args[fname][0]
        condition_key = self.args[fname][1]
        condition_value = self.args[fname][2]
        relative_condition = self.args[fname][3]
        condition_attr_value = self.args[fname][4]
        s_log.info("Navigating to Library Condition Page")
        UI_methods.retry_now(self, library_condtion_page.navigate_to_page)
        # library_condtion_page.delete_library_condition_if_exists(condition_name=condition_name)
        # Above line commented as library_condition is deleted in setup part by delete_library_conditions_with_prefix
        library_condtion_page.create_new_simple_library_condition(condition_name=condition_name,
                                                                  condition_key=condition_key,
                                                                  condition_value=condition_value,
                                                                  condition_attr_value=condition_attr_value,
                                                                  relative_condition=relative_condition)
        for i in range(0, 5):
            self.args['create_simple_library_condition'].pop(0)

    def delete_multiple_library_condition(self):
        fname = 'delete_multiple_library_condition'
        library_condtion_page = LibraryConditions(self.app, s_log)
        conditions = self.args[fname][0]
        UI_methods.retry_now(self, library_condtion_page.navigate_to_page)
        for condition in conditions:
            s_log.info("Deleting {} library Condition...".format(condition))
            library_condtion_page.search_conditions_library(condition)
            library_condtion_page.delete_condition(condition)
            time.sleep(3)
        for i in range(0, 1):
            self.args['delete_multiple_library_condition'].pop(0)

    def navigate_to_policy_set(self):
        fname = 'navigate_to_policy_set'
        policy_page = RadPolicySets(app=self.app, logger=s_log)
        polic_set_name = self.args[fname][0]
        policy_page.navigate_to_page()
        policy_page.enter_policy_set_view_by_name(polic_set_name)
        time.sleep(3)

    def create_policy_set(self):
        s_log.info("Creating Policy Set")
        fname = 'create_policy_set'
        policy_page = RadPolicySets(app=self.app, logger=s_log)
        policy_set_name = self.args[fname][0]
        policy_cond_name = self.args[fname][1]
        policy_set_protocol = self.args[fname][2]
        time.sleep(2)
        policy_page.navigate_to_page()
        time.sleep(4)
        policy_page.delete_policy_set_if_exists(policy_set_name=[policy_set_name])
        policy_page.create_new_policy_set(policy_set_name, policy_cond_name, policy_set_protocol)
        for i in range(0, 3):
            self.args[fname].pop(0)

    def create_authentication_rule_for_simple_condition(self):
        fname = 'create_authentication_rule_for_simple_condition'
        policy_page = RadPolicySets(app=self.app, logger=s_log)
        policy_set_name = self.args[fname][0]
        auth_policy_name = self.args[fname][1]
        auth_cond_name = self.args[fname][2]
        auth_store = self.args[fname][3]
        policy_page.navigate_to_page()
        time.sleep(3)
        policy_page.enter_policy_set_view_by_name(policy_set_name)
        time.sleep(4)
        policy_page.create_new_authentication_rule_for_simple_condition(auth_policy_name, auth_cond_name, auth_store)
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=4)

    def create_authorization_rule_for_simple_condition(self):
        fname = 'create_authorization_rule_for_simple_condition'
        policy_page = RadPolicySets(app=self.app, logger=s_log)
        policy_set_name = self.args[fname][0]
        authz_policy_name = self.args[fname][1]
        authz_cond_name = self.args[fname][2]
        profile = self.args[fname][3]
        security_group = self.args[fname][4]
        policy_page.navigate_to_page()
        time.sleep(3)
        policy_page.enter_policy_set_view_by_name(policy_set_name)
        time.sleep(4)
        policy_page.create_new_authorization_rule_for_simple_condition(authz_policy_name, authz_cond_name, profile,
                                                                       security_group)

        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=5)

    def delete_policy_set(self):
        fname = 'delete_policy_set'
        policy_page = RadPolicySets(app=self.app, logger=s_log)
        policy_set_list = self.args[fname][0]
        policy_page.navigate_to_page()
        policy_page.delete_policy_set_by_name(policy_set_list=policy_set_list)
        for i in range(0, 1):
            self.args[fname].pop(0)

    def delete_multiple_authentication_policy(self):
        fname = 'delete_multiple_authentication_policy'
        policy_page = RadPolicySets(app=self.app, logger=s_log)
        policy_set_name = self.args[fname][0]
        auth_policy_list = self.args[fname][1]
        policy_page.navigate_to_page()
        time.sleep(3)
        policy_page.enter_policy_set_view_by_name(policy_set_name)
        s_log.info("Deleting Authentication Policies ")
        time.sleep(5)
        policy_page.delete_multiple_authentication_policy_by_policy_name(auth_policy_list=auth_policy_list)

    def delete_multiple_authorization_policy(self):
        fname = 'delete_multiple_authorization_policy'
        policy_page = RadPolicySets(app=self.app, logger=s_log)
        policy_set_name = self.args[fname][0]
        authz_policy_list = self.args[fname][1]
        policy_page.navigate_to_page()
        time.sleep(3)
        policy_page.enter_policy_set_view_by_name(policy_set_name)
        time.sleep(5)
        policy_page.delete_multiple_authorization_policy_by_policy_name(authz_policy_list=authz_policy_list)

    def adding_id_source(self):
        from tests.suites.radius_token.identity_source_sequences_new import IdentitySourceSequences
        fname = 'adding_id_source'
        sequence = IdentitySourceSequences(app=self.app, logger=s_log)
        sequence.navigate_to_page()
        policy_set_name = self.args[fname][0]
        sequence.add_identity_to_all_user_id_store(policy_set_name)
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=1)

    def removing_id_source(self):
        from tests.suites.radius_token.identity_source_sequences_new import IdentitySourceSequences
        fname = 'removing_id_source'
        sequence = IdentitySourceSequences(app=self.app, logger=s_log)
        sequence.navigate_to_page()
        policy_set_name = self.args[fname][0]
        sequence.remove_identity_from_all_user_id_store(policy_set_name)

    def library_condition_attribute_operator_validation(self):
        from tests.configurations.ise.ui.policy.policy_elements.conditions.library_conditions import LibraryConditions
        LC = LibraryConditions(self.app, s_log)
        attr_type, attr_values = self.args['library_condition_attribute_operator_validation'][0], \
                                 self.args['library_condition_attribute_operator_validation'][1]
        result = []
        failed = False
        for key, value in attr_values.items():
            LC.navigate_to_page()
            LC.load_library_condition()
            LC.add_attribute.click()
            if not LC.select_attribute_popover.is_displayed():
                s_log.info("Found the instruction screen")
                LC.add_attribute.click()
            time.sleep(2)
            LC.choose_attribute_key_value(value[0], value[1])
            operator_value = LC.get_operator_list.get_text()
            operator_list = operator_value.split("\n")
            for data in attr_type[key]:
                if data not in operator_list:
                    failed = True
                    result.append('{},{} operator values mismatch.Expected {} but got {}'.format(value[0], value[1],
                                                                                                 attr_type[key],
                                                                                                 operator_list))
                    break
        if failed:
            for data in result:
                s_log.info("------------Mismatch details---------------")
                s_log.info(data)
            assert False, 'Operator value is not retrieved as expected. Check above logs for info.'
        else:
            s_log.info('Operator values retrieved as expected.')

    def create_scope_with_ad(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        ad = ActiveDirectory(app=self.app, logger=s_log)
        ad.navigate_to_page()
        time.sleep(5)
        scope_name = self.args['create_scope_with_ad'][0]
        ad_name = self.args['create_scope_with_ad'][1]
        domain_name = self.args['create_scope_with_ad'][2]
        username = self.args['create_scope_with_ad'][3]
        password = self.args['create_scope_with_ad'][4]
        ad.create_scope_with_ad_instance(scope_name, ad_name, domain_name, username, password)

    def create_scope_with_ad_join(self):

        '''Edited - vinoarum'''

        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        ad = ActiveDirectory(app=self.app, logger=s_log)
        ad.navigate_to_page()
        time.sleep(5)
        scope_name = self.args['create_scope_with_ad_join'][0]
        ad_name = self.args['create_scope_with_ad_join'][1]
        domain_name = self.args['create_scope_with_ad_join'][2]
        username = self.args['create_scope_with_ad_join'][3]
        password = self.args['create_scope_with_ad_join'][4]
        group_ad = self.args['create_scope_with_ad_join'][5]
        expected_to_join = self.args['create_scope_with_ad_join'][6]

        join_status = ad.create_scope_with_ad_instance_join_groups(scope_name, ad_name, domain_name, username,
                                                                   password, group_ad)
        self.logger.info("The join status was expected to be {} and the actual join status was {}"
                         .format(expected_to_join, join_status))
        if expected_to_join is not join_status:
            assert False, "Check above log info for more details."

        for i in range(0, 7):
            self.args['create_scope_with_ad_join'].pop(0)

    def delete_ad_in_scope(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        active_directory = ActiveDirectory(app=self.app, logger=self.logger)
        scope_name = self.args['delete_ad_in_scope'][0]
        ad_name = self.args['delete_ad_in_scope'][1]
        active_directory.navigate_to_page()
        active_directory.delete_ad_in_scope(scope_name=scope_name, ad_name=ad_name)
        for i in range(0, 2):
            self.args['delete_ad_in_scope'].pop(0)

    def delete_scope(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        active_directory = ActiveDirectory(app=self.app, logger=self.logger)
        scope_name = self.args['delete_scope'][0]
        active_directory.navigate_to_page()
        active_directory.delete_scope(scope_name)
        for i in range(0, 1):
            self.args['delete_scope'].pop(0)

    def exit_scope_mode(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        active_directory = ActiveDirectory(app=self.app, logger=self.logger)
        active_directory.navigate_to_page()
        active_directory.exit_scope_mode()

    def Enable_Eap_MD5(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowedprotocols = AllowedProtocols(self.app, self.logger)
        allowedprotocols.navigate_to_page()
        allowedprotocols.Eap_MD5_enable()

    def add_nad_group(self):
        s_log.info("<-- Creating network device group -->")
        time.sleep(5)
        from tests.configurations.ise.ui.administration.network_resources.network_device_group import NetworkDeviceGroup
        nad_group = NetworkDeviceGroup(app=self.app, logger=s_log)
        group_name = self.args['add_nad_group'][0]
        parent_group = self.args['add_nad_group'][1]
        nad_group.navigate_to_page()
        time.sleep(5)
        nad_group.add_network_device_group(group_name=group_name, group_type=parent_group)

    def delete_nad_group(self):
        s_log.info("<-- Deleting network device group -->")
        time.sleep(5)
        from tests.configurations.ise.ui.administration.network_resources.network_device_group import NetworkDeviceGroup
        group = NetworkDeviceGroup(app=self.app, logger=s_log)
        group_name = self.args['delete_nad_group'][0]
        group.navigate_to_page()
        time.sleep(5)
        group.flat_view_NDG_click.wait_for_element(timeout=10)
        group.flat_view_NDG_click.click()
        if group.check_if_ndgs_are_present(ndg_array=[group_name]):
            s_log.info(" <-- Group found -->")
            group.delete_ndg_group(group_name=group_name)

    def add_network_device_with_nad_group(self):
        s_log.info('Adding the NAD device with NAD group')
        from tests.configurations.ise.ui.administration.network_resources.network_device import NetworkDevice
        nad = NetworkDevice(app=self.app, logger=s_log)
        networkDevicePage.driver.execute_script(
            'window.location.hash = "#administration/administration_networkresources/administration_networkresources_devices"')
        time.sleep(10)

        name = self.args['add_network_device_with_nad_group'][0]
        ip = self.args['add_network_device_with_nad_group'][1]
        shared_secret = self.args['add_network_device_with_nad_group'][2]
        device_name = self.args['add_network_device_with_nad_group'][3]
        # nad.navigate_to_page()
        time.sleep(5)

        # Check if the NAD is already exist
        if nad.nad_by_name(nad_name=name):
            nad.delete_network_device(name1=name)
        time.sleep(3)

        try:
            success_msg, sucess_alert = nad.add_network_device_type(name=name,
                                                                    ip_address=ip,
                                                                    shared_secret=shared_secret,
                                                                    device_name=device_name)
            if success_msg is None:
                raise Exception("Success Message is not Displayed - {}".format(success_msg))

        except Exception as e:
            assert False, "***** Add Network Device with NAD Group Failed *****"

    def create_scope_and_add_groups(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        from tests.configurations.ise.ui.policy.policy_sets.new_policy_sets import RadPolicySets
        scope_meth = ActiveDirectory(app=self.app, logger=s_log)
        scope_meth.navigate_to_page()
        time.sleep(5)
        scope_name = self.args['create_scope_and_add_groups'][0]
        ad_name = self.args['create_scope_and_add_groups'][1]
        domain_name = self.args['create_scope_and_add_groups'][2]
        username = self.args['create_scope_and_add_groups'][3]
        password = self.args['create_scope_and_add_groups'][4]
        group_ad = self.args['create_scope_and_add_groups'][5]
        scope_meth.create_scope_with_multiple_ad_instance(scope_name=scope_name, ad_name=ad_name,
                                                          domain_name=domain_name, username=username,
                                                          password=password, group_ad=group_ad)

        for i in range(0, 6):
            self.args['create_scope_and_add_groups'].pop(0)

    # pakota
    def retrive_attribute_ad(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        activedirectory = ActiveDirectory(self.app, s_log)
        time.sleep(5)
        activedirectory.navigate_to_page()
        time.sleep(5)
        ad_value = self.args['retrive_attribute_ad'][0]
        username = self.args['retrive_attribute_ad'][1]
        ad_scope = self.args['retrive_attribute_ad'][2]
        group_attributes = self.args['retrive_attribute_ad'][3]
        # activedirectory.add_all_user_attributes_from_active_directory_authstores(username=username)
        activedirectory.select_multiple_attributes_from_ad(ad_value=ad_value, user_name=username, ad_scope=ad_scope,
                                                           group_attributes=group_attributes)
        s_log.info("All attributes fetched from active directory")

    def create_scope_with_ad_join_attribute(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        ad = ActiveDirectory(app=self.app, logger=s_log)
        ad.navigate_to_page()
        time.sleep(10)
        scope_name = self.args['create_scope_with_ad_join_attribute'][0]
        ad_name = self.args['create_scope_with_ad_join_attribute'][1]
        domain_name = self.args['create_scope_with_ad_join_attribute'][2]
        username = self.args['create_scope_with_ad_join_attribute'][3]
        password = self.args['create_scope_with_ad_join_attribute'][4]
        group_ad = self.args['create_scope_with_ad_join_attribute'][5]
        group_attributes = self.args['create_scope_with_ad_join_attribute'][6]
        s_log.info(group_ad, "AD Group added")
        ad.create_scope_with_ad_instance_join_groups_attributes(scope_name, ad_name, domain_name, username,
                                                                password, group_ad, group_attributes)
        for i in range(0, 6):
            self.args['create_scope_and_add_groups'].pop(0)

    # pakota
    def create_new_authorization_policy_rule(self):
        policy_page = RadPolicySets(app=self.app, logger=s_log)
        rule_name = self.args['create_new_authorization_policy_rule'][0]
        rule_line_num = self.args['create_new_authorization_policy_rule'][1]
        profiles = self.args['create_new_authorization_policy_rule'][2]
        attribute = self.args['create_new_authorization_policy_rule'][3]
        attribute_value = self.args['create_new_authorization_policy_rule'][4]

        policy_page.create_new_authorization_policy_rule2(rule_name=rule_name, rule_line_num=rule_line_num,
                                                          profiles=profiles, attribute=attribute,
                                                          attribute_value=attribute_value, sgts=None)

    def check_user_name(self, username):
        from tests.configurations.ise.ui.operations.radius.live_logs import Livelogs
        live_logs = Livelogs(app=self.app, logger=s_log)
        live_logs.navigate_to_page()
        usr = live_logs.live_log_details_get_attributes(['Username'])
        s_log.info("***********************")
        s_log.info(usr)
        if not usr.get('Username') == username:
            s_log.info("***********************")
            s_log.info("Username is not as expected")
            s_log.info("***********************")

    def check_for_policy_set_list(self):
        fname = 'check_for_policy_set_list'
        policies_list = self.args[fname][0]
        s_log.info('checking for policy set names ')
        policy_page = RadPolicySets(self.app, s_log)
        policy_page.navigate_to_page()
        time.sleep(5)
        missing_policies_list, found_policies_list = UI_methods.check_policy_name_exist(self,
                                                                                        policies_list=policies_list)
        s_log.info("{} found policies ".format(found_policies_list))
        if len(missing_policies_list) > 0:
            s_log.error("{} policy names are not availble".format(missing_policies_list))
            assert False, "Failed to find {} policies ".format(missing_policies_list)
        time.sleep(3)
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=1)

    def check_for_authen_policy_list(self):
        fname = 'check_for_authen_policy_list'
        policy_set = self.args[fname][0]
        policies_list = self.args[fname][1]
        s_log.info('checking for authentication policy rules')
        policy_page = RadPolicySets(self.app, s_log)
        policy_page.navigate_to_page()
        time.sleep(5)
        policy_page.enter_policy_set_view_by_name(policy_set)
        time.sleep(5)
        policy_page.authentication_policy_expand.click()
        time.sleep(3)
        missing_policies_list, found_policies_list = UI_methods.check_policy_name_exist(self,
                                                                                        policies_list=policies_list)
        s_log.info("{} found policies ".format(found_policies_list))
        if len(missing_policies_list) > 0:
            s_log.error("{} policy names are not availble".format(missing_policies_list))
            assert False, "Failed to find {} policies ".format(missing_policies_list)
        time.sleep(3)
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=2)

    def check_for_authz_policy_list(self):
        fname = 'check_for_authz_policy_list'
        policy_set = self.args[fname][0]
        policies_list = self.args[fname][1]
        s_log.info('checking for authorization policy rules')
        policy_page = RadPolicySets(self.app, s_log)
        policy_page.navigate_to_page()
        time.sleep(5)
        policy_page.enter_policy_set_view_by_name(policy_set)
        time.sleep(5)
        policy_page.authorization_policy_expand.click()
        time.sleep(3)
        missing_policies_list, found_policies_list = UI_methods.check_policy_name_exist(self,
                                                                                        policies_list=policies_list)
        s_log.info("{} found policies ".format(found_policies_list))
        if len(missing_policies_list) > 0:
            s_log.error("{} policy names are not availble".format(missing_policies_list))
            assert False, "Failed to find {} policies ".format(missing_policies_list)
        time.sleep(3)
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=2)

    @staticmethod
    def check_policy_name_exist(self, policies_list=None):
        missing_policies = []
        found_policies = []
        for policy in policies_list:
            policy_name = BaseElement(By.XPATH, "//span[contains(text(),'{}')]".format(policy), self.app.driver)
            if policy_name.is_element_displayed():
                found_policies.append(policy)
                self.logger.info("Policy created successfully")
            else:
                missing_policies.append(policy)
                self.logger.info("unable to create policy")
        return missing_policies, found_policies

    def domain_authentication_disable(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        ad = ActiveDirectory(app=self.app, logger=s_log)
        time.sleep(5)
        scope_name = self.args['domain_authentication_disable'][0]
        ad_name = self.args['domain_authentication_disable'][1]
        domain_name = self.args['domain_authentication_disable'][2]
        ad.navigate_to_page()
        ad.disable_authentication_domain(scope_name=scope_name, ad_scope=ad_name, domain_name=domain_name)

        for i in range(0, 3):
            self.args['domain_authentication_disable'].pop(0)

    def domain_authentication_enable(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        ad = ActiveDirectory(app=self.app, logger=s_log)
        time.sleep(5)
        scope_name = self.args['domain_authentication_enable'][0]
        ad_name = self.args['domain_authentication_enable'][1]
        domain_name = self.args['domain_authentication_enable'][2]
        ad.navigate_to_page()
        ad.enable_authentication_domain(scope_name=scope_name, ad_scope=ad_name, domain_name=domain_name)

        for i in range(0, 3):
            self.args['domain_authentication_enable'].pop(0)

    def diagnostic_tool_for_run_all_test(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        active_directory = ActiveDirectory(app=self.app, logger=self.logger)
        ad_name = self.args['diagnostic_tool_for_run_all_test'][0]
        active_directory.navigate_to_page()
        active_directory.Diagnostic_tool_run_all_test(ad_name=ad_name)
        for i in range(0, 1):
            self.args['diagnostic_tool_for_run_all_test'].pop(0)

    def diagnostic_tool_for_run_selected_test_randomly(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        active_directory = ActiveDirectory(app=self.app, logger=self.logger)
        ad_name = self.args['diagnostic_tool_for_run_selected_test_randomly'][0]
        random_numer = self.args['diagnostic_tool_for_run_selected_test_randomly'][1]
        active_directory.navigate_to_page()
        active_directory.diagnostic_tool_run_selected_tests(ad_name=ad_name, random_number_of_tests=random_numer)
        for i in range(0, 2):
            self.args['diagnostic_tool_for_run_selected_test_randomly'].pop(0)

    def diagnostic_tool_stop_and_collect_no_run_details(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        active_directory = ActiveDirectory(app=self.app, logger=self.logger)
        ad_name = self.args['diagnostic_tool_stop_and_collect_no_run_details'][0]
        active_directory.navigate_to_page()
        active_directory.diagnostic_tool_stop_and_collect_no_run_details(ad_name=ad_name)
        for i in range(0, 1):
            self.args['diagnostic_tool_stop_and_collect_no_run_details'].pop(0)

    def find_details_in_diagnostic_tool(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        active_directory = ActiveDirectory(app=self.app, logger=self.logger)
        ad_name = self.args['find_details_in_diagnostic_tool'][0]
        test_name = self.args['find_details_in_diagnostic_tool'][1]
        active_directory.navigate_to_page()
        active_directory.validation_for_diagnostic_run_all_test(ad_name=ad_name)
        result = active_directory.get_diaganostic_status(test_name=test_name)
        self.logger.info(result[0])
        self.logger.info("*" * 50)
        self.logger.info(result[1])
        inside_textbox_keys = []
        inside_texbox_values = []
        for index in result[0]:
            inside_textbox_keys.append(index)
            inside_texbox_values.append(result[0][index])
        for compared_values in result[1]:
            if compared_values.strip() in inside_texbox_values or compared_values + " sec" in inside_texbox_values:
                self.logger.info(compared_values + "                           is present in test details")
                self.logger.info("")
            else:
                self.logger.info("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                self.logger.info(compared_values + "                          is not present in test details")
                self.logger.info("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        for i in range(0, 2):
            self.args['find_details_in_diagnostic_tool'].pop(0)

    def validate_diagnostic_tool_details(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        active_directory = ActiveDirectory(app=self.app, logger=self.logger)
        scope_name = self.args['validate_diagnostic_tool_details'][0]
        ad_name = self.args['validate_diagnostic_tool_details'][1]
        test_name_details = self.args['validate_diagnostic_tool_details'][2]
        active_directory.navigate_to_page()
        active_directory.navigate_to_diagnostic_tool(ad_name, scope_name)
        active_directory.diagnostic_tool_run_test(run_all=True)
        results = []
        for test_name, expected_result in test_name_details.items():

            test_result, _ = active_directory.get_diaganostic_status(test_name)
            s_log.info("Test result for {}".format(test_name))
            s_log.info(test_result)
            s_log.info("The expected result is {}".format(expected_result))
            if (test_result['Status'] == 'Successful') == expected_result:
                s_log.info("Diagnostic run result as expected.")
                results.append(True)
            else:
                s_log.info('Diagnostic run result not as expected.')
                results.append(False)
        if not all(results):
            assert False, "Diagnostic run failed.Check above logs for failed reason."

        for i in range(0, 3):
            self.args['validate_diagnostic_tool_details'].pop(0)

    @staticmethod
    def enable_ssh(host, port):
        from tests.configurations.ise.cli.ssh_client_connect import SshClientConnect
        ssh_con = SshClientConnect(host=host, port=port)
        return ssh_con

    @staticmethod
    def get_cli_configuration_cmds(cfg_action='chg_dns_config', cfg_action_params=None):
        """
        :param cfg_actions: name of the cfg_action from cli_cmds
        :param cfg_action_params: dict of {param:value} that needs to be replaced in cfg_action
                example : {IP_NAME_SERVER : 10.0.10.10}
        :return: list of cli cmds to accomplish the cfg_actions
        """

        from tests.suites.network_access.uplift_test.configuration_commands import DEFAULT_COMMANDS
        import re
        default_commands_list = DEFAULT_COMMANDS[cfg_action]
        final_cmds_list = []
        if cfg_action_params:
            for item in default_commands_list:
                command, prompt = item
                for param, value in cfg_action_params.items():
                    if param in command:
                        cmd = re.sub(param, value, command)
                        final_cmds_list.append((cmd, prompt))
                    else:
                        final_cmds_list.append(item)
        else:
            for command in default_commands_list:
                final_cmds_list.append(command)

        return final_cmds_list

    @staticmethod
    def run_cli_configuration_cmds(host, port, username, password, cfg_action, cfg_action_params):
        """
        host, port , username, password for which the ssh connection needs to be
            established or the mahcine where list of cli cmds needs to be executed

        :return:
        """
        import time
        ssh = UI_methods.enable_ssh(host, port)
        cli_commands_list = UI_methods.get_cli_configuration_cmds(cfg_action=cfg_action,
                                                                  cfg_action_params=cfg_action_params)
        print(cli_commands_list)
        try:
            ssh.connect_ssh_client(username=username, password=password)
            for item in cli_commands_list:
                cmd, prompt = item
                cli_output = ssh.execute_command(cmd)
                cli_output, status = UI_methods.wait_until_prompt(ssh, prompt, 600, cli_output, 5)
                time.sleep(3)
        except Exception as msg:
            s_log.error(msg)
            ssh.close_connection()
        s_log.info(cli_output)
        ssh.execute_command('exit\n')
        s_log.info("Command execution result is :{}".format(status))
        ssh.close_connection()

    def check_app_up(ip):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        root_pass = "lab123"
        root_user = "root"
        ssh_to_ise = SSH(ip, root_user, root_pass, timeout=5, logger=logger)
        ssh_to_ise.connect()
        ssh_to_ise.invoke_shell()
        time.sleep(5)
        y = 0
        for x in range(1, 20):
            logger.debug("wait to ISE process to be in running state")
            _, output, _, _ = ssh_to_ise.exec_command("/opt/CSCOcpm/bin/appservercontrol.sh status | awk '{print $3}'")
            logger.debug(output)
            if 'running\n' in output:
                break

            logger.debug("state is not running, sleep 60 sec")
            time.sleep(60)
            _, output, _, _ = ssh_to_ise.exec_command("/opt/CSCOcpm/bin/appservercontrol.sh status | awk '{print $3}'")
            logger.debug(output)
            logger.info("Waited " + str(x) + " minutes.")
            if 'not\n' in output:
                _, output, _, _ = ssh_to_ise.exec_command("/opt/CSCOcpm/bin/appservercontrol.sh start")
            y += 1
            if x == 15:
                logger.error('App Server did not come up, subsequent tests will likely fail.')

        if y == 15:
            assert False
        else:
            logger.debug("ISE service is up and running ")

    def wait_until_prompt(conn_obj, prompt, timeout, command_output, retry_timeout=10):
        time_counter = 0
        s_log.info(command_output)
        while True:
            if command_output.endswith(prompt):
                s_log.info("Prompt is found , command output is completed...")
                return [command_output, True]
            elif time_counter >= timeout:
                s_log.error("Command execution could not be completed within the timeout specified")
                return [command_output, False]
            else:
                s_log.info("command output is not captured completely , ie no prompt visible...")
                time_counter += retry_timeout
                time.sleep(retry_timeout)
                s_log.info("retrying again...")
                output = conn_obj.execute_command("\n")
                s_log.info("time_counter : {} secs".format(time_counter))
                command_output += output.strip()
                s_log.info(output.strip())

    def verify_join_status(self):
        fname = 'verify_join_status'
        scope = self.args[fname][0]
        join_point = self.args[fname][1]
        expected_status = self.args[fname][2]
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        ad = ActiveDirectory(self.app, s_log)
        retrieved_status = ad.retrieve_join_status(scope, join_point).strip()
        s_log.info("The status retrieved is : {}".format(retrieved_status))
        # retrieved_status = retrieved_status == 'Operational'
        assert expected_status == retrieved_status, "The join status is not as expected. Check the logs above."
        for i in range(0, 3):
            self.args[fname].pop(0)

    def select_ad_and_multiple_group_attributes(self):
        """
        __author__: pakota(17-09-2018)
        This function is useful for selecting AD in non scope mode.
        :return:
        """
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        active_directory = ActiveDirectory(app=self.app, logger=self.logger)
        ad_name = self.args['select_ad_and_multiple_group_attributes'][0]
        group_ad = self.args['select_ad_and_multiple_group_attributes'][1]
        active_directory.navigate_to_page()
        active_directory.select_ad_and_group_attributes(ad_name=ad_name, groups=group_ad)

        for i in range(0, 2):
            self.args['select_ad_and_multiple_group_attributes'].pop(0)

    # pakota-17-09-2018
    def select_multiple_attributes_from_ad_with_no_scope_mode(self):
        """
        __author__: pakota(17-09-2018)
        This function is useful for selecting the AD and retrive 'attributes' by not entering in to the scope mode
        :return:
        """

        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        active_directory = ActiveDirectory(app=self.app, logger=self.logger)
        ad_name = self.args['select_multiple_attributes_from_ad_with_no_scope_mode'][0]
        user_name = self.args['select_multiple_attributes_from_ad_with_no_scope_mode'][1]
        attributes = self.args['select_multiple_attributes_from_ad_with_no_scope_mode'][2]
        active_directory.navigate_to_page()
        time.sleep(2)
        active_directory.select_multi_attributes_from_ad_with_no_scope_mode(ad_name=ad_name, user_name=user_name,
                                                                            attributes=attributes)
        for i in range(0, 3):
            self.args['select_multiple_attributes_from_ad_with_no_scope_mode'].pop(0)

    def edit_protocls_radius_settings(self):

        """
                __author__: ymookkan(19-09-2018)
                This function is useful editing the radius protocol settings in Administration->System->Settings.
                :return:
                """
        from tests.configurations.ise.ui.administration.system.settings.Protocols.RADIUS.radius import Radius
        edit_rad_settings = Radius(self.app, self.logger)
        failure = self.args['edit_protocls_radius_settings'][0]
        rejection_req = self.args['edit_protocls_radius_settings'][1]
        edit_rad_settings.navigate_to_page()
        time.sleep(5)
        try:
            success_msg, alert = edit_rad_settings.edit_rad_settings_suppress(failure=failure,
                                                                              rejection_req=rejection_req)

            if success_msg is None:
                raise Exception("RADIUS Settings not saved - {}".format(alert))
        except Exception as e:
            assert False, "Editing RADIUS Settings  Failed - {0}".format(e)

        for i in range(0, 2):
            self.args['edit_protocls_radius_settings'].pop(0)

    def enable_mschapv1(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowed_protocol = AllowedProtocols(app=self.app, logger=s_log)
        allowed_protocol.navigate_to_page()
        allowed_protocol.default_network_access.click()
        time.sleep(5)
        allowed_protocol.mschap_v1.select()
        time.sleep(5)
        allowed_protocol.save.scroll_to_element()
        allowed_protocol.save.click()
        s_log.info("Saved the changes")
        time.sleep(5)

    def export_policy_locally(self):
        from tests.configurations.ise.ui.administration.system.backup_restore.policy_export import PolicyExport
        encryption_key = self.args['export_policy_locally'][0]
        policy_expo = PolicyExport(self.app, self.logger)
        policy_expo.navigate_to_page()
        time.sleep(5)
        policy_expo.export_policy_to_local_machine(encryption_key)
        time.sleep(30)

        self.args['export_policy_locally'].pop(0)

    @staticmethod
    def copy_and_read_file_from_remote_host(host, username, password, remote_path, local_file_name):
        from utilities.file_handling.ssh_utilities import SSHUtilities
        ssh_con = SSHUtilities(host, username, password)
        file_content = ssh_con.remote_file_copy_to_local(remote_path,
                                                         local_file_name)
        return file_content

    @staticmethod
    def copy_file_from_local_to_remote(host, username, password, local_file_path, remote_file_path):
        """

        to copy a file from docker to remote machine
        :author : nandpara
        :param host: ip of remote machine
        :param username: Username to access the remote machine
        :param password: password for the user
        :param local_file_path: path of the local file that needs to be transfered to remote
        :param remote_file_path: file path of remote machine where the file to be placed/transfered
        :return: None
        """
        from utilities.file_handling.ssh_utilities import SSHUtilities
        ssh_con = SSHUtilities(host, username, password)
        ssh_con.put_file_from_local_to_remote(local_file_path, remote_file_path)
        s_log.info("copied file : {}  to {} ".format(local_file_path, remote_file_path))

    def verify_if_exported_policy_are_in_order(self):
        import re
        from tests.configurations.ise.ui.policy.policy_sets.new_policy_sets import RadPolicySets
        fname = 'verify_if_exported_policy_are_in_order'
        policy_type = self.args[fname][0]
        remote_host = self.args[fname][1]
        user = self.args[fname][2]
        password = self.args[fname][3]
        file_abs_path = self.args[fname][4]
        policy_set_name = self.args[fname][5]
        policy_type_map = {'authorization': 'authorRules',
                           'authentication': 'authenRules'
                           }
        exported_contents = UI_methods.copy_and_read_file_from_remote_host(remote_host,
                                                                           user,
                                                                           password,
                                                                           file_abs_path,
                                                                           'tmp.xml'
                                                                           )
        radius_policy_sets = re.findall('<radiusPolicySet>.*?</radiusPolicySet>',
                                        exported_contents,
                                        re.DOTALL)
        for content in radius_policy_sets:
            if re.search('<name>{}</name>'.format(policy_set_name), content, re.DOTALL) is not None:
                radius_policy_set = content
        xml_list = re.findall('<{0}>.*?<name>(.*?)</name>.*?</{0}>'.format(policy_type_map[policy_type]),
                              radius_policy_set
                              , re.DOTALL)
        xml_list.remove('Default')
        s_log.info("The list of rules read from the XML is:\n{} ".format('\n'.join(xml_list)))
        page = RadPolicySets(self.app, s_log)
        page.navigate_to_page()
        time.sleep(4)
        page.enter_policy_set_view_by_name(policy_set_name)
        time.sleep(4)
        gui_list = page.retrieve_list_of_existing_rules(policy_type, len(xml_list))

        if xml_list == gui_list:
            s_log.info("The elements matched and are in order")
        else:
            assert False, "The elements are not matched, ie they are not in order as expected or values are missing"
        for index in range(6):
            self.args[fname].pop(0)

    # demmanni
    # To retreive multiple attributes fron AD in Scope Mode
    def select_multiple_attributes_from_ad_in_scope_mode(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import \
            ActiveDirectory

        active_directory = ActiveDirectory(app=self.app, logger=self.logger)
        scope_name = self.args['select_multiple_attributes_from_ad_in_scope_mode'][0]
        ad_name = self.args['select_multiple_attributes_from_ad_in_scope_mode'][1]
        user_name = self.args['select_multiple_attributes_from_ad_in_scope_mode'][2]
        attributes = self.args['select_multiple_attributes_from_ad_in_scope_mode'][3]
        active_directory.navigate_to_page()
        time.sleep(2)
        active_directory.select_multi_attributes_from_ad_in_scope_mode(scope_name=scope_name,
                                                                       ad_name=ad_name,
                                                                       user_name=user_name,
                                                                       attributes=attributes)
        for i in range(0, 4):
            self.args['select_multiple_attributes_from_ad_in_scope_mode'].pop(0)

    # demmanni
    # To create Library condition
    def create_library_condition(self):
        from tests.configurations.ise.ui.policy.policy_elements.conditions.library_conditions import \
            LibraryConditions
        fname = 'create_library_condition'
        library_condtion_page = LibraryConditions(self.app, s_log)
        condition_key = self.args[fname][0]
        condition_value = self.args[fname][1]
        condition_attr_value = self.args[fname][2]
        condition_name = self.args[fname][3]
        final_condition_name = self.args[fname][4]
        s_log.info("Navigating to Library Condition Page")
        UI_methods.retry_now(self, library_condtion_page.navigate_to_page)
        library_condtion_page.create_library_conditions(condition_key=condition_key,
                                                        condition_value=condition_value,
                                                        condition_attr_value=condition_attr_value,
                                                        condition_name=condition_name,
                                                        final_condition_name=final_condition_name)
        for i in range(0, 5):
            self.args['create_library_condition'].pop(0)

    # To create Library condition
    def library_condition_with_dict_for_attrvalue(self):
        from tests.configurations.ise.ui.policy.policy_elements.conditions.library_conditions import \
            LibraryConditions
        fname = 'library_condition_with_dict_for_attrvalue'
        library_condtion_page = LibraryConditions(self.app, s_log)
        condition_key = self.args[fname][0]
        condition_value = self.args[fname][1]
        relation = self.args[fname][2]
        condition_attr_value = self.args[fname][3]
        sub_condition = self.args[fname][4]
        condition_name = self.args[fname][5]
        final_condition_name = self.args[fname][6]
        s_log.info("Navigating to Library Condition Page")
        UI_methods.retry_now(self, library_condtion_page.navigate_to_page)
        library_condtion_page.library_condition_with_dict_for_attrvalue(condition_key=condition_key,
                                                                        condition_value=condition_value,
                                                                        relation=relation,
                                                                        condition_attr_value=condition_attr_value,
                                                                        sub_condition=sub_condition,
                                                                        condition_name=condition_name,
                                                                        final_condition_name=final_condition_name)
        for i in range(0, 7):
            self.args[fname].pop(0)

    def create_active_directory_with_any_mode(self):
        """
        Author: Na_Uplift
        Used for creating AD, retrive group/s and retrive attribute/s
        in any mode(Scope Mode/`Non Scope Mode) with all possibilities.
        For usage of the method please verify create_active_directory_any_mode
        pom file
        :return: None
        """
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        activedirectory = ActiveDirectory(self.app, self.logger)

        ad_name = self.args['create_active_directory_with_any_mode'][0]
        domain_name = self.args['create_active_directory_with_any_mode'][1]
        username = self.args['create_active_directory_with_any_mode'][2]
        password = self.args['create_active_directory_with_any_mode'][3]
        scope_mode = self.args['create_active_directory_with_any_mode'][4]
        scope_name = self.args['create_active_directory_with_any_mode'][5]
        group_name = self.args['create_active_directory_with_any_mode'][6]
        attribute_name = self.args['create_active_directory_with_any_mode'][7]
        ad_user = self.args['create_active_directory_with_any_mode'][8]

        confirm_join = True
        if len(self.args['create_active_directory_with_any_mode']) > 9:
            additional_params = self.args['create_active_directory_with_any_mode'][9]
            confirm_join = additional_params.get('confirm_join', confirm_join)

        # Navigate to Active Directory Page
        time.sleep(3)
        activedirectory.navigate_to_page()
        time.sleep(10)

        # Exit Scope mode if it is in the same
        # Exit Scope mode if it is in the same

        if not scope_mode:
            activedirectory.exit_scope_mode()
            time.sleep(5)
            if activedirectory.exit_scope.is_displayed():
                s_log.error("##############  The Scope Mode is not Exited  ##############")
                assert False, "##############  The Scope Mode is not Exited  ##############"

            else:
                s_log.info("##############  Verified if the Scope mode is exited ##############  ")

        # Check if the AD is existing already , if so delete the same
        try:
            activedirectory.delete_active_directory(ad_name=ad_name)
        except:
            s_log.info("ISE instance given does not exist.")

        # Add Active Directory based on the input passed
        activedirectory.create_active_directory_any_mode(ad_name=ad_name, domain_name=domain_name,
                                                         username=username, password=password,
                                                         scope_mode=scope_mode, scope_name=scope_name,
                                                         group_name=group_name,
                                                         attribute_name=attribute_name, ad_user=ad_user,
                                                         confirm_join=confirm_join)

        # Pop out objects
        for i in range(len(self.args['create_active_directory_with_any_mode'])):
            self.args['create_active_directory_with_any_mode'].pop(0)

    def enable_eap_tls_session_resume(self):

        from tests.configurations.ise.ui.administration.system.settings.EAP_TLS import \
            EAP_TLS
        eap_tls = EAP_TLS(app=self.app, logger=None)
        time.sleep(3)
        eap_tls.navigate_to_page()
        time.sleep(4)
        session_resume = self.args['enable_eap_tls_session_resume']
        eap_tls.enabling_eap_tls_session_resume(session_resume=session_resume)

        for i in range(0, 1):
            self.args['enable_eap_tls_session_resume'].pop(0)

    def enable_eap_fast_pacless_session_resume(self):

        from tests.configurations.ise.ui.administration.system.settings.EAP_FAST import \
            EAP_FAST
        eap_fast = EAP_FAST(app=self.app, logger=None)
        time.sleep(3)
        eap_fast.navigate_to_page()
        time.sleep(4)
        session_resume = self.args['enable_eap_fast_pacless_session_resume']
        eap_fast.enabling_pacless_session_resume(session_resume=session_resume)

        for i in range(0, 1):
            self.args['enable_eap_fast_pacless_session_resume'].pop(0)

    def enable_eap_tls_with_session_resume(self):

        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowed = AllowedProtocols(app=self.app, logger=None)
        eap_tls = self.args['enable_eap_tls_with_session_resume'][0]
        eap_tls_session_resume = self.args['enable_eap_tls_with_session_resume'][1]

        time.sleep(3)
        allowed.navigate_to_page()
        time.sleep(4)
        allowed.default_network_access.click()
        allowed.enable_allow_eap_tls_inner_methods(eap_tls=eap_tls, eap_tls_session_resume=eap_tls_session_resume)
        allowed.save.click()
        self.logger.info("Saved the changes")
        for i in range(0, 2):
            self.args['enable_eap_tls_with_session_resume'].pop(0)

    def enable_eap_fast_with_inner_method_eap_tls_only(self):

        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowed = AllowedProtocols(app=self.app, logger=None)
        eap_tls_auth_check = self.args['enable_eap_fast_with_inner_method_eap_tls_only'][0]

        time.sleep(3)
        allowed.navigate_to_page()
        time.sleep(4)
        allowed.default_network_access.click()
        allowed.configure_eap_fast_protocol(eap_tls_auth_check=eap_tls_auth_check)
        allowed.save.click()
        self.logger.info("Saved the changes")
        for i in range(0, 1):
            self.args['enable_eap_fast_with_inner_method_eap_tls_only'].pop(0)

    def use_pac_eap_fast(self):

        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowed = AllowedProtocols(app=self.app, logger=None)
        tunnel_pac_time_to_live = self.args['use_pac_eap_fast'][0]
        tunnel_pac_time_to_live_format = self.args['use_pac_eap_fast'][1]
        proactive_pac_update_percentage = self.args['use_pac_eap_fast'][2]
        eap_tls_require_client_check = self.args['use_pac_eap_fast'][3]
        eap_fast_pac_auth_pac_ttl = self.args['use_pac_eap_fast'][4]
        eap_fast_pac_auth_pac_ttl_units = self.args['use_pac_eap_fast'][5]
        time.sleep(3)
        allowed.navigate_to_page()
        time.sleep(4)
        allowed.default_network_access.click()
        time.sleep(5)
        allowed.use_pac_eap_fast(tunnel_pac_time_to_live=tunnel_pac_time_to_live,
                                 tunnel_pac_time_to_live_format=tunnel_pac_time_to_live_format,
                                 proactive_pac_update_percentage=proactive_pac_update_percentage,
                                 eap_tls_require_client_check=eap_tls_require_client_check,
                                 eap_fast_pac_auth_pac_ttl=eap_fast_pac_auth_pac_ttl,
                                 eap_fast_pac_auth_pac_ttl_units=eap_fast_pac_auth_pac_ttl_units)
        allowed.save.click()
        self.logger.info("Saved the changes")
        for i in range(0, 6):
            self.args['use_pac_eap_fast'].pop(0)

    def disable_basic_rule_status(self):
        policySetsPage = RadPolicySets(self.app, self.logger)
        policySetsPage.navigate_to_policy_set_page()
        status = self.args["disable_basic_rule_status"][0]
        policySetsPage.change_basic_atuhenticated_rule_status(status=status)
        for i in range(0, 1):
            self.args['disable_basic_rule_status'].pop(0)

    ##adevudug##
    def create_identity_source_sequence(self):

        from tests.configurations.ise.ui.administration.identity_management.identity_source_sequences import \
            IdentitySourceSequences
        fname = 'create_identity_source_sequence'
        sequence = IdentitySourceSequences(app=self.app, logger=s_log)
        identity_sequence = self.args[fname][0]
        identity_source_list = self.args[fname][1]
        sequence.navigate_to_page()

        # Check if the AD is existing already , if so delete the same
        try:
            sequence.delete_identity_sequence(identity_sequence=identity_sequence)
        except:
            s_log.info("Identity Sequence given does not exist.")

        connection_msg, connection_alert = sequence.add_identity_sequence(identity_sequence=identity_sequence,
                                                                          identity_source_list=identity_source_list)

        # Verify the Identity Source Sequence is added
        if connection_msg is None:
            assert False, "********* Identity Source Sequence is not added successfully - ****".format(
                connection_alert)
        else:
            s_log.info("********* Identity Source Sequence is added successfully ****")
            s_log.info("********* Server response : {}".format(connection_msg))
        time.sleep(10)

        for i in range(0, 2):
            self.args[fname].pop(0)

    ##adevudug###
    def delete_identity_source_sequence(self):
        from tests.configurations.ise.ui.administration.identity_management.identity_source_sequences import \
            IdentitySourceSequences
        fname = 'delete_identity_source_sequence'
        sequence = IdentitySourceSequences(app=self.app, logger=s_log)
        identity_sequence = self.args[fname][0]
        sequence.navigate_to_page()
        sequence.delete_identity_sequence(identity_sequence=identity_sequence)

        for i in range(0, 1):
            self.args[fname].pop(0)

    # ---------- sxp related functions ------------

    def enable_only_sxp_service(self):
        """
        Edited : nandpara
        Function to enable the sxp service for given persona
        Note : considered only for standalone machine
        :return:
        """
        from tests.configurations.ise.ui.administration.system.deployment import Deployment
        deployment_page = Deployment(self.app, self.logger)
        fname = "enable_only_sxp_service"
        persona = self.args[fname][0]
        deployment_page.navigate_to_page()
        time.sleep(3)
        s_log.info("Checking if sxp service is enabled for {}".format(persona))
        deployment_page.select_node_from_table(persona)
        time.sleep(3)
        deployment_page.edit_button.click()
        time.sleep(3)
        deployment_page.wait_for_loader([deployment_page.sxp_service_checkbox])
        deployment_page.sxp_service_checkbox.scroll_to_element()
        time.sleep(3)
        if not deployment_page.sxp_service_checkbox.check_selected:
            s_log.info("Sxp service is not enabled for {} hence Enabling it...".format(persona))
            deployment_page.sxp_service_checkbox.click()
            time.sleep(2)
            deployment_page.save_button.click()
            deployment_page.fail_if_no_success_response_and_log_alert()
            deployment_page.wait_for_loader([deployment_page.edit_node_popup], timeout=180)
        else:
            s_log.info("sxp service is already enabled for {}".format(persona))

        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=1)

    def sxp_add_domain_name(self):
        """creating new domain name in SXP device
             :param domain_name: name of the domain. Can be a list or a string
             :return:
        """
        from tests.configurations.ise.ui.workcenters.trustsec.sxp import sxp_devices
        sxpDevicesPage = sxp_devices.SxpDevices(self.app, self.logger)
        domainName = self.args['sxp_add_domain_name'][0]
        sxpDevicesPage.navigate_to_page()
        if sxpDevicesPage.popup_ok_button.wait_for_element(20):
            sxpDevicesPage.popup_ok_button.click()
        sxpDevicesPage.create_sxp_domain(domain_name=domainName)
        time.sleep(5)
        for i in range(0, 1):
            self.args['sxp_add_domain_name'].pop(0)

    def change_global_password(self):
        """
        Author : nandpara
        changes the global (alias default ) password for the Sxp devices
        :param:global_password: new password which need to be changed to
        """
        from tests.configurations.ise.ui.workcenters.trustsec.settings.sxp_settings import SxpSettings
        fname = 'change_global_password'
        global_password = self.args[fname][0]
        sxpsettingspage = SxpSettings(self.app, s_log)
        sxpsettingspage.navigate_to_page()
        sxpsettingspage.change_global_password(global_password)
        time.sleep(2)
        for i in range(0, 1):
            self.args['change_global_password'].pop(0)

    def add_sxp_device_with_custom_attributes(self):
        """
        Author : nandpara
        Adds a new sxp Device with custom attributes
        :param name: new sxp device name
        :param ip_address: new sxp device ip address
        :param peer_role: new peer role for sxp device , can be 'SPEAKER', 'LISTENER'
        :param psns: new psns for sxp device
        :param sxp_domain: new domain for sxp device
        :param status: new status for sxp device, can be 'Enabled', 'Disabled'
        :param password_type: new password type , can be 'DEFAULT', 'NONE', 'CUSTOM'
        :param password: new password if password type is 'CUSTOM'
        :param version: new version for sxp device , can be 'V1','V2','V3','V4'
        :param new_attrs is a dict of above key:pair of required values
            example: {'version':'V4', 'domain':'tokyo'}
        """
        from tests.configurations.ise.ui.workcenters.trustsec.sxp.sxp_devices import SxpDevices
        fname = 'add_sxp_device_with_custom_attributes'
        default = {'name': None,
                   'ip_address': None,
                   'peer_role': None,
                   'psns': None,
                   'sxp_domain': None,
                   'status': None,
                   'password_type': None,
                   'password': None,
                   'version': None
                   }
        new_attrs = self.args[fname][0]
        for key, value in new_attrs.items():
            default[key] = value
        sxp_devices_page = SxpDevices(self.app, self.logger)
        s_log.info("Adding a New SXP device...")
        sxp_devices_page.navigate_to_page()
        time.sleep(5)
        sxp_devices_page.add_sxp_device(name_text=default['name'],
                                        ip_address=default['ip_address'],
                                        peer_role=default['peer_role'],
                                        psn=default['psns'],
                                        domain_name=default['sxp_domain'],
                                        status=default['status'],
                                        password_type=default['password_type'],
                                        custom_password=default['password'],
                                        version=default['version'])

        time.sleep(10)
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=1)

    def edit_sxp_device_attributes(self):
        """
        Author : nandpara
        edits attributes of already added sxp device
        :param filter_ip: ip of sxp device for which edit is required
        :param name: new sxp device name
        :param ip_address: new sxp device ip address
        :param peer_role: new peer role for sxp device , can be 'SPEAKER', 'LISTENER'
        :param psns: new psns for sxp device
        :param sxp_domain: new domain for sxp device
        :param status: new status for sxp device
        :param password_type: new password type , can be 'DEFAULT', 'NONE', 'CUSTOM'
        :param password: new password if password type is 'CUSTOM'
        :param version: new version for sxp device , can be 'V1','V2','V3','V4'
        :param new_attrs is a dict of above key:pair of required values
            example: {'version':'V4', 'domain':'tokyo'}
        """
        from tests.configurations.ise.ui.workcenters.trustsec.sxp.sxp_devices import SxpDevices
        fname = 'edit_sxp_device_attributes'
        default = {'filter_ip': None,
                   'name': None,
                   'ip_address': None,
                   'peer_role': None,
                   'psns': None,
                   'sxp_domain': None,
                   'status': None,
                   'password_type': None,
                   'password': None,
                   'version': None
                   }
        new_attrs = self.args[fname][0]
        for key, value in new_attrs.items():
            default[key] = value
        sxp_devices_page = SxpDevices(self.app, self.logger)
        s_log.info("Editing SXP device...")
        sxp_devices_page.navigate_to_page()
        time.sleep(5)
        sxp_devices_page.edit_device_attributes(ip=default['filter_ip'],
                                                name=default['name'],
                                                ip_address=default['ip_address'],
                                                peer_role=default['peer_role'],
                                                psns=default['psns'],
                                                sxp_domain=default['sxp_domain'],
                                                status=default['status'],
                                                password_type=default['password_type'],
                                                password=default['password'],
                                                version=default['version'])
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=1)

    def delete_sxp_device(self):
        """
        Author : jayaprsu
        deletes the sxp device based on its name

        :param: name_of_the_sxp_device : name of the sxp device that needs to be deleted

        """
        from tests.configurations.ise.ui.workcenters.trustsec.sxp import sxp_devices
        fname = 'delete_sxp_device'
        sxpDevicepage = sxp_devices.SxpDevices(self.app, self.logger)
        name_of_the_sxp_device = self.args[fname][0]
        wait_for_success_pop_up = self.args[fname][1]

        sxpDevicepage.navigate_to_page()
        time.sleep(3)
        sxpDevicepage.delete_particular_sxp_device(name_of_the_sxp_device=name_of_the_sxp_device,
                                                   wait_for_success_pop_up=wait_for_success_pop_up)
        time.sleep(2)
        for i in range(0, 2):
            self.args['delete_sxp_device'].pop(0)

    def create_ip_sgt_static_mapping(self):
        """
        This function is useful for adding ise ip for sgt mapping.
        :param ip_address: ip address of the ise machine
        :param sgt: sgt group type. i.e:Employee group or guest etc...
        :param device_name: device type
        :param sxp_domain: name of the domain
        :return:
        """
        from tests.configurations.ise.ui.workcenters.trustsec.components.ip_sgt_static_mapping import \
            ip_sgt_static_mapping
        ip_mapping = ip_sgt_static_mapping(self.app, self.logger)

        ip_address = self.args['create_ip_sgt_static_mapping'][0]
        sgt = self.args['create_ip_sgt_static_mapping'][1]
        device_name = self.args['create_ip_sgt_static_mapping'][2]
        sxp_domain = self.args['create_ip_sgt_static_mapping'][3]
        time.sleep(5)
        ip_mapping.navigate_to_page()
        time.sleep(5)
        ip_mapping.add_ip_sgt_static_mapping(ip=ip_address, sgt=sgt, device_name=device_name, sxp_domain=sxp_domain)
        time.sleep(2)
        for i in range(0, 4):
            self.args['create_ip_sgt_static_mapping'].pop(0)

    def verify_all_sxp_mapping_attributes(self):
        """
        Author : nandpara
        verifies the all_sxp_mapping attributes for a given ip

        :param: ip_address_value : ip address of the device for which the attributes needs to be verified
        :param: expected_values : dict of expected attributes, note: you can skip any key:pair yet the
                function shall work
            ex: expected_values = {'ip':'','sgt':'','learned_from':'','learned_by':'',
                                         'sxp_domain':'','pns_involved':'',}
        :return: verifies the expeted_values dict with actual values dict and fails the testcase if it does not match
        """
        from tests.configurations.ise.ui.workcenters.trustsec.sxp.all_sxp_mappings import AllSxpMappings
        fname = 'verify_all_sxp_mapping_attributes'
        ip_address_value = self.args[fname][0]
        expected_values = self.args[fname][1]

        all_sxp_mappings_page = AllSxpMappings(self.app, s_log)
        all_sxp_mappings_page.navigate_to_page()
        time.sleep(4)
        actual_values = all_sxp_mappings_page.get_all_sgt_mapping_attributes_for_given_ip(
            ip_address_value=ip_address_value)
        s_log.info("Retrieved values: {}\n".format(actual_values))
        s_log.info("Expected values: {}\n".format(expected_values))
        for key, value in expected_values.items():
            if actual_values[key] == value:
                s_log.info("{} value retrieved matches expected value of {}".format(key, value))
            else:
                s_log.info("{} value retrieved does not match expected value of {}".format(key, value))
                assert False, "{} value retrieved does not match expected value of {}".format(key, value)
        time.sleep(2)
        for i in range(0, 2):
            self.args[fname].pop(0)

    def verify_sxp_device_attributes(self):
        """
        Author : nandpara
        verifies the all_sxp_mapping attributes for a given ip

        :param: ip_address_value : ip address of the device for which the attributes needs to be verified
        :param: expected_values : dict of expected attributes , note: you can skip any key:pair yet the
                function shall work
            ex: expected_values = {'name':'','ip':'','status':'','peer_role':'',
                                         'password_type':'','negotiated_version':'','sxp_version': '',
                                      'connected_to': '','duration': '','sxp_domain': ''}
        :return: verifies the expeted_values dict with actual values dict and fails the testcase if it does not match
        """

        from tests.configurations.ise.ui.workcenters.trustsec.sxp.sxp_devices import SxpDevices
        fname = 'verify_sxp_device_attributes'
        ip_address_value = self.args[fname][0]
        expected_values = self.args[fname][1]

        sxp_device_page = SxpDevices(self.app, s_log)
        # Sleep time for the connection to be established
        time.sleep(120)
        sxp_device_page.navigate_to_page()
        time.sleep(4)
        actual_values = sxp_device_page.get_sxp_device_attributes_for_given_ip(ip_address_value=ip_address_value)
        print(actual_values)
        for key, value in expected_values.items():
            if actual_values[key] == value:
                s_log.info("{} value matches {}".format(key, value))
            else:
                s_log.info("{} value doesnot match {}".format(key, value))
                assert False, "{} does not match {}".format(key, value)
        time.sleep(2)
        for i in range(0, 2):
            self.args['verify_sxp_device_attributes'].pop(0)

    def verify_sgt_mapping_attributes(self):
        """
        Author : nandpara
        verifies the all_sxp_mapping attributes for a given ip

        :param: ip_address_value : ip address of the device for which the attributes needs to be verified
        :param: expected_values : dict of expected attributes , note: you can skip any key:pair yet the
                function shall work
            ex: expected_values = {'ip':'', 'sgt_value':'','mapping_group':'','deploy_via':'','deploy_to':''}
        :return: verifies the expeted_values dict with actual values dict and fails the testcase if it does not match
        """

        from tests.configurations.ise.ui.workcenters.trustsec.components.ip_sgt_static_mapping import \
            ip_sgt_static_mapping
        sgt_mapping_page = ip_sgt_static_mapping(self.app, self.logger)
        fname = 'verify_sgt_mapping_attributes'
        ip_address_value = self.args[fname][0]
        expected_values = self.args[fname][1]

        sgt_mapping_page.navigate_to_page()
        time.sleep(4)
        actual_values = sgt_mapping_page.get_sgt_mapping_attributes(ip_address_value=ip_address_value)
        print(actual_values)
        for key, value in expected_values.items():
            if actual_values[key] == value:
                s_log.info("{} value matches {}".format(key, value))
            else:
                s_log.info("{} value doesnot match {}".format(key, value))
                assert False, "{} does not match {}".format(key, value)
        time.sleep(2)
        for i in range(0, 2):
            self.args['verify_sgt_mapping_attributes'].pop(0)

    # ---------- sxp related functions ------------

    ##adevudug##
    def create_identity_source_sequence(self):
        from tests.configurations.ise.ui.administration.identity_management.identity_source_sequences import \
            IdentitySourceSequences
        fname = 'create_identity_source_sequence'
        sequence = IdentitySourceSequences(app=self.app, logger=s_log)
        identity_sequence = self.args[fname][0]
        identity_source_list = self.args[fname][1]
        sequence.navigate_to_page()
        sequence.add_identity_sequence(identity_sequence=identity_sequence,
                                       identity_source_list=identity_source_list)

        for i in range(0, 2):
            self.args[fname].pop(0)

    ##adevudug###
    def delete_identity_source_sequence(self):
        from tests.configurations.ise.ui.administration.identity_management.identity_source_sequences import \
            IdentitySourceSequences
        fname = 'delete_identity_source_sequence'
        sequence = IdentitySourceSequences(app=self.app, logger=s_log)
        identity_sequence = self.args[fname][0]
        sequence.navigate_to_page()
        sequence.delete_identity_sequence(identity_sequence=identity_sequence)

        for i in range(0, 1):
            self.args[fname].pop(0)

    def delete_or_add_mult_domain_in_ip_sgt_mapping(self):
        """
        __author: narendk2
        :param mapped_ip: already mapped ip
        :param domain_for_delete: List of domain to delete
        :param domain_for_add: List of domain to add
        :return:
        """
        from tests.configurations.ise.ui.workcenters.trustsec.components.ip_sgt_static_mapping import \
            ip_sgt_static_mapping
        sgt_mapping_page = ip_sgt_static_mapping(self.app, self.logger)
        fname = 'delete_or_add_mult_domain_in_ip_sgt_mapping'
        mapped_ip = self.args[fname][0]
        domain_for_delete = self.args[fname][1]
        domain_for_add = self.args[fname][2]
        sgt_mapping_page.navigate_to_page()
        time.sleep(5)
        sgt_mapping_page.edit_ip_sgt_mapping_domain(ip=mapped_ip,
                                                    delete_domains=domain_for_delete,
                                                    add_domains=domain_for_add)
        for i in range(0, 3):
            self.args['delete_or_add_mult_domain_in_ip_sgt_mapping'].pop(0)

    def new_allowed_protocol(self):
        ed_pro = AllowedProtocols(app=self.app, logger=self.logger)
        fname = 'new_allowed_protocol'
        ad_name = self.args['new_allowed_protocol'][0]
        # condition = self.args['edit_default_allowed_protocols'][1]
        # pass_cond =  self.args['edit_default_allowed_protocols'][2]
        ed_pro.navigate_to_page()
        time.sleep(2)
        ed_pro.configure_outer_allowed_protocol(name=ad_name)
        ed_pro.save.javascript_click()
        for i in range(0, 1):
            self.args[fname].pop(0)

    def delete_sxp_custom_domain_name(self):
        """
        __author: sadrajan
        deleting new domain name in SXP device
             :param domain_name: name of the domain
             :return:
        """
        from tests.configurations.ise.ui.workcenters.trustsec.sxp import sxp_devices
        sxpDevicesPage = sxp_devices.SxpDevices(self.app, self.logger)
        fname = 'delete_sxp_custom_domain_name'
        domainName = self.args[fname][0]
        time.sleep(3)
        sxpDevicesPage.navigate_to_page()
        time.sleep(3)
        sxpDevicesPage.delete_sxp_domain_name(domain_name=domainName)
        # for i in range(0, 1):
        self.args[fname].pop(0)

    def edit_default_allowed_protocols(self):
        ed_pro = AllowedProtocols(app=self.app, logger=self.logger)
        ad_name = self.args['edit_default_allowed_protocols'][0]
        condition = self.args['edit_default_allowed_protocols'][1]
        # pass_cond =  self.args['edit_default_allowed_protocols'][2]
        ed_pro.navigate_to_page()
        time.sleep(2)
        ed_pro.edit_protocol_by_name(policy_name=ad_name, process_host_lookup=condition, pap_ascii=condition,
                                     auth_chap=condition, mschapv1=condition, eap_md5=condition)

        ed_pro.enable_allow_eap_tls_inner_methods(eap_tls=condition)
        time.sleep(5)
        ed_pro.enable_peap_inner_methods(allow_peap=condition)
        time.sleep(5)
        ed_pro.configure_eap_fast_protocol(eap_fast1=condition)
        ed_pro.use_pac_ttls(eap_ttls=condition)
        time.sleep(10)
        ed_pro.save.javascript_click()
        s_log.info("Protocol Saved Successfully")
        for i in range(0, 2):
            self.args['edit_default_allowed_protocols'].pop(0)

    def check_protocol_status(self):
        ed_pro = AllowedProtocols(app=self.app, logger=self.logger)
        ad_name = self.args['check_protocol_status'][0]
        time.sleep(5)
        ed_pro.navigate_to_page()
        time.sleep(2)
        ed_pro.verification_allowed_protocols_default(policy_name=ad_name)
        for i in range(0, 1):
            self.args['check_protocol_status'].pop(0)

    def enable_eap_chaining_machine_authentication(self):
        ad_pro = AllowedProtocols(app=self.app, logger=self.logger)
        ad_pro.navigate_to_page()
        time.sleep(2)
        name = self.args['enable_eap_chaining_machine_authentication'][0]
        chaining = self.args['enable_eap_chaining_machine_authentication'][1]
        ad_pro.edit_protocol_by_name(policy_name=name)
        ad_pro.configure_eap_fast_protocol(eap_fast_enable_chaining_checkbox=chaining)
        ad_pro.save.javascript_click()

    def reset_default_allowed_protocols(self):
        ed_pro = AllowedProtocols(app=self.app, logger=self.logger)
        ad_name = self.args['reset_default_allowed_protocols'][0]
        condition = self.args['reset_default_allowed_protocols'][1]
        ed_pro.navigate_to_page()
        time.sleep(2)
        ed_pro.edit_protocol_by_name(policy_name=ad_name, eap_md5=condition, pap_ascii=condition,
                                     auth_chap=condition)
        ed_pro.configure_eap_fast_protocol(name=ad_name, eap_fast1=condition
                                           )
        ed_pro.enable_peap_inner_methods(name=ad_name, allow_peap=condition)
        ed_pro.save.javascript_click()
        for i in range(0, 2):
            self.args['reset_default_allowed_protocols'].pop(0)

    def networkDevices_setDefaultDevice_tacacs(self):
        from tests.configurations.ise.ui.administration.network_resources.network_device import NetworkDevice
        networkDevicePage = NetworkDevice(self.app, self.logger)

        networkDeviceSecret = self.args['networkDevices_setDefaultDevice_tacacs'][0]

        networkDevicePage.navigate_to_page()
        time.sleep(10)
        networkDevicePage.enable_tacacs_on_default_device(networkDeviceSecret)
        time.sleep(10)

        self.args['networkDevices_setDefaultDevice_tacacs'].pop(0)

    def fips_mode_enabling_and_disabling(self):
        from tests.configurations.ise.ui.administration.system.settings.fips_mode import FipsMode
        fips_setup = FipsMode(self.app, self.logger)
        fips_setup.navigate_to_page()
        time.sleep(10)
        fips_mode = self.args['fips_mode_enabling_and_disabling'][0]
        fips_setup.fips_enable_elem(elem=fips_mode)
        for i in range(0, 1):
            self.args['fips_mode_enabling_and_disabling'].pop(0)

    def delete_ip_sgt_static_mapping(self):
        """
         __author: sadrajan
        deletes ip SGT static mapping
        """
        from tests.configurations.ise.ui.workcenters.trustsec.components.ip_sgt_static_mapping import \
            ip_sgt_static_mapping
        ip_mapping = ip_sgt_static_mapping(self.app, self.logger)
        time.sleep(3)
        ip_mapping.navigate_to_page()
        time.sleep(3)
        ip_mapping.delete_all_mapping()
        time.sleep(3)

    @staticmethod
    def delete_from_selenium_client(ip, user, password, command):
        from utilities.file_handling.ssh_utilities import SSHUtilities
        ssh_conn = SSHUtilities(ip, user, password)
        ssh_conn.remote_execute_command(command, print_result=True)
        del ssh_conn

    def delete_all_policy_sets(self):
        policy_page = RadPolicySets(app=self.app, logger=s_log)
        policy_page.navigate_to_page()
        s_log.info(policy_page.delete_all_new_policy_sets())

    @staticmethod
    def retry_now(obj, func):
        retry_attempt = 3
        while retry_attempt > 0:
            obj.logger.info("Attempt Number: {}".format(retry_attempt))
            try:
                func()
                obj.logger.info("Function execution successful")
                return
            except Exception as e:
                obj.logger.error("Unable to navigate to the page. {}".format(e))
                retry_attempt -= 1
        assert False, "Function failed. Retry attempts exhausted. Check above logs for troubleshooting"

    def delete_library_conditions_with_prefix(self):
        """
        __author__: narendk2
        :prefix_condition_name : Prefix name for conditions
        :return: Name of belonging conditions
        """
        fname = 'delete_library_conditions_with_prefix'
        condition_list = []
        prefix = self.args[fname][0]
        library_condition_page = LibraryConditions(self.app, s_log)
        UI_methods.retry_now(self, library_condition_page.navigate_to_page)
        time.sleep(10)
        s_log.info(library_condition_page.delete_conditions_by_prefix(prefix))

        for i in range(0, 1):
            self.args[fname].pop(0)

    def enable_allowed_protocol_eap_fast_inner_method_eaptls_only(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowedprotocols = AllowedProtocols(self.app, self.logger)
        allowedprotocols.navigate_to_page()
        allowedprotocols.eap_fast_tls_client_cert()
        time.sleep(2)

    def disable_allowed_protocol_eap_fast_inner_method_eaptls_only(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowedprotocols = AllowedProtocols(self.app, self.logger)
        allowedprotocols.navigate_to_page()
        allowedprotocols.delete_eap_fast_tls_client_cert()
        time.sleep(2)

    def remove_all_identity_source_from_sequence(self):
        from tests.configurations.ise.ui.administration.identity_management.identity_source_sequences import \
            IdentitySourceSequences
        fname = 'remove_all_identity_source_from_sequence'
        sequence_item = self.args[fname][0]
        exception_source_list = self.args[fname][1]
        if exception_source_list is 'default':
            exception_list = ['Internal Users',
                              'All_AD_Join_Points',
                              'Guest Users']
        else:
            exception_list = exception_source_list
        sequence = IdentitySourceSequences(app=self.app, logger=s_log)
        sequence.deselect_all_idenity_sources(sequence_item, exception_list)
        for i in range(2):
            self.args[fname].pop(0)

    def rejected_ep_report_search(self):
        fname = "rejected_ep_report_search"
        from tests.configurations.ise.ui.operations.operations_reports.reports.endpointsandusers.rejected_endpoints import \
            RejectedEndpoints
        rejected_ep = RejectedEndpoints(self.app, s_log)
        rejected_ep.navigate_to_page()
        time.sleep(10)
        mac_id = self.args[fname][0]
        server = self.args[fname][1]
        status = self.args[fname][2]
        report = rejected_ep.get_endpoint_details(mac=mac_id)
        if type(report) == dict:
            if report['Server'] != server or report['Status'] != status:
                self.failed(
                    "Expected value are {},{}, but returned values are {},{}".format(status, server, report['Server'],
                                                                                     report['Status']))
            else:
                s_log.info('Expected values are present in Rejected endpoints page')
        elif type(report) == str:
            self.failed("{}".format(report))

        for i in range(3):
            self.args[fname].pop(0)

    def reset_radius_settings_to_default(self):
        from tests.configurations.ise.ui.administration.system.settings.Protocols.RADIUS.radius import Radius
        radius_page = Radius(self.app, self.logger)
        radius_page.navigate_to_page()
        time.sleep(10)
        radius_page.reset_to_defaults_button_click()
        time.sleep(2)
        radius_page.yes_reset_to_default_button.click()
        time.sleep(3)
        radius_page.save_button.javascript_click()

    def release_rejected_endpoint(self):
        from tests.configurations.ise.ui.context_visibility.endpoints import Endpoints
        ep_page = Endpoints(self.app, self.logger)
        ep_page.navigate_to_page()
        time.sleep(10)
        mac_id = self.args['release_rejected_endpoint'][0]
        ep_page.release_rejected_endpoint(mac_address=mac_id)

    # -----------------------syslog_related-----------------------

    def add_remote_syslog_target(self):
        from tests.suites.interface_testing.UI.remote_syslog import RemoteLoggingTargets
        fname = 'add_remote_syslog_target'
        default = {
            'name': None,
            'host': None,
            'port': None,
            'type': None,
            'buffer_on': None,
            'ca_name': None,
            'buffer_size': None,
            'reconnect_time': None,
        }
        new_attrs = self.args[fname][0]
        for key, value in new_attrs.items():
            default[key] = value
        remote_logging_page = RemoteLoggingTargets(self.app, s_log)
        remote_logging_page.navigate_to_page()
        if remote_logging_page.check_syslog_exists(syslog_name=default['name']):
            s_log.info("Already syslog target with name : {} exists".format(default['name']))
            time.sleep(3)
            s_log.info("Deleting syslog Target {}".format(default['name']))
            remote_logging_page.delete_remote_syslog(syslog_name=default['name'])
            time.sleep(4)
        s_log.info("Adding Remote Syslog Target...")
        success_msg, alert_msg = remote_logging_page.add_remote_syslog(name=default['name'],
                                                                       host=default['host'],
                                                                       port=default['port'],
                                                                       type=default['type'],
                                                                       buffer_on=default['buffer_on'],
                                                                       ca_name=default['ca_name'],
                                                                       buffer_size=default['buffer_size'],
                                                                       reconnect_time=default['reconnect_time'],
                                                                       )
        if success_msg is not None:
            s_log.info('Message text: ' + success_msg)
        else:
            if alert_msg:
                s_log.info("Alert text: {}".format(alert_msg))
            assert False, "add action could not be saved."

        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=1)

    def verify_syslog_target_added_successfully(self):
        from tests.suites.interface_testing.UI.remote_syslog import RemoteLoggingTargets
        remote_logging_page = RemoteLoggingTargets(self.app, s_log)
        remote_target_name = self.args['verify_syslog_target_added_successfully'][0]
        time.sleep(5)
        remote_logging_page.navigate_to_page()
        time.sleep(5)
        assert remote_logging_page.check_syslog_exists(
            remote_target_name), "{} remote syslog target not presented".format(remote_target_name)
        s_log.info("{} remote target added succuessfully".format(remote_target_name))

        for i in range(0, 1):
            self.args['verify_syslog_target_added_successfully'].pop(0)

    def edit_syslog_target_parameters(self):
        from tests.suites.interface_testing.UI.remote_syslog import RemoteLoggingTargets
        fname = 'edit_syslog_target_parameters'
        default = {
            'syslog_name': None,
            'new_port': None,
            'buffer_on': None,
            'buffer_size': None,
            'reconnect_time': None,
        }
        new_attrs = self.args[fname][0]
        for key, value in new_attrs.items():
            default[key] = value
        remote_logging_page = RemoteLoggingTargets(self.app, s_log)
        remote_logging_page.navigate_to_page()
        time.sleep(3)
        s_log.info("Editing Remote Syslog Target...")
        success_msg, alert_msg = remote_logging_page.edit_remote_target(syslog_name=default['syslog_name'],
                                                                        new_port=default['new_port'],
                                                                        buffer_on=default['buffer_on'],
                                                                        buffer_size=default['buffer_size'],
                                                                        reconnect_time=default['reconnect_time'],
                                                                        )
        if success_msg is not None:
            s_log.info('Message text: ' + success_msg)
        else:
            if alert_msg:
                s_log.info("Alert text: {}".format(alert_msg))
            assert False, "Edit action could not be saved."
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=1)

    def delete_remote_syslog_target(self):
        from tests.suites.interface_testing.UI.remote_syslog import RemoteLoggingTargets
        fname = 'delete_remote_syslog_target'
        syslog_target_names = self.args[fname][0]
        remote_logging_page = RemoteLoggingTargets(self.app, s_log)
        remote_logging_page.navigate_to_page()
        time.sleep(2)
        for syslog_target_name in syslog_target_names:
            s_log.info("Deleting syslog Target: {}".format(syslog_target_name))
            success_msg, alert_msg = remote_logging_page.delete_remote_syslog(syslog_name=syslog_target_name)
            if success_msg is not None:
                s_log.info('Message text: ' + success_msg)
            else:
                if alert_msg:
                    s_log.info("Alert text: {}".format(alert_msg))
                assert False, "Delete action could not be saved."
            time.sleep(2)
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=1)

    def add_syslog_targets_to_log_categories(self):
        from tests.configurations.ise.ui.administration.system.logging.logging_categories import Logging_Categories
        fname = 'add_syslog_targets_to_log_categories'
        syslog_target_name = self.args[fname][0]
        log_categories_list = self.args[fname][1]
        enable_local_log = self.args[fname][2]
        log_category_page = Logging_Categories(self.app, s_log)
        for log_category in log_categories_list:

            log_category_page.navigate_to_page()
            s_log.info("Adding syslog target: {} to category: {} ".format(syslog_target_name, log_category))
            time.sleep(10)
            success_msg, alert_msg = log_category_page.define_syslog_in_category(syslog_name=syslog_target_name,
                                                                                 category_name=log_category,
                                                                                 enable_local_log=enable_local_log)
            if success_msg is not None:
                s_log.info('Message text: ' + success_msg)
            else:
                if alert_msg:
                    s_log.info("Alert text: {}".format(alert_msg))
                assert False, "Add syslog targets to log categories not saved"
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=3)

    @staticmethod
    def get_syslog_dianostic_report(tc_obb, row_number):
        from tests.configurations.ise.ui.operations.operations_reports.reports.diagnostics.system_diagnostic \
            import System_Diagnostics
        sys_diag_obj = System_Diagnostics(tc_obb.app, s_log)
        sys_diag_obj.navigate_to_page()
        entry = sys_diag_obj.get_system_diagnostic_row_value(row_number)
        row_count = sys_diag_obj.fetch_row_count()
        s_log.info("System Diagnostic Report...")
        s_log.info(entry)
        s_log.info(row_count)
        return row_count, entry

    def move_log_category(self):
        from tests.configurations.ise.ui.administration.system.logging.logging_categories import Logging_Categories
        fname = 'move_log_category'
        logging_category_obj = Logging_Categories(self.app, s_log)
        logging_category_obj.navigate_to_page()
        category_name = self.args[fname][0]
        syslog_targets = self.args[fname][1]  # Syslog details should be a list data type or None.
        enable_local_log = self.args[fname][2]
        to_select = self.args[fname][3]
        log_severity = self.args[fname][4] if self.args[fname][4] else None
        logging_category_obj.move_syslog_in_category(category_name, syslog_targets, enable_local_log=enable_local_log,
                                                     selected=to_select)
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=5)

    @staticmethod
    def execute_command_on_remote_machine_and_return_output(host, port, username, password, command, prompt):
        ssh = UI_methods.enable_ssh(host, port)
        ssh.connect_ssh_client(username=username, password=password)
        try:
            s_log.info("Starts ssh connection ...")
            ssh.connect_ssh_client(username=username, password=password)
            output = ssh.execute_command(command + '\n')
            output, status = UI_methods.wait_until_prompt(ssh, prompt, 300, output, 10)
            s_log.info("The command output{}".format(output))
        except Exception as e:
            status = s_log.info("SSH client exception was raised : {}".format(e))
            output = None
        ssh.close_connection()
        return output

    @staticmethod
    def find_in_list(data, str1):
        found = 0
        new = ""
        new_data = data.splitlines()
        s_log.info("The new_data is {}".format(new_data))
        s_log.info("The new_data len is {}".format(len(new_data)))
        for new in new_data:
            if new.find(str1) >= 0:
                # s_log.info("found message is : {} ".format(new))
                found = 1

        return found

    @staticmethod
    def verify_process_run_in_port(host, port, username, password, process_port, prompt, state, connected_to, process):
        try:
            s_log.info("Verify process run status ...")
            command = "netstat -tulpan |grep " + process_port
            output = UI_methods.execute_command_on_remote_machine_and_return_output(host, port, username, password,
                                                                                    command, prompt)
            time.sleep(3)
            s_log.info("The netstat output is: {}".format(output))
            expected_regex = "{}.*\s+{}:[\d*]+\s+{}.*{}".format(process_port, connected_to, state, process)
            if re.search(expected_regex, output) is not None:
                s_log.info("The process is running and state is as expected")
                return True
            s_log.info("The result is not as expected")
            return False
        except Exception as e:
            s_log.info("SSH client exception was raised : {}".format(e))

    @staticmethod
    def create_baseline(host, port, username, password, location, prompt):
        baseline = None
        command = "wc -l < " + location
        output = UI_methods.execute_command_on_remote_machine_and_return_output(host, port, username, password, command,
                                                                                prompt)
        time.sleep(3)
        out = re.findall(r'(\d+)', output)
        s_log.info("The outvalue is :{}".format(out[0] if out else 0))
        baseline = int(out[0]) if out else 0
        s_log.info("The baseline value is:{}".format(baseline))
        return baseline

    @staticmethod
    def check_log(host, port, username, password, location, baseline, regex, prompt,
                  regex_timeout=60, prompt_timeout=60):
        wait_for_prompt_timeout = prompt_timeout
        retry_time = 0
        ssh = UI_methods.enable_ssh(host, port)
        ssh.connect_ssh_client(username, password)
        command = "tail -n +{} {} | grep -a '{}'".format(baseline, location, regex)
        while True:
            s_log.info("Executing command : {}".format(command))
            output = ssh.execute_command(command + '\n')
            output, prompt_status = UI_methods.wait_until_prompt(ssh, prompt, wait_for_prompt_timeout, output)
            if prompt_status is False:
                s_log.info("output not caputred completely, seems tail output is very large")
                s_log.error("Failed to get complete log i.e no prompt displayed after tail")
                assert False
            else:  # tail is completed and prompt is visible
                s_log.info("Checking if regex is found...")
                required_match = re.findall(regex, output)  # check for log present in tailed log
                if len(required_match) > 0:  # if regex is mathced then return True
                    s_log.info("Regex :{} is present in log: {}".format(regex, location))
                    s_log.info("The occurance count is {}".format(len(required_match)))
                    ssh.close_connection()
                    return len(required_match), True
                else:  # check if timedout and if not retry
                    retry_time += 10
                    s_log.info("Regex is not found in logs... Retrying again... Retry Time : {}".format(retry_time))
                    if not retry_time >= regex_timeout:
                        s_log.info("waited {} secs for logs to enter in logfile...".format(retry_time))
                        time.sleep(10)
                        continue
                    else:
                        s_log.error("Could tail the complete log but unable to find regex in tailed logs...")
                        ssh.close_connection()
                        return len(required_match), False

    @staticmethod
    def remove_processes_on_port(host, port, username, password, process_port, prompt):
        s_log.info("Removing running processes on port {}".format(process_port))
        try:
            s_log.info("Verify  status ...")
            command = "ps -ef | grep {} | awk '{{print $2}}' | xargs kill -9".format(process_port)
            output = UI_methods.execute_command_on_remote_machine_and_return_output(host, port, username, password,
                                                                                    command, prompt)
            s_log.info("Removed running processes on port {}".format(process_port))

        except Exception as e:
            s_log.info("SSH client exception was raised : {}".format(e))

    def change_log_level(self):
        """
        changes log level of the log componenets
        send list of log compenenets for which u need to change the log level
        :return:
        """
        from corelib.selenium.selenium_ui_base_test import change_log_level
        fname = 'change_log_level'
        host = self.args[fname][0]
        components = self.args[fname][1]
        log_level = self.args[fname][2]

        for component in components:
            change_log_level(node=host, component=component, level=log_level, app_obj=self.app)
            time.sleep(2)

        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=3)

    def retrive_ldap_group_check(self):
        from tests.configurations.ise.ui.administration.identity_management.ldap import Ldap
        fname = 'retrive_ldap_group_check'
        ldap_name = self.args[fname][0]
        filter_string = self.args[fname][1]
        group_name = self.args[fname][2]
        ldap_page = Ldap(self.app, self.logger)
        ldap_page.navigate_to_page()
        assert ldap_page.ldap_retrieve_group_with_filter(ldap_name, filter_string, group_name), "Group is not retrieved"
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=3)

    def change_strip_settings_in_ldap(self):
        from tests.configurations.ise.ui.administration.identity_management.ldap import Ldap
        fname = 'change_strip_settings_in_ldap'
        ldap_name = self.args[fname][0]
        strip_start = self.args[fname][1]
        strip_end = self.args[fname][2]
        start_char = self.args[fname][3]
        end_char = self.args[fname][4]
        ldap_page = Ldap(self.app, self.logger)
        ldap_page.navigate_to_page()
        ldap_page.change_strip_settings(ldap_name,
                                        strip_start,
                                        strip_end,
                                        start_char,
                                        end_char)
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=5)

    @staticmethod
    def toggle_ise_application(ip, username, password, cmd, timeout=300):
        """ Start or Stop ise application server
        :param ip:str : IP address of the ISE machine
        :param user: str: Username to log into ISE machine
        :param password: str: Password to log into ISE machine
        :cmd : str: either start or stop to make app on that state
        :param timeout: int : In multiples of 60 , time to wait for application to stop
        :return: bool : Return True if the admin prompt
                        is returned within timeout or False otherwise
        """

        s_log.info("Executing command to {} ise application".format(cmd))
        ssh = UI_methods.enable_ssh(ip, 22)
        ssh.connect_ssh_client(username=username, password=password)
        result = ssh.execute_command('application {} ise\n'.format(cmd))
        if 'PAN Auto Failover' in result:
            result += ssh.execute_command('y\n')
        final_output, status = UI_methods.wait_until_prompt(ssh, "admin#", timeout, result, 60)
        ssh.execute_command("exit\n")
        ssh.close_connection()
        if status:
            s_log.info("The final output if true".format(final_output))
            return (final_output, True)
        else:
            s_log.info("The final output if false".format(final_output))
            return (final_output, False)

    POWERSHELL_PATH = '/cygdrive/c/Windows/system32/WindowsPowerShell/v1.0/'
    POWER_SHELL_EXEC_POLICY = 'set-ExecutionPolicy Unrestricted'

    @staticmethod
    def run_command_on_ad_using_powershell(ip, username, password, cmd, timeout=300):
        s_log.info("Executing command to {} ise application".format(cmd))
        ssh = UI_methods.enable_ssh(ip, 22)
        ssh.connect_ssh_client(username=username, password=password)
        result = ssh.execute_command('export PATH=$PATH:{}\n'.format(UI_methods.POWERSHELL_PATH))
        s_log.info(result)
        s_log.info("Path set for powershell....")
        result = ssh.execute_command('echo $PATH\n')
        s_log.info(result)
        result = ssh.execute_command('powershell\n')
        s_log.info(result)
        s_log.info("Entered into powershell subprocess....")
        result = ssh.execute_command(UI_methods.POWER_SHELL_EXEC_POLICY + '\n')
        s_log.info(result)
        s_log.info("Execution policy set for powershell....")
        result = ssh.execute_command(cmd + '\n')
        s_log.info(result)
        s_log.info("Command execution completed....")
        ssh.execute_command('exit\n')
        ssh.close_connection()

    def create_allowed_protocol_for_eap_fast_protocol_enable_anonymous_pac(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowedprotocols = AllowedProtocols(app=self.app, logger=s_log)
        fname = "create_allowed_protocol_for_eap_fast_protocol_enable_anonymous_pac"
        allowed_prot_name = self.args[fname][0]
        allowed_prot_desp = self.args[fname][1]
        allowedprotocols.navigate_to_page()
        if allowedprotocols.select_protocol_by_name(allowed_prot_name).is_displayed():
            allowedprotocols.delete_allowed_prtocol(allowed_prot_name)
        allowedprotocols.create_new_allowed_protocol_with_name_and_description(name_text=allowed_prot_name,
                                                                               description_text=allowed_prot_desp)
        allowedprotocols.eap_fast_in_allowed_protocol(eap_fast_check=True,
                                                      eap_fast_eap_mschapv2=True,
                                                      Use_PAC=True,
                                                      eap_fast_Allow_Anonymous_In_Band_PAC_checkbox=True,
                                                      Eap_fast_authenticated_provisioning_checkbox=True,
                                                      Eap_Fast_Server_Returns_Access_checkbox=True)
        for i in range(len(self.args[fname])):
            self.args[fname].pop(0)

    def create_allowed_protocol_for_eap_fast_protocol(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowedprotocols = AllowedProtocols(app=self.app, logger=s_log)
        fname = "create_allowed_protocol_for_eap_fast_protocol"
        allowed_prot_name = self.args[fname][0]
        allowed_prot_desp = self.args[fname][1]
        allowedprotocols.navigate_to_page()
        if allowedprotocols.select_protocol_by_name(allowed_prot_name).is_displayed():
            allowedprotocols.delete_allowed_prtocol(allowed_prot_name)
        allowedprotocols.create_new_allowed_protocol_with_name_and_description(name_text=allowed_prot_name,
                                                                               description_text=allowed_prot_desp)
        allowedprotocols.eap_fast_in_allowed_protocol(eap_fast_check=True,
                                                      eap_fast_eap_mschapv2=True,
                                                      Use_PAC=True,
                                                      Eap_fast_authenticated_provisioning_checkbox=True,
                                                      Eap_Fast_Server_Returns_Access_checkbox=True)

        for i in range(len(self.args[fname])):
            self.args[fname].pop(0)

    def verify_login_with_identity_source(self):
        """
        Author : nandpara
        login to ise using user/pass from any indentity store
        """
        fname = 'verify_login_with_identity_source'
        admin = self.args[fname][0]
        admin_password = self.args[fname][1]
        ise_url = self.args[fname][2]
        selenium_url = self.args[fname][3]
        identity_source = self.args[fname][4]
        app = App(selenium_url)
        login_page = Login(app, self.logger, ise_url)
        login_page.navigate_to_page()
        login_page.login_with_identity_source(admin, admin_password, identity_source)
        try:
            login_page.wait_for_loader([Button(By.XPATH,
                                               "//div[text() = 'Identity Services Engine']", app.driver)])
        except Exception as err:
            assert False, "Unable to login with identity source..."

    def join_existing_ad(self):
        """
        Author : nanpara
        Joins the already existing AD
        """
        fname = "join_existing_ad"
        default = {'ad_name': None,
                   'ad_username': None,
                   'ad_password': None,
                   }
        new_attrs = self.args[fname][0]
        for key, value in new_attrs.items():
            default[key] = value
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        ad_page = ActiveDirectory(app=self.app, logger=s_log)
        ad_page.navigate_to_page()
        time.sleep(3)
        status = ad_page.enter_existing_AD(adname=default['ad_name'],
                                           username=default['ad_username'],
                                           password=default['ad_password'])
        if status is not True:
            assert False, 'Failed while joinning AD...'

        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=1)

    def retrieve_groups_for_existing_ad(self):
        """
        Author : nanpara
        retrieve groups for already existing AD
        """
        fname = "retrieve_groups_for_existing_ad"
        default = {'ad_name': None,
                   'groups': None,
                   }
        new_attrs = self.args[fname][0]
        for key, value in new_attrs.items():
            default[key] = value
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        ad_page = ActiveDirectory(app=self.app, logger=s_log)
        ad_page.navigate_to_page()
        time.sleep(3)
        ad_page.active_dir(default['ad_name']).click()
        time.sleep(2)
        ad_page.select_ad(default['ad_name'])
        time.sleep(2)
        success_msg, alert = ad_page.select_groups_from_ad(scope_ad=default['ad_name'],
                                                           group_name=default['groups'], )
        s_log.info("Success Msg : {}".format(success_msg))
        if success_msg is None:
            s_log.info("Alert Msg : {}".format(alert))
            assert False, 'Failed while retrieving groups...'
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=1)

    def retrieve_user_attributes_for_ad(self):
        """
        Author : nanpara
        retrieve user attributes for already existing AD
        """

        fname = "retrieve_user_attributes_for_ad"
        default = {'ad_name': None,
                   'ad_user': None,
                   'ad_user_attributes': None,
                   }
        new_attrs = self.args[fname][0]
        for key, value in new_attrs.items():
            default[key] = value

        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        ad_page = ActiveDirectory(app=self.app, logger=s_log)
        ad_page.navigate_to_page()
        time.sleep(3)
        ad_page.active_dir(default['ad_name']).click()
        time.sleep(2)
        ad_page.select_ad(default['ad_name'])
        time.sleep(2)
        success_msg, alert = ad_page.select_attributes_from_ad(ad_name=default['ad_name'],
                                                               user_name=default['ad_user'],
                                                               attributes=default['ad_user_attributes'])
        s_log.info("Success Msg : {}".format(success_msg))
        if success_msg is None:
            s_log.info("Alert Msg : {}".format(alert))
            assert False, 'Failed while retrieving User Attributes...'
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=1)

    def enable_session_resume_allowed_protocol_for_eap_fast(self):
        from tests.configurations.ise.ui.policy.policy_elements.results.authentication.allowed_protocols import \
            AllowedProtocols
        allowedprotocols = AllowedProtocols(self.app, self.logger)
        allowedprotocols.navigate_to_page()
        allowedprotocols.default_network_access.click()
        time.sleep(5)
        allowedprotocols.eap_fast_in_allowed_protocol(authenticate_eap_fast_use_pacs_stateless_session_ttl_units=True)
        time.sleep(3)

    def eap_tls_allowed_protocol(self):
        ed_pro = AllowedProtocols(app=self.app, logger=self.logger)
        fname = 'eap_tls_allowed_protocol'
        ad_name = self.args[fname][0]
        eap_checkbox = self.args[fname][1]
        eap_textbox = self.args[fname][2]
        ed_pro.navigate_to_page()
        time.sleep(2)
        ed_pro.configure_outer_allowed_protocol(name=ad_name)
        time.sleep(5)
        ed_pro.use_pac_ttls(eapttls_preferred_eap_checkbox=eap_checkbox,
                            eapttls_preferred_eap_textbox=eap_textbox)
        ed_pro.save.javascript_click()
        for i in range(0, 3):
            self.args[fname].pop(0)

    def networkDevice_edit_second_shared_key(self):
        from tests.configurations.ise.ui.administration.network_resources import network_device
        networkDevicePage = network_device.NetworkDevice(self.app, self.logger)

        networkDeviceSecret1 = self.args['networkDevice_edit_second_shared_key'][0]
        networkDeviceSecret2 = self.args['networkDevice_edit_second_shared_key'][1]

        networkDevicePage.navigate_to_page()
        networkDevicePage.edit_network_device_sec_shared_secret(networkDeviceSecret1, networkDeviceSecret2)
        time.sleep(3)

        self.args['networkDevice_edit_second_shared_key'].pop(0)

    def na_users_import(self):
        from tests.configurations.ise.ui.administration.identity_management.users import Users
        page = Users(self.app, s_log)
        fname = 'na_users_import'
        path = self.args[fname][0]
        key = self.args[fname][1]
        update_existing_user = self.args[fname][2]
        page.navigate_to_page()
        page.import_na_users(path, key, update_existing_user)

        for i in range(0, 3):
            self.args[fname].pop(0)

    def validate_imported_user_detail(self):
        from tests.configurations.ise.ui.administration.identity_management.users import Users
        page = Users(self.app, s_log)
        fname = 'validate_imported_user_detail'
        validation_list = self.args[fname][0]
        for expected_detail in validation_list:
            page.navigate_to_page()
            retrieved_detail = page.retrieve_user_details(expected_detail['user_name'])
            for attr in expected_detail:
                value_retrieved = retrieved_detail[attr].get_attribute('value').strip() \
                    if not isinstance(retrieved_detail[attr], BaseElement) \
                    else retrieved_detail[attr].get_attribute_value(attribute_name='value').strip()
                s_log.info("Expected value for '{}' is '{}', retrived value is '{}'".format(attr,
                                                                                            expected_detail[attr],
                                                                                            value_retrieved))
                if not expected_detail[attr] == value_retrieved:
                    assert False, "Expected value not present"
        self.args[fname].pop(0)

    def delete_multiple_ad(self):
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        ad = ActiveDirectory(app=self.app, logger=s_log)
        ad.navigate_to_page()
        time.sleep(5)
        ad.delete_all_active_directory_instances()

    def na_export_all_users(self):
        from tests.configurations.ise.ui.administration.identity_management.users import Users
        page = Users(self.app, s_log)
        fname = 'na_export_all_users'
        key = self.args[fname][0]
        page.navigate_to_page()
        page.export_all_na_users(key)

        self.args[fname].pop(0)

    def import_network_devices_csv(self):
        from tests.configurations.ise.ui.administration.network_resources import network_device
        network_device_page = network_device.NetworkDevice(app=self.app, logger=s_log)
        network_device_page.driver.execute_script(
            'window.location.hash = "#administration/administration_networkresources/administration_networkresources_devices"')
        time.sleep(10)
        file_path = self.args['import_network_devices_csv'][0]
        # network_device_page.navigate_to_page()
        network_device_page.delete_all_devices()
        time.sleep(1)
        network_device_page.import_nad(file_path)
        time.sleep(2)
        for i in range(0, 1):
            self.args['import_network_devices_csv'].pop(0)

    def export_network_devices_csv(self):
        from tests.configurations.ise.ui.administration.network_resources import network_device
        network_device_page = network_device.NetworkDevice(app=self.app, logger=s_log)
        network_device_page.driver.execute_script(
            'window.location.hash = "#administration/administration_networkresources/administration_networkresources_devices"')
        time.sleep(10)

        # network_device_page.navigate_to_page()
        time.sleep(5)
        network_device_page.export_all()
        time.sleep(2)

    def edit_shared_secret_radius(self):
        from tests.configurations.ise.ui.administration.network_resources import network_device
        network_device_page = network_device.NetworkDevice(app=self.app, logger=s_log)
        network_device_page.driver.execute_script(
            'window.location.hash = "#administration/administration_networkresources/administration_networkresources_devices"')
        time.sleep(10)
        nad_name = self.args['edit_shared_secret_radius'][0]
        shared_secret = self.args['edit_shared_secret_radius'][1]
        # network_device_page.navigate_to_page()
        time.sleep(1)
        network_device_page.edit_network_device_radius_shared_secret(nad_name, shared_secret)
        time.sleep(2)
        for i in range(0, 2):
            self.args['edit_shared_secret_radius'].pop(0)

    @staticmethod
    def create_repo(host, port, admin_username, admin_password, repository_name, upgrade_bundle_path, credential,
                    sftp=False):
        try:
            status = False
            s_log.info("Connecting to ssh for repo creation")
            from tests.configurations.ise.cli.ssh_client_connect import SshClientConnect
            ssh_con = SshClientConnect(host, port)
            ssh_con.connect_ssh_client(admin_username, admin_password)
            result = ssh_con.execute_command("config\n")
            time.sleep(10)
            s_log.info("The result is{}".format(result))
            result = ssh_con.execute_command("repository " + repository_name + "\n")
            result += ssh_con.execute_command("url " + upgrade_bundle_path + "\n")
            result += ssh_con.execute_command("" + credential + "\n")
            result += ssh_con.execute_command("end\n")
            time.sleep(120)
            if sftp:
                sftp_list = upgrade_bundle_path.split('/')
                sftp_host = sftp_list[2]
                result += ssh_con.execute_command("crypto host_key add host " + sftp_host + "\n")
                s_log.info("sftp output {}".format(result))
                if "host key fingerprint added" in result:
                    s_log.info("Host key added successfully")
                else:
                    s_log.info("Host key not added")
            status = True
            s_log.info("Repo created successfully")
            print(result)
            status = True
            s_log.info("Repo created successfully")
            print(result)
        except Exception as e:
            s_log.error("e")
            result = ssh_con.execute_command("end\n")
            result += ssh_con.execute_command("exit\n")
            print(result)
        finally:
            ssh_con.close_connection()
            return status

    @staticmethod
    def db_restore(host, port, db_name, repository_name, encrpytion_key, admin_username, admin_password):
        try:
            s_log.info("Connecting to ssh from upgrade")
            from tests.configurations.ise.cli.ssh_client_connect import SshClientConnect
            sshcon = SshClientConnect(host, port)
            sshcon.connect_ssh_client(admin_username, admin_password)
            result = sshcon.execute_command(
                "restore " + db_name + " repository " + repository_name + " encryption-key plain " + encrpytion_key + "\n")
            s_log.info(result)
            time_counter = 0
            passed = False
            while True:
                if result.endswith("/admin#"):
                    s_log.info("restoring backup Finished")
                    restore_status = sshcon.execute_command("show restore history" + "\n")
                    s_log.info(restore_status)
                    s_log.info(db_name + ' from repository ' + repository_name + ': success')
                    # Sometimes the word 'success' is broken up in different lines
                    # We cannot use the entire word using str.find()
                    # Hence checking for the word 'success' with a new line character in between
                    if 'success' in restore_status:
                        return True
                    for index in range(1, len('success')):
                        search_string = list('success')
                        search_string.insert(index, '\r\n')
                        s_log.info("Searching for " + ''.join(search_string))
                        if ''.join(search_string) in restore_status:
                            sshcon.execute_command("exit\n")
                            sshcon.close_connection()
                            s_log.info("DB Restore Success")
                            return True
                    return False
                elif (time_counter >= 12000):
                    s_log.info("Timeout exceeds")
                    return False
                else:
                    time.sleep(120)
                    output = sshcon.execute_command("\n")
                    print(output.strip())
                    time_counter = time_counter + 120
                    result += output.strip()
                    continue
            self.ssh_con.close_connection()
        except Exception as e:
            s_log.error(e)
            s_log.error("There is exception occured")
            result = sshcon.execute_command("end\n")
            result += sshcon.execute_command("exit\n")
            print(result)
            return False

    def add_ldap_server(self):
        from tests.configurations.ise.ui.administration.identity_management.ldap import Ldap
        ldap_name = self.args["add_ldap_server"][0]
        description = self.args["add_ldap_server"][1]
        primary_server_host_or_ip = self.args["add_ldap_server"][2]
        primary_server_port = self.args["add_ldap_server"][3]
        primary_admin_dn = self.args["add_ldap_server"][4]
        primary_admin_password = self.args["add_ldap_server"][5]
        subject_search_base = self.args["add_ldap_server"][6]
        group_search_base = self.args["add_ldap_server"][7]
        user_name_in_schema = self.args["add_ldap_server"][8]
        ca_name = self.args["add_ldap_server"][9]
        issuer_ca = self.args["add_ldap_server"][10]
        page = Ldap(self.app, self.logger)
        time.sleep(2)
        page.navigate_to_page()
        time.sleep(5)
        self.logger.info('entering into ldap page')
        if page.delete_ldap_if_exists(ldap_name=ldap_name):
            assert False, "Failed to delete Ldap, ldap may be referred to some policy... "
        if not page.add_ad_as_ldap_sessionapi(name=ldap_name,
                                              description=description,
                                              primary_server_host_or_ip=primary_server_host_or_ip,
                                              primary_server_port=primary_server_port,
                                              primary_admin_dn=primary_admin_dn,
                                              primary_admin_password=primary_admin_password,
                                              subject_search_base=subject_search_base,
                                              group_search_base=group_search_base,
                                              user_name_in_schema=user_name_in_schema,
                                              ca_name=ca_name,
                                              issuer_ca=issuer_ca):
            raise Exception("Failed to configure Ldap server".format(ldap_name))

        for i in range(0, 10):
            self.args['add_ldap_server'].pop(0)

    def edit_identity_source_in_policy(self):
        from tests.configurations.ise.ui.policy.policy_sets.new_policy_sets import RadPolicySets
        edit_policy_page = RadPolicySets(app=self.app, logger=s_log)
        fname = 'edit_identity_source_in_policy'
        policy_name = self.args[fname][0]
        policy_set = self.args[fname][1]
        use_val = self.args[fname][2]
        edit_policy_page.navigate_to_policy_set_page()
        time.sleep(10)
        edit_policy_page.enter_policy_set_view_by_name(name=policy_name)
        time.sleep(15)
        edit_policy_page.authentication_policy_expand.wait_for_enable()
        edit_policy_page.authentication_policy_expand.click()
        time.sleep(20)
        edit_policy_page.change_identity_source_in_auth_policy(name=policy_set, use_val=use_val)

        for i in range(0, 2):
            self.args[fname].pop(0)
            time.sleep(2)

    def mntlog_for_radius_authentications(self):
        from tests.configurations.ise.ui.operations.operations_reports.reports.endpointsandusers.radius_authentications import \
            RadiusAuthentications
        rad_aut = RadiusAuthentications(app=self.app, logger=self.logger)
        fname = 'mntlog_for_radius_authentications'
        username = self.args[fname][0]
        rad_aut.navigate_to_page()
        time.sleep(10)
        rad_aut.mnt_log_for_radius_authentications(username=username)
        for i in range(0, 1):
            self.args[fname].pop(0)

    def retrieve_group_from_existing_ldap(self):
        from tests.configurations.ise.ui.administration.identity_management.ldap import Ldap
        ldap = Ldap(app=self.app, logger=s_log)
        name = self.args['retrieve_group_from_existing_ldap'][0]
        ldap_group = self.args['retrieve_group_from_existing_ldap'][1]
        time.sleep(5)
        ldap.navigate_to_page()
        ldap.ldap_retrieve_group_from_existing(name=name, ldap_group=ldap_group)
        time.sleep(5)

        for i in range(0, 2):
            self.args['retrieve_group_from_existing_ldap'].pop(0)

    def add_group_in_admin_group_with_external_group_map(self):
        from tests.configurations.ise.ui.administration.system.admin_access.administrators.admin_groups import \
            AdminGroups
        admingroups = AdminGroups(app=self.app, logger=s_log)
        group_name = self.args['add_group_in_admin_group_with_external_group_map'][0]
        external_group_name = self.args['add_group_in_admin_group_with_external_group_map'][1]
        admingroups.navigate_to_page()

        admingroups.add_another_group_in_admin_group_with_external_group_mapped(group_name=group_name,
                                                                                external_group_name=external_group_name)
        time.sleep(5)

        for i in range(0, 2):
            self.args['add_group_in_admin_group_with_external_group_map'].pop(0)

    def check_live_log_steps(self):
        from tests.configurations.ise.ui.operations.radius.live_logs import Livelogs
        fname = 'check_live_log_steps'
        steps_to_check = self.args[fname][0]
        live_logs = Livelogs(self.app, logger=s_log)
        live_logs.navigate_to_page()
        time.sleep(10)
        live_logs.refresh_click()
        time.sleep(10)
        detailed_steps = live_logs.steps()
        for step in steps_to_check:
            if step not in detailed_steps:
                assert "The step provided - {}, is not listed in live log".format(step)
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=1)

    def change_primary_ldap_ip(self):
        from tests.configurations.ise.ui.administration.identity_management.ldap import Ldap
        fname = 'change_primary_ldap_ip'
        timeout = None
        ldap_name = self.args[fname][0]
        new_ip = self.args[fname][1]
        if len(self.args[fname]) > 2:
            timeout = self.args[fname][2]
        page = Ldap(self.app, s_log)
        page.navigate_to_page()
        page.wait_for_loader([page.ldap_delete_button], timeout=5)
        Button(By.XPATH, "//div[@title='" + ldap_name + "']/preceding::*[1]", page.app.driver).click()
        page.ldap_edit_button.click()
        time.sleep(2)
        page.wait_for_loader([page.connection_tab], timeout=5)
        page.connection_tab.click()
        page.wait_for_loader([page.ldap_primary_server_host_name_or_ip], timeout=5)
        page.ldap_primary_server_host_name_or_ip.send_text(new_ip)
        time.sleep(2)
        if timeout:
            page.primary_server_timeout.send_text(timeout)
            time.sleep(3)
            page.access_primary_server_first.click()
            s_log.info("Enabled always access primary server first ")
        time.sleep(3)
        page.ldap_submit_button.click()
        page.server_response.wait_for_ui_element(timeout=30)

        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=2)

    def toggle_internal_user_status(self):
        from tests.configurations.ise.ui.administration.identity_management import identities
        identitiesPage = identities.Identities(self.app, self.logger)
        identitiesPage.navigate_to_page()
        fname = 'toggle_internal_user_status'
        user = self.args[fname][0]
        status = self.args[fname][1]
        status_retrieved = identitiesPage.user_status(user)
        if status != status_retrieved:
            identitiesPage.change_user_status(user)
        else:
            s_log.info("User is already in {} state".format(status_retrieved))
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=2)

    def change_log_level_to_default_value(self):
        from tests.configurations.ise.ui.administration.system.logging.debug_log_configuration import \
            DebugLogConfiguration
        logconfig_page = DebugLogConfiguration(self.app, self.logger)
        logconfig_page.navigate_to_page()
        fname = 'change_log_level_to_default_value'
        host = self.args[fname][0]
        components = self.args[fname][1]
        for category in components:
            logconfig_page.set_component_default_value(host, category)
            logconfig_page.node_list.click()
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=2)

    def verify_logging_category_level(self):
        from tests.configurations.ise.ui.administration.system.logging.debug_log_configuration import \
            DebugLogConfiguration
        logconfig_page = DebugLogConfiguration(self.app, self.logger)
        logconfig_page.navigate_to_page()
        fname = 'verify_logging_category_level'
        host = self.args[fname][0]
        component_map = self.args[fname][1]  # dict
        for component, log_level in component_map.items():
            assert logconfig_page.test_component_level(host, component, log_level), "Log level is not as expected"
            logconfig_page.node_list.click()
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=2)

    def verify_configuration_audit_on_recent_change(self):
        from tests.configurations.ise.ui.operations.operations_reports.reports.audit.change_configuration_audit import \
            ChangeConfigurationAudit
        s_log.info("Start verify_configuration_audit_on_reset_log_level")
        fname = 'verify_configuration_audit_on_recent_change'

        event = self.args[fname][0]
        object_type = self.args[fname][1]
        obj_name = self.args[fname][2]
        object_updated = self.args[fname][3]

        reports_page = ChangeConfigurationAudit(self.app, self.logger)
        reports_page.navigate_to_page()
        reports_page.changeconfigurationaudit_verify_elements_exists_with_quickfilter(
            [event], object_type, obj_name)
        reports_page.click_on_event(event)
        self.window = 1
        self.app.switch_to_newwindow(self.window)
        time.sleep(5)
        reports_page.check_event_details([object_updated])
        time.sleep(2)
        self.app.close()
        self.app.switch_to_newwindow(0)
        time.sleep(2)
        s_log.info("End verify configuration audit on reset log level")
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=4)

        # SHA1 Ciphers

    def check_and_select_if_security_options_exist(self):
        """
        Author : nanpara
        """
        fname = "check_and_select_if_security_options_exist"
        security_options = self.args[fname][0]
        is_select = self.args[fname][1]
        from tests.configurations.ise.ui.administration.system.settings.security_settings import securitySettings
        security_page = securitySettings(self.app, self.logger)
        security_page.navigate_to_page()
        time.sleep(3)
        status = security_page.check_and_select_if_security_option_exist(security_options=security_options,
                                                                         select=is_select)
        assert status, 'One or more of the security Options are not available in Security Settings Page'
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=2)

    def select_SHA1_ciphers_radio_option(self):
        """
        Author : nanpara
        options : 'allowAll' or 'allowOnlyAES128'
        """
        fname = "select_SHA1_ciphers_radio_option"
        SHA1_radio_option = self.args[fname][0]
        from tests.configurations.ise.ui.administration.system.settings.security_settings import securitySettings
        security_page = securitySettings(self.app, self.logger)
        security_page.navigate_to_page()
        time.sleep(3)
        security_page.select_SHA1_cipher_option(option=SHA1_radio_option)
        if security_page.save.get_attribute_value('disabled') != 'True':
            security_page.save.click()
            security_page.fail_if_no_success_response_and_log_alert()
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=1)

    def run_session_trace_test(self):
        fname = "run_session_trace_test"
        details = self.args[fname][0]  # Expecting a dictionary
        host = details.get('host', 'Positron.demo.local')
        test_name = details.get('test_name', 'Positron.demo.local')
        expected_data = details.get('comparison_data', None)
        from tests.configurations.ise.ui.operations.radius.live_logs import Livelogs
        live_logs = Livelogs(app=self.app, logger=self.logger)
        retrieved_data = live_logs.run_session_trace_and_read_result(host, test_name)
        s_log.info("Results Data: {}".format(retrieved_data))
        if expected_data is not None:
            for stage, result in expected_data.items():
                s_log.info("Comparing retrieved data - {},\n with expected data{}".format(retrieved_data[stage],
                                                                                          expected_data[stage]))
                assert result == retrieved_data[stage], "Test result is not as expected"
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=1)

    def verify_authentication_domain_status(self):
        fname = 'verify_authentication_domain_status'
        scope = self.args[fname][0]
        join_point = self.args[fname][1]
        domain_name = self.args[fname][2]
        expected_status = self.args[fname][3]
        from tests.configurations.ise.ui.administration.identity_management.active_directory import ActiveDirectory
        ad = ActiveDirectory(self.app, s_log)
        retrieved_status = ad.retrieve_domain_status(scope, join_point, domain_name).strip()
        s_log.info("The status retrieved is : {}".format(retrieved_status))
        if expected_status == retrieved_status:
            s_log.info("The join status is expected for {} is {} ".format(join_point, retrieved_status))
        else:
            s_log.info("The join status is not expected for {}".format(join_point))
            ad.enable_authentication_domain(scope, join_point, domain_name)

        for i in range(0, 4):
            self.args[fname].pop(0)

    def delete_ip_sgt_mapping(self):
        """
        deletes ip SGT static mapping specific record
        """
        from tests.configurations.ise.ui.workcenters.trustsec.components.ip_sgt_static_mapping import \
            ip_sgt_static_mapping
        ip_mapping = ip_sgt_static_mapping(self.app, self.logger)
        fname = 'delete_ip_sgt_mapping'
        ip_address = self.args[fname][0]
        sgt = self.args[fname][1]
        ip_mapping.navigate_to_page()
        time.sleep(3)
        ip_mapping.delete_ip_sgt_mapping(ip=ip_address, sgt=sgt)
        time.sleep(3)
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=2)

    @staticmethod
    def execute_command_on_remote_machine_and_return_output_without_prompt(host, port, username, password, command,
                                                                           prompt):
        ssh = UI_methods.enable_ssh(host, port)
        ssh.connect_ssh_client(username=username, password=password)
        try:
            s_log.info("Starts ssh connection ...")
            ssh.connect_ssh_client(username=username, password=password)
            output = ssh.execute_command(command + '\n')
            s_log.info("The command output{}".format(output))
        except Exception as e:
            status = s_log.info("SSH client exception was raised : {}".format(e))
            output = None
        ssh.close_connection()
        return output

    @staticmethod
    def add_certificate_to_user_on_ad(ip, user, password, certicate_path):
        cert_obj_cmd = '$cert=New-Object System.Security.Cryptography.X509Certificates.X509Certificate "{}"'.format(
            certicate_path)
        cert_add_cmd = 'Set-ADUser -Identity test_user1 -Certificates @{Add=$cert}'
        UI_methods.run_command_on_ad_using_powershell(ip, user, password, cert_obj_cmd + ';' + cert_add_cmd)

    def add_radius_token_servers(self):
        from tests.configurations.ise.ui.administration.identity_management.radius_token import RadiusToken
        radtoken = RadiusToken(self.app, self.logger)
        fname = "add_radius_token_servers"
        default = {'name': None,
                   'IP': None,
                   'shared_secret': None,
                   'primary_port': None,
                   'primary_timeout': None,
                   'primary_retries': None,
                   'secondary_server': None,
                   'secondary_ip': None,
                   'secondary_shared': None,
                   'secondary_port': None,
                   'secondary_timeout': None,
                   'secondary_retries': None
                   }
        new_attrs = self.args[fname][0]
        for key, value in new_attrs.items():
            default[key] = value
        s_log.info("Adding Radius Token Server...")
        radtoken.navigate_to_page()
        time.sleep(5)
        connection_msg, connection_alert = radtoken.add_radius_token_servers(name=default['name'],
                                                                             IP=default['IP'],
                                                                             shared_secret=default['shared_secret'],
                                                                             primary_port=default['primary_port'],
                                                                             primary_timeout=default['primary_timeout'],
                                                                             primary_retries=default['primary_retries'],
                                                                             secondary_server=default[
                                                                                 'secondary_server'],
                                                                             secondary_ip=default['secondary_ip'],
                                                                             secondary_shared=default[
                                                                                 'secondary_shared'],
                                                                             secondary_port=default['secondary_port'],
                                                                             secondary_timeout=default[
                                                                                 'secondary_timeout'],
                                                                             secondary_retries=default[
                                                                                 'secondary_retries'])
        # Verify the Radius Token is added
        if connection_msg is None:
            assert False, "********* Radius  Token servers is not added successfully - ****".format(
                connection_alert)
        else:
            s_log.info("********* Radius Token is added successfully ****")
            s_log.info("********* Server response : {}".format(connection_msg))

        time.sleep(10)
        UI_methods.remove_binded_args_after_run(obj=self, func_name=fname, args_count=1)

    def add_radius_vendor_dictionary(self):
        from tests.configurations.ise.ui.policy.policy_elements.dictionaries.dictionaries import Dictionary
        fname = 'add_radius_vendor_dictionary'
        dictionary_name = self.args[fname][0]
        vendor_id = self.args[fname][1]
        page = Dictionary(self.app, s_log)
        page.navigate_to_page()
        page.add_new_radius_vendor_dictionary(dictionary_name, vendor_id)
        for i in range(0, 2):
            self.args[fname].pop(0)

    def add_radius_vendor_dictionary_attribute(self):
        from tests.configurations.ise.ui.policy.policy_elements.dictionaries.dictionaries import Dictionary
        fname = 'add_radius_vendor_dictionary_attribute'
        dictionary_name = self.args[fname][0]
        attribute_name = self.args[fname][1]
        vendor_id = self.args[fname][2]
        description = self.args[fname][3]
        data_type = self.args[fname][4]
        direction = self.args[fname][5]
        page = Dictionary(self.app, s_log)
        page.navigate_to_page()
        page.add_new_radius_vendor_dictionary_attribute(dictionary_name, attribute_name, vendor_id,
                                                        description=description, data_type=data_type,
                                                        direction=direction)
        for i in range(0, 6):
            self.args[fname].pop(0)

    def delete_radius_vendor_dictionary(self):
        from tests.configurations.ise.ui.policy.policy_elements.dictionaries.dictionaries import Dictionary
        fname = 'delete_radius_vendor_dictionary'
        dictionary_name_list = self.args[fname][0]
        page = Dictionary(self.app, s_log)
        for dictionary_name in dictionary_name_list:
            page.navigate_to_page()
            result = page.radius_vendor_dictionary_delete(dictionary_name)
            assert result, "Given dictionary name {} is not found to delete.".format(dictionary_name)
        self.args[fname].pop(0)

    def validate_radius_vendor_dictionary_exist(self):
        from tests.configurations.ise.ui.policy.policy_elements.dictionaries.dictionaries import Dictionary
        fname = 'validate_radius_vendor_dictionary_exist'
        dictionary_name_list = self.args[fname][0]
        expected_result = self.args[fname][1]
        page = Dictionary(self.app, s_log)
        assert_condition = True
        for dictionary_name in dictionary_name_list:
            page.navigate_to_page()
            result = page.check_radius_vendor_dictionary(dictionary_name)
            if result is expected_result:
                s_log.info("Result-->{}, Expected Result-->{}.Got result as expected.".format(result, expected_result))
            else:
                assert_condition = False
                s_log.info(
                    "Result-->{}, Expected Result-->{}.Result is not as expected.".format(result, expected_result))
        assert assert_condition
        for i in range(0, 2):
            self.args[fname].pop(0)

    def verify_identitiy_source_moved(self):
        fname = "verify_identitiy_source_moved"
        sequence_map = self.args[fname][0]
        from tests.configurations.ise.ui.administration.identity_management.identity_source_sequences import \
            IdentitySourceSequences
        iden_source_page = IdentitySourceSequences(app=self.app, logger=s_log)
        iden_source_page.navigate_to_page()
        time.sleep(5)
        for sequence, identity_source in sequence_map.items():
            s_log.info("The key:  {} and value: {}".format(sequence, identity_source))
            assert iden_source_page.check_identity_source_to_sequence(sequence, identity_source), \
                "One or more identity source is present/not present as expected"
            iden_source_page.navigate_to_page()

    def check_mydevice_auth_method(self):
        fname = 'check_mydevice_auth_method'
        auth_method = self.args[fname][0]
        from tests.configurations.ise.ui.administration.device_portal_management.my_devices import My_Devices
        my_device_page = My_Devices(app=self.app, logger=s_log)
        my_device_page.navigate_to_page()
        time.sleep(5)
        assert my_device_page.verify_default_device_portal_auth_method(auth_method), \
            "Auth policy not matching"

    def check_selfregistered_guest_portal_auth_method(self):
        fname = 'check_selfregistered_guest_portal_auth_method'
        auth_method = self.args[fname][0]
        from tests.configurations.ise.ui.workcenters.guest_access.guest_portals import GuestPortals
        guest_portal_page = GuestPortals(app=self.app, logger=s_log)
        guest_portal_page.navigate_to_page()
        time.sleep(5)
        assert guest_portal_page.verify_selfregistered_guest_portal_auth_method(auth_method), \
            "Auth policy not matching"

    def check_default_sponsor_portal_auth_method(self):
        fname = 'check_default_sponsor_portal_auth_method'
        auth_method = self.args[fname][0]
        from tests.configurations.ise.ui.workcenters.guest_access.sponsor_portals import SponsorPortals
        sponsor_portal_page = SponsorPortals(app=self.app, logger=s_log)
        sponsor_portal_page.navigate_to_page()
        time.sleep(5)
        assert sponsor_portal_page.verify_default_sponsor_portal_auth_method(auth_method), \
            "Auth policy not matching"



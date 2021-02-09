import allure
import pytest

from services.bbcomms.accounts_api import AccountTestAPI
from utils.genericutils.execution_status_utils import ExecutionStatus
from utils.genericutils.get_json_testdata import get_data
from utils.genericutils.root_dir import *
from conftest import *

positive_testdata_path = str(project_path) + "/resourcesfile/artifacts/test_data/bbcomms/superintendent_bio_positive_testdata.json"
negative_testdata_path = str(project_path) + "/resourcesfile/artifacts/test_data/bbcomms/superintendent_bio_negative_testdata.json"

"""
This Testcase deals with both positive & negative scenarios of the accounts/superintendent/bio/? api

Positive Scenario:
This test case does not accept any in paramenters. If the authorization is valid, it returns the html content of the superintendent.  

Negative Scenario:
This test case does not accept any in paramenters. If the authorization is not valid, it returns the 401 Unauthorized.

"""

@pytest.mark.usefixtures('initialize')
class TestAPI:
	@pytest.fixture(scope = 'function')
	def initialize(self, rp_logger):
		self.api_obj = AccountTestAPI()
		self.exe_status = ExecutionStatus()
		self.exe_status.__init__()

		def cleanup():
			# data cleaning steps to be written here
			rp_logger.info('Cleaning Test Data.')
			yield
			cleanup()

	@allure.severity(allure.severity_level.BLOCKER)
	@allure.testcase("SuperIntendent Positive Case")
	@pytest.mark.smoke
	@pytest.mark.parametrize("positivetestdata", get_data(positive_testdata_path))
	def test_request_positive(self, positivetestdata, rp_logger, cmdopt):
		self.api_obj.get_common_handler_data(positivetestdata, cmdopt)

	@allure.severity(allure.severity_level.CRITICAL)
	@allure.testcase("SuperIntendent Negative Case")
	@pytest.mark.regression
	@pytest.mark.parametrize("negativetestdata", get_data(negative_testdata_path))
	def test_request_negative(self, negativetestdata, rp_logger):
		self.api_obj.get_common_handler_data_negative_scenario(negativetestdata, cmdopt)



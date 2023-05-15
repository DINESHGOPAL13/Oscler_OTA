import os
import unittest
import requests
# imports functions from prototype class for testing
'''This test class includes the below test method
1.test_connect_success
2.test_connect_Failure_1_invalid_url
3.test_connect_Failure_2_empty_url
4.test_connect_Failure_3_Server_error
5.test_retrieve_firmware_available_success
6.test_download_firmware_verify_file_exist
7.test_download_firmware_verify_file_non_exist
8.test_download_firmware_verify_file_name
'''
from test_Oscler_OTA.Task_1_OTA_main_prototype_code import (
    connect,
    retrieve_firmware_available,
    get_device_firmware_revision,
    download_firmware,
    get_device_hardware_revision,
    version_compatible,
    program_firmware,
    reboot,
)


class TestOTA(unittest.TestCase):

    def test_connect_success(self):
        """Here Actual valid End-Point URL is passed so the test need to connect and pass successfully
        EXPECTED RESULT: Not Null and 'Successfully connected to Server Portal'
        ACTUAL RESULT: Not Null and 'Successfully connected to Server Portal'
        """
        response = connect('http://localhost:8080/OTA/firmware.bin')
        '''Check the connection is made or not'''
        self.assertTrue(response)
        '''Check the response object return response and its not null'''
        self.assertIsNotNone(response)

    def test_connect_Failure_1_invalid_url(self):
        """Here passed the invalid URL so the test need to log the connection error
        EXPECTED RESULT:Not Null and Error Unable to connect to Server Portal
        ACTUAL RESULT: Not Null and Error Unable to connect to Server Portal """
        response = connect('http://localhost:8080/OTA/firmware.bin12£$%%%%%')
        '''Check the Expected error is returned or not'''
        self.assertFalse(response)
        '''Check the Error response is returned ,not null pre-defined error value is returned or not'''
        self.assertTrue(response is not None)

    def test_connect_Failure_2_empty_url(self):
        """Here passed the Null value to the URL so the test need to log the connection error
        EXPECTED RESULT:Not Null and Error while connecting to device: Invalid URL ''
        ACTUAL RESULT: Not Null and Error while connecting to device: Invalid URL '' """
        response = connect('')
        '''Check the Expected error is returned or not'''
        self.assertFalse(response)
        '''Check the Error response is returned ,not null pre-defined error value is returned or not'''
        self.assertTrue(response is not None)

    def test_connect_Failure_3_Server_error(self):
        """Here mocked the server error so I have stopped the Deployed service on Tomcat server
          the test need to log the connection error

        EXPECTED RESULT:Not Null and Error while connecting to Server Portal: HTTPConnection connection Error''

        ACTUAL RESULT: Not Null and Error while connecting to Server Portal: HTTPConnectionPool(host='localhost', port=8080):
        Max retries exceeded with url: /OTA/firmware.bin (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x0000016788DF8460>: Failed to establish a new connection: [WinError 10061] No connection could be made because the target machine actively refused it')) '' """
        response = connect('http://localhost:8080/OTA/firmware.bin')
        '''Check the Expected error is returned or not'''
        self.assertFalse(response)
        '''Check the Error response is returned ,not null pre-defined error value is returned or not'''
        self.assertTrue(response is not None)

    def test_retrieve_firmware_available_success(self):
        """Test retrieval of available firmware"""
        response = retrieve_firmware_available()
        self.assertTrue(response)
        self.assertTrue(len(response) > 0)

    def test_download_firmware_verify_file_exist(self):
        """Test that firmware is downloaded successfully and saved to folder"""
        # downloaded firmware file path
        firmware_file_path = 'C://Users//DineshGopal//Documents//Oscler_OTA//test_Oscler_OTA//firmware.bin'
        self.assertTrue(os.path.exists(firmware_file_path))

    def test_download_firmware_verify_file_non_exist(self):
        """Test that firmware is not downloaded and saved to folder (before download stage)
         Verify non-occurrence of file in folder"""
        # firmware file path
        firmware_file_path = 'C://Users//DineshGopal//Documents//Oscler_OTA//test_Oscler_OTA//firmware.bin'
        self.assertFalse(os.path.exists(firmware_file_path))

    def test_download_firmware_verify_file_name(self):
        """Test that firmware is  downloaded and saved to folder and
         Verify file name in folder"""
        # downloaded firmware file path
        firmware_file_path = 'C://Users//DineshGopal//Documents//Oscler_OTA//test_Oscler_OTA//firmware.bin'
        self.assertEqual(os.path.basename(firmware_file_path),'firmware.bin')


if __name__ == '__main__':
    unittest.main()

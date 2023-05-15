import logging
import struct
import os

''' 
->Deployed the firmware.bin image file to my local Tomcat webserver and made the local server active so that 
firmware can download from below deployed URL through that cloud portal firmware image download is simulated 
->URL = 'http://localhost:8080/OTA/firmware.bin 
->Trying to hit the URL and download the file and place it on workspace then check the download file exists or not 
->Based on that will perform the version compatibility and then after program firmware and reboot finally the OTA firmware image is updated to device successfully 
 
->And Included the ota.log file within workspace for to track the execution flow with log'''

import requests

# Constants (Based on firmware image bytes mentioned on table)


FIRMWARE_IMAGE_OFFSET = 6

#log file configuration
logging.basicConfig(filename='ota.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# predefined Functions from production code
def connect(URL = 'http://localhost:8080/OTA/firmware.bin'):

    filename = 'firmware.bin'

    global response
    try:
        response = requests.get(URL)

        if response.status_code == 200:
            print('Successfully connected to Server Portal')
            logging.info('Successfully connected to Server Portal')
            return True
        else:
            print('Unable to connect to Server Portal')
            logging.info('Unable to connect to Server Portal')
            return False
    except requests.exceptions.RequestException as e:
        print(f'Error while connecting to Server Portal: {e}')
        logging.info(f'Error while connecting to Server Portal: {e}')
        return False


def retrieve_firmware_available():
    return (2, 0)


def get_device_firmware_revision():
    return (1, 0)


# In this function will download and open the firmware file
def download_firmware():
    filename = 'firmware.bin'
    try:
        with open(filename, 'wb') as f:
            f.write(response.content)
        # check if the file exists on working directory(file storage repository)
        if os.path.exists(filename):
            print(f'{filename} image downloaded successfully')
            logging.info(f'{filename} image downloaded successfully')
            return True
        else:
            print(f'Error: {filename} image was not downloaded')
            logging.info(f'Error: {filename} image was not downloaded')
            return False
    except IOError as e:
        logging.error(f'Error while downloading firmware: {e}')
        return False


def get_device_hardware_revision():
    return (4, 6)


def version_compatible(latest_version, device_version):
    """Check device version compatible (latest firmware device settings version need to be lessthan or equal to
     current device version) """
    device_version = get_device_hardware_revision()
    latest_version = retrieve_firmware_available()

    if latest_version[0] <= device_version[0]:

        if latest_version[1] <= device_version[1]:
            return True

    return False


def program_firmware(firmware_image):
    return True


def reboot():
    print('Device is Rebooted successfully')
    logging.info('Device is Rebooted successfully')
    pass


# Main code for OTA sequence flow
if __name__ == '__main__':
    if connect():
        print('Connected to local tomcat server')
        logging.info('Connected to local tomcat server')
        latest_firmware = retrieve_firmware_available()
        current_firmware = get_device_firmware_revision()
        if latest_firmware > current_firmware:
            firmware_image = download_firmware()
            if firmware_image:
                print('OTA update is available')
                logging.info('OTA update is available')
                hardware_revision = get_device_hardware_revision()
                #version compatibility checking
                if version_compatible(latest_firmware, hardware_revision):

                    if program_firmware(firmware_image):
                        reboot()

                        print('OTA firmware is Updated Successfully to device')
                        logging.info('OTA firmware is Updated Successfully to device')
                else:
                    print('OTA update failed due to incompatible hardware revision')
                    logging.error('OTA update failed: Incompatible hardware revision')
            else:
                print('Failed to download firmware')
                logging.error('OTA update failed: Failed to download firmware')
        else:
            print('No OTA update available')
            logging.info('OTA update not available')
    else:
        print('Failed to connect to device')
        logging.error('OTA update failed: Failed to connect to device')

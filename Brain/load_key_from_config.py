import configparser

config = configparser.ConfigParser()
config.read('Config/config.ini')

#This Method will load the key from config file
def getConfigKey(keyName):
    return config.get('api_keys', keyName)
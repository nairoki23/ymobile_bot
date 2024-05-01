import ymobile
import json
config_file = open("./config.json")
config = json.load(config_file)
config_file.close()

PhoneNumber=config["PhoneNumber"]
password=config["PassWord"]
discord_token = config["discord_token"]
print(PhoneNumber)
print(password)

ymobile.get_info(PhoneNumber,password)
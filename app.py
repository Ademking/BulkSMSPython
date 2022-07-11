# BulkSMSPython v1.0
# By: Adem Kouki
# Github: https://github.com/Ademking/BulkSMSPython
# FB: https://facebook.com/Ademkouki.Officiel
# 15/10/2018

import os
import subprocess
import sys
import time
import re


# test if substring exists in string
def found(text, substring):
    if text.find(substring) != -1:
        return True
    else:
        return False


# excute cmd and return response
def cmd_res(cmd):
    a = os.popen(cmd).read()
    return a


# excute cmd without return
def cmd(cmd):
    os.system(cmd)


# check if device connected
def device_ready():
    a = cmd_res("adb devices").count("device")
    if a == 2:
        # print('Device Ready')
        return True
    else:
        # print('No Device Found! Please plug your device')
        return False


# check android version
def android_version():
    a = cmd_res("adb shell getprop ro.build.version.release")
    print(f"version={a}")
    if found(a, "8."):
        return "Android Oreo"
    elif found(a, "7."):
        return "Android Nougat"
    elif found(a, "6."):
        return "Android Marshmallow"
    elif found(a, "5."):
        return "Android Lollipop"
    elif found(a, "10"):
        return "Android 10"
    else:
        print("your device isn't compatible. Your device must be Android 5+")
        sys.exit()


# Clear the screen
def cls():
    subprocess.call("cls", shell=True)


# Read from txt file
def readnumbers():
    tel_array = []
    try:
        with open("numbers.txt") as my_file:
            for line in my_file:
                tel_array.append(line.strip())
            return tel_array
    except FileNotFoundError:
        print("numbers.txt Not Found!")
        sys.exit()


# Get SMS Body from txt file
def getSMSBody():
    try:
        with open("message.txt", "r") as myfile:
            data = open("message.txt", "r").read()
            return data
    except FileNotFoundError:
        print("numbers.txt Not Found!")
        sys.exit()


# Replace space with "\ "
def formatSMS(SMS):
    newSMS = re.escape(SMS.replace("\n", " "))
    return newSMS


# Main
def main():

    cls()

    if device_ready():

        print("=" * 60)
        print("Android SMS Sender")
        print("=" * 60)
        print("Your Android Version : " + android_version())
        print("=" * 60)
        time.sleep(2)

        # array of numbers
        numbers_arr = readnumbers()
        if len(numbers_arr) == 0:
            print(
                "\n[Error] : Your list is empty ! Please check your list in numbers.txt"
            )
            sys.exit()
        SMS = formatSMS(getSMSBody())
        if SMS == "":
            print(
                "\n[Error] : Your SMS Message is empty! Please check your message in message.txt"
            )
            sys.exit()
        counter = 0
        for number in numbers_arr:
            print(f"android_version={android_version()}")
            print(f"numbers_arr={numbers_arr}")
            if android_version() == "Android Oreo":
                counter += 1
                print("(" + str(counter) + ") Sending SMS to " + number)
                a = cmd_res(
                    'adb shell service call isms 7 i32 0 s16 "com.android.mms.service" s16 "'
                    + number
                    + '" s16 "null" s16 "'
                    + SMS
                    + '" s16 "null" s16 "null"'
                )
                time.sleep(2)
            elif android_version == "Android Nougat":
                counter += 1
                print("(" + str(counter) + ") Sending SMS to " + number)
                a = cmd_res(
                    'adb shell service call isms 7 i32 1 s16 "com.android.mms" s16 "'
                    + number
                    + '" s16 "null" s16 "'
                    + SMS
                    + '" s16 "null" s16 "null"'
                )
                time.sleep(2)
            elif android_version == "Android Marshmallow":
                counter += 1
                print("(" + str(counter) + ") Sending SMS to " + number)
                a = cmd_res(
                    'adb shell service call isms 7 i32 1 s16 "com.android.mms" s16 "'
                    + number
                    + '" s16 "null" s16 "'
                    + SMS
                    + '" s16 "null" s16 "null"'
                )
                time.sleep(2)
            elif android_version == "Android Lollipop":
                counter += 1
                print("(" + str(counter) + ") Sending SMS to " + number)
                a = cmd_res(
                    'adb shell service call isms 9 s16 "com.android.mms" s16 "'
                    + number
                    + '" s16 "null" s16 "'
                    + SMS
                    + '" s16 "null" s16 "null"'
                )
                time.sleep(2)
            elif android_version() == "Android 10":
                counter += 1
                print("(" + str(counter) + ") Sending SMS to " + number)
                a = cmd_res(
                    'adb shell service call isms 7 i32 0 s16 "com.android.mms.service" s16 "'
                    + number
                    + '" s16 "null" s16 "'
                    + SMS
                    + '" s16 "null" s16 "null"'
                )
                print(f"cmd_outptu={a}")
                if a != " Parcel(00000000    '....')":
                    raise Exception(
                        "Error sending the message, the output was" + f":{a}"
                    )
                time.sleep(2)
        print("Sending Done Successfully!")
        sys.exit()

    else:
        print(
            "\n[Error] : Please Plug Your Device.. or check if you have ADB Installed"
        )


#################################
#################################


if __name__ == "__main__":
    main()

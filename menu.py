#!python
import os
import subprocess
import time

introMessage = "Reid's Powershell Remote Control\n\nPlease Select An Item From The List or Run A Command:\n\n[1] Volume\n[2] Shutdown\n[3] Get and Set Default Audio Device\n[4] More To Come!\n[99] Quit\n\nChoose a Number and Press [ENTER]: "


def intro(message):
    while True:
        try:
            inputVarUnsanitized = input("Reid's Powershell Remote Control\n\nPlease Select An Item From The List or Run A Command:\n\n[1] Volume\n[2] Shutdown\n[3] Get and Set Default Audio Device\n[4] More To Come!\n[99] Quit\n\nChoose a Number and Press [ENTER]: ")
            inputVarIntro = inputVarUnsanitized
            inputVarString = str(inputVarIntro)
            if (inputVarString.casefold() == "exit" or inputVarString.casefold() == "quit" or int(inputVarIntro) == int(99)):
                exit()
            elif (int(inputVarIntro) == int(1)):
                volume()
            elif (int(inputVarIntro) == int(2)):
                shutdown("Set Shutdown Timer in Minutes: ")
            elif (int(inputVarIntro) == int(3)):
                audioDevice("Commands: (1)Current, (2)List, or (3)Set\nPlease Enter A Command: ")

            else:
                print("Invalid Input. Please Try Again.\n")
                time.sleep(1)
                os.system('powershell.exe clear')
                intro(introMessage)
        except ValueError:
            os.system('powershell.exe clear')
            print("Invalid Input. Please Try Again.\n")
            intro(introMessage)
        else: 
            return
            break

def volume():
    currentDeviceRaw = subprocess.getoutput('powershell.exe Get-AudioDevice -Playback').replace("\n", " : ")
    currentDevice = currentDeviceRaw.split(" : ")
    currentDeviceName = currentDevice[9]
    currentVolume = subprocess.getoutput('powershell.exe Get-AudioDevice -PlaybackVolume')
    currentVolumeString = currentVolume.replace("%", "")
    currentVolumeFloat = float(currentVolumeString)
    currentVolumeInt = int(currentVolumeFloat)
    print("\nThe current device playing audio is: "+currentDeviceName)
    print("The current volume is: "+currentVolume)
    inputVar1Unsanitized = input("\nEnter A Command: ")
    inputVar1 = inputVar1Unsanitized.strip()
    try:
        if inputVar1.casefold() == "volume up" or inputVar1.casefold() == "volume increase" or inputVar1.casefold() == "up":
            increaseVolume = currentVolumeFloat + float(5)
            os.system('powershell.exe Set-AudioDevice -PlaybackVolume '+str(increaseVolume))
            print("Volume Increased Default Value of 5")
            time.sleep(2)
        elif inputVar1.casefold() == "volume down" or inputVar1.casefold() == "volume decrease" or inputVar1.casefold() == "down":
            DecreaseVolume = currentVolumeFloat - float(5)
            os.system('powershell.exe Set-AudioDevice -PlaybackVolume '+str(DecreaseVolume))
            print("Volume Decreased Default Value of 5")
            time.sleep(2)
        elif (inputVar1.casefold() == "exit"):
            exit()
        elif (int(inputVar1) <= int(100) and int(inputVar1) >= int(0)):
            if (int(currentVolumeInt) < int(inputVar1)):
                os.system('powershell.exe Set-AudioDevice -PlaybackVolume '+str(inputVar1))
                print("Increased Volume From: " + str(currentVolumeInt) + " to " + str(inputVar1))
                time.sleep(2)
            elif (int(currentVolumeInt) > int(inputVar1)):
                os.system('powershell.exe Set-AudioDevice -PlaybackVolume '+str(inputVar1))
                print("Decreased Volume From: " + str(currentVolumeInt) + " to " + str(inputVar1))
                time.sleep(2)
            else:
                print("Volume Unchanged")
                time.sleep(2)
        else:
            print("Volume Unchanged")
            time.sleep(2)
    except ValueError:
        print("Invalid Command. (Hint: Try entering a number between 0-100 or volume up or down)")
        volume()
    else:
        intro(introMessage)
        return


def shutdown(message):
    while True:
        try:
            inputVar2Unsanitized = input(message)
            inputVar2 = float(inputVar2Unsanitized)
            inputVar2Seconds = inputVar2 * float(60)
            if (inputVar2 >= 0):
                os.system('shutdown -s -t '+str(int(inputVar2Seconds)))
        except ValueError:
            print("Not a number! Try Again.")
            continue
        else:
            return inputVar2Unsanitized
            break


def audioDevice(message):
    currentDevice = subprocess.getoutput('powershell.exe Get-AudioDevice -Playback')
    allDevices = subprocess.getoutput('powershell.exe Get-AudioDevice -list')
    print("Current Device: "+currentDevice)
    while True:
        try:
            inputVar3Unsanitizerd = input(message)
            inputVar3Int = int(inputVar3Unsanitizerd)
            inputVar3Str = str(inputVar3Unsanitizerd)
            print(inputVar3Str)
            if (inputVar3Int == int(1)):
                print("Current Device: \n"+currentDevice)
                continue
            elif (inputVar3Int == int(2)):
                print("Device List: \n"+allDevices)
                continue
            elif (inputVar3Int == int(3)):
                print("Device List: \n"+allDevices)
                inputVar3_1 = input("Please Enter the index number of the device you would like to set as default: ")
                if (int(inputVar3_1) >= int(1)):
                    os.system('powershell.exe Set-AudioDevice -Index '+str(inputVar3_1))
                    newCurrentDevice = subprocess.getoutput('powershell.exe Get-AudioDevice -Playback')
                    print("Set Default Audio Device to "+newCurrentDevice)
                else:
                    print("ERROR!")
        except ValueError:
            print("Not A Valid Command. Try Again.")
            continue
        else:
            return inputVar3Str
            break

intro(introMessage)
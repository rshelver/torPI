import os
import subprocess
import time

version = "1.0"

w = open("/home/pi/torPI/config.txt", "w+")
w.close()
g = open("/home/pi/torPI/config.txt", "r")




def intro():
    print("-=-=-=-=-= TorPI =-=-=-=-=-")
    print("version: " + version)
    print("developed by Mutiny27")
def clear():
    os.system("clear")

def install():
    cprint("[X] Tor not installed", "red")
    installTor = input("Would you like to install tor? Y/N: ")
    if installTor == "y":
        os.system("sudo apt-get -y install tor")
        intitializeTor()

    if installTor == "n":
        print("Goodbye...")
        time.sleep(3)
        quit()

def intitializeTor():

    process = subprocess.Popen(["service tor status"], stdout=subprocess.PIPE, shell=True)
    checkTor = process.communicate()[0]
    if not b'Active:' in checkTor:
        install()

    cprint("[+] Starting Tor", "green")
    os.system("sudo service tor start")
    process = subprocess.Popen(["curl http://icanhazip.com/"], stdout=subprocess.PIPE, shell=True)
    rawIP = process.communicate()[0]

    process2 = subprocess.Popen(["torify curl http://icanhazip.com/"], stdout=subprocess.PIPE, shell=True)
    torIP = process2.communicate()[0]

    if rawIP != torIP:
        cprint("[+] Tor connection successfully established", "green")

    else:
        cprint("[X] Tor connection unsuccessful", "red")
        cprint("[X] Retrying...", "red")
        intitializeTor()

def getTorIP():
    process = subprocess.Popen(["curl http://icanhazip.com/"], stdout=subprocess.PIPE, shell=True)
    rawIP = process.communicate()[0]

    process2 = subprocess.Popen(["torify curl http://icanhazip.com/"], stdout=subprocess.PIPE, shell=True)
    torIP = process2.communicate()[0]

    if rawIP != torIP and torIP != b'':
        torIP = bytes.decode(torIP, "utf-8")
        return torIP

    else:
        rawIP = bytes.decode(rawIP, "utf-8")
        return rawIP



def cprint(text, color):
    if color == "red":
        print("\033[1;31;40m" + text)
    if color == "green":
        print("\033[1;32;40m" + text)
    if color == "blue":
        print("\033[1;34;40m" + text)



clear()
intro()

intitializeTor()



process = subprocess.Popen("service tor status".split(), stdout=subprocess.PIPE)
output = process.communicate()[0]

#print(output)
if b'Active: active' in output:
    cprint("[+] tor started", "green")

if not b'Active: acitve' in output:
    intitializeTor()

startLoop = True

while startLoop:
    raw_ip = getTorIP()
    process = subprocess.Popen("service tor status".split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    clear()
    cprint("-=-=-=-=-= TorPI =-=-=-=-=-", "blue")
    if b'Active: active' in output:
        cprint("[+] Tor Status: Active", "green")
        cprint("[IP]: " + raw_ip, "blue")
    if b'Active: inactive' in output:
        cprint("[X] Tor Status: Inactive", "red")
        cprint("[IP]: " + raw_ip, "blue")


    cprint("\n[1] stop tor", "green")
    cprint("[2] restart tor", "green")
    if b'Active: active' in output:
        cprint("[3] Torify terminal", "green")

    if b'Active: inactive' in output:
        cprint("[99] Start tor", "green")

    cprint("[00] Config", "green")
    cprint("[0] Quit", "green")

    mainChoice = input("\033[1;34;40mPlease Enter one of the options: ")



    if mainChoice == "1":
        if b'Active: inactive' in output:
            cprint("[X] unable to stop tor (tor isn't running)", "red")
            input("Press Enter to Continue...")
        else:
            cprint("[X] stopping tor...", "red")
            os.system("sudo service tor stop")
            torStop = True
            while torStop:
                process = subprocess.Popen("service tor status".split(), stdout=subprocess.PIPE)
                output = process.communicate()[0]

                if b'Active: inactive' in output:
                    cprint("[+] Tor stopped", "green")
                    input("Press Enter to Continue...")
                    torStop = False

    if mainChoice == "2":
        if b'Active: inactive' in output:
            cprint("[X] unable to restart tor (tor isn't running)", "red")
            input("Press Enter to Continue...")
        else:
            cprint("[X] Restarting tor...", "red")
            os.system("sudo service tor restart")
            cprint("[+] Tor restarted", "green")
            input("Press Enter to Continue...")

    if mainChoice == "3":
        cmd_input = input("Please enter the command you wish to run: ")
        os.system("torify " + cmd_input)
        input("Press Enter to Continue...")
        with open('/home/pi/torPI/config.txt') as f:
            if 'restartTerminal: y' in f.read():
                print("test terminal")
                os.system("sudo service tor restart")
                getTorIP()

    if mainChoice == "99":
        cprint("[+] Starting tor...", "green")
        torStart = True
        os.system("sudo service tor start")
        while torStart:
            process = subprocess.Popen("service tor status".split(), stdout=subprocess.PIPE)
            output = process.communicate()[0]
            if b'Active: active' in output:
                cprint("[+] Tor Started", "green")
                input("Press Enter to Continue...")
                torStart = False

    if mainChoice == "00":
        f = open("/home/pi/torPI/config.txt", "w+")

        restartSupport = input("Have tor restart after every torify command. [Y/N]: ")
        if restartSupport.lower() == "y":

            f.write("restartTerminal: y")
        else:
            f.write("restartTerminal: n")

        input("Press Enter to restart program...")
        f.close()
        quit()

    if mainChoice == "0":
        quit()
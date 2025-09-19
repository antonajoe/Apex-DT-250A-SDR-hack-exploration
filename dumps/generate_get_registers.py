# generates a .vbs script that opens putty.exe, 
# loads a serial config to access the ApexDTV debug console,
# and runs the 'rrc' command for every register address in the output of 'rlkup *.*'
# 'rrc' stands for 'read register in C', 
# it reads the register value and outputs C code that will write the value
# Example:
#           ZMon>rrc 0x48500000 0x48500004
#           WriteTLReg (FIRST_BEETLE_REG,
#               REGFIELD(GENCLK_GLOBAL_CTRL_TRP_STC_CLOCK_SRC,1));  
#
# the generated script runs one command every 60 seconds,
# this is to ensure that each command has time to complete
#
# Putty Settings:
# 
#    Connection Type: Serial
#    Serial Line: open device manager in Windows and search for your COM port
#    Speed: 115200       
# 
#    ### MAKE SURE LOGGING IS ENABLED ###
# 
#    In Putty side panel under Session --> Logging 'Session logging'
#    select 'All session output' 
#    set your desired log name and location
#    
#    back under 'Session' --> 'Saved sessions' enter 'ApexDTV' and select 'Save' 
#
#    you can try speeding it up by modifying the '60000' to soemhing lower like '30000' 
#    or maybe even '20000' 
#
#    there are roughly 1400 registers so it takes about a day at '60000' if runs fully...
#
#    in my case attempting to read certain blocks of registers reboot the system,
#    I don't know if this always happens or has something to do with my box.
#    I will be testing other boxes and will modify this script to exclude registers 
#    that are confirmed to cause reboots. 


import pandas as pd

df = pd.read_csv(r'rlkup.csv', sep= ' ')

print(df.head())
print()
addrs = df['ADDRESS'].values

with open("get_registers.vbs", "w") as file:
    file.write('set WshShell = WScript.CreateObject("WScript.Shell")'+'\n')
    file.write('WshShell.Run "putty.exe -load ApexDTV"'+'\n')

    for i in range(0,len(addrs)):
        file.write("WScript.Sleep 1000"+'\n')
        file.write('WshShell.SendKeys "~"'+'\n')
        file.write("WScript.Sleep 60000"+'\n')
        cmd = 'WshShell.SendKeys "rrc ' + str(addrs[i]) + " " + str(addrs[i+1]) + '"'
        file.write(cmd+'\n')
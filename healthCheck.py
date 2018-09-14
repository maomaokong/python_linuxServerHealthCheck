#! /usr/bin/python

#########################################################################################
#
# Linux Server Health Check
# Created by    Desmond Teoh, no right reserved.
# Date:         7 January 2017
# Version:      1.0
# Objective:    The script will check the server average CPU and Memory Utilisation
#               and send email to recipients.
#
#########################################################################################

import os
import datetime
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

lsFromAddr = 'abc@def.com'
lsToAddr = 'mno@pqr.com'
msg = MIMEMultipart()
msg['From'] = lsFromAddr
msg['To'] = lsToAddr
msg['Subject'] = 'Server Health Check Report'

lsServerName = os.uname()[1].upper()
llCPU_Uti = round(float(os.popen('''
                                grep 'cpu ' /proc/stat 
                                | awk '{usage = ($2 + $4) * 100 / ($2 + $4 + $5)} END {print usage}' 
                                ''').readline()), 2)
llMem_Uti = round(float(os.popen('''
                                free -m | grep Mem: 
                                | awk '{mem} = ($3 / $2) * 100 END {print mem}'
                                ''').readline()), 2)

if (llCPU_Uti >= 80 or llMem_Uti >= 80):
    lbSendEmail = 1
    lsBgColor = 'red'
else:
    lbSendEmail = 0
    lsBgColor = 'blue'

lsOutputReport = """
<HTML>
<HEAD>
    <TITLE>Server Health Check Report</TITLE>
</HEAD>
<BODY background-color:peachbuff>
    <H2><font color='#99000' face='Microsoft Tai le'>Server Health Check Report</font></H2>
    <table border=1 cellpadding=0 cellspacing=0>
        <tr bgcolor=gray align=center>
            <td><b>Server Name</b></td>
            <td><b>Avg.CPU Utilisation</b></td>
            <td><b>Memory Utilisation</b></td>
        </tr>
        <tr bgcolor={0}>
            <td>{1}</td>
            <td>{2}</td>
            <td>{3}</td>            
        </tr>
    </table>
</BODY>
</HTML>
""".format(lsBgColor, lsServerName, llCPU_Uti, llMem_Uti)
msg.attach(MIMEText(lsOutputReport, 'html'))

# print HTML Report

if (lbSendEmail == 1):
    server = smtplib.SMTP('{SMTP Server Name}')
    server.sendmail(lsFromAddr, lsToAddr, msg.as_string())
    server.quit()
    print("{0} - The Health Check Report sent!!".format(datetime.datetime.now()))
else:
    print("{0} - The Health Check Report failed to send out!!".format(datetime.datetime.now()))
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
import datetime as dt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def main():
    from_addr = 'abc@def.com'
    to_addr = 'mno@pqr.com'
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = 'Server Health Check Report'

    server_name = os.uname()[1].upper()
    cpu_uti = round(float(os.popen('''
                                    grep 'cpu ' /proc/stat | awk '{usage = ($2 + $4) * 100 / ($2 + $4 + $5)} END {print usage}' 
                                    ''').readline()), 2)
    mem_uti = round(float(os.popen('''
                                    free -m | grep Mem: | awk '{mem = ($3 / $2) * 100} END {print mem}'
                                    ''').readline()), 2)

    if cpu_uti >= 80 or mem_uti >= 80:
        send_email = True
        bg_color = 'red'
    else:
        send_email = False
        bg_color = 'blue'

    report_output = """
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
    """.format(bg_color, server_name, cpu_uti, mem_uti)
    msg.attach(MIMEText(report_output, 'html'))

    if send_email:
        server = smtplib.SMTP('{SMTP Server Name}')
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
        print("{0} - The Health Check Report sent!!".format(dt.datetime.now()))
    else:
        print("{0} - The Health Check Report not required!!".format(dt.datetime.now()))


if __name__ == '__main__':
    main()

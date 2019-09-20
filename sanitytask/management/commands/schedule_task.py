import datetime
import smtplib
from email.mime.text import MIMEText

from django.core.management.base import BaseCommand

from sanitytask.models import Check, CheckTask

h_user = """
<head></head>
<body>
<table class="m_3340458643124832238main" style="border-radius:4px;font-size:16px;color:#2f2936;border-collapse:separate;border-spacing:0;max-width:700px;font-family:&quot;Lato&quot;,&quot;Helvetica Neue&quot;,helvetica,sans-serif;border:1px solid #c7d0d4;padding:0;width:100%;font-weight:300;margin:15px auto;background-color:#fff">
  <tbody><tr style="font-weight:300">
    <td style="padding:0;font-weight:300;margin:0;text-align:center">
      <div class="m_3340458643124832238header" style="padding:23px 0;font-size:14px;font-weight:300;border-bottom:1px solid #dee7eb">
        <div class="m_3340458643124832238container" style="padding:0 20px;max-width:600px;font-weight:300;margin:0 auto;text-align:left">

<div style="padding-right: 30px; padding-left: 30px; margin-top: 40px; margin-bottom: 30px;">
    <p><img src="http://fdctech.com/images/logo-fdc.png" style="height: 36px;"></p>
    <p style="line-height:1.4"><span style="font-size:24px;"><font color="434245" face="helvetica"><strong>Hello {}</strong></font></span></p>
    <p style="line-height:1.5"><span style="font-size:17px;"><font color="434245" face="helvetica">You have tasks today.</font></span></p>
    <p style="line-height:1.5"><span style="font-size:17px;"><font color="434245" face="helvetica">You have to follow the link, and carry out the checks. Checks should be conducted until 10 am.</font></span></p>
    <p style="line-height:1.5"><span style="font-size:17px;"><font color="434245" face="helvetica">Your today tasks:</font></span></p>
"""
h_task = """
<li style="line-height:1.5"><span style="font-size:12px;"><font color="434245" face="helvetica">For company: {} ,Task: {}.</font></span></li>"""

h_endblock = """   
    
    <p style="padding-top:15px; padding-bottom:15px"><span style="cursor: pointer"><a href="http://who-is-on-duty-today.fdctech.com/" target="_blank"><button class="sm_auto_width sm_block button_link" style="cursor: pointer; min-width: 234px; border: 13px solid #005ab9; border-radius: 4px; background-color: #005ab9; font-face: helvetica; font-size: 16px; color: #ffffff; display: inline-block; text-align: center; vertical-align: top; text-decoration: none !important; "><strong>Start the check</strong></button></a></span></p>
    <p style="line-height:1.5"><span style="font-size:17px;"><font color="434245" face="helvetica">Have a nice day</font></span></p>
    <p style="line-height:1.5"><span style="font-size:17px;"><font color="434245" face="helvetica">The Forex Development Team</font></span><br> &nbsp;</p>
</div>
<hr size=".5px">
<div style="padding-right: 17px; padding-left: 30px; margin-top: 40px; margin-bottom: 30px; text-align: center">
    <font color="434245" face="helvetica">&nbsp;</font>
    <font color="A0A0A2" face="helvetica" style="font-size: 15px;">Made by </font>
    <font color="565759" face="helvetica" style="font-size: 15px;">FDC</font>
    <font face="helvetica"> </font>
</div>

</body>
</tbody></table>
"""


def get_shift(weekday):
    days_list = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    tmp = 'Shift.objects.filter({}=1)'.format(days_list[weekday])
    shifts = eval(tmp)
    user_set = set()

    for shift in shifts:
        user_set.add(shift.user)
        print (shift.checkgroup.client)
        tasks = CheckTask.objects.filter(check_group=shift.checkgroup)
        for task in tasks:
            Check.objects.create(date=datetime.datetime.today(), result=0, hidden_result=False, check_task_id=task.id,
                                 user_id=shift.user.id)

    try:
        server = smtplib.SMTP('gmail-smtp-in.l.google.com:25')
        server.ehlo()
    except:
        print 'Something went wrong...'

    for user in user_set:
        msg_temp = h_user.format(user)
        tmp = 'Shift.objects.filter({}=1).filter(user=user)'.format(days_list[weekday], )
        checkgroup_for_user = eval(tmp)
        for checkgroup in checkgroup_for_user:
            tasks_name = CheckTask.objects.filter(check_group=checkgroup.checkgroup)
            for task_name in tasks_name:
                msg_temp += h_task.format(checkgroup.checkgroup.client.name, task_name.name_task)
        msg_temp += h_endblock
        msg = MIMEText(msg_temp, 'html')

        msg['Subject'] = '[SanityChecker] Active task'
        msg['From'] = "SanityChecker"
        msg['To'] = user.email
        server.sendmail("SanityChecker@forexdevelopment.com", user.email, msg.as_string())
    server.quit()


class Command(BaseCommand):
    def handle(self, **options):
        day_week = datetime.datetime.today().weekday()
        get_shift(day_week)

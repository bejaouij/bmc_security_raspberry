# coding: utf-8

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

FROM = "noreply.bmc.contact@gmail.com"
PASSWORD = "nikleta69"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

def notifySuspectActivity(user_email):
	SUBJECT = "Activité suspecte détectée sur le dispositif nom du dispositif"
	MESSAGE = "Le dispositif nom du dispositif a détecté une activité suspecte. Rendez vous sur votre espace personnel pour confirmer ou infirmer cet évènement."

	msg = MIMEMultipart()
	msg['From'] = FROM
	msg['To'] = user_email
	msg['Subject'] = SUBJECT

	msg.attach(MIMEText(MESSAGE))

	mailserver = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
	mailserver.starttls()
	mailserver.login(FROM, PASSWORD)
	mailserver.sendmail(FROM, user_email, msg.as_string())
	mailserver.quit()

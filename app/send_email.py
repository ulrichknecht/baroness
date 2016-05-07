import smtplib
import database
# import email
# from email.mime.text import MIMEText
# from email.MIMEText import MIMEText
import user

def send_email(recipient, subject, body):
    gmail_user = 'bier1baroness'
    gmail_pwd = 'test11test11'
    FROM = 'bier1baroness@gmail.com'
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = u"Content-Type: text/plain; charset=utf-8\nFrom: Baroness <%s>\nTo: %s\nSubject: %s\n\n%s" % (FROM, recipient, SUBJECT, TEXT)
    message = message.encode('utf-8')

    # message = msg.as_string()
    print message
    try:
        server = smtplib.SMTP("smtp.gmail.com:587")
        #server.set_debuglevel(1)
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, recipient, message)
        server.quit()
        print 'Mail was sent to %s' % recipient

    except:
        print "Failed to send mail to %s" %recipient

def send_emails(body, subject, users):
    FROM = 'bier1baroness@gmail.com'

    for user in users:
        debt = database.get_debt(user.name)
        subject_parsed = parse_email(subject, user, debt)
        body_parsed = parse_email(body, user, debt)
        send_email(user.email, subject_parsed, body_parsed)




def parse_email(text, u, dept):

    text = text.replace('%%longname%%', u.longname)
    text = text.replace('%%dept%%', str(dept))

    if text.find('%%if_is_black%%', 0, text.__len__()):
        start = text.find('%%if_is_black%%', 0, text.__len__())
        end = text.find('%%end_if_is_black%%')

        if not u.isblack:
            text = text.replace(text[start:end], '')
        text = text.replace('%%if_is_black%%', '')
        text = text.replace('%%end_if_is_black%%', '')

    return text

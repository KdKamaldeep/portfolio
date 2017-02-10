import os
from onlineportfolio.settings import PROJECT_ROOT
from django.core.mail import send_mail
import sendgrid
import json
from django.core.signing import Signer

def send_verification_email(user):
    try:
        API_USER = 'parmjeet.pk'
        API_KEY = 'roar@dude1'
        signer = Signer()
        encrypteduserid = signer.sign(user.id)

        mail_to = user.email
        subject = 'Email Verification!'
        mail_from = 'parmjeet@ameotech.com'

        sg = sendgrid.SendGridClient(API_USER, API_KEY)

        plaintext = "xcvxcv"
        htmlbody = "vxvxv"

        message = sendgrid.Mail()
        message.add_filter('templates', 'enable', '1')
        message.add_filter('templates', 'template_id', '14a1d552-5805-40f5-902f-6bb587a6a47f')

        message.add_to(mail_to)
        message.add_substitution('[%first_name%]', user.first_name)
        message.add_substitution('[%last_name%]', user.last_name)
        message.add_substitution('[%verifyemail-url%]','http://localhost:8000/account/verifyemail/?id={0}'.format(encrypteduserid))
        message.set_subject(subject)
        message.set_html(htmlbody)
        message.set_text(plaintext)
        message.set_from(mail_from)

        status, msg = sg.send(message)

        print "HTTP STATUS", status

        msg = json.loads(msg)
    except Exception as e:
        raise e

def send_welcome_email(user):
    try:
        API_USER = 'parmjeet.pk'
        API_KEY = 'roar@dude1'
        signer = Signer()
        encrypteduserid = signer.sign(user.id)

        mail_to = user.email
        subject = 'Welcome {0} {1}!'.format(user.first_name,user.last_name)
        mail_from = 'parmjeet@ameotech.com'

        sg = sendgrid.SendGridClient(API_USER, API_KEY)

        plaintext = "xcvxcv"
        htmlbody = "vxvxv"

        message = sendgrid.Mail()
        message.add_filter('templates', 'enable', '1')
        message.add_filter('templates', 'template_id', 'b428616f-f29f-4896-8de5-725c6126b0a4')

        message.add_to(mail_to)
        message.add_substitution('[%first_name%]', user.first_name)
        message.add_substitution('[%last_name%]', user.last_name)
        message.set_subject(subject)
        message.set_html(htmlbody)
        message.set_text(plaintext)
        message.set_from(mail_from)

        status, msg = sg.send(message)

        print "HTTP STATUS", status

        msg = json.loads(msg)
    except Exception as e:
        raise e

def change_status_email(sender,teamname,recipient):
    try:
        API_USER = 'parmjeet.pk'
        API_KEY = 'roar@dude1'
        signer = Signer()
        encrypteduserid = signer.sign(sender.id)

        print recipient.email;
        print teamname;
        print sender.first_name;
        print sender.last_name;
        mail_to = recipient.email
        subject = 'Change Of {0} Status !'.format(teamname)
        mail_from = 'parmjeet@ameotech.com'

        sg = sendgrid.SendGridClient(API_USER, API_KEY)

        message = sendgrid.Mail()
        message.add_filter('templates', 'enable', '1')
        message.add_filter('templates', 'template_id', 'b428616f-f29f-4896-8de5-725c6126b0a4')

        message.add_to(mail_to)
        message.add_substitution('[%first_name%]', sender.first_name)
        message.add_substitution('[%last_name%]', sender.last_name)
        message.set_subject(subject)
        message.set_from(mail_from)

        status, msg = sg.send(message)

        print "HTTP STATUS", status

        msg = json.loads(msg)
    except Exception as e:
        raise e

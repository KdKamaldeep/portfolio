import os
from onlineportfolio.settings import PROJECT_ROOT
from django.core.mail import send_mail
from sendgrid import sendgrid

def sendverificationemail(user):

    sg = sendgrid.SendGridAPIClient(apikey ="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")

    message = sendgrid.Email()
    message.add_to('Parm <parmjeet@ameotech.com>')
    message.set_subject('Example')
    message.set_html('Body')
    message.set_text('Body')
    message.set_from('Doe John <doe@email.com>')

    # This next section is all to do with Template Engine

    # You pass substitutions to your template like this
    message.add_substitution('-thing_to_sub-', 'Hello! I am in a template!')

    # Turn on the template option
    message.add_filter('templates', 'enable', '1')

    # Tell SendGrid which template to use
    message.add_filter('templates', 'template_id', 'TEMPLATE_20160915110621035')

    # Get back a response and status
    status, msg = sg.send(message)



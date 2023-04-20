from __future__ import print_function

import os
from pprint import pprint

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

'''
Website Bot Diff

Made with <3 by Toby Chow[link to github]

You are currently tracking these links:
<link> on <date>
<link> on <date>
<link> on <date>

There has been a change to the following page(s):
<link>

Thank you for using my bot, have a nice day!

_____

Feel free to leave a star on my Github[github]

Template url:
https://my.sendinblue.com/template/RQxov1dhjN5CHaWr43DsOEPKByhdHas9DGGK4Qyy.xffe.okSNUjWAph
#1
'''


def test_email():
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.environ.get("SENDINBLUE_KEY")

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    sender = {"name": "Website Bot Diff", "email": "website.bot.diff@gmail.com"}
    to = [{"email": "tobychow98@gmail.com", "name": "Toby Chow"}]
    headers = {"Some-Custom-Name": "unique-id-1234"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, template_id=1, sender=sender)

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

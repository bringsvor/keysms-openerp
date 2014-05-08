
{
    "name": "KeySMS Client",
    "version": "1.0",
    "depends": ["base"],
    "author": "Bringsvor Consulting AS",
    'images': ['images/sms.jpeg', 'images/gateway.jpeg', 'images/gateway_access.jpeg','images/client.jpeg','images/send_sms.jpeg'],
    "description": """
This is a client for the Norwegian SMS service keysms.no. You will have to register there to obtain an
APIKEY that needs to be configured in OpenERP.

This OpenERP module borows heavily from smsclient.
    """,
    "website": "http://www.bringsvor.com",
    "category": "Tools",
    "demo": [],
    "data": [
#        "security/groups.xml",
#        "security/ir.model.access.csv",
        "keysms_view.xml",
###        "serveraction_view.xml",
#        "smsclient_wizard.xml",
#        "smsclient_data.xml",
#        "wizard/mass_sms_view.xml",
###        "partner_sms_send_view.xml",
        'parameters.xml',
    ],
    "active": True,
    "installable": True,
}

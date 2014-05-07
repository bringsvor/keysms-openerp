from KeySMS import KeySMS

__author__ = 'tbri'


from openerp.osv import fields, osv
from openerp.osv import orm, fields
import logging

_logger = logging.getLogger('smsclient')

"""
class stock_config_settings(osv.osv_memory):
    _name = 'stock.config.settings'
    _inherit = 'res.config.settings'
"""


class KeySMSConfig(osv.osv_memory):
    _name = "keysms.configuration"
    _inherit = ['res.config.settings']




    _columns = {
        'apikey' : fields.char('API Key',
                               help = 'Enter API key from keysms.no'),
        'userid' : fields.char('User ID',
                                 help = 'User name (mobile number)')
    }
"""
    def send_sms(self, cr, uid, message, receivers, context = None):
        # Find config
        config_ids = self.search(cr, uid, [], context)

        assert len(config_ids) == 1
        for cfg in self.browse(cr, uid, config_ids, context = context):
            keySms = KeySMS()
            keySms.auth(cfg.userId, cfg.apiKey)
            response = keySms.sms(message, receivers)
            if not response['ok']:
                raise 'Error while sending SMS to %s : %s' % (repr(receivers), repr(response))
                """
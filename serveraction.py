__author__ = 'tbri'

from openerp.osv import orm, fields

_logger = logging.getLogger('smsclient')

class ServerAction(orm.Model):
    """
    Possibility to specify the SMS Gateway when configure this server action
    """
    _inherit = 'ir.actions.server'

    _columns = {
        'apikey' : fields.char('API Key',
                               help = 'Enter API key from keysms.no'),
        'userName' : fields.char('User Name',
                                 help = 'User name (mobile number)')
    }

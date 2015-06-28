from KeySMS import KeySMS

__author__ = 'tbri'

from openerp import models, fields, api, _
from urllib import urlencode, quote as quote
import logging

# Taken from email_template

_logger = logging.getLogger(__name__)

try:
    # We use a jinja2 sandboxed environment to render mako templates.
    # Note that the rendering does not cover all the mako syntax, in particular
    # arbitrary Python statements are not accepted, and not all expressions are
    # allowed: only "public" attributes (not starting with '_') of objects may
    # be accessed.
    # This is done on purpose: it prevents incidental or malicious execution of
    # Python code that may break the security of the server.
    from jinja2.sandbox import SandboxedEnvironment
    mako_template_env = SandboxedEnvironment(
        block_start_string="<%",
        block_end_string="%>",
        variable_start_string="${",
        variable_end_string="}",
        comment_start_string="<%doc>",
        comment_end_string="</%doc>",
        line_statement_prefix="%",
        line_comment_prefix="##",
        trim_blocks=True,               # do not output newline after blocks
        autoescape=True,                # XML/HTML automatic escaping
    )
    mako_template_env.globals.update({
        'str': str,
        'quote': quote,
        'urlencode': urlencode,
    })
except ImportError:
    _logger.warning("jinja2 not available, templating features will not work!")

class sms_template(models.Model):
    _name = "keysms.template"
    _description = 'SMS Templates'
    _order = 'name'

    name = fields.Char('Name')
    model_id = fields.Many2one('ir.model', 'Applies to', help="The kind of document with with this template can be used")
    model = fields.Char(string='Related Document Model', related='model_id.model',
                                size=128, select=True, store=True, readonly=True)
    lang = fields.Char('Language',
                            help="Optional translation language (ISO code) to select when sending out an email. "
                                 "If not set, the english version will be used. "
                                 "This should usually be a placeholder expression "
                                 "that provides the appropriate language code, e.g. "
                                 "${object.partner_id.lang.code}.",
                            placeholder="${object.partner_id.lang.code}")
    body = fields.Text('Body', translate=True, help="Text version of the message (placeholders may be used here)")

    def render(self, record):
        #template = self.browse(cr, uid, template_id, context)
        #t#emplate_str = tools.ustr(template.body)

        user = None # self.pool.get('res.users').browse(cr, uid, uid, context=context)
        context = self._context

        variables = {
                'object': record,
                'user': user,
                'ctx': context,     # context kw would clash with mako internals
            }


        template_str = self.body #TODO Possibly add translation.
        result = mako_template_env.from_string(template_str).render(variables)
        print "RESULT RENDER", result
        return result


    def get_paths(self, cr, uid, keysms):
        proxy = self.pool.get('ir.config_parameter')
        apikey = proxy.get_param(cr, uid, 'keysms_apikey')
        userid = proxy.get_param(cr, uid, 'keysms_userid')
        print "APIKEY", apikey, userid
        keysms.auth(userid, apikey)


    def send_sms(self, message, receivers):
        # Find config
        #config_ids = self.search(cr, uid,  [], context=context)

        #assert len(config_ids) == 1
        #for cfg in self.browse(cr, uid, config_ids, context = context):
        keySms = KeySMS()
        self.get_paths(keySms)
        #keySms.auth(cfg.userId, cfg.apiKey)
        response = keySms.sms(message, receivers)
        if not response['ok']:
            raise Exception('Error while sending SMS to %s : %s' % (repr(receivers), repr(response)))

    @api.one
    def render_and_send(self, record, receivers):
        message = self.render(record)
        print "MESSAGE", message
        self.send_sms(message, receivers)
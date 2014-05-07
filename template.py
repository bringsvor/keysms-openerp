__author__ = 'tbri'

from openerp.osv import osv, fields
from openerp import tools
from openerp.tools.translate import _
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

class sms_template(osv.osv):
    _name = "keysms.template"
    _description = 'SMS Templates'
    _order = 'name'

    _columns = {
        'name': fields.char('Name'),
        'model_id': fields.many2one('ir.model', 'Applies to', help="The kind of document with with this template can be used"),
        'model': fields.related('model_id', 'model', type='char', string='Related Document Model',
                                size=128, select=True, store=True, readonly=True),
        'lang': fields.char('Language',
                            help="Optional translation language (ISO code) to select when sending out an email. "
                                 "If not set, the english version will be used. "
                                 "This should usually be a placeholder expression "
                                 "that provides the appropriate language code, e.g. "
                                 "${object.partner_id.lang.code}.",
                            placeholder="${object.partner_id.lang.code}"),
        'body': fields.text('Body', translate=True, help="Text version of the message (placeholders may be used here)"),
        }

    def render(self, cr, uid, template, model, res_id, context=None):
        template_str = tools.ustr(template.body)
        record = None
        if res_id:
            record = self.pool.get(model).browse(cr, uid, res_id, context=context)
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)

        variables = {
                'object': record,
                'user': user,
                'ctx': context,     # context kw would clash with mako internals
            }


        result = mako_template_env.from_string(template_str).render(variables)
        print "RESULT RENDER", result
        return result
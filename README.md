keysms-openerp
==============

OpenERP module to integrate with the keysms.no API.

Currently the module only supports programmatic invocation.

After you deploy you have to configure two parameters:

Settings -> Parameters -> System Parameters

The parameter keysms_userid should be your userid, and the keysms_apikey should be your apikey (from keysms.no).

Then you need a template:



`<record id="my_sms_template" model="keysms.template">
    <field name="name">Reminder SMS</field>
    <field name="mobile_to">${object.mobile|safe}</field>
    <field name="lang">${object.lang}</field>
    <field name="model_id" ref="base.model_res_partner"/>
    <field name="auto_delete" eval="True"/>
    <field name="body"><![CDATA[Hello ${object.name},]]></field>
</record>`

TODO:

Add buttons in the partner form to send SMS.
Clean up the menus, they don't work right now.

Author:

Torvald B. bringsvor <bringsvor@bringsvor.com>
Contact us if you have a need for customizations or developments.
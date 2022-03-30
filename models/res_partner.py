from odoo import api, fields,models


class Partner(models.Model):
    _inherit = 'res.partner'
    
    is_pegawaibakery = fields.Boolean(string='Pegawai Bakery', default=False)
    is_customerbakery = fields.Boolean(string='Customer Bakery', default=False)    

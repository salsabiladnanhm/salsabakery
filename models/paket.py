from odoo import api, fields, models


class Paket(models.Model):
    _name = 'bakery.paket'
    _description = 'Bundle Package'

    name = fields.Char(string='Nama Paket')
    paketmenudetail_ids = fields.One2many(
        comodel_name='bakery.paketmenudetail', 
        inverse_name='paket_id', 
        string='Detail Menu')

    stok = fields.Integer(string='Stok Paket')
    
    potongan_paket = fields.Integer(string='Diskon')
    
    total_harga_paket = fields.Integer(compute='_compute_total', string='Total Harga Paket')
    
    @api.depends('paketmenudetail_ids')
    def _compute_total(self):
        for record in self:
            a = sum(self.env['bakery.paketmenudetail'].search([('paket_id', '=', record.id)]).mapped('harga'))
            record.total_harga_paket = a - record.potongan_paket
    
class PaketMenuDetail(models.Model):
    _name = 'bakery.paketmenudetail'
    _description = 'Detail Menu Paket'

    paket_id = fields.Many2one(comodel_name='bakery.paket', string='Paket')
    menu_paket_id = fields.Many2one(comodel_name='bakery.menu', string='Daftar Menu')

    name = fields.Char(string='Name')
    qty = fields.Integer(string='Quantity')
    harga_satuan = fields.Integer(compute='_compute_harga_satuan', string='Harga Satuan')

    @api.depends('menu_paket_id')
    def _compute_harga_satuan(self):
        for record in self:
            record.harga_satuan = record.menu_paket_id.harga

    harga = fields.Integer(compute='_compute_harga', string='Total Harga')

    @api.depends('qty','harga_satuan')
    def _compute_harga(self):
        for record in self:
           record.harga = record.harga_satuan * record.qty

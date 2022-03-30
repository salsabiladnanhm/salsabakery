from odoo import api, fields, models
from odoo.exceptions import ValidationError

class Order(models.Model):
    _name = 'bakery.order'
    _description = 'Order Pesanan' 
    
    name = fields.Char(string='Kode Order', required=True)
    tanggal_pesan = fields.Datetime('Tanggal Pemesanan',default=fields.Datetime.now())
    
    nama_pemesan = fields.Many2one(
        comodel_name='res.partner', 
        string='Nama Pemesan', 
        domain=[('is_customerbakery','=', True)])

    jenis_pembayaran = fields.Selection(string='Jenis Pembayaran', selection=[('transfer_bank','Transfer Bank'), ('tunai','Tunai'), ('ewallet','E-wallet')])
    
    menu_ids = fields.One2many(
        comodel_name='bakery.ordermenudetail', 
        inverse_name='orderm_id', 
        string='Detail Menu')
    
    paket_ids = fields.One2many(
        comodel_name='bakery.orderpaketdetail', 
        inverse_name='orderp_id', 
        string='Detail Paket')
    
    total_harga_order = fields.Integer(compute='_compute_total', string='Total')

    @api.depends('menu_ids')
    def _compute_total(self):
        for record in self:
            a = sum(self.env['bakery.ordermenudetail'].search([('orderm_id', '=', record.id)]).mapped('harga'))
            b = sum(self.env['bakery.orderpaketdetail'].search([('orderp_id', '=', record.id)]).mapped('harga'))
            record.total_harga_order = a + b

class OrderMenuDetail(models.Model):
    _name = 'bakery.ordermenudetail'
    _description = 'Detail Menu Order'

    orderm_id = fields.Many2one(comodel_name='bakery.order', string='Order')
    menu_order_id = fields.Many2one(
        comodel_name='bakery.menu', 
        string='Detail Menu', 
        domain=[('stok','>','0')])
    
    name = fields.Char(string='Name')
    harga_satuan = fields.Integer(compute='_compute_harga_satuan', string='Harga Satuan')
    
    @api.depends('menu_order_id')
    def _compute_harga_satuan(self):
        for record in self:
            record.harga_satuan = record.menu_order_id.harga

    qty = fields.Integer(string='Quantity')
    
    @api.constrains('qty')
    def _check_stokm(self):
        for record in self:
            cek_stokm = self.env['bakery.menu'].search([('stok', '<',record.qty),('id', '=',record.id)])
            if cek_stokm:
                raise ValidationError("Stok menu yang dipilih tidak cukup")

    harga = fields.Integer(compute='_compute_harga', string='Total Harga')

    @api.depends('qty','harga_satuan')
    def _compute_harga(self):
        for record in self:
           record.harga = record.harga_satuan * record.qty

    @api.model
    def create(self,vals):
        record = super(OrderMenuDetail, self).create(vals) 
        if record.qty:
            self.env['bakery.menu'].search([('id','=',record.menu_order_id.id)]).write({'stok':record.menu_order_id.stok-record.qty})
            return record

class OrderPaketDetail(models.Model):
    _name = 'bakery.orderpaketdetail'
    _description = 'Detail Paket Order'

    orderp_id = fields.Many2one(comodel_name='bakery.order', string='Order')
    paket_order_id = fields.Many2one(
        comodel_name='bakery.paket', 
        string='Detail Paket', 
        domain=[('stok','>','0')])
    
    name = fields.Char(string='Name')
    
    harga_satuan = fields.Integer(compute='_compute_harga_satuan', string='Harga Satuan')
    @api.depends('paket_order_id')
    def _compute_harga_satuan(self):
        for record in self:
            record.harga_satuan = record.paket_order_id.total_harga_paket

    qty = fields.Integer(string='Quantity')
    
    @api.constrains('qty')
    def _check_stokp(self):
        for record in self:
            cek_stokp = self.env['bakery.paket'].search([('stok', '<',record.qty),('id', '=',record.id)])
            if cek_stokp:
                raise ValidationError("Stok paket yang dipilih tidak cukup")

    harga = fields.Integer(compute='_compute_harga', string='Total Harga')

    @api.depends('qty','harga_satuan')
    def _compute_harga(self):
        for record in self:
           record.harga = record.harga_satuan * record.qty
    
    @api.model
    def create(self,vals):
        record = super(OrderPaketDetail, self).create(vals) 
        if record.qty:
            self.env['bakery.paket'].search([('id','=',record.paket_order_id.id)]).write({'stok':record.paket_order_id.stok-record.qty})
            return record
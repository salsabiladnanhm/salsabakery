from odoo import api, fields, models


class Menu(models.Model):
    _name = 'bakery.menu'
    _description = 'Daftar Menu Bakery'

    name = fields.Char(string='Nama Menu')
    harga = fields.Integer(string='Harga')
    kategori = fields.Selection(string='Kategori', selection=[('roti','Roti'), ('kue','Kue'), ('pastry','Pastry')])
    stok = fields.Integer(string='Stok')
    deskripsi = fields.Char(string='Deskripsi')
    img = fields.Binary(string='Gambar')
    
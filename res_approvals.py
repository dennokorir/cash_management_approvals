from openerp import models, fields, api

class approval_entry(models.Model):
    _inherit = 'approval.entry'

    bank_transfer_id = fields.Many2one('cash.management.bank.transfer.header')

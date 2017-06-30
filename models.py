from openerp import models, fields, api

class approval_entry(models.Model):
    _inherit = 'approval.entry'

    bank_transfer_id = fields.Many2one('cash.management.bank.transfer.header')
    payment_header_id = fields.Many2one('cash.management.payment.header')
    petty_cash_id = fields.Many2one('cash.management.petty.cash.header')



class bank_transfer_header(models.Model):
    _inherit = 'cash.management.bank.transfer.header'

    current_approver = fields.Many2one('res.users')
    show = fields.Boolean(compute = 'toggle_buttons')

    @api.one
    @api.depends('current_approver')
    def toggle_buttons(self):
        if self.current_approver.id == self.env.user.id:
            self.show = True
        else:
            pass

class payment_voucher(models.Model):
    _inherit = 'cash.management.payment.header'

    current_approver = fields.Many2one('res.users')
    show = fields.Boolean(compute = 'toggle_buttons')

    @api.one
    @api.depends('current_approver')
    def toggle_buttons(self):
        if self.current_approver.id == self.env.user.id:
            self.show = True
        else:
            pass


class petty_cash(models.Model):
    _inherit = 'cash.management.petty.cash.header'

    current_approver = fields.Many2one('res.users')
    show = fields.Boolean(compute = 'toggle_buttons')

    @api.one
    @api.depends('current_approver')
    def toggle_buttons(self):
        if self.current_approver.id == self.env.user.id:
            self.show = True
        else:
            pass

    @api.one
    def reset_to_draft(self):
        self.state = 'open'

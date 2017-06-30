from openerp import models, fields, api
from openerp.exceptions import ValidationError

'''
Copy, paste and modify where necessary.
Ensure you have the following functions:
::>>SendApprovalRequest
::>>checkAdditionalApprovers-->should not change much for subsequent models
::>>CancelApprovalRequest
::>>ApproveApprovalRequest
::>>rejectApprovalRequest
'''

class bank_transfer_approvals(models.Model):
    _inherit = 'cash.management.bank.transfer.header'

    approvers = fields.Integer(compute = 'count_approvers')
    approval_entries = fields.One2many('approval.entry','bank_transfer_id')
    #state = fields.Selection([('open',"Open"),('pending',"Pending Approval"),('approved',"Approved"),('rejected',"Rejected")], default = 'open')

    @api.one
    @api.depends('approval_entries')
    def count_approvers(self):
        self.approvers = len(self.approval_entries)

    @api.one
    def checkAdditionalApprovers(self,document_type,document_no):
        #init
        approval_template = self.env['approval.template'].search([('document_type','=',document_type)])
        additional_approvers = self.env['additional.approvers']
        approval_entry = self.env['approval.entry']
        #continue
        approvers = {}

        if len(approval_template)<=0:
            raise ValidationError("No approval template found for Document Type: "+ document_type)

        else:
            approvers = additional_approvers.search([('template_id','=',approval_template.id)])

            if len(approvers)<=0:
                raise ValidationError("No additional approvers for document type:"+document_type)

            else:
                sequence = 0
                for approver in approvers:
                    sequence +=1
                    status = ''
                    if sequence == 1:
                        status = 'open'
                    else:
                        status = 'created'
                    self.env['approval.entry'].create({'document_type':document_type,'document_no':document_no,'document_id':self.id,'sequence':sequence,'approver_id':approver.approver_id.id,'sender_id':self.env.user.id,'status':status,'sender':self.env.user.id,'approver':approver.approver_id.id,'model':'cash.management.bank.transfer.header'})
        self.approveApprovalRequest()


    @api.one
    def sendApprovalRequest(self):
        if self.state != 'open':
            raise ValidationError("Status must be open to send request")

        document_type = 'bank_transfer'
        #template_name = 'member_app'

        self.checkAdditionalApprovers(document_type,self.name)


    @api.one
    def cancelApprovalRequest(self):#this is standard. Dont modify for subsequent models
        document_type = 'bank_transfer'
        if self.state != 'pending':
            raise ValidationError("Status must be pending to cancel request")

        approval_entry = self.env['approval.entry'].search([('document_no','=',self.name),('document_type','=',document_type),('status','!=','rejected')])
        if len(approval_entry)>0:
            #raise ValidationError("Found approval entries to cancel")
            approval_entry.write({'status':'cancelled'})
            self.state = 'open'
            self.current_approver = ''

    @api.one
    def approveApprovalRequest(self):
        #init
        document_type = 'bank_transfer'
        approval_entry = self.env['approval.entry'].search([('document_no','=',self.name),('status','=','open'),('approver_id','=',self.env.user.id),('document_type','=',document_type)])
        approval_entry.write({'status':'approved'})
        next_approval_entry = self.env['approval.entry'].search([('document_no','=',self.name),('status','in',['created','open'])])
        #next_approval_entry.sorted(key=lambda r: r.sequence)
        if len(next_approval_entry)>0:
            next_approval_entry = min(next_approval_entry)
            next_approval_entry.status = 'open'
            self.state = 'pending'
            self.current_approver = next_approval_entry.approver.id
            return False
        else:
            self.state = 'approved'
            return True

    @api.one
    def rejectApprovalRequest(self):
        document_type = 'bank_transfer'
        if self.state != 'pending':
            raise ValidationError("Status must be pending to reject request")
        #init

        approval_entry = self.env['approval.entry'].search([('document_no','=',self.name),('document_type','=',document_type),('status','!=','cancelled')])


        if len(approval_entry)>0:
            #raise ValidationError('Found approval entries to cancel')
            approval_entry.write({'status':'rejected'})
            self.state = 'rejected'
            self.current_approver = ''



class payment_voucher_approvals(models.Model):
    _inherit = 'cash.management.payment.header'


    approvers = fields.Integer(compute = 'count_approvers')
    approval_entries = fields.One2many('approval.entry','payment_header_id')
    #state = fields.Selection([('open',"Open"),('pending',"Pending Approval"),('approved',"Approved"),('rejected',"Rejected")], default = 'open')

    @api.one
    @api.depends('approval_entries')
    def count_approvers(self):
        self.approvers = len(self.approval_entries)

    @api.one
    def checkAdditionalApprovers(self,document_type,document_no):
        #init
        approval_template = self.env['approval.template'].search([('document_type','=',document_type)])
        additional_approvers = self.env['additional.approvers']
        approval_entry = self.env['approval.entry']
        #continue
        approvers = {}

        if len(approval_template)<=0:
            raise ValidationError("No approval template found for Document Type: "+ document_type)

        else:
            approvers = additional_approvers.search([('template_id','=',approval_template.id)])

            if len(approvers)<=0:
                raise ValidationError("No additional approvers for document type:"+document_type)

            else:
                sequence = 0
                for approver in approvers:
                    sequence +=1
                    status = ''
                    if sequence == 1:
                        status = 'open'
                    else:
                        status = 'created'
                    self.env['approval.entry'].create({'document_type':document_type,'document_no':document_no,'document_id':self.id,'sequence':sequence,'approver_id':approver.approver_id.id,'sender_id':self.env.user.id,'status':status,'sender':self.env.user.id,'approver':approver.approver_id.id,'model':'cash.management.payment.header'})
        self.approveApprovalRequest()


    @api.one
    def sendApprovalRequest(self):
        if self.state != 'open':
            raise ValidationError("Status must be open to send request")

        document_type = 'payment_voucher'
        self.checkAdditionalApprovers(document_type,self.name)


    @api.one
    def cancelApprovalRequest(self):#this is standard. Dont modify for subsequent models
        document_type = 'payment_voucher'
        if self.state != 'pending':
            raise ValidationError("Status must be pending to cancel request")

        approval_entry = self.env['approval.entry'].search([('document_no','=',self.name),('document_type','=',document_type),('status','!=','rejected')])
        if len(approval_entry)>0:
            approval_entry.write({'status':'cancelled'})
            self.state = 'open'
            self.current_approver = ''

    @api.one
    def approveApprovalRequest(self):
        #init
        document_type = 'payment_voucher'
        approval_entry = self.env['approval.entry'].search([('document_no','=',self.name),('status','=','open'),('approver_id','=',self.env.user.id),('document_type','=',document_type)])
        approval_entry.write({'status':'approved'})
        next_approval_entry = self.env['approval.entry'].search([('document_no','=',self.name),('status','in',['created','open'])])
        #next_approval_entry.sorted(key=lambda r: r.sequence)
        if len(next_approval_entry)>0:
            next_approval_entry = min(next_approval_entry)
            next_approval_entry.status = 'open'
            self.state = 'pending'
            self.current_approver = next_approval_entry.approver.id
            return False
        else:
            self.state = 'approved'
            return True

    @api.one
    def rejectApprovalRequest(self):
        document_type = 'payment_voucher'
        if self.state != 'pending':
            raise ValidationError("Status must be pending to reject request")
        approval_entry = self.env['approval.entry'].search([('document_no','=',self.name),('document_type','=',document_type),('status','!=','cancelled')])


        if len(approval_entry)>0:
            approval_entry.write({'status':'rejected'})
            self.state = 'rejected'
            self.current_approver = ''

class petty_cash_approvals(models.Model):
    _inherit = 'cash.management.petty.cash.header'


    approvers = fields.Integer(compute = 'count_approvers')
    approval_entries = fields.One2many('approval.entry','petty_cash_id')
    #state = fields.Selection([('open',"Open"),('pending',"Pending Approval"),('approved',"Approved"),('rejected',"Rejected")], default = 'open')

    @api.one
    @api.depends('approval_entries')
    def count_approvers(self):
        self.approvers = len(self.approval_entries)

    @api.one
    def checkAdditionalApprovers(self,document_type,document_no):
        #init
        approval_template = self.env['approval.template'].search([('document_type','=',document_type)])
        additional_approvers = self.env['additional.approvers']
        approval_entry = self.env['approval.entry']
        #continue
        approvers = {}

        if len(approval_template)<=0:
            raise ValidationError("No approval template found for Document Type: "+ document_type)

        else:
            approvers = additional_approvers.search([('template_id','=',approval_template.id)])

            if len(approvers)<=0:
                raise ValidationError("No additional approvers for document type:"+document_type)

            else:
                sequence = 0
                for approver in approvers:
                    sequence +=1
                    status = ''
                    if sequence == 1:
                        status = 'open'
                    else:
                        status = 'created'
                    self.env['approval.entry'].create({'document_type':document_type,'document_no':document_no,'document_id':self.id,'sequence':sequence,'approver_id':approver.approver_id.id,'sender_id':self.env.user.id,'status':status,'sender':self.env.user.id,'approver':approver.approver_id.id,'model':'cash.management.petty.cash.header'})
        self.approveApprovalRequest()


    @api.one
    def sendApprovalRequest(self):
        if self.state != 'open':
            raise ValidationError("Status must be open to send request")
        document_type = 'petty_cash'
        self.checkAdditionalApprovers(document_type,self.name)


    @api.one
    def cancelApprovalRequest(self):#this is standard. Dont modify for subsequent models
        document_type = 'petty_cash'
        if self.state != 'pending':
            raise ValidationError("Status must be pending to cancel request")

        approval_entry = self.env['approval.entry'].search([('document_no','=',self.name),('document_type','=',document_type),('status','!=','rejected')])
        if len(approval_entry)>0:
            approval_entry.write({'status':'cancelled'})
            self.state = 'open'
            self.current_approver = ''

    @api.one
    def approveApprovalRequest(self):
        #init
        document_type = 'petty_cash'
        approval_entry = self.env['approval.entry'].search([('document_no','=',self.name),('status','=','open'),('approver_id','=',self.env.user.id),('document_type','=',document_type)])
        approval_entry.write({'status':'approved'})
        next_approval_entry = self.env['approval.entry'].search([('document_no','=',self.name),('status','in',['created','open'])])
        #next_approval_entry.sorted(key=lambda r: r.sequence)
        if len(next_approval_entry)>0:
            next_approval_entry = min(next_approval_entry)
            next_approval_entry.status = 'open'
            self.state = 'pending'
            self.current_approver = next_approval_entry.approver.id
            return False
        else:
            self.state = 'approved'
            return True

    @api.one
    def rejectApprovalRequest(self):
        document_type = 'petty_cash'
        if self.state != 'pending':
            raise ValidationError("Status must be pending to reject request")
        approval_entry = self.env['approval.entry'].search([('document_no','=',self.name),('document_type','=',document_type),('status','!=','cancelled')])


        if len(approval_entry)>0:
            approval_entry.write({'status':'rejected'})
            self.state = 'rejected'
            self.current_approver = ''


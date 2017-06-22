# -*- coding: utf-8 -*-
from openerp import http

# class CashManagementApprovals(http.Controller):
#     @http.route('/cash_management_approvals/cash_management_approvals/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cash_management_approvals/cash_management_approvals/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cash_management_approvals.listing', {
#             'root': '/cash_management_approvals/cash_management_approvals',
#             'objects': http.request.env['cash_management_approvals.cash_management_approvals'].search([]),
#         })

#     @http.route('/cash_management_approvals/cash_management_approvals/objects/<model("cash_management_approvals.cash_management_approvals"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cash_management_approvals.object', {
#             'object': obj
#         })
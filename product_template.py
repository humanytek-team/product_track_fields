# -*- coding: utf-8 -*-


from openerp import models, fields, api, _
from datetime import datetime, timedelta, date
#import time

class product_template(models.Model):
	_inherit = 'product.template'

	@api.multi
	def _compute_first_entry(self):
		#print '_compute_first_entry'
		#PurchaseOrder = self.env['Purchase'].search([('state', '=', 'done'),\
			#('order_line.product_id', '=', self.id)])
		list_prod_id=[]
		ProductProduct =  self.env['product.product'].search([('product_tmpl_id','=',self.id)])
		if ProductProduct:
			for prod in ProductProduct:
				list_prod_id.append(prod.id)
		StockPicking = self.env['stock.picking'].search([('state', '=', 'done'),('picking_type_id.name','=',('Receipts','Recepciones')),('pack_operation_product_ids.product_id', 'in', (list_prod_id))],limit=1, order='date_done asc')
		#PurchaseOrder = self.env['purchase.order'].search([('order_line.product_id', '=', self.id)],limit=1, order='date_order asc')
		if StockPicking:
			for rec in StockPicking:
				self.first_entry_date = rec.date_done
				#break
		return

	@api.multi
	def _compute_last_entry(self):
		#print '_compute_last_entry'
		#PurchaseOrder = self.env['Purchase'].search([('state', '=', 'done'),\
			#('order_line.product_id', '=', self.id)])
		list_prod_id=[]
		ProductProduct =  self.env['product.product'].search([('product_tmpl_id','=',self.id)])
		if ProductProduct:
			for prod in ProductProduct:
				list_prod_id.append(prod.id)
		StockPicking = self.env['stock.picking'].search([('state', '=', 'done'),('picking_type_id.name','=',('Receipts','Recepciones')),('pack_operation_product_ids.product_id', 'in', (list_prod_id))],limit=1, order='date_done desc')
		#PurchaseOrder = self.env['purchase.order'].search([('order_line.product_id', '=', self.id)],limit=1, order='date_order desc')
		if StockPicking:
			for rec in StockPicking:
				self.last_entry_date = rec.date_done
				#break
		return

	@api.multi
	def _compute_last_qty(self):
		#print '_compute_last_qty'
		#PurchaseOrder = self.env['Purchase'].search([('state', '=', 'done'),\
			#('order_line.product_id', '=', self.id)])
		result=0
		list_prod_id=[]
		ProductProduct =  self.env['product.product'].search([('product_tmpl_id','=',self.id)])
		if ProductProduct:
			for prod in ProductProduct:
				list_prod_id.append(prod.id)
		StockPicking = self.env['stock.picking'].search([('state', '=', 'done'),('picking_type_id.name','=',('Receipts','Recepciones')),('pack_operation_product_ids.product_id', 'in', (list_prod_id))],limit=1, order='date_done desc')
		#PurchaseOrder = self.env['purchase.order'].search([('order_line.product_id', '=', self.id)],limit=1, order='date_order desc')
		if StockPicking:
			for rec in StockPicking:
				for rec_line in rec.pack_operation_product_ids:
					print 'LIST_PROD_ID: ', list_prod_id, rec_line.product_id

					if rec_line.product_id.id in list_prod_id:
						print 'ENTRO'
						result += rec_line.qty_done
				#break
		self.qty_last_entry = result
		return

	@api.multi
	def _compute_delivery_time_avg(self):
		#print '_compute_delivery_time_avg'
		#PurchaseOrder = self.env['Purchase'].search([('state', '=', 'done'),\
			#('order_line.product_id', '=', self.id)])
		suma_dias=0
		num=1
		average_time=0
		list_prod_id=[]
		ProductProduct =  self.env['product.product'].search([('product_tmpl_id','=',self.id)])
		if ProductProduct:
			for prod in ProductProduct:
				list_prod_id.append(prod.id)
		StockPicking = self.env['stock.picking'].search([('state', '=', 'done'),('picking_type_id.name','=',('Receipts','Recepciones')),('pack_operation_product_ids.product_id', 'in', (list_prod_id))])
		if StockPicking:
			for rec in StockPicking:
				PurchaseOrder = self.env['purchase.order'].search([('name', '=', rec.origin)],limit=1)
				if PurchaseOrder:
					# if PurchaseOrder.date_planned:
					# 	d0 = datetime.strptime(rec.date_done,"%Y-%m-%d %H:%M:%S")
					# 	d1 = datetime.strptime(PurchaseOrder.date_planned,"%Y-%m-%d %H:%M:%S")
					# 	delta = d0 - d1
					# 	suma_dias += delta.days
					if PurchaseOrder.date_received_by_supplier:
						d0 = datetime.strptime(rec.date_done,"%Y-%m-%d %H:%M:%S")
					 	d1 = datetime.strptime(PurchaseOrder.date_received_by_supplier,"%Y-%m-%d %H:%M:%S")
					 	delta = d0 - d1
					 	suma_dias += delta.days
					else:
						d0 = datetime.strptime(rec.date_done,"%Y-%m-%d %H:%M:%S")
						d1 = datetime.strptime(PurchaseOrder.date_order,"%Y-%m-%d %H:%M:%S")
						delta = d0 - d1
						suma_dias += delta.days
					num += 1

			average_time = suma_dias / num
		self.delivery_average_time = average_time
		return 

	@api.multi
	def _compute_supplier_returns(self):
		#print '_compute_delivery_time_avg'
		#PurchaseOrder = self.env['Purchase'].search([('state', '=', 'done'),\
			#('order_line.product_id', '=', self.id)])
		cant = 0
		list_prod_id=[]
		ProductProduct =  self.env['product.product'].search([('product_tmpl_id','=',self.id)])
		if ProductProduct:
			for prod in ProductProduct:
				list_prod_id.append(prod.id)
		StockPicking = self.env['stock.picking'].search([('state', '=', 'done'),('pack_operation_product_ids.product_id', 'in', (list_prod_id)),('location_dest_id.name','in',('Vendors','Proveedores'))])
		if StockPicking:
			for rec in StockPicking:
				for rec_pack in rec.pack_operation_product_ids:
					if rec_pack.product_id.id in list_prod_id:
						cant += rec_pack.qty_done
		self.supplier_returns = cant
		return

	first_entry_date = fields.Date('Fecha primera entrada', compute='_compute_first_entry', readonly=True)
	last_entry_date = fields.Date('Fecha ultima entrada', compute='_compute_last_entry', readonly=True)
	qty_last_entry = fields.Integer('Cantidad ultima entrada', compute='_compute_last_qty', readonly=True)
	delivery_average_time = fields.Float('Tiempo de entrega promedio',compute='_compute_delivery_time_avg', readonly=True)
	supplier_returns = fields.Integer('Devoluciones',compute='_compute_supplier_returns', readonly=True)
	 
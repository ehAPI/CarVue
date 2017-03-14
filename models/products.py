from openerp.osv import fields, osv

class new_product(osv.osv):

	_name = 'new.product'
	_columns = {
	#package		
			'code':fields.char('Code'),
			'name':fields.char('Name'),
	#product
			'code':fields.char('Code'),
			'name':fields.char('Name'),
			'type':fields.selection([('misc','Miscellaneous'),
				('labour','Labour'),
				('parts','Parts'),
				('oil','Oil'),
				('other','Other Fluids'),
				('wheels','Wheels & Tyres'),
				('body','Bodyworks'),
				('cons','Consumables'),
				('env','Environmental'),
				('car','carriage'),
				('sub','Sublet')],'TYPE'),
			'notes':fields.char('NOTES'),
			'track':fields.boolean('TRACKABLE INVENTORY'),
			'purchase':fields.char('PURCHASE'),
			'unit_cost':fields.char('UNIT COST'),
			'acc':fields.selection([('4200_parts','4200 Parts Purchases'),
				('4300_lab','4300 Labour Purchases')],'ACCOUNT'),
			'tax':fields.char('TAX RATE'),
			'sales':fields.char('SALES'),
			'unit_price':fields.char('UNIT PRICE'),
	}

new_product()

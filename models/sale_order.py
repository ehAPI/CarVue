from openerp.osv import fields, osv
import time 
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

class sale_order(osv.osv):

	_inherit="sale.order"
	_columns = {
	'notes':fields.text('Notes'),
	'due_in':fields.datetime('Due In'),
	'due_out':fields.datetime('Due Out'),
	'advisor':fields.many2one('res.users','Advisor',ondelete='set null'),
	'technician':fields.many2one('res.users','Technician',ondelete='set null'),
	'bay' :fields.selection([('parking','Parking'),('ramp1','Ramp 1'),('ramp2','Ramp 2')],'Bay'),
	'reference': fields.char('Reference'),
	'mile':fields.integer('Mileage In'),
	'state':fields.selection([('draft','In Progress'),
			('sent','Paused'),
			('cancel','Parts On Order'),
			('waiting_date','Parts Arrived'),
			('progress','Awaiting Authority'),
			('manual','Cleaning'),
			('shipping_except','Customer Contacted'),
			('done','Work Completed')],'Status'),
	}

sale_order()
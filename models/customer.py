from openerp.osv import fields, osv
# from datetime import datetime

class customer(osv.osv):
	_inherit = 'res.partner'

	def _show_vehicles(self, cr, uid, ids, name, args, context=None):
		res = {}
		c_ids = self.pool.get('vehicle.dashboard').search(cr,uid,[('child_ids','=',ids[0])])
		for t_id in self.browse(cr,uid,ids):
			res[t_id.id] = c_ids
		return res
	def _show_jobs(self, cr, uid, ids, name, args, context=None):
		res = {}
		c_ids = self.pool.get('job.order').search(cr,uid,[('child_ids','=',ids[0])])
		for t_id in self.browse(cr,uid,ids):
			res[t_id.id] = c_ids
		return res
	_columns = {
	'veh': fields.function(_show_vehicles, relation='vehicle.dashboard', type="one2many", string='My Vehicles'),
	'jobs': fields.function(_show_jobs, relation='job.order', type="one2many", string='My Jobs'),
	'related_user':fields.many2one('res.users','Related User'),
	'company':fields.many2one('res.users','Company',ondelete='set null'),


	}

customer()
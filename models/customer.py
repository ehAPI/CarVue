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
	_columns = {
	# 'veh' : fields.one2many('vehicle.dashboard', 'registration', 'Vehicles'),
	'veh': fields.function(_show_vehicles, relation='vehicle.dashboard', type="one2many", string='My Vehicles'),
	}


customer()

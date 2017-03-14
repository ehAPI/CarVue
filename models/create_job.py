from openerp.osv import fields, osv

class create_job(osv.osv):

	_name = 'create.job'
	_columns = {
		'name':fields.char('Vehicle ID', readonly=True),
	}

create_job()

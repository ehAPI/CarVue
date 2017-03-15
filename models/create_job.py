from openerp.osv import fields, osv
import time 


class create_job(osv.osv):

	_name = 'create.job'
	
	_columns = {
		# 'new':fields.char('New Job Card'),
		'name':fields.char('New Job Card', readonly=True),
		'notes':fields.text('Notes',size=5),
		'status':fields.selection([('due','DUE')],'STATUS'),


		'due_in':fields.datetime('DUE IN'),
		'due_out':fields.datetime('DUE OUT'),
		'advisor':fields.selection([('due','Due')],'ADVISOR'),
		
	}

create_job()


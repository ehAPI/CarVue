from openerp.osv import fields, osv
import time 
# from datetime import timedelta
# from openerp import models, fields, api, exceptions

# class Course(models.Model):
#     attendee_ids = fields.Many2many('res.partner', string="Attendees")

#     taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
#     end_date = fields.Date(string="End Date", store=True,
#         compute='_get_end_date', inverse='_set_end_date')

   

#     @api.depends('start_date', 'duration')
#     def _get_end_date(self):
#         for r in self:
#             if not (r.start_date and r.duration):
#                 r.end_date = r.start_date
#                 continue

#             # Add duration to start_date, but: Monday + 5 days = Saturday, so
#             # subtract one second to get on Friday instead
#             start = fields.Datetime.from_string(r.start_date)
#             duration = timedelta(days=r.duration, seconds=-1)
#             r.end_date = start + duration

#     def _set_end_date(self):
#         for r in self:
#             if not (r.start_date and r.end_date):
#                 continue

#             # Compute the difference between dates, but: Friday - Monday = 4 days,
#             # so add one day to get 5 days instead
#             start_date = fields.Datetime.from_string(r.start_date)
#             end_date = fields.Datetime.from_string(r.end_date)
#             r.duration = (end_date - start_date).days + 1
# Course()            


class create_job(osv.osv):

	_name = 'create.job'
	
	_columns = {
		# 'new':fields.char('New Job Card'),
		'name':fields.char('New Job Card', readonly=True),
		'notes':fields.char('NOTES'),
		'status':fields.selection([('due','Due In')],'STATUS'),
		'due_in':fields.datetime('DUE IN'),
		'due_out':fields.datetime('DUE OUT'),
		'advisor':fields.many2one('res.users','ADVISOR',ondelete='set null'),
		
	}

create_job()


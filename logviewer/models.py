from django.db import models

class PhoneRecord(models.Model):
	type = models.CharField(max_length=3)
	ext = models.IntegerField()
	trunk = models.IntegerField()
	line_number = models.IntegerField()
	incoming_ext = models.IntegerField()
	start_time = models.DateTimeField()
	duration = models.TimeField()

	#def __unicode__(self):
#		return self.duration

	def f(self):
		lists = {'type': self.type, 'ext': str(self.ext), 'trunk': str(self.trunk), 'line_number': str(self.line_number),
                 'incoming_ext': str(self.incoming_ext), 'start_time': str(self.start_time), 'duration': self.duration}
		
		return lists


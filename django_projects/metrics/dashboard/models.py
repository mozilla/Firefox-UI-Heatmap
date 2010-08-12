from django.db import models
from math import log

# Create your models here.
class Heatmap(models.Model):
	name = models.CharField(max_length=100)
	category = models.CharField(max_length=100)	
	code = models.CharField(max_length=100)		
	is_in_table = models.BooleanField()
	os = models.CharField(max_length=30)		
	skill = models.CharField(max_length=30)	
	time_on_web = models.IntegerField()	
	perc = models.FloatField()
	clicks_per_user = models.FloatField()
	clicks_per_user_median = models.FloatField()
	
	def heat_perc(self):
		normalize = log((self.perc * 100) + 1 )/ log(100)
		h = 360 * (1 - normalize)
		s = normalize * 75
		l = normalize * 50
		return "hsl(" + str(h) + "," + str(s) +"%," + str(l) + "%)"	
		
	def heat_freq(self):
		normalize = log(self.clicks_per_user + 1 )/ log(103.3) #change to MAX
		h = 360 * (1 - normalize)
		s = normalize * 75
		l = normalize * 50
		return "hsl(" + str(h) + "," + str(s) +"%," + str(l) + "%)"			
		
	def __unicode__(self):
		return 'A heatmap of id %d' % (self.id)
		
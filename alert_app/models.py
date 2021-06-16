from django.db import models

# Create your models here.

class NotifyData(models.Model):
	data = models.CharField(max_length=500,null=True,blank=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return str(self.data)
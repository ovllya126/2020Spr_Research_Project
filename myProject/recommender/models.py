from django.db import models

# Create your models here.

class User(models.Model):
	user_id = models.CharField(max_length=20, primary_key = True)
	user_name = models.CharField(max_length=50)
	user_psw = models.CharField(max_length=50)
	user_gender = models.CharField(max_length=10)
	user_state = models.CharField(max_length=20)
	user_email = models.CharField(max_length=50)

	def __str__(self):
		return self.user_id

class Session(models.Model):
	session_id = models.ForeignKey(User, on_delete=models.CASCADE)
	timestamp = models.CharField(max_length=100)
	course_id = models.CharField(max_length=40)
	category = models.CharField(max_length=5)

	def __str__(self):
		return self.session_id


class Course(models.Model):
	cour_id = models.CharField(max_length=40)
	cour_cate = models.CharField(max_length=5)

	def __str__(self):
		return self.cour_id
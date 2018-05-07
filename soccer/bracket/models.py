from django.db import models

# Create your models here.

class UserGroup(models.Model):
	name = models.CharField(max_length=30)
	userName = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	groupID = models.CharField(max_length=10)
	
	def __str__(self):
		return self.name
	

class User(models.Model):
	firstName = models.CharField(max_length=30)
	lastName = models.CharField(max_length=30)
	userName = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	points = models.IntegerField(default=0)
	group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)

	groupA1 = models.CharField(max_length=30, default="", blank=True)
	groupA2 = models.CharField(max_length=30, default="", blank=True)
	groupB1 = models.CharField(max_length=30, default="", blank=True)
	groupB2 = models.CharField(max_length=30, default="", blank=True)
	groupC1 = models.CharField(max_length=30, default="", blank=True)
	groupC2 = models.CharField(max_length=30, default="", blank=True)
	groupD1 = models.CharField(max_length=30, default="", blank=True)
	groupD2 = models.CharField(max_length=30, default="", blank=True)
	groupE1 = models.CharField(max_length=30, default="", blank=True)
	groupE2 = models.CharField(max_length=30, default="", blank=True)
	groupF1 = models.CharField(max_length=30, default="", blank=True)
	groupF2 = models.CharField(max_length=30, default="", blank=True)
	groupG1 = models.CharField(max_length=30, default="", blank=True)
	groupG2 = models.CharField(max_length=30, default="", blank=True)
	groupH1 = models.CharField(max_length=30, default="", blank=True)
	groupH2 = models.CharField(max_length=30, default="", blank=True)
	
	win1 = models.CharField(max_length=30, default="", blank=True)
	win2 = models.CharField(max_length=30, default="", blank=True)
	win3 = models.CharField(max_length=30, default="", blank=True)
	win4 = models.CharField(max_length=30, default="", blank=True)
	win5 = models.CharField(max_length=30, default="", blank=True)
	win6 = models.CharField(max_length=30, default="", blank=True)
	win7 = models.CharField(max_length=30, default="", blank=True)
	win8 = models.CharField(max_length=30, default="", blank=True)
	win9 = models.CharField(max_length=30, default="", blank=True)
	win10 = models.CharField(max_length=30, default="", blank=True)
	win11 = models.CharField(max_length=30, default="", blank=True)
	win12 = models.CharField(max_length=30, default="", blank=True)
	win13 = models.CharField(max_length=30, default="", blank=True)
	win14 = models.CharField(max_length=30, default="", blank=True)
	champion = models.CharField(max_length=30, default="", blank=True)
	third = models.CharField(max_length=30, default="", blank=True)
	
	def __str__(self):
		return self.userName
	
	
class Group(models.Model):
	name = models.CharField(max_length=20)
	winner1 = models.CharField(max_length=20, blank=True)
	winner2 = models.CharField(max_length=20, blank=True)
	
	def __str__(self):
		return self.name
	
	
class Team(models.Model):
	name = models.CharField(max_length=30, blank=True)
	ranking = models.IntegerField(default=0)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.name
		
	
class Admin(models.Model):
	firstName = models.CharField(max_length=30)
	lastName = models.CharField(max_length=30)
	userName = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	
	def __str__(self):
		return self.firstName + " " + self.lastName
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *

# Create your views here.

def index(request):
	return render(request, 'bracket/main.html',)
	
	
def createUser(request):
	return render(request, 'bracket/createUser.html',)
	
	
def userCreate(request):
	firstNameG = request.POST.get('firstName')
	lastNameG = request.POST.get('lastName')
	userNameG = request.POST.get('userName')
	passwordG = request.POST.get('password')
	groupIDG = request.POST.get('groupID')
	
	try:
		existingGroup = UserGroup.objects.get(groupID=groupIDG)
		
		try:
			existingUserName = User.objects.get(userName=userNameG)
			existing = True
		except:
			existing = False
		
		if(existing):
			return render(request, 'bracket/createUser.html', {'error_message': "USERNAME IS ALREADY BEING USED"})
		else:

			existingGroup.user_set.create(firstName=firstNameG, lastName=lastNameG, userName=userNameG, password=passwordG)
			existingGroup.save()
			
	except:
		return render(request, 'bracket/createUser.html', {'error_message': "INVALID GROUP ID"})

	return	HttpResponseRedirect(reverse('bracket:index',))
	
	
	
def createGroup(request):
	return render(request, 'bracket/createGroup.html',)
	
def groupCreate(request):
	nameG = request.POST.get('firstName')
	userNameG = request.POST.get('userName')
	passwordG = request.POST.get('password')
	groupIDG = request.POST.get('groupID')
	
	try:
		existingGroupID = UserGroup.objects.get(groupID=groupIDG)
		existing = True
	except:
		existing = False
		
	try:
		existingUserName = UserGroup.objects.get(userName=userNameG)
		existing = True
	except:
		existing = existing
		
	if(existing):
		#return HttpResponse("if")
		return render(request, 'bracket/createGroup.html', {'error_message': "GROUP ID OR USERNAME IS ALREADY BEING USED"})
	else:
		#return HttpResponse("else")
		group = UserGroup(name=nameG, userName=userNameG, password=passwordG, groupID=groupIDG)
		group.save()

		return	HttpResponseRedirect(reverse('bracket:index',))
	

def choice(request, user_id, group_id):
	person = User.objects.get(id=user_id)
	group = Group.objects.get(id=group_id)
	context = {'user': person, 'group': group}

	return render(request, 'bracket/index.html', context)
	

def submit(request, user_id, group_id):
	person = User.objects.get(id=user_id)
	group = Group.objects.get(id=group_id)
	
	name = group.name
	
	if request.POST[name + '1'] != request.POST[name + '2']:
		if name == "GroupA":
			person.groupA1 = request.POST[name + '1']
			person.groupA2 = request.POST[name + '2']
			person.save()
		elif name == "GroupB":
			person.groupB1 = request.POST[name + '1']
			person.groupB2 = request.POST[name + '2']
			person.save()
		elif name == "GroupC":
			person.groupC1 = request.POST[name + '1']
			person.groupC2 = request.POST[name + '2']
			person.save()
		elif name == "GroupD":
			person.groupD1 = request.POST[name + '1']
			person.groupD2 = request.POST[name + '2']
			person.save()
		elif name == "GroupE":
			person.groupE1 = request.POST[name + '1']
			person.groupE2 = request.POST[name + '2']
			person.save()
		elif name == "GroupF":
			person.groupF1 = request.POST[name + '1']
			person.groupF2 = request.POST[name + '2']
			person.save()
		elif name == "GroupG":
			person.groupG1 = request.POST[name + '1']
			person.groupG2 = request.POST[name + '2']
			person.save()
		elif name == "GroupH":
			person.groupH1 = request.POST[name + '1']
			person.groupH2 = request.POST[name + '2']
			person.save()
		
	else:
		return HttpResponseRedirect(reverse('bracket:choice', args=(person.id, group.id,)))
	
	return HttpResponseRedirect(reverse('bracket:choice', args=(person.id, group.id + 1)))
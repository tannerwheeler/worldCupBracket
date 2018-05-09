from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *

# Create your views here.

def index(request):
	return render(request, 'bracket/main.html',)
	
	
def createUser(request):
	return render(request, 'bracket/createUser.html',)
	
	
def adminGroups(request, admin_id):
	groups = Group.objects.all()
	admin = get_object_or_404(Admin, pk=admin_id)
	
	context = {'groups': groups, 'admin': admin}
	
	return render(request, 'bracket/adminGroups.html', context)
	
	
def addT(request, admin_id):
	admin = get_object_or_404(Admin, pk=admin_id)
	nameT = request.POST.get('Name')
	groupName = request.POST.get('group')
	rankT = request.POST.get('Rank')
	
	groups = Group.objects.all()
	
	if nameT == "" or rankT == "":
		context = {'team_error': "Please enter a group name", 'admin': admin, 'groups': groups,}
		
		return render(request, 'bracket/adminGroups.html', context,)
	
	try:
		t = Team.objects.get(name=nameT)
		
		context = {'team_error': "Team already exists", 'admin': admin, 'groups': groups,}
		
		return render(request, 'bracket/adminGroups.html', context,)
	except:
		p = Group.objects.get(name=groupName)
		p.team_set.create(name=nameT, ranking=rankT)
		p.save()
	
		context = {'team_created': "" + nameT + " was created successfully", 'admin': admin, 'groups': groups,}
	
	return render(request, 'bracket/adminGroups.html', context,)
	

def addG(request, admin_id):
	admin = get_object_or_404(Admin, pk=admin_id)
	groups = Group.objects.all()
	
	if request.POST.get('GroupName') == "":
		context = {'group_error': "Please enter a group name", 'admin': admin, 'groups': groups,}
		
		return render(request, 'bracket/adminGroups.html', context,)
	
	try:
		p = Group.objects.get(name=request.POST.get('GroupName'))
		context = {'group_error': "Group already exists", 'admin': admin, 'groups': groups,}
		
		return render(request, 'bracket/adminGroups.html', context,)
	except:
		g = Group(name=request.POST.get('GroupName'))
		g.save()
	
		context = {'group_created': "" + g.name + " was created successfully", 'admin': admin, 'groups': groups,}
	
	return render(request, 'bracket/adminGroups.html', context,)
	
	
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
	try:
		group = Group.objects.get(id=group_id)
	except:
		return	HttpResponseRedirect(reverse('bracket:index',))

	try:
		person = User.objects.get(id=user_id)
	except:
		return	HttpResponseRedirect(reverse('bracket:index',))
		
	context = {'user': person, 'group': group}

	return render(request, 'bracket/index.html', context)
	

def submit(request, user_id, group_id):
	person = User.objects.get(id=user_id)
	group = Group.objects.get(id=group_id)
	
	name = group.name
	
	if request.POST[name + '1'] != request.POST[name + '2']:
		if name == "Group A":
			person.groupA1 = request.POST[name + '1']
			person.groupA2 = request.POST[name + '2']
			person.save()
		elif name == "Group B":
			person.groupB1 = request.POST[name + '1']
			person.groupB2 = request.POST[name + '2']
			person.save()
		elif name == "Group C":
			person.groupC1 = request.POST[name + '1']
			person.groupC2 = request.POST[name + '2']
			person.save()
		elif name == "Group D":
			person.groupD1 = request.POST[name + '1']
			person.groupD2 = request.POST[name + '2']
			person.save()
		elif name == "Group E":
			person.groupE1 = request.POST[name + '1']
			person.groupE2 = request.POST[name + '2']
			person.save()
		elif name == "Group F":
			person.groupF1 = request.POST[name + '1']
			person.groupF2 = request.POST[name + '2']
			person.save()
		elif name == "Group G":
			person.groupG1 = request.POST[name + '1']
			person.groupG2 = request.POST[name + '2']
			person.save()
		elif name == "Group H":
			person.groupH1 = request.POST[name + '1']
			person.groupH2 = request.POST[name + '2']
			person.save()
		
	else:
		return HttpResponseRedirect(reverse('bracket:choice', args=(person.id, group.id,)))
	
	return HttpResponseRedirect(reverse('bracket:choice', args=(person.id, group.id + 1)))
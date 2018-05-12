from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *

# Create your views here.

def index(request):
	return render(request, 'bracket/main.html',)
	
	
def userView(request, user_id):
	person = get_object_or_404(User, pk=user_id)
	
	context = { 'user': person, }
	
	return render(request, 'bracket/bracket.html', context)
	
	
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
	
	
def bracket(request, user_id):
	try:
		person = User.objects.get(id=user_id)
	except:
		return	HttpResponseRedirect(reverse('bracket:index',))
		
	context = {'user': person,}

	return render(request, 'bracket/finish.html', context)	

	
def choice(request, user_id):
	try:
		person = User.objects.get(id=user_id)
	except:
		return	HttpResponseRedirect(reverse('bracket:index',))
	
	group = person.group.group_set.all()
		
	context = {'user': person, 'group': group}

	return render(request, 'bracket/index.html', context)
	
	
def submit(request, user_id):
	#return HttpResponse("Submit")
	person = User.objects.get(id=user_id)
	
	name = request.POST.get('group')
	
	if request.POST['1'] != request.POST['2']:
		if name == "Group A":
			person.groupA1 = request.POST['1']
			person.groupA2 = request.POST['2']
			person.save()
		elif name == "Group B":
			person.groupB1 = request.POST['1']
			person.groupB2 = request.POST['2']
			person.save()
		elif name == "Group C":
			person.groupC1 = request.POST['1']
			person.groupC2 = request.POST['2']
			person.save()
		elif name == "Group D":
			person.groupD1 = request.POST['1']
			person.groupD2 = request.POST['2']
			person.save()
		elif name == "Group E":
			person.groupE1 = request.POST['1']
			person.groupE2 = request.POST['2']
			person.save()
		elif name == "Group F":
			person.groupF1 = request.POST['1']
			person.groupF2 = request.POST['2']
			person.save()
		elif name == "Group G":
			person.groupG1 = request.POST['1']
			person.groupG2 = request.POST['2']
			person.save()
		elif name == "Group H":
			person.groupH1 = request.POST['1']
			person.groupH2 = request.POST['2']
			person.save()
		
	else:
		return HttpResponseRedirect(reverse('bracket:choice', args=(person.id,)))
	
	return HttpResponseRedirect(reverse('bracket:choice', args=(person.id,)))
	

	
def win(request, user_id):
	person = get_object_or_404(User, pk=user_id)
	
	button = request.POST.get('button')
	team = request.POST.get('team')
	
	if team != "":
		if button == "Game 1":
			person.win1 = team
		elif button == "Game 2":
			person.win2 = team
		elif button == "Game 3":
			person.win3 = team
		elif button == "Game 4":
			person.win4 = team
		elif button == "Game 5":
			person.win5 = team
		elif button == "Game 6":
			person.win6 = team
		elif button == "Game 7":
			person.win7 = team
		elif button == "Game 8":
			person.win8 = team
		elif button == "Game 9":
			person.win9 = team
		elif button == "Game 10":
			person.win10 = team
		elif button == "Game 11":
			person.win11 = team
		elif button == "Game 12":
			person.win12 = team
		elif button == "Game 13":
			if team == person.win9:
				person.win13 = person.win10
				person.loss1 = team
			else:
				person.win13 = team
				person.loss1 = person.win9
		elif button == "Game 14":
			if team == person.win11:
				person.win14 = person.win12
				person.loss2 = team
			else:
				person.win14 = team
				person.loss2 = person.win11
		elif button == "Champion":
			person.champion = team
		elif button == "Third Place":
			person.third = team
		
	person.save()
		
	return HttpResponseRedirect(reverse('bracket:bracket', args=(person.id,)))
	
	
	
def dele(request, user_id):
	person = get_object_or_404(User, pk=user_id)
	
	button = request.POST.get('button')
	
	if button == "Go Back to Game 1":
		person.win1 = ""
	elif button == "Go Back to Game 2":
		person.win2 = ""
	elif button == "Go Back to Game 3":
		person.win3 = ""
	elif button == "Go Back to Game 4":
		person.win4 = ""
	elif button == "Go Back to Game 5":
		person.win5 = ""
	elif button == "Go Back to Game 6":
		person.win6 = ""
	elif button == "Go Back to Game 7":
		person.win7 = ""
	elif button == "Go Back to Game 8":
		person.win8 = ""
	elif button == "Go Back to Game 9":
		person.win9 = ""
	elif button == "Go Back to Game 10":
		person.win10 = ""
	elif button == "Go Back to Game 11":
		person.win11 = ""
	elif button == "Go Back to Game 12":
		person.win12 = ""
	elif button == "Go Back to Game 13":
		person.win13 = ""
		person.loss1 = ""
	elif button == "Go Back to Game 14":
		person.win14 = ""
		person.loss2 = ""
	elif button == "Go Back to Champion":
		person.champion = ""
	elif button == "Go Back to Third":
		person.third = ""
	
	
	person.save()
		
	return HttpResponseRedirect(reverse('bracket:bracket', args=(person.id,)))
	
	
def adminGroups(request, userGroup_id):
	admin = get_object_or_404(UserGroup, pk=userGroup_id)
	groups = admin.group_set.all()
	
	context = {'groups': groups, 'admin': admin}
	
	return render(request, 'bracket/adminGroupsTest.html', context)
	

	
def addG(request, userGroup_id):
	admin = get_object_or_404(UserGroup, pk=userGroup_id)
	groups = admin.group_set.all()
	
	if request.POST.get('GroupName') == "":
		context = {'group_error': "Please enter a group name", 'admin': admin, 'groups': groups,}
		
		return render(request, 'bracket/adminGroupsTest.html', context,)
	
	try:
		admin.group_set.get(name=request.POST.get('GroupName'))
		context = {'group_error': "Group already exists", 'admin': admin, 'groups': groups,}
		
		return render(request, 'bracket/adminGroupsTest.html', context,)
	except:
		nameG = request.POST.get('GroupName')
	
		admin.group_set.create(name=nameG)
		admin.save()
	
		context = {'group_created': "" + str(nameG) + " was created successfully", 'admin': admin, 'groups': groups,}
	
	return render(request, 'bracket/adminGroupsTest.html', context,)
	
	
	
def addT(request, userGroup_id):
	admin = get_object_or_404(UserGroup, pk=userGroup_id)
	nameT = request.POST.get('Name')
	groupName = request.POST.get('group')
	rankT = request.POST.get('Rank')
	
	groups = admin.group_set.all()
	
	specGroup = groups.get(name=groupName)
	
	if nameT == "" or rankT == "":
		context = {'team_error': "Please enter a group name", 'admin': admin, 'groups': groups,}
		
		return render(request, 'bracket/adminGroupsTest.html', context,)
	
	try:
		t = specGroup.team_set.get(name=nameT)
		
		context = {'team_error': "Team already exists", 'admin': admin, 'groups': groups,}
		
		return render(request, 'bracket/adminGroupsTest.html', context,)
	except:
		specGroup.team_set.create(name=nameT, ranking=rankT)
		specGroup.save()
	
		context = {'team_created': "" + str(nameT) + " was created successfully", 'admin': admin, 'groups': groups,}
	
	return render(request, 'bracket/adminGroupsTest.html', context,)
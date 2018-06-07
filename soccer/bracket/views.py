from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *

# Create your views here.



###################################################################
#if request.session.get('order', 'none') == str(order_pk) or request.session.get('employee', 'False') == True:
#        wait_time = WaitTime.objects.last()
 #       order = get_object_or_404(Order, id=int(order_pk))
  #      context = {
    #        'order': order,
     #       'wait_time': wait_time
  #      }
   #     return render(request, 'restaurant/customerOrder.html', context)
    #else:
     #   return HttpResponseRedirect(reverse('restaurant:index'),)
		


		
#request.session['order'] = str(new_order.id)
#request.session.set_expiry(900)


#if request.session.get('employee', 'false') == 'true':
 #       wait_time = WaitTime.objects.last()
  #      tables = Table.objects.all()
   #     context = {
    #        'wait_time': wait_time,
     #       'tableList': tables
      #  }
       # return render(request, 'restaurant/serverPage.html', context)
    #else:
    #    return render(request, 'restaurant/login.html')
		
		
########################################################


# Main Page
def index(request):
	return render(request, 'bracket/main.html',)
	
	
def userLogin(request):
	try:
		person = User.objects.get(userName=request.POST.get('userName'))
		
		if str(person.password) != str(request.POST.get('password')):
			return HttpResponseRedirect(reverse('bracket:index',))
	except:
		return	HttpResponseRedirect(reverse('bracket:index',))
		
	request.session['userMain'] = str(person.userName + person.password)
	request.session.set_expiry(900)
		
	return HttpResponseRedirect(reverse('bracket:choice', args=(person.id,)))



def userGroupLogin(request):
	try:
		group = UserGroup.objects.get(userName=request.POST.get('userNameG'))
		
		if str(group.password) != str(request.POST.get('passwordG')):
			return HttpResponseRedirect(reverse('bracket:index',))
	except:
		return	HttpResponseRedirect(reverse('bracket:index',))
		
	request.session['userAdmin'] = str(group.userName + group.password)
	request.session.set_expiry(900)
		
	return HttpResponseRedirect(reverse('bracket:userGroupView', args=(group.id,)))
	
	
def userLogout(request):
	request.session['userMain'] = "You have been logged out"
		
	return HttpResponseRedirect(reverse('bracket:index',))
	
	
def userGroupLogout(request):
	request.session['userAdmin'] = "You have been logged out!"
		
	return HttpResponseRedirect(reverse('bracket:index',))
	
	
# User main view page
def userView(request, user_id):
	person = get_object_or_404(User, pk=user_id)

	if request.session.get('userMain', 'none') != str(person.userName + person.password):
		return HttpResponseRedirect(reverse('bracket:index',))
		
	if not person.saved:
		return HttpResponseRedirect(reverse('bracket:bracket', args=(person.id,)))
	
	
	context = { 'user': person, }
	
	return render(request, 'bracket/bracket.html', context)
	

# Page to create a User
def createUser(request):
	return render(request, 'bracket/createUser.html',)
	
# Creates a User	
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
			
			request.session['userMain'] = str(userNameG + passwordG)
			request.session.set_expiry(900)
			
	except:
		return render(request, 'bracket/createUser.html', {'error_message': "INVALID GROUP ID"})
		
	existingUserName = User.objects.get(userName=userNameG)

	return HttpResponseRedirect(reverse('bracket:choice', args=(existingUserName.id,)))
	
	
# Page to create a userGroup
def createGroup(request):
	return render(request, 'bracket/createGroup.html',)

# Creates a userGroup	
def groupCreate(request):
	nameG = request.POST.get('firstName')
	prizeG = request.POST.get('lastName')
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
		group = UserGroup(name=nameG, userName=userNameG, password=passwordG, groupID=groupIDG, prize=prizeG)
		group.save()
		
		request.session['userMain'] = str(group.userName + group.password)
		request.session.set_expiry(900)

		return HttpResponseRedirect(reverse('bracket:userGroupView', args=(group.id,)))
	

# Finishing Bracket	
def bracket(request, user_id):
	try:
		person = User.objects.get(id=user_id)
	except:
		return	HttpResponseRedirect(reverse('bracket:index',))
		
	if request.session.get('userMain', 'none') != str(person.userName + person.password):
		return HttpResponseRedirect(reverse('bracket:index',))
		
		
	context = {'user': person,}	
		
	if person.group.edit:
		if not person.saved:
			return render(request, 'bracket/finish.html', context)
			
		else:
			return HttpResponseRedirect(reverse('bracket:userView', args=(person.id,)))
			
	else:
		return HttpResponseRedirect(reverse('bracket:userView', args=(person.id,)))
		
		

def saved(request, user_id):
	person = get_object_or_404(User, pk=user_id)
	
	if request.session.get('userMain', 'none') != str(person.userName + person.password):
		return HttpResponseRedirect(reverse('bracket:index',))
	
	person.saved = True
	person.save()
		
	return HttpResponseRedirect(reverse('bracket:userView', args=(person.id,)))

		
		
		
# Finishing Bracket after Group Stage		
def bracketChange(request, user_id):
	try:
		person = User.objects.get(id=user_id)
	except:
		return	HttpResponseRedirect(reverse('bracket:index',))
		
		
	if request.session.get('userMain', 'none') != str(person.userName + person.password):
		return HttpResponseRedirect(reverse('bracket:index',))
		
	if not person.group.edit and not person.group.editBracket:
		return HttpResponseRedirect(reverse('bracket:userView', args=(person.id,)))
		
	context = {'user': person,}
	
	if person.group.edit:
		person.saved = False
		person.groupA1 = person.group.groupA1
		person.groupA2 = person.group.groupA2
		person.groupB1 = person.group.groupB1
		person.groupB2 = person.group.groupB2
		person.groupC1 = person.group.groupC1
		person.groupC2 = person.group.groupC2
		person.groupD1 = person.group.groupD1
		person.groupD2 = person.group.groupD2
		person.groupE1 = person.group.groupE1
		person.groupE2 = person.group.groupE2
		person.groupF1 = person.group.groupF1
		person.groupF2 = person.group.groupF2
		person.groupG1 = person.group.groupG1
		person.groupG2 = person.group.groupG2
		person.groupH1 = person.group.groupH1
		person.groupH2 = person.group.groupH2
		
		person.win1 = ""
		person.win2 = ""
		person.win3 = ""
		person.win4 = ""
		person.win5 = ""
		person.win6 = ""
		person.win7 = ""
		person.win8 = ""
		person.win9 = ""
		person.win10 = ""
		person.win11 = ""
		person.win12 = ""
		person.loss1 = ""
		person.loss2 = ""
		person.win13 = ""
		person.win14 = ""
		person.champion = ""
		person.third = ""
		
		person.save()
	
		return render(request, 'bracket/finish.html', context)	
	else:
		return HttpResponseRedirect(reverse('bracket:userView', args=(person.id,)))
		
		
# Make Group Stage Choices
def choice(request, user_id):
	try:
		person = User.objects.get(id=user_id)
	except:
		return	HttpResponseRedirect(reverse('bracket:index',))
		
	if request.session.get('userMain', 'none') != str(person.userName + person.password):
		return HttpResponseRedirect(reverse('bracket:index',))
	
	if person.group.edit:
		if not person.win1:
			group = person.group.group_set.all()
		
			context = {'user': person, 'group': group}

			return render(request, 'bracket/index.html', context)
		else:
			return HttpResponseRedirect(reverse('bracket:bracket', args=(person.id,)))
	else:
		return HttpResponseRedirect(reverse('bracket:userView', args=(person.id,)))
	
	
# Submits Group winner and second place choices
def submit(request, user_id):
	#return HttpResponse("Submit")
	person = User.objects.get(id=user_id)
	
	
	if request.session.get('userMain', 'none') != str(person.userName + person.password):
		return HttpResponseRedirect(reverse('bracket:index',))
	
	name = request.POST.get('group')
	
	check = "Sven is the best person ever in the world."
	
	try:
		first = request.POST['1']
	except:
		first = "Sven is the best person ever in the world."
		
	try:
		second = request.POST['2']
	except:
		second = "Sven is the best person ever in the world."
	
	if first != second:
		if name == "Group A":
			if first != "Sven is the best person ever in the world." and first != person.groupA2:
				person.groupA1 = first
			if second != "Sven is the best person ever in the world." and second != person.groupA1:
				person.groupA2 = second
			person.save()
		elif name == "Group B":
			if first != "Sven is the best person ever in the world." and first != person.groupB2:
				person.groupB1 = first
			if second != "Sven is the best person ever in the world." and second != person.groupB1:
				person.groupB2 = second
			person.save()
		elif name == "Group C":
			if first != "Sven is the best person ever in the world." and first != person.groupC2:
				person.groupC1 = first
			if second != "Sven is the best person ever in the world." and second != person.groupC1:
				person.groupC2 = second
			person.save()
		elif name == "Group D":
			if first != "Sven is the best person ever in the world." and first != person.groupD2:
				person.groupD1 = first
			if second != "Sven is the best person ever in the world." and second != person.groupD1:
				person.groupD2 = second
			person.save()
		elif name == "Group E":
			if first != "Sven is the best person ever in the world." and first != person.groupE2:
				person.groupE1 = first
			if second != "Sven is the best person ever in the world." and second != person.groupE1:
				person.groupE2 = second
			person.save()
		elif name == "Group F":
			if first != "Sven is the best person ever in the world." and first != person.groupF2:
				person.groupF1 = first
			if second != "Sven is the best person ever in the world." and second != person.groupF1:
				person.groupF2 = second
			person.save()
		elif name == "Group G":
			if first != "Sven is the best person ever in the world." and first != person.groupG2:
				person.groupG1 = first
			if second != "Sven is the best person ever in the world." and second != person.groupG1:
				person.groupG2 = second
			person.save()
		elif name == "Group H":
			if first != "Sven is the best person ever in the world." and first != person.groupH2:
				person.groupH1 = first
			if second != "Sven is the best person ever in the world." and second != person.groupH1:
				person.groupH2 = second
			person.save()
		
	else:
		return HttpResponseRedirect(reverse('bracket:choice', args=(person.id,)))
	
	return HttpResponseRedirect(reverse('bracket:choice', args=(person.id,)))
	

# Submits the winner and saves to User	
def win(request, user_id):
	person = get_object_or_404(User, pk=user_id)
	
	
	if request.session.get('userMain', 'none') != str(person.userName + person.password):
		return HttpResponseRedirect(reverse('bracket:index',))
	
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
			if str(team) == str(person.win9):
				person.win13 = person.win9
				person.loss1 = person.win10
			else:
				person.win13 = person.win10
				person.loss1 = person.win9
		elif button == "Game 14":
			if str(team) == str(person.win11):
				person.win14 = person.win11
				person.loss2 = person.win12
			else:
				person.win14 = person.win12
				person.loss2 = person.win11
		elif button == "Third Place":
			person.third = team
		elif button == "Champion":
			person.champion = team
		
	person.save()
		
	return HttpResponseRedirect(reverse('bracket:bracket', args=(person.id,)))
	
	
# Deletes the previous choice for the winners
def dele(request, user_id):
	person = get_object_or_404(User, pk=user_id)
	
	
	if request.session.get('userMain', 'none') != str(person.userName + person.password):
		return HttpResponseRedirect(reverse('bracket:index',))
	
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
	elif button == "Reselect Third":
		person.third = ""
	elif button == "Reselect Champion":
		person.champion = ""
	
	
	person.save()
		
	return HttpResponseRedirect(reverse('bracket:bracket', args=(person.id,)))
	
	
# Main view for adding teams and groups to userGroup
def adminGroups(request, userGroup_id):
	admin = get_object_or_404(UserGroup, pk=userGroup_id)
	
	if request.session.get('userAdmin', 'none') != str(admin.userName + admin.password):
		return HttpResponseRedirect(reverse('bracket:index',))
	
	groups = admin.group_set.all()
	
	context = {'groups': groups, 'admin': admin}
	
	return render(request, 'bracket/adminGroupsTest.html', context)
	

# Adds a group to a userGroup
def addG(request, userGroup_id):
	admin = get_object_or_404(UserGroup, pk=userGroup_id)
	
	if request.session.get('userAdmin', 'none') != str(admin.userName + admin.password):
		return HttpResponseRedirect(reverse('bracket:index',))
	
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
	
	
# Adds a team to a group in the userGroup
def addT(request, userGroup_id):
	admin = get_object_or_404(UserGroup, pk=userGroup_id)
	
	if request.session.get('userAdmin', 'none') != str(admin.userName + admin.password):
		return HttpResponseRedirect(reverse('bracket:index',))
	
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
	
	
# Main view for a userGroup
def userGroupView(request, userGroup_id):
	userGroup = get_object_or_404(UserGroup, pk=userGroup_id)
	
	if request.session.get('userAdmin', 'none') != str(userGroup.userName + userGroup.password):
		return HttpResponseRedirect(reverse('bracket:index',))
	
	context = { 'userGroup': userGroup, }
	
	return render(request, 'bracket/winner.html', context,)
	
# Changes value of editing for the userGroup
def userGroupEdit(request, userGroup_id):
	admin = get_object_or_404(UserGroup, pk=userGroup_id)
	
	if request.session.get('userAdmin', 'none') != str(admin.userName + admin.password):
		return HttpResponseRedirect(reverse('bracket:index',))
	
	if admin.edit:
		admin.edit = False
	else:
		admin.edit = True
		
	admin.save()
		
	return HttpResponseRedirect(reverse('bracket:userGroupView', args=(admin.id,)))
	
	
# Setting the winners of the groups
def userStage(request, userGroup_id):
	userGroup = get_object_or_404(UserGroup, pk=userGroup_id)
	
	if request.session.get('userAdmin', 'none') != str(userGroup.userName + userGroup.password):
		return HttpResponseRedirect(reverse('bracket:index',))
	
	team = request.POST.get('team')
	position = request.POST.get('position')
	
	
	if str(position) != "NOTHING" and str(team) != "NOTHING":
		if str(position) == "A1":
			userGroup.groupA1 = team;
		elif str(position) == "A2":
			userGroup.groupA2 = team;
		elif str(position) == "B1":
			userGroup.groupB1 = team;
		elif str(position) == "B2":
			userGroup.groupB2 = team;
		elif str(position) == "C1":
			userGroup.groupC1 = team;
		elif str(position) == "C2":
			userGroup.groupC2 = team;
		elif str(position) == "D1":
			userGroup.groupD1 = team;
		elif str(position) == "D2":
			userGroup.groupD2 = team;
		elif str(position) == "E1":
			userGroup.groupE1 = team;
		elif str(position) == "E2":
			userGroup.groupE2 = team;
		elif str(position) == "F1":
			userGroup.groupF1 = team;
		elif str(position) == "F2":
			userGroup.groupF2 = team;
		elif str(position) == "G1":
			userGroup.groupG1 = team;
		elif str(position) == "G2":
			userGroup.groupG2 = team;
		elif str(position) == "H1":
			userGroup.groupH1 = team;
		elif str(position) == "H2":
			userGroup.groupH2 = team;
		else:
			return HttpResponseRedirect(reverse('bracket:userGroupView', args=(userGroup.id,)))
			
		userGroup.save()
	
	else:
		return HttpResponseRedirect(reverse('bracket:userGroupView', args=(userGroup.id,)))
		
	return HttpResponseRedirect(reverse('bracket:userGroupView', args=(userGroup.id,)))
	
	
# Setting the winners of the bracket
def userBracket(request, userGroup_id):
	userGroup = get_object_or_404(UserGroup, pk=userGroup_id)
	
	if request.session.get('userAdmin', 'none') != str(userGroup.userName + userGroup.password):
		return HttpResponseRedirect(reverse('bracket:index',))
	
	team = request.POST.get('team')
	game = request.POST.get('game')
	
	
	if str(game) != "NOTHING" and str(team) != "NOTHING":
		if str(game) == "Game 1":
			userGroup.win1 = team;
		elif str(game) == "Game 2":
			userGroup.win2 = team;
		elif str(game) == "Game 3":
			userGroup.win3 = team;
		elif str(game) == "Game 4":
			userGroup.win4 = team;
		elif str(game) == "Game 5":
			userGroup.win5 = team;
		elif str(game) == "Game 6":
			userGroup.win6 = team;
		elif str(game) == "Game 7":
			userGroup.win7 = team;
		elif str(game) == "Game 8":
			userGroup.win8 = team;
		elif str(game) == "Game 9":
			userGroup.win9 = team;
		elif str(game) == "Game 10":
			userGroup.win10 = team;
		elif str(game) == "Game 11":
			userGroup.win11 = team;
		elif str(game) == "Game 12":
			userGroup.win12 = team;
		elif str(game) == "Game 13":
			if str(team) == str(userGroup.win9):
				userGroup.win13 = userGroup.win9
				userGroup.loss1 = userGroup.win10
			else:
				userGroup.win13 = userGroup.win10
				userGroup.loss1 = userGroup.win9
		elif str(game) == "Game 14":
			if str(team) == str(userGroup.win11):
				userGroup.win14 = userGroup.win11
				userGroup.loss2 = userGroup.win12
			else:
				userGroup.win14 = userGroup.win12
				userGroup.loss2 = userGroup.win11
		elif str(game) == "Third":
			userGroup.third = team;
		elif str(game) == "Champion":
			userGroup.champion = team;
		else:
			return HttpResponseRedirect(reverse('bracket:userGroupView', args=(userGroup.id,)))
			
		userGroup.save()
	
	else:
		return HttpResponseRedirect(reverse('bracket:userGroupView', args=(userGroup.id,)))
		
	return HttpResponseRedirect(reverse('bracket:userGroupView', args=(userGroup.id,)))
	
	
# Gives points to the Users in the userGroup for  the Groups
def sumGroupStage(request, userGroup_id):
	admin = get_object_or_404(UserGroup, pk=userGroup_id)
	
	if request.session.get('userAdmin', 'none') != str(admin.userName + admin.password):
		return HttpResponseRedirect(reverse('bracket:index',))
	
	if not admin.editBracket:
		currentLeader = False
		name = ""
	
		for person in admin.user_set.all():
			person.groupPoints = 0
	
			leader1 = admin.groupA1
			leader2 = admin.groupA2
		
			if leader1 == person.groupA1 and leader2 == person.groupA2:
				person.groupPoints = person.groupPoints + 4
			elif leader1 == person.groupA1:
				person.groupPoints = person.groupPoints + 2
			elif leader2 == person.groupA2:
				person.groupPoints = person.groupPoints + 2
			elif leader1 == person.groupA2 and leader2 == person.groupA1:
				person.groupPoints = person.groupPoints + 2
			elif leader1 == person.groupA2:
				person.groupPoints = person.groupPoints + 1
			elif leader2 == person.groupA1:
				person.groupPoints = person.groupPoints + 1
		
			leader1 = admin.groupB1
			leader2 = admin.groupB2
		
			if leader1 == person.groupB1 and leader2 == person.groupB2:
				person.groupPoints = person.groupPoints + 4
			elif leader1 == person.groupB1:
				person.groupPoints = person.groupPoints + 2
			elif leader2 == person.groupB2:
				person.groupPoints = person.groupPoints + 2
			elif leader1 == person.groupB2 and leader2 == person.groupB1:
				person.groupPoints = person.groupPoints + 2
			elif leader1 == person.groupB2:
				person.groupPoints = person.groupPoints + 1
			elif leader2 == person.groupB1:
				person.groupPoints = person.groupPoints + 1
		
			leader1 = admin.groupC1
			leader2 = admin.groupC2
		
			if leader1 == person.groupC1 and leader2 == person.groupC2:
				person.groupPoints = person.groupPoints + 4
			elif leader1 == person.groupC1:
				person.groupPoints = person.groupPoints + 2
			elif leader2 == person.groupC2:
				person.groupPoints = person.groupPoints + 2
			elif leader1 == person.groupC2 and leader2 == person.groupC1:
				person.groupPoints = person.groupPoints + 2
			elif leader1 == person.groupC2:
				person.groupPoints = person.groupPoints + 1
			elif leader2 == person.groupC1:
				person.groupPoints = person.groupPoints + 1
		
		
			leader1 = admin.groupD1
			leader2 = admin.groupD2
		
			if leader1 == person.groupD1 and leader2 == person.groupD2:
				person.groupPoints = person.groupPoints + 4
			elif leader1 == person.groupD1:
				person.groupPoints = person.groupPoints + 2
			elif leader2 == person.groupD2:
				person.groupPoints = person.groupPoints + 2
			elif leader1 == person.groupD2 and leader2 == person.groupD1:
				person.groupPoints = person.groupPoints + 2
			elif leader1 == person.groupD2:
				person.groupPoints = person.groupPoints + 1
			elif leader2 == person.groupD1:
				person.groupPoints = person.groupPoints + 1
		
		
			leader1 = admin.groupE1
			leader2 = admin.groupE2
		
			if leader1 == person.groupE1 and leader2 == person.groupE2:
				person.groupPoints = person.groupPoints + 4
			elif leader1 == person.groupE1:
				person.groupPoints = person.groupPoints + 2
			elif leader2 == person.groupE2:
				person.groupPoints = person.groupPoints + 2
			elif leader1 == person.groupE2 and leader2 == person.groupE1:
				person.groupPoints = person.groupPoints + 2
			elif leader1 == person.groupE2:
				person.groupPoints = person.groupPoints + 1
			elif leader2 == person.groupE1:
				person.groupPoints = person.groupPoints + 1
		
		
			leader1 = admin.groupF1
			leader2 = admin.groupF2
		
			if leader1 == person.groupF1 and leader2 == person.groupF2:
				person.groupPoints = person.groupPoints + 4
			elif leader1 == person.groupF1:
				person.groupPoints = person.groupPoints + 2
			elif leader2 == person.groupF2:
				person.groupPoints = person.groupPoints + 2
			elif leader1 == person.groupF2 and leader2 == person.groupF1:
				person.groupPoints = person.groupPoints + 2
			elif leader1 == person.groupF2:
				person.groupPoints = person.groupPoints + 1
			elif leader2 == person.groupF1:
				person.groupPoints = person.groupPoints + 1
		
		
			leader1 = admin.groupG1
			leader2 = admin.groupG2
		
			if leader1 == person.groupG1 and leader2 == person.groupG2:
				person.groupPoints = person.groupPoints + 4
			elif leader1 == person.groupG1:
				person.groupPoints = person.groupPoints + 2
			elif leader2 == person.groupG2:
				person.groupPoints = person.groupPoints + 2
			elif leader1 == person.groupG2 and leader2 == person.groupG1:
				person.groupPoints = person.groupPoints + 2
			elif leader1 == person.groupG2:
				person.groupPoints = person.groupPoints + 1
			elif leader2 == person.groupG1:
				person.groupPoints = person.groupPoints + 1
		
		
			leader1 = admin.groupH1
			leader2 = admin.groupH2
		
			if leader1 == person.groupH1 and leader2 == person.groupH2:
				person.groupPoints = person.groupPoints + 4
			elif leader1 == person.groupH1:
				person.groupPoints = person.groupPoints + 2
			elif leader2 == person.groupH2:
				person.groupPoints = person.groupPoints + 2
			elif leader1 == person.groupH2 and leader2 == person.groupH1:
				person.groupPoints = person.groupPoints + 2
			elif leader1 == person.groupH2:
				person.groupPoints = person.groupPoints + 1
			elif leader2 == person.groupH1:
				person.groupPoints = person.groupPoints + 1
		
		
			person.points = 0
			person.points = person.groupPoints
		
		
			if currentLeader == False:
				currentLeader = person
				name = "" + str(person.firstName) + " " + str(person.lastName)
			else:
				if person.groupPoints > currentLeader.groupPoints:
					currentLeader = person
					name = "" + str(person.firstName) + " " + str(person.lastName)
				elif person.points == currentLeader.points:
					name += " / " + str(person.firstName) + " " + str(person.lastName)
				
			person.save()
		
		admin.leader = name
		admin.editBracket = True
	
		admin.save()
		
	else:
		admin.save()
	
	return HttpResponseRedirect(reverse('bracket:userGroupView', args=(admin.id,)))
	
	
# Gives points to the Users in userGroup for the bracket
def sumBracketStage(request, userGroup_id):
	admin = get_object_or_404(UserGroup, pk=userGroup_id)
	
	if request.session.get('userAdmin', 'none') != str(admin.userName + admin.password):
		return HttpResponseRedirect(reverse('bracket:index',))

	if admin.editBracket:
		currentLeader = False
		name = ""
	
		for person in admin.user_set.all():
			person.bracketPoints = 0
	
			# First Round
			if person.win1 == admin.win1:
				person.bracketPoints = person.bracketPoints + 2
			else:
				person.win1 = "XX " + person.win1 + " XX"
		
			if person.win2 == admin.win2:
				person.bracketPoints = person.bracketPoints + 2
			else:
				person.win2 = "XX " + person.win2 + " XX"
			
			if person.win3 == admin.win3:
				person.bracketPoints = person.bracketPoints + 2
			else:
				person.win3 = "XX " + person.win3 + " XX"
			
			if person.win4 == admin.win4:
				person.bracketPoints = person.bracketPoints + 2
			else:
				person.win4 = "XX " + person.win4 + " XX"
				
			if person.win5 == admin.win5:
				person.bracketPoints = person.bracketPoints + 2
			else:
				person.win5 = "XX " + person.win5 + " XX"
			
			if person.win6 == admin.win6:
				person.bracketPoints = person.bracketPoints + 2
			else:
				person.win6 = "XX " + person.win6 + " XX"
			
			if person.win7 == admin.win7:
				person.bracketPoints = person.bracketPoints + 2
			else:
				person.win7 = "XX " + person.win7 + " XX"
			
			if person.win8 == admin.win8:
				person.bracketPoints = person.bracketPoints + 2
			else:
				person.win8 = "XX " + person.win8 + " XX"
			
			# Second Round
			if person.win9 == admin.win9:
				person.bracketPoints = person.bracketPoints + 4
			else:
				person.win9 = "XX " + person.win9 + " XX"
		
			if person.win10 == admin.win10:
				person.bracketPoints = person.bracketPoints + 4
			else:
				person.win10 = "XX " + person.win10 + " XX"
	
			if person.win11 == admin.win11:
				person.bracketPoints = person.bracketPoints + 4
			else:
				person.win11 = "XX " + person.win11 + " XX"
				
			if person.win12 == admin.win12:
				person.bracketPoints = person.bracketPoints + 4
			else:
				person.win12 = "XX " + person.win12 + " XX"
				
			# Third Round
			if person.win13 == admin.win13:
				person.bracketPoints = person.bracketPoints + 8
			else:
				person.win13 = "XX " + person.win13 + " XX"
		
			if person.win14 == admin.win14:
				person.bracketPoints = person.bracketPoints + 8
			else:
				person.win14 = "XX " + person.win14 + " XX"
			
			
			# Final
			if person.champion == admin.champion:
				person.bracketPoints = person.bracketPoints + 16
			else:
				person.champion = "XX " + person.champion + " XX"
			
			if person.third == admin.third:
				person.bracketPoints = person.bracketPoints + 10
			else:
				person.third = "XX " + person.third + " XX"
		
		
			person.points = 0
			person.points = person.groupPoints + person.bracketPoints	
		
	
			if currentLeader == False:
				currentLeader = person
				name = "" + str(person.firstName) + " " + str(person.lastName)
			else:
				if person.bracketPoints > currentLeader.bracketPoints:
					currentLeader = person
					name = "" + str(person.firstName) + " " + str(person.lastName)
				elif person.points == currentLeader.points:
					name += " / " + str(person.firstName) + " " + str(person.lastName)	
		
			person.save()
		
		admin.leader = name
	
		admin.save()
	
	else:
		admin.save()
	
	return HttpResponseRedirect(reverse('bracket:userGroupView', args=(admin.id,)))


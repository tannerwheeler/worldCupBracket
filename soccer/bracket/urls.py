from django.urls import path

from . import views

app_name = 'bracket'
urlpatterns = [
	path('', views.index, name='index'),
	path('user/', views.createUser, name='createUser'),
	path('user/create/', views.userCreate, name='userCreate'),
	path('group/', views.createGroup, name='createGroup'),
	path('group/create/', views.groupCreate, name='groupCreate'),
	path('<int:user_id>/', views.userView, name='userView'),
	path('ulogin/', views.userLogin, name='userLogin'),
	path('ulogout/', views.userLogout, name='userLogout'),
	path('<int:user_id>/choice/', views.choice, name='choice'),
	path('<int:user_id>/choice/submit/', views.submit, name='submit'),
	path('<int:user_id>/bracket/', views.bracket, name='bracket'),
	path('<int:user_id>/bracket/bracketChange/', views.bracketChange, name='bracketChange'),
	path('<int:user_id>/bracket/saved/', views.saved, name='saved'),
	path('<int:user_id>/bracket/win', views.win, name='win'),
	path('<int:user_id>/bracket/dele', views.dele, name='dele'),
	path('userAdmin/<int:userGroup_id>/view/', views.userGroupView, name='userGroupView'),
	path('userAdmin/login/', views.userGroupLogin, name='userGroupLogin'),
	path('userAdmin/logout/', views.userGroupLogout, name='userGroupLogout'),
	path('userAdmin/<int:userGroup_id>/view/editChange', views.userGroupEdit, name='userGroupEdit'),
	path('userAdmin/<int:userGroup_id>/view/group/', views.userStage, name='userStage'),
	path('userAdmin/<int:userGroup_id>/view/bracket/', views.userBracket, name='userBracket'),
	path('userAdmin/<int:userGroup_id>/create/', views.adminGroups, name='adminGroups'),
	path('userAdmin/<int:userGroup_id>/create/addG/', views.addG, name='addG'),
	path('userAdmin/<int:userGroup_id>/create/addT/', views.addT, name='addT'),
	path('userAdmin/<int:userGroup_id>/view/sumGroup/', views.sumGroupStage, name='sumGroupStage'),
	path('userAdmin/<int:userGroup_id>/view/sumBracket/', views.sumBracketStage, name='sumBracketStage'),
	path('userAdmin/<int:userGroup_id>/view/allBracket/', views.viewAllBrackets, name='viewAllBrackets'),
]
from django.urls import path

from . import views

app_name = 'bracket'
urlpatterns = [
	path('', views.index, name='index'),
	path('user/', views.createUser, name='createUser'),
	path('user/create/', views.userCreate, name='userCreate'),
	path('group/', views.createGroup, name='createGroup'),
	path('group/create', views.groupCreate, name='groupCreate'),
	#path('userAdmin/', views., name=''),
	path('<int:user_id>/<int:group_id>', views.choice, name='choice'),
	path('<int:user_id>/<int:group_id>/submit', views.submit, name='submit'),
]
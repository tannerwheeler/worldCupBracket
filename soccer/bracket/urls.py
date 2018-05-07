from django.urls import path

from . import views

app_name = 'bracket'
urlpatterns = [
	path('', views.index, name='index'),
	path('user/', views.createUser, name='createUser'),
	path('<int:user_id>/<int:group_id>', views.choice, name='choice'),
	path('<int:user_id>/<int:group_id>/submit', views.submit, name='submit'),
]
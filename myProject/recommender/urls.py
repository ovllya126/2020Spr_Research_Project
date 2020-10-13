from django.urls import path

from . import views

urlpatterns = [
	path('', views.home_page, name='home_page'),
	path('log_out/', views.log_out, name='log_out'),
	path('user_center/',views.user_center, name='user_center'), #<string:user_id>
	path('courses/', views.show_courses, name='show_courses'),
]
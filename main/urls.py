from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/rate/', views.rate_movie, name='rate_movie'),
    path('movie/<int:movie_id>/comment/',
         views.add_comment, name='add_comment'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('movie/<int:movie_id>/edit/', views.edit_movie, name='edit_movie'),
    path('movie/<int:movie_id>/delete/',
         views.delete_movie, name='delete_movie'),
    path('feedback/', views.feedback_view, name='feedback'),
]

from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/review/<int:review_pk>/update/', views.update_review, name='update_review'),
    path('<int:movie_pk>/review/<int:review_pk>/delete/', views.delete_review, name='delete_review'),
    path('<int:movie_pk>/review/create/', views.create_review, name='create_review'),
]

from django.urls import path
from . import views, views2

app_name = 'movies'

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/review/<int:review_pk>/update/', views.update_review, name='update_review'),
    path('<int:movie_pk>/review/<int:review_pk>/delete/', views.delete_review, name='delete_review'),
    path('<int:movie_pk>/rank/', views.rank_create, name='rank_create'),
    path('<int:movie_pk>/rank/<int:rank_pk>/update', views.rank_update, name='rank_update'),
    path('<int:movie_pk>/rank/<int:rank_pk>/delete', views.rank_delete, name='rank_delete'),
    path('worldcup/', views2.worldcup, name="worldcup"),
]

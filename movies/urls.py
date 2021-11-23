from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/review/<int:review_pk>/update/', views.update_review, name='update_review'),
    path('<int:movie_pk>/review/<int:review_pk>/delete/', views.delete_review, name='delete_review'),
    path('<int:movie_pk>/rank/', views.create_rank, name='create_rank'),
    path('<int:movie_pk>/rank/<int:rank_pk>/update', views.update_rank, name='update_rank'),
    path('<int:movie_pk>/rank/<int:rank_pk>/delete', views.delete_rank, name='delete_rank'),
    path('worldcup/', views.worldcup_init, name="worldcup_init"),
    path('worldcup/next/', views.worldcup_next_round, name="worldcup_next_round"),
    path('worldcup/end/', views.worldcup_end, name="worldcup_end"),
    path('worldcup/select_round/',views.worldcup_select_round, name="worldcup_select_round"),
]


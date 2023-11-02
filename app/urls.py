from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:page_number>', views.index, name='page'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('ask', views.ask, name='ask'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('profile', views.profile, name='profile'),
    path('popular_tags/<slug:tag>/', views.popular_tags, name='popular_tags'),
    path('hot/', views.hot, name='hot'),
]
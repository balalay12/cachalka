import views

from django.conf.urls import url
from django.views.decorators.csrf import ensure_csrf_cookie

urlpatterns = [
    url(r'^$', ensure_csrf_cookie(views.Main.as_view()), name='main'),
    url(r'^reg/$', views.Registration.as_view(), name='reg'),
    url(r'^login/$', views.LogIn.as_view(), name='login'),
    url(r'^logout/$', views.LogOut.as_view(), name='logout'),
    url(r'^api/exercises/$', views.Exercises.as_view(), name='exercises'),
    url(r'^api/sets/$', views.Sets.as_view(), name='sets'),
    url(r'^api/repeats/$', views.Repeats.as_view(), name='repeats'),
    url(r'^api/categories/$', views.Categories.as_view(), name='categories'),
    url(r'^api/check/$', views.CheckReg.as_view(), name='check'),
    url(r'^api/check/auth/$', views.CheckAuth.as_view(), name='auth')
]

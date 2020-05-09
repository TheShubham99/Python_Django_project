from django.urls import path
from . import views
urlpatterns = [
    path('Pratham/', views.loaddata, name='homepage'),
    path('Plot/', views.getimage, name='plot'),
    path('Analysis/',views.analyze,name='Analysis'),
]

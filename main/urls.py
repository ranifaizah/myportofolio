from django.urls import path

from main.views import create_experiences, show_main, show_experiences,show_skills,create_skills,create_experiences

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experiences, name="show_experiences"),
    path('skills/', show_skills, name='show_skills'),
    path("skills/add/", create_skills, name="create_skills"), 
    path("experiences/add/", create_experiences, name="create_experiences"), 
]
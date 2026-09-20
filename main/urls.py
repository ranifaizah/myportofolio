from django.urls import path

from main.views import *
app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experiences/", show_experience, name="show_experiences"),
    path('skills/', show_skills, name='show_skills'),
    path("skills/add/", create_skills, name="create_skills"), 
    path("experiences/add/", create_experiences, name="create_experiences"), 
    path("api/skills/", get_skills_json, name="get_skills_json"),
    path("skills/<uuid:skill_id>/delete/",delete_skill,name="delete_skill"),
    path("experiences/<uuid:experience_id>/delete/",delete_experience,name="delete_experience"),


]
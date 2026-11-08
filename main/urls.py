
from django.urls import path
from main.views import *

app_name = "main"

urlpatterns = [
    # Halaman utama
    path("", show_main, name="show_main"),

    # Experience
    path("experiences/", show_experience, name="show_experiences"),
    path("experiences/add/", create_experiences, name="create_experiences"),
    path("experiences/add-ajax/", create_experience_ajax, name="create_experience_ajax"),
    path(
        "experiences/<uuid:experience_id>/delete/",
        delete_experience,
        name="delete_experience",
    ),
    path(
        "experiences/<uuid:experience_id>/update/",
        update_experience,
        name="update_experience",
    ),
    path(
        "experiences/<uuid:experience_id>/star/",
        toggle_star,
        name="toggle_star",
    ),

    # Skills
    path("skills/", show_skills, name="show_skills"),
    path("skills/add/", create_skills, name="create_skills"),
    path("skills/<uuid:skill_id>/delete/", delete_skill, name="delete_skill"),
    path("skills/<uuid:skill_id>/update/", update_skill, name="update_skill"),
    path("skills/json-view/", show_skills_deserialized, name="show_skills_deserialized"),

    # JSON lama
    path("api/skills/", get_skills_json, name="get_skills_json"),
    path("api/experiences/", get_experience_json, name="get_experience_json"),

    # Authentication
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
]

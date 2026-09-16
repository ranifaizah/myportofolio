
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import SkillForm
from main.forms import ExperienceForm
from main.models import Experience
from main.models import Skill





def show_main(request):
    context = {
        "name": "Rani",
        "npm": "2506624013",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Rani",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_skills(request):
    skills = Skill.objects.all()   
    context = {
        'name': 'Rani',
        'skill_list': skills,  
    }
    return render(request, 'skills.html', context)

def create_skills(request):
    form = SkillForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill baru berhasil ditambahkan!")
        return redirect("main:show_skills")

    context = {
        "name": "Rani",
        "form": form,
    }
    return render(request, "skills_form.html", context)

def create_experiences(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience baru berhasil ditambahkan!")
        return redirect("main:show_experieces")

    context = {
        "name": "Rani",
        "form": form,
    }
    return render(request, "experiences_form.html", context)
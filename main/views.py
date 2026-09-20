
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import SkillForm
from main.forms import ExperienceForm
from main.models import Experience
from main.models import Skill
from main.models import Project
from main.forms import ProjectForm





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
        return redirect("main:show_experiences")

    context = {
        "name": "Rani",
        "form": form,
    }
    return render(request, "experience_form.html", context)

def get_skills_json(request):
    title_query = request.GET.get("title", "").strip()
    skills = Skill.objects.all()

    if title_query:
        skills = skills.filter(title__icontains=title_query)

    skills_json = serializers.serialize("json", skills)
    return HttpResponse(skills_json, content_type="application/json")

def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill berhasil dihapus!")
        return redirect("main:show_skills")

    return redirect("main:show_skills")

def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experience = Experience.objects.all()

    if title_query:
        experience = experience.filter(title__icontains=title_query)

    experience_json = serializers.serialize("json", experience)
    return HttpResponse(experience_json, content_type="application/json")

def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experiences")

    return redirect("main:show_experiences")


# --- SHOW / LIST ---
def show_projects(request):
    project_list = Project.objects.all()
    context = {'project_list': project_list}
    return render(request, "show_projects.html", context)

# --- CREATE ---
def create_project(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_projects')
    context = {'form': form}
    return render(request, "create_project.html", context)

# --- UPDATE ---
def update_project(request, id):
    project = get_object_or_404(Project, pk=id)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_projects')
    context = {'form': form}
    return render(request, "update_project.html", context)

# --- DELETE ---
def delete_project(request, id):
    project = get_object_or_404(Project, pk=id)
    project.delete()
    return redirect('main:show_projects')

# --- AMBIL DATA JSON (semua) ---
def show_json(request):
    project_list = Project.objects.all()
    json_data = serializers.serialize("json", project_list)
    return HttpResponse(json_data, content_type="application/json")

# --- AMBIL DATA JSON (by id) ---
def show_json_by_id(request, id):
    project = Project.objects.filter(pk=id)
    json_data = serializers.serialize("json", project)
    return HttpResponse(json_data, content_type="application/json")

# --- TAMPILKAN HASIL DESERIALISASI JSON ---
def show_projects_json_view(request):
    project_list = Project.objects.all()
    json_data = serializers.serialize("json", project_list)
    deserialized_projects = list(serializers.deserialize("json", json_data))
    context = {
        'projects': deserialized_projects,  # tiap item punya .object utk akses field
    }
    return render(request, "projects_json_view.html", context)


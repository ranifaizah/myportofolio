
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count
from django.views.decorators.http import require_POST

from main.forms import SkillForm
from main.forms import ExperienceForm
from main.models import Experience
from main.models import Skill

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import datetime

from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied  




def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Rani",
        "form": form,
    }
    return render(request, "login.html", context)


def show_main(request):
    last_login = request.COOKIES.get("last_login", "Belum login")

    context = {
        "name": "Rani",
        "npm": "2506624013",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
        "last_login": last_login,
    }

    return render(request, "index.html", context)


def show_experience(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Rani",
        "title_query": title_query,
        "form": ExperienceForm(),
    }

    return render(request, "experience.html", context)

def show_skills(request):
    title_query = request.GET.get("title", "").strip()
    skills = Skill.objects.all()

    if title_query:
        skills = skills.filter(name__icontains=title_query)

    context = {
        'name': 'Rani',
        'skill_list': skills,
        'title_query': title_query,
    }
    return render(request, 'skills.html', context)

@login_required(login_url="/login/") 
def create_skills(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = SkillForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill baru berhasil ditambahkan!")
        return redirect("main:show_skills")

    context = {
        "name": "Rani",
        "form": form,
        "is_edit": False,
    }
    return render(request, "skills_form.html", context)

@login_required(login_url="/login/") 
def create_experiences(request):
    form = ExperienceForm(request.POST or None)
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience baru berhasil ditambahkan!")
        return redirect("main:show_experiences")

    context = {
        "name": "Rani",
        "form": form,
        "is_edit": False,
    }
    return render(request, "experience_form.html", context)

def get_skills_json(request):
    title_query = request.GET.get("title", "").strip()
    skills = Skill.objects.all()

    if title_query:
        skills = skills.filter(name__icontains=title_query)

    skills_json = serializers.serialize("json", skills)
    return HttpResponse(skills_json, content_type="application/json")

@login_required(login_url="/login/") 
def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill berhasil dihapus!")
        return redirect("main:show_skills")

    return redirect("main:show_skills")

def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()

    experiences = Experience.objects.prefetch_related(
        "starred_by"
    ).all()

    if title_query:
        experiences = experiences.filter(
            title__icontains=title_query
        )

    data = []

    for experience in experiences:
        starred_users = experience.starred_by.all()

        is_starred = (
            request.user in starred_users
            if request.user.is_authenticated
            else False
        )

        starred_by_names = ", ".join(
            [
                user.username
                for user in starred_users
            ]
        )

        data.append({
            "pk": str(experience.id),
            "fields": {
                "title": experience.title,
                "description": experience.description,
                "category": experience.category,
                "thumbnail": experience.thumbnail,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(
        data,
        safe=False
    )

@login_required(login_url="/login/") 
def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experiences")

    return redirect("main:show_experiences")


@login_required(login_url="/login/")
def update_skill(request, skill_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    skill = get_object_or_404(Skill, pk=skill_id)
    form = SkillForm(request.POST or None, instance=skill)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill berhasil diperbarui!")
        return redirect("main:show_skills")

    context = {
        "name": "Rani",
        "form": form,
        "is_edit": True,
    }

    return render(request, "skills_form.html", context)

@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience berhasil diperbarui!")
        return redirect("main:show_experiences")

    context = {
        "name": "Rani",
        "form": form,
        "is_edit": True,
    }
    return render(request, "experience_form.html", context)

def show_skills_deserialized(request):
    skills_json = serializers.serialize("json", Skill.objects.all())
    skills = list(serializers.deserialize("json", skills_json))
    context = {"name": "Rani", "skill_list": skills}
    return render(request, "skills_deserialized.html", context)


def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Burhan",
        "form": form,
    }
    return render(request, "register.html", context)




def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

# Tanpa cek is_superuser: semua akun yang sudah login boleh memberi star
@login_required(login_url="/login/")
def toggle_star(request, experience_id):
    experience = get_object_or_404(
        Experience,
        pk=experience_id
    )

    if request.method == "POST":

        if request.user in experience.starred_by.all():
            # Jika sudah memberi star, batalkan star
            experience.starred_by.remove(request.user)
        else:
            # Jika belum memberi star, tambahkan star
            experience.starred_by.add(request.user)

    return redirect("main:show_experiences")

@login_required(login_url="/login/")
@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan experience."},
            status=403,
        )

    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "experience berhasil ditambahkan.", "pk": str(experience.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

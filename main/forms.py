from django.forms import ModelForm, TextInput, Textarea, URLInput, ChoiceField, Select
from django.forms.fields import DateTimeField
from django.forms.widgets import DateTimeInput
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

from main.models import Experience, Skill

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = [
            "name",
            "category",
            "proficiency",
            "icon",
            "added_at",
        ]

        labels = {
            "name": "Nama Skill",
            "category": "Katergori skill",
            "proficiency": "proficiency",
            "icon": "icon skill",
            "added_at": "ditambahkan kapan",
        }

        widgets = {
            "nama": TextInput(
                attrs={
                    "placeholder": "figma,canva,iot,django",
                    "maxlength": 255,
                }
            ),
            "cattegory": Textarea(
                attrs={
                    "placeholder": "programming,design",
                    "rows": 3,
                }
            ),
            "icon": URLInput(
                attrs={
                    "placeholder": "hhttps://drive.google.com/thumbnail?id=FILE_ID&sz=w1000",
                }
            ),
            "added_at": DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
        }

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
        ]

        labels = {
            "title": "Jabatan pada experience",
            "description": "experience description",
            "category": "Katergori experience",
            "thumbnail": "experience pic",
            "started_at": "when you started",
            "ended_at": "when ypu ended",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Ketua Osis",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "managing projects and maintaining security",
                    "rows": 3,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=FILE_ID&sz=w1000",
                }
            ),
            "started_at": DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
            "ended_at": DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
        }
        def clean_title(self):
            title = strip_tags(self.cleaned_data["title"]).strip()
            if not title:
                raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
            return title

    def clean_tech_stack(self):
        return strip_tags(self.cleaned_data["tech_stack"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()


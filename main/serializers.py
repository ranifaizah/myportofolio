
from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Experience


class ExperienceSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id",
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
            "is_ongoing",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]

        read_only_fields = [
            "id",
            "is_ongoing",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]

    # Membersihkan title dari HTML
    def validate_title(self, value):
        value = strip_tags(value).strip()

        if not value:
            raise serializers.ValidationError(
                "Title cannot be empty."
            )

        return value

    # Membersihkan description dari HTML
    def validate_description(self, value):
        value = strip_tags(value).strip()

        if not value:
            raise serializers.ValidationError(
                "Description cannot be empty."
            )

        return value

    # Menghitung jumlah star
    def get_star_count(self, obj):
        return obj.starred_by.count()

    # Mengecek apakah user sudah memberikan star
    def get_is_starred(self, obj):
        request = self.context.get("request")

        if request is None or not request.user.is_authenticated:
            return False

        return obj.starred_by.filter(
            pk=request.user.pk
        ).exists()

    # Mengambil nama user yang memberikan star
    def get_starred_by_names(self, obj):
        return ", ".join(
            user.username
            for user in obj.starred_by.all()
        )

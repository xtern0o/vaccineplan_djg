import pathlib

import django.contrib.auth.models
import django.core.validators
import django.db.models
import sorl

import clinics.models


class CustomUser(django.contrib.auth.models.AbstractUser):
    class GenderChoices(django.db.models.TextChoices):
        MALE = ("M", "мужской")
        FEMALE = ("F", "женский")

    gender = django.db.models.CharField(
        "пол",
        max_length=1,
        choices=GenderChoices.choices,
    )

    birthday = django.db.models.DateField(
        "дата рождения",
        blank=True,
        null=True,
    )

    image = django.db.models.ImageField(
        "аватарка",
        blank=True,
        null=True,
        upload_to="users/%Y/%m/%d/",
    )

    middle_name = django.db.models.CharField(
        "отчество",
        blank=True,
        null=True,
        max_length=128,
    )

    is_clinic_admin = django.db.models.BooleanField(
        verbose_name="администратор клиники",
        help_text="является ли этот пользователь администратором клиники",
        default=False,
    )

    clinic = django.db.models.ForeignKey(
        to=clinics.models.Clinics,
        verbose_name="клиника",
        help_text="клиника, к которой прикреплен пользователь",
        blank=True,
        null=True,
        on_delete=django.db.models.deletion.CASCADE,
        related_name="clinic",
    )

    featured_clinics = django.db.models.ManyToManyField(
        to=clinics.models.Clinics,
        verbose_name="отслеживаемые клиники",
        help_text="клиники, которые выбрал пользователь для отслеживания",
        related_name="featured_clinics",
    )

    def get_image_x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "300x300",
            crop="center",
            quality=51,
        )

    def image_tmb(self):
        if self.image:
            return django.utils.safestring.mark_safe(
                f'<img src="{self.get_image_x300().url}">',
            )
        return "изображения нет"

    image_tmb.short_description = "превью (300x300)"
    image_tmb.allow_tags = True

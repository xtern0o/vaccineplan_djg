import django.contrib.auth.forms
import django.contrib.auth.models
import django.forms
import django.forms.fields

import clinics.models
import users.models


__all__ = []


class SignUpForm(django.contrib.auth.forms.UserCreationForm):
    email = django.forms.EmailField(
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            users.models.CustomUser.birthday.field.name
        ].widget = django.forms.fields.TextInput(
            {
                "type": "date",
            },
        )

    class Meta:
        model = users.models.CustomUser
        fields = [
            users.models.CustomUser.username.field.name,
            users.models.CustomUser.email.field.name,
            users.models.CustomUser.first_name.field.name,
            users.models.CustomUser.last_name.field.name,
            users.models.CustomUser.middle_name.field.name,
            users.models.CustomUser.city.field.name,
            users.models.CustomUser.gender.field.name,
            users.models.CustomUser.birthday.field.name,
        ]


class ProfileForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            users.models.CustomUser.birthday.field.name
        ].widget = django.forms.fields.TextInput(
            {
                "type": "date",
            },
        )
        self.fields[
            users.models.CustomUser.image.field.name
        ].widget = django.forms.FileInput()
        self.fields["clinic"] = django.forms.ModelChoiceField(
            clinics.models.Clinics.objects.filter(approved=True),
        )
        self.fields["clinic"].required = False

    class Meta:
        model = users.models.CustomUser
        fields = [
            users.models.CustomUser.username.field.name,
            users.models.CustomUser.first_name.field.name,
            users.models.CustomUser.last_name.field.name,
            users.models.CustomUser.middle_name.field.name,
            users.models.CustomUser.birthday.field.name,
            users.models.CustomUser.city.field.name,
            users.models.CustomUser.image.field.name,
            users.models.CustomUser.clinic.field.name,
        ]

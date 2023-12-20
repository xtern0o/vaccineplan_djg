import datetime

import django.conf
import django.contrib.auth
import django.contrib.auth.decorators
import django.contrib.auth.mixins
import django.contrib.auth.models
import django.contrib.messages
import django.core.mail
import django.shortcuts
import django.urls
import django.utils.timezone
import django.views.generic
import jwt

import core.utils
import users.forms
import users.models


__all__ = []


@django.contrib.auth.decorators.login_required
def profile(request):
    template = "users/profile.html"
    user = request.user
    form = users.forms.ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=user,
        initial={
            "birthday": user.birthday,
            "image": user.image,
        },
    )

    if request.method == "POST":
        if form.is_valid():
            form.save()
            django.contrib.messages.success(
                request,
                "Данные профиля успешно обновлены",
            )
            return django.shortcuts.redirect("users:profile")
        django.contrib.messages.warning(
            request,
            "Некорректные данные",
        )
        return django.shortcuts.redirect("users:profile")

    context = {
        "form": form,
    }
    return django.shortcuts.render(request, template, context)


class SignupFormView(django.views.generic.FormView):
    template_name = "users/signup.html"
    form_class = users.forms.SignUpForm

    def form_valid(self, form):
        user = form.save()
        user.save()

        if django.conf.settings.DEFAULT_USER_IS_ACTIVE:
            user.is_active = True
            user.save()

        expiration = django.utils.timezone.now() + datetime.timedelta(
            hours=django.conf.settings.LINK_EXPIRATION,
        )

        exp_timestamp = int(expiration.timestamp())

        token_context = {
            "username": user.username,
            "exp": exp_timestamp,
        }

        token = jwt.encode(
            token_context,
            django.conf.settings.SECRET_KEY,
            algorithm="HS256",
        )

        activation_link = self.request.build_absolute_uri(
            django.urls.reverse(
                "users:activate",
                kwargs={
                    "token": token,
                },
            ),
        )

        msg_text = (
            f"Вам необходимо активировать аккаунт в течение 12 "
            "часов после регистрации. "
            "Для активации перейдите по ссылке, указанной в"
            " данном письме.\n"
            f"Ссылка для активации: {activation_link}"
        )

        django.core.mail.send_mail(
            "Активация аккаунта VaccinePlan",
            msg_text,
            django.conf.settings.EMAIL_ADDRESS,
            [user.email],
        )

        return django.shortcuts.redirect(
            django.urls.reverse("homepage:home"),
        )


class ActivateUserView(django.views.generic.TemplateView):
    template_name = "users/activation_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token = self.kwargs["token"]
        data, status_ok = core.utils.decode_token(token)

        if status_ok:
            try:
                user = users.models.CustomUser.objects.get(
                    username=data["username"],
                )
                user.is_active = True
                user.save()
                context["ok"] = status_ok
                context["info"] = data
            except users.models.CustomUser.DoesNotExist:
                context["ok"] = False
                context["info"] = "Пользователь не найден"
        else:
            context["ok"] = status_ok
            context["info"] = data

        return context


class ProfileView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.FormView,
):
    template_name = "users/profile.html"
    form_class = users.forms.ProfileForm
    success_url = django.urls.reverse_lazy("users:profile")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        instance = self.request.user
        kwargs["initial"] = {
            users.models.CustomUser.first_name.field.name: instance.first_name,
            users.models.CustomUser.last_name.field.name: instance.last_name,
            users.models.CustomUser.middle_name.field.name: instance.middle_name,
            users.models.CustomUser.birthday.field.name: instance.birthday,
            users.models.CustomUser.clinic.field.name: instance.clinic,
        }
        return kwargs

    def form_valid(self, form):
        user = form.save()
        user.birthday = form.cleaned_data["birthday"]
        user.save()
        return super().form_valid(form)

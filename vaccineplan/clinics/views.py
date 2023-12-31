import django.conf
import django.contrib.messages
import django.core.mail
import django.shortcuts
import django.urls
import django.views.generic

import clinics.forms
import clinics.models
import users.mixins
import vaccines.models

__all__ = []


class ClinicRegistrationFormView(
    users.mixins.ActiveUserRequiredMixin,
    django.views.generic.FormView,
):
    template_name = "clinics/registration.html"
    form_class = clinics.forms.ClinicsForm
    success_url = django.urls.reverse_lazy("clinics:registration")

    def get(self, request, *args, **kwargs):
        if clinics.models.Clinics.objects.filter(
            admin_id=request.user,
        ).exists():
            django.contrib.messages.success(
                request=self.request,
                message="Вы уже являетесь администратором клиники.",
            )
            return django.shortcuts.redirect("users:profile")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        new_clinic = clinics.models.Clinics(**form.cleaned_data)
        new_clinic.admin = self.request.user
        new_clinic.save()
        django.contrib.messages.success(
            request=self.request,
            message="Форма успешно отправлена! "
            "Вы получите письмо на почту, когда заявку одобрят.",
        )
        return super().form_valid(form)


class ClinicAdmin(django.views.generic.UpdateView):
    template_name = "clinics/admin.html"
    form_class = clinics.forms.ClinicEditForm

    def get_success_url(self):
        return django.urls.reverse_lazy(
            "clinics:admin",
            kwargs={"pk": self.kwargs["pk"]},
        )

    def get_object(self, queryset=None):
        pk = self.kwargs["pk"]
        return clinics.models.Clinics.objects.get(
            admin_id=self.request.user,
            pk=pk,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clinic"] = self.get_object()
        return context


def clinic_vaccines(request, pk):
    template = "clinics/check_vaccines.html"

    clinic_object = clinics.models.Clinics.objects.get(pk=pk)
    if request.method == "POST":
        vaccines.models.Availability.objects.filter(clinic=pk).delete()
        checked_vaccines = request.POST.getlist("vaccines")
        for vaccine_id in checked_vaccines:
            vaccine_object = vaccines.models.Vaccines.objects.get(
                pk=int(vaccine_id),
            )
            vaccines.models.Availability.objects.create(
                vaccines=vaccine_object,
                clinic_id=clinic_object.id,
            )
        django.contrib.messages.add_message(
            request,
            django.contrib.messages.SUCCESS,
            "Изменения успешно сохранены.",
        )
        return django.shortcuts.redirect(
            "clinics:vaccines",
            pk=pk,
        )
    vaccines_context = (
        vaccines.models.Vaccines.objects.all()
        .select_related(
            "category",
        )
        .only(
            "name",
            "category",
            "category__name",
            "category__id",
        )
    )
    already_checked = [
        el.vaccines.id
        for el in vaccines.models.Availability.objects.get_already_checked(
            clinic_object,
        )
    ]

    context = {
        "vaccines": vaccines_context,
        "already_checked": already_checked,
        "clinic_id": clinic_object.id,
    }
    return django.shortcuts.render(request, template, context)

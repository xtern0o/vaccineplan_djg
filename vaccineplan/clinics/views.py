import django.conf
import django.contrib.messages
import django.core.mail
import django.shortcuts
import django.urls
import django.views.generic

import clinics.forms
import clinics.models

__all__ = []


class ClinicRegistrationFormView(django.views.generic.FormView):
    template_name = "clinics/registration.html"
    form_class = clinics.forms.ClinicsForm
    success_url = django.urls.reverse_lazy("clinics:registration")

    def get(self, request, *args, **kwargs):
        if clinics.models.Clinics.objects.filter(
            admin_id=request.user
        ).exists():
            django.contrib.messages.success(
                request=self.request,
                message="Вы уже являетесь администратором клиники.",
            )
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        new_clinic = clinics.models.Clinics(**form.cleaned_data)
        new_clinic.admin = self.request.user
        new_clinic.save()
        django.contrib.messages.success(
            request=self.request,
            message="Форма успешно отправлена!"
            "Вы получите письмо на почту, когда заявку одобрят.",
        )
        return super().form_valid(form)


class ClinicAdmin(django.views.generic.UpdateView):
    template_name = "clinics/admin.html"
    form_class = clinics.forms.ClinicEditForm

    def get_object(self, queryset=None):
        return clinics.models.Clinics.objects.get(
            admin_id=self.request.user.id
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clinic"] = self.get_object()
        return context

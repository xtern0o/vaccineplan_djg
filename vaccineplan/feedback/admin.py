from django.contrib import admin

import feedback.models

__all__ = []


@admin.register(feedback.models.Feedback)
class FeedbackModelAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.Feedback.name.field.name,
        feedback.models.Feedback.status.field.name,
    )

    list_display_links = (feedback.models.Feedback.name.field.name,)

    readonly_fields = (
        feedback.models.Feedback.name.field.name,
        feedback.models.Feedback.text.field.name,
        feedback.models.Feedback.mail.field.name,
        feedback.models.Feedback.category.field.name,
    )

    list_editable = (feedback.models.Feedback.status.field.name,)

    def save_model(self, request, obj, form, change):
        if change and form.cleaned_data["status"] != form.initial.get(
            "status",
        ):
            feedback.models.StatusLogFeedback.objects.create(
                user=request.user,
                from_status=form.initial.get("status"),
                to=form.cleaned_data.get("status"),
                feedback=obj,
            )

        super().save_model(request, obj, form, change)


@admin.register(feedback.models.StatusLogFeedback)
class StatusLogAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.StatusLogFeedback.user.field.name,
        feedback.models.StatusLogFeedback.from_status.field.name,
        feedback.models.StatusLogFeedback.to.field.name,
    )

    readonly_fields = (
        feedback.models.StatusLogFeedback.timestamp.field.name,
        feedback.models.StatusLogFeedback.user.field.name,
        feedback.models.StatusLogFeedback.from_status.field.name,
        feedback.models.StatusLogFeedback.to.field.name,
    )

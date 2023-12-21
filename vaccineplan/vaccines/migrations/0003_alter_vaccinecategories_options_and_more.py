# Generated by Django 4.2 on 2023-12-21 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("clinics", "0007_remove_clinics_admins_clinics_admin_and_more"),
        ("vaccines", "0002_alter_vaccinecategories_description_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="vaccinecategories",
            options={
                "verbose_name": "категория",
                "verbose_name_plural": "категории",
            },
        ),
        migrations.AlterModelOptions(
            name="vaccines",
            options={
                "verbose_name": "вакцина",
                "verbose_name_plural": "вакцины",
            },
        ),
        migrations.AlterField(
            model_name="vaccines",
            name="category",
            field=models.ForeignKey(
                default=1,
                help_text="категория вакцины - название болезни, от которой она предназначена",
                on_delete=django.db.models.deletion.CASCADE,
                to="vaccines.vaccinecategories",
                verbose_name="категория",
            ),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="Availability",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "clinic",
                    models.ForeignKey(
                        help_text="поликлинка, в которой находится вакцина",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="clinics.clinics",
                        verbose_name="клиника",
                    ),
                ),
                (
                    "vaccine",
                    models.ForeignKey(
                        help_text="название имеющейся вакцины в поликлинике",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vaccines.vaccines",
                        verbose_name="вакцина",
                    ),
                ),
            ],
            options={
                "verbose_name": "наличие",
                "verbose_name_plural": "Наличия",
            },
        ),
    ]

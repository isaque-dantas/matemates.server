# Generated by Django 5.0.7 on 2024-08-03 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_user_is_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='term',
            name='gender',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], default=None, max_length=16),
        ),
        migrations.AlterField(
            model_name='term',
            name='grammatical_category',
            field=models.CharField(choices=[('substantivo', 'Substantive'), ('verbo', 'Verb'), ('adjetivo', 'Adjective'), ('numeral', 'Numeral')], default=None, max_length=16),
        ),
    ]
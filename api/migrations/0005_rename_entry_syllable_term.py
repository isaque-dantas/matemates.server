# Generated by Django 5.0.7 on 2024-08-03 23:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_term_gender_alter_term_grammatical_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='syllable',
            old_name='entry',
            new_name='term',
        ),
    ]

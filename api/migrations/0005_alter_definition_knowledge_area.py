# Generated by Django 5.0.7 on 2024-10-20 15:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_definition_knowledge_area_alter_image_entry_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='definition',
            name='knowledge_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.knowledgearea'),
        ),
    ]

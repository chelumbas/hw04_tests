# Generated by Django 2.2.16 on 2023-02-14 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]

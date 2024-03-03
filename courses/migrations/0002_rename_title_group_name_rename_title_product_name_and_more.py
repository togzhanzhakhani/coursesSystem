# Generated by Django 4.2.6 on 2024-03-02 17:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='title',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='title',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='group',
            name='max_students',
        ),
        migrations.RemoveField(
            model_name='group',
            name='min_students',
        ),
        migrations.RemoveField(
            model_name='product',
            name='users',
        ),
        migrations.AddField(
            model_name='product',
            name='max_students',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='min_students',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
# Generated by Django 5.1.1 on 2024-09-16 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(default=1, upload_to='', verbose_name='Photo de profil'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pic'),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('CREATOR', 'Créateur'), ('SUBSCRIBER', 'Abonné')], default=1, max_length=30, verbose_name='Role'),
            preserve_default=False,
        ),
    ]

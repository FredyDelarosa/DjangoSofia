# Generated by Django 5.1.6 on 2025-02-09 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sofia_blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('release_date', models.DateField()),
                ('poster', models.ImageField(blank=True, null=True, upload_to='movies/')),
            ],
        ),
    ]

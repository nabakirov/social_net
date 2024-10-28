# Generated by Django 5.1.2 on 2024-10-27 08:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('is_private', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True, null=True)),
                ('like_count', models.BigIntegerField(null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='post.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('post', 'user')},
            },
        ),
    ]
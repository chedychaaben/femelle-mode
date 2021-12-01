# Generated by Django 3.1.4 on 2021-10-29 10:59

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Adresse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prenom', models.CharField(max_length=50)),
                ('nom', models.CharField(max_length=50)),
                ('societe', models.CharField(blank=True, max_length=50, null=True)),
                ('adresse', models.CharField(max_length=50)),
                ('adresse2', models.CharField(blank=True, max_length=50, null=True)),
                ('codepostal', models.CharField(blank=True, max_length=50, null=True)),
                ('ville', models.CharField(max_length=50)),
                ('telephone', models.CharField(max_length=50)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('prix', models.DecimalField(decimal_places=3, default=0, max_digits=8)),
                ('discount_prix', models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=7, null=True)),
                ('description', models.TextField(default='', null=True)),
                ('label', models.TextField(default='', null=True)),
                ('size', models.TextField(default='', null=True)),
                ('color', models.TextField(default='', null=True)),
                ('published', models.DateTimeField(default=datetime.datetime(2021, 10, 29, 11, 59, 6, 550245))),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=30, populate_from='title', unique=True, verbose_name='slug')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='ArticleImgs')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('device', models.CharField(blank=True, max_length=40, null=True)),
                ('transaction_id', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('ordered_date', models.DateTimeField()),
                ('ordered', models.BooleanField(default=False)),
                ('prix', models.DecimalField(decimal_places=3, default=0, max_digits=20)),
                ('checkout_step', models.CharField(blank=True, max_length=40, null=True)),
                ('adresse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='femalemodeapp.adresse')),
            ],
        ),
        migrations.CreateModel(
            name='OrderArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.CharField(blank=True, max_length=40, null=True)),
                ('quantity', models.IntegerField(default=1)),
                ('ordered', models.BooleanField(default=False)),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='femalemodeapp.article')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SlideImg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='sliderImgs')),
            ],
        ),
        migrations.CreateModel(
            name='OrderState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(choices=[('0', 'Anuler'), ('1', 'En cours de préparation'), ('2', 'Commande confirmée'), ('3', 'Expédié')], max_length=50)),
                ('color', models.CharField(blank=True, choices=[('0', '#FF0000'), ('1', '#FFA500'), ('2', '#00FF7F'), ('3', '#006400')], editable=False, max_length=50, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('related_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='femalemodeapp.order')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, max_length=250, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('orderarticle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='femalemodeapp.orderarticle')),
                ('related_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='femalemodeapp.order')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='messages',
            field=models.ManyToManyField(blank=True, to='femalemodeapp.OrderMessage'),
        ),
        migrations.AddField(
            model_name='order',
            name='orderarticles',
            field=models.ManyToManyField(to='femalemodeapp.OrderArticle'),
        ),
        migrations.AddField(
            model_name='order',
            name='states',
            field=models.ManyToManyField(blank=True, to='femalemodeapp.OrderState'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article',
            name='images',
            field=models.ManyToManyField(related_name='images', to='femalemodeapp.ArticleImage'),
        ),
    ]

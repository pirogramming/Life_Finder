# Generated by Django 2.2.9 on 2020-08-17 17:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('create_profile', '0001_initial'),
        ('photo', '0003_auto_20200818_0209'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': '자유게시판 댓글', 'verbose_name_plural': '자유게시판 댓글'},
        ),
        migrations.RemoveField(
            model_name='comment',
            name='approved_comment',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='text',
        ),
        migrations.AddField(
            model_name='comment',
            name='content',
            field=models.TextField(null=True, verbose_name='댓글내용'),
        ),
        migrations.AddField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='작성일'),
        ),
        migrations.AddField(
            model_name='comment',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='삭제여부'),
        ),
        migrations.AddField(
            model_name='comment',
            name='writer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='create_profile.Profile', verbose_name='댓글작성자'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='photo.Photo', verbose_name='게시글'),
        ),
        migrations.AlterModelTable(
            name='comment',
            table='자유게시판 댓글',
        ),
    ]

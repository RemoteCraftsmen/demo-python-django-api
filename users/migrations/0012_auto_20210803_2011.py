# Generated by Django 3.2.6 on 2021-08-03 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_user_passwordresettoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='passwordResetTokenExpiresAt',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='passwordResetToken',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
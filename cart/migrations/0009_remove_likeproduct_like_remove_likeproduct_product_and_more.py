# Generated by Django 5.1.3 on 2025-03-02 00:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0008_alter_cartproduct_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likeproduct',
            name='like',
        ),
        migrations.RemoveField(
            model_name='likeproduct',
            name='product',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
        migrations.DeleteModel(
            name='LikeProduct',
        ),
    ]

# Generated by Django 5.0.3 on 2024-08-31 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mkopoApp', '0004_loanpayment_modified_by_alter_loan_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], max_length=20),
        ),
    ]
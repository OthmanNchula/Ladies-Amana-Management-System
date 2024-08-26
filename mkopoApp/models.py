from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=date.today)
    status = models.CharField(max_length=10, choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ])
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='loan_modified_by')

    def save(self, *args, **kwargs):
        if 'modified_by' in kwargs:
            self.modified_by = kwargs.pop('modified_by')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"

class LoanPayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payments')
    year = models.IntegerField()
    month = models.IntegerField(choices=[
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ])
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='loanpayment_modified_by')

    def save(self, *args, **kwargs):
        if 'modified_by' in kwargs:
            self.modified_by = kwargs.pop('modified_by')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment for {self.loan.user.username} - {self.year}/{self.month}: {self.amount}"

    class Meta:
        ordering = ['year', 'month']

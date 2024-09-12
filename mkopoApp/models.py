from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=date.today)
    status = models.CharField(max_length=20, choices=[
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
    payment_date = models.DateField()  # Single field for the payment date
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='loanpayment_modified_by')

    def save(self, *args, **kwargs):
        if 'modified_by' in kwargs:
            self.modified_by = kwargs.pop('modified_by')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment for {self.loan.user.username} - {self.payment_date}: {self.amount}"

    class Meta:
        ordering = ['payment_date']
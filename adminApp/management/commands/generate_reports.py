import os
from django.core.management.base import BaseCommand
from adminApp.models import MonthlyReport, YearlyReport, User
from django.utils import timezone
import openpyxl
from django.core.mail import EmailMessage
from django.conf import settings
from django.db.models import Sum
from mtajiApp.models import Mtaji
from michangoApp.models import Michango
from swadaqaApp.models import Swadaqa
from pathlib import Path

class Command(BaseCommand):
    help = 'Generate monthly and yearly reports, and send them to admin'

    def handle(self, *args, **kwargs):
        self.generate_monthly_report()
        self.generate_yearly_report()

    def generate_monthly_report(self):
        current_year = timezone.now().year
        current_month = timezone.now().month

        # Create or retrieve the MonthlyReport instance
        report, created = MonthlyReport.objects.get_or_create(year=current_year, month=current_month)

        # Generate the Excel file
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = f"Monthly Report {current_year}-{current_month}"

        headers = ['S/N', 'JINA', 'MTAJI', 'SWADAQA'] + [f'{month} {current_year}' for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]
        ws.append(headers)

        users = User.objects.filter(is_staff=False, is_superuser=False)
        for index, user in enumerate(users, start=1):
            mtaji = Mtaji.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
            swadaqa = Swadaqa.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
            row = [index, user.get_full_name(), mtaji, swadaqa]
            for month in range(1, 13):
                michango = Michango.objects.filter(user=user, year=current_year, month=month).aggregate(total=Sum('amount'))['total'] or 0
                row.append(michango)
            ws.append(row)

        # Save the report to file
        reports_dir = Path('reports')
        reports_dir.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
        report_path = reports_dir / f'monthly_report_{current_year}_{current_month}.xlsx'
        wb.save(report_path)
        report.file_path = str(report_path)
        report.save()

        # Send the report via email to admins
        self.send_report_via_email(report_path, f'Monthly Report - {current_year}/{current_month}')

    def generate_yearly_report(self):
        current_year = timezone.now().year

        # Create or retrieve the YearlyReport instance
        report, created = YearlyReport.objects.get_or_create(year=current_year)

        # Generate the Excel file
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = f"Yearly Report {current_year}"

        headers = ['S/N', 'JINA', 'MTAJI', 'SWADAQA', 'Total Michango', 'Total Swadaqa']
        ws.append(headers)

        users = User.objects.filter(is_staff=False, is_superuser=False)
        for index, user in enumerate(users, start=1):
            mtaji = Mtaji.objects.filter(user=user, year=current_year).aggregate(total=Sum('amount'))['total'] or 0
            swadaqa = Swadaqa.objects.filter(user=user, year=current_year).aggregate(total=Sum('amount'))['total'] or 0
            total_michango = Michango.objects.filter(user=user, year=current_year).aggregate(total=Sum('amount'))['total'] or 0
            total_swadaqa = Swadaqa.objects.filter(user=user, year=current_year).aggregate(total=Sum('amount'))['total'] or 0
            row = [index, user.get_full_name(), mtaji, swadaqa, total_michango, total_swadaqa]
            ws.append(row)

        # Save the report to file
        reports_dir = Path('reports')
        reports_dir.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
        report_path = reports_dir / f'yearly_report_{current_year}.xlsx'
        wb.save(report_path)
        report.file_path = str(report_path)
        report.save()

        # Send the report via email to admins
        self.send_report_via_email(report_path, f'Yearly Report - {current_year}')

    def send_report_via_email(self, file_path, subject):
        email = EmailMessage(
            subject=subject,
            body='Please find the attached report.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[admin.email for admin in User.objects.filter(is_staff=True, is_active=True)]
        )
        email.attach_file(str(file_path))
        email.send()

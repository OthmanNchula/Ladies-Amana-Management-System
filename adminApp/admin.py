from django.contrib import admin
from .models import ActivityLog, PendingChanges

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('admin', 'action', 'timestamp')
    search_fields = ('admin__username', 'action', 'details')
    readonly_fields = ('admin', 'action', 'timestamp', 'details')

@admin.register(PendingChanges)
class PendingChangesAdmin(admin.ModelAdmin):
    list_display = ('admin', 'table_name', 'action', 'created_at', 'is_approved', 'approved_by')
    search_fields = ('admin__username', 'table_name', 'action', 'data')
    readonly_fields = ('admin', 'table_name', 'action', 'created_at', 'data', 'approved_by')

    def approve_change(self, request, queryset):
        for change in queryset:
            if not change.is_approved:
                # Apply the change (this part should be customized based on the actual data structure)
                model_class = globals()[change.table_name]
                instance_data = change.data
                instance = model_class.objects.get(pk=instance_data['id'])
                for field, value in instance_data.items():
                    setattr(instance, field, value)
                instance.save()

                # Mark as approved
                change.is_approved = True
                change.approved_by = request.user
                change.save()

                self.message_user(request, f"Change approved for {change.table_name}")

    actions = ['approve_change']

    def reject_change(self, request, queryset):
        for change in queryset:
            if not change.is_approved:
                # Just mark the change as rejected (custom logic can be added here)
                change.delete()
                self.message_user(request, f"Change rejected for {change.table_name}")

    actions += ['reject_change']

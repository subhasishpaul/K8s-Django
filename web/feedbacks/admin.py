from django.contrib import admin

from .models import Mobile, Circle, Ssa

admin.site.site_header = "EZ MNP feedback portal - Admin"

class CircleAdmin(admin.ModelAdmin):
    # Delete option is disabled
    def has_delete_permission(self, request, obj = None): 
        return False

class MobileAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    list_display = ('msisdn', 'name', 'address', 'ssa', 'circle', 'upc_date')
    list_filter = ('circle', 'ssa', 'msisdn')
    # fields = ['msisdn', 'name', 'address', 'ssa', 'circle', 'upc_date',
    #           ('reason_for_PO', 'remarks', 'feedback_date')]

    
    # fieldsets = (
    #     (None, {
    #         'fields': ('msisdn', 'name', 'address', 'city', 'circle', 'ssa', 'upc_date', 'upc_expiry_date', 'connection_type', 'avg_monthly_revenue', 'port_status')
    #     }),
    #     ('Enter feedback:', {
    #         'fields': ('customer_contacted', 'remarks', 'feedback_date', 'reason_for_PO', 'user')
    #     }),
    # )

    # Delete option is disabled
    def has_delete_permission(self, request, obj = None): 
        return False

    # readonly_fields = ('msisdn', 'name', 'address', 'ssa', 'circle', 'upc_date')
    def download_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        f = open('report.csv', 'w')
        writer = csv.writer(f)
        writer.writerow(['msisdn', 'name', 'address', 'ssa', 'circle', 'upc_date'])

        for s in queryset:
            writer.writerow([s.msisdn, s.name, s.address, s.ssa, s.circle, s.upc_date])

        f.close()

        f = open('report.csv', 'r')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=stat-info.csv'
        return response

    download_csv.short_description = "Download CSV file for selected stats."

admin.site.register(Mobile, MobileAdmin)

admin.site.register(Circle)
admin.site.register(Ssa)
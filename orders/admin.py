from dataclasses import fields
from urllib import response

from django.contrib import admin
from .models import Order, OrderItem
import csv
import datetime
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe
# Register your models here.



def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')
order_pdf.short_description = 'PDF Invoice'

def export_to_csv(modeladmin,request,queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)


    writer = csv.writer(response)

    fields = [
    field for field in opts.get_fields()
    if field.concrete and not field.many_to_many
]

    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

    

class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
   

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
   list_display=['first_name','email','order_id','paid',order_pdf,'created',]
   inlines = [OrderItemAdmin]
   actions = [export_to_csv]
   



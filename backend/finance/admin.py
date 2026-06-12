from django.contrib import admin

from .models import Invoice, MicroLoan

admin.site.register(MicroLoan)
admin.site.register(Invoice)

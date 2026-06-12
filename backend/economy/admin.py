from django.contrib import admin

from .models import ExportCertificate, FarmerCreditScore, GroupPurchase, InputPrice, LiveAuction

admin.site.register(LiveAuction)
admin.site.register(GroupPurchase)
admin.site.register(FarmerCreditScore)
admin.site.register(ExportCertificate)
admin.site.register(InputPrice)

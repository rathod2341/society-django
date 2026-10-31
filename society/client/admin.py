from django.contrib import admin
from client.models import housingmember
from client.models import family_members
from client.models import notice
from client.models import events
from client.models import complaints
from client.models import events
from client.models import house_worker_type
from client.models import house_worker
from client.models import maintanance_payment , clubhouse_booking


# Register your models here.
admin.site.register(housingmember)
admin.site.register(family_members)
admin.site.register(notice)
admin.site.register(complaints)
admin.site.register(events)
admin.site.register(house_worker_type)
admin.site.register(house_worker)
admin.site.register(maintanance_payment)
admin.site.register(clubhouse_booking)








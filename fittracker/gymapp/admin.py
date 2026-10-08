from django.contrib import admin
from .models import MemberShipPlan, Member, Trainer, Attendance, Payment

# Register your models here.
class MemeberAdmin(admin.ModelAdmin):
    model=Member
    list_display=['id','name','email','phone']
class MemberShipPlan_Admin(admin.ModelAdmin):
    model=MemberShipPlan
    list_display=['id','price','duration_days']
class Trainer_admin(admin.ModelAdmin):
    model=Trainer
    list_display=['id','name','specialization','contact']

class Payment_admin(admin.ModelAdmin):
    model=Payment
    list_display=['id','amount','date','status']
class Attendance_admin(admin.ModelAdmin):
    model=Attendance
    list_display = ['id','date','member','check_in',]
admin.site.register(MemberShipPlan,MemberShipPlan_Admin)
admin.site.register(Member,MemeberAdmin)
admin.site.register(Trainer,Trainer_admin)
admin.site.register(Attendance,Attendance_admin)
admin.site.register(Payment,Payment_admin)
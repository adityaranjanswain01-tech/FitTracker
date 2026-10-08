from django.urls import path
from .views import *

urlpatterns = [
    path('',home, name='home'),
    path('members/',member_list, name='member_list'),
    path('members/add',add_member, name='add_member'),
    path('update_member/<int:data>/',update_member,name='update_member'),
    path('trainers/', trainer_list, name='trainer_list'),
    path('trainers/add/', add_trainer, name='add_trainer'),
    path('update_trainer/<int:trainer_id>/', update_trainer, name='update_trainer'),
    path('payments/',payment_list,name='payment_list'),
    path('payments/add/',add_payment,name='add_payment'),
    path('update_payment/<int:payment_id>/',update_payment,name='update_payment'),
    path('payments/mark-paid/<int:payment_id>/', mark_as_paid, name='mark_as_paid'),
    path('attendances/',attendance_list,name='attendance_list'),
    path('attendances/add/',add_attendance,name='add_attendance'),
    path('attendance/checkout/<int:attendance_id>/', checkout_attendance, name='checkout_attendance'),
    path('plans/', plan_list, name='plan_list'),
    path('plans/add/', add_plan, name='add_plan'),
    path('update_plan/<int:plan_id>/', update_plan, name='update_plan'),
    path('member/delete/<int:id>/', delete_member, name='delete_member'),
    path('trainer/delete/<int:id>/', delete_trainer, name='delete_trainer'),
    path('payment/delete/<int:id>/', delete_payment, name='delete_payment'),
    path('attendance/delete/<int:id>/', delete_attendance, name='delete_attendance'),
    path('plan/delete/<int:id>/', delete_plan, name='delete_plan'),
    
]

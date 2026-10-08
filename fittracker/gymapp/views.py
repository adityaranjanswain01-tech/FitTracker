from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Q
from .models import *


@login_required(login_url='login_')
def home(request):
    user = request.user
    my_members = Member.objects.filter(owner=user)
    members = my_members

    today = timezone.localdate()
    week_later = today + timedelta(days=7)
    total_members = my_members.count()
    checked_in_today = Attendance.objects.filter(owner=user, date=today).count()
    paid_payments = Payment.objects.filter(owner=user, status__iexact='paid')

    collected_this_month = paid_payments.filter(
        date__month=today.month,
        date__year=today.year,
    ).aggregate(total=Sum('amount'))['total'] or 0

    total_collection = paid_payments.aggregate(total=Sum('amount'))['total'] or 0

    pending_amount = 0
    expiring_soon = 0

    for member in my_members.select_related('plan').filter(plan__isnull=False):
        mine = paid_payments.filter(member=member)
        if member.join_date:
            mine = mine.filter(date__gte=member.join_date)
        total_paid = mine.aggregate(total=Sum('amount'))['total'] or 0
        pending_amount += max(member.plan.price - total_paid, 0)

        if member.is_active and member.join_date:
            expiry_date = member.join_date + timedelta(days=member.plan.duration_days)
            if today <= expiry_date <= week_later:
                expiring_soon += 1

    recent_checkins = Attendance.objects.filter(owner=user).order_by('-check_in')[:5]

    if 'search' in request.GET:
        q = request.GET['search']
        members = my_members.filter(
            Q(name__icontains=q) |
            Q(email__icontains=q) |
            Q(phone__icontains=q)
        )
        recent_checkins = Attendance.objects.filter(
            owner=user, member__in=members
        ).order_by('-check_in')[:5]

    context = {
        'members': members,
        'total_members': total_members,
        'checked_in_today': checked_in_today,
        'expiring_soon': expiring_soon,
        'collected_this_month': collected_this_month,
        'total_collection': total_collection,
        'pending_amount': pending_amount,
        'recent_checkins': recent_checkins,
    }
    return render(request, 'home.html', context)

@login_required(login_url='login_')
def member_list(request):
    my_members = Member.objects.filter(owner=request.user)
    members = my_members
    if 'search' in request.GET:
        q = request.GET['search']
        members = my_members.filter(
            Q(name__icontains=q) |
            Q(email__icontains=q) |
            Q(phone__icontains=q)
        )
    context_M = {
        'weekly_members': my_members.filter(plan__duration_days=7).count(),
        'monthly_members': my_members.filter(plan__duration_days=30).count(),
        'quarterly_members': my_members.filter(plan__duration_days=90).count(),
        'yearly_members': my_members.filter(plan__duration_days=365).count(),
        'total_members': my_members.count(),
        'members': members,
    }
    return render(request, 'member_list.html', context_M)


@login_required(login_url='login_')
def add_member(request):
    plans = MemberShipPlan.objects.filter(owner=request.user)
    if request.method == 'POST':
        plan = get_object_or_404(MemberShipPlan, id=request.POST['plan'], owner=request.user)
        Member.objects.create(
            owner=request.user,
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            plan=plan,
            is_active='is_active' in request.POST,
        )
        return redirect('member_list')
    return render(request, 'add_member.html', {'plans': plans})


@login_required(login_url='login_')
def update_member(request, data):
    modify_member = get_object_or_404(Member, id=data, owner=request.user)
    plans = MemberShipPlan.objects.filter(owner=request.user)

    if request.method == 'POST':
        plan = get_object_or_404(MemberShipPlan, id=request.POST['plan'], owner=request.user)

        modify_member.name = request.POST['name']
        modify_member.email = request.POST['email']
        modify_member.phone = request.POST['phone']
        modify_member.plan = plan
        modify_member.is_active = 'is_active' in request.POST
        modify_member.save()
        return redirect('member_list')

    return render(request, 'update_member.html', {'member': modify_member, 'plans': plans})


@login_required(login_url='login_')
def trainer_list(request):
    trainers = Trainer.objects.filter(owner=request.user)
    if 'search' in request.GET:
        q = request.GET['search']
        trainers = trainers.filter(
            Q(name__icontains=q) |
            Q(specialization__icontains=q) |
            Q(contact__icontains=q)
        )
    return render(request, 'trainer_list.html', {'trainers': trainers})


@login_required(login_url='login_')
def add_trainer(request):
    if request.method == 'POST':
        Trainer.objects.create(
            name=request.POST['name'],
            specialization=request.POST['specialization'],
            contact=request.POST['contact'],
            owner=request.user,
        )
        return redirect('trainer_list')
    return render(request, 'add_trainer.html')


@login_required(login_url='login_')
def update_trainer(request, trainer_id):
    trainer = get_object_or_404(Trainer, id=trainer_id, owner=request.user)

    if request.method == 'POST':
        trainer.name = request.POST['name'].strip()
        trainer.specialization = request.POST['specialization'].strip()
        trainer.contact = request.POST['contact'].strip()
        trainer.save()
        return redirect('trainer_list')

    return render(request, 'update_trainer.html', {
        'trainer': trainer,
        'specialization_choices': Trainer.SPECIALIZATION_CHOICES,
    })


def get_paid_total(member, exclude_payment_id=None):
    # Payments are always scoped to the member's owner as well.
    payments = Payment.objects.filter(
        owner=member.owner, member=member, status__iexact='paid'
    )
    if member.join_date:
        payments = payments.filter(date__gte=member.join_date)
    if exclude_payment_id:
        payments = payments.exclude(id=exclude_payment_id)
    return payments.aggregate(total=Sum('amount'))['total'] or Decimal('0')


@login_required(login_url='login_')
def payment_list(request):
    user = request.user
    q = request.GET.get('search', '').strip()

    today = timezone.localdate()
    paid_payments = Payment.objects.filter(owner=user, status__iexact='paid')
    total_payment = paid_payments.aggregate(total=Sum('amount'))['total'] or 0

    collected_this_month = paid_payments.filter(
        date__month=today.month,
        date__year=today.year,
    ).aggregate(total=Sum('amount'))['total'] or 0

    rows = []
    total_pending = 0
    pending_members = 0
    expiring_soon = 0

    for member in Member.objects.filter(owner=user).select_related('plan'):

        mine = paid_payments.filter(member=member)
        if member.join_date:
            mine = mine.filter(date__gte=member.join_date)

        price = member.plan.price if member.plan_id else 0
        member.price = price
        member.total_paid = mine.aggregate(total=Sum('amount'))['total'] or 0

        last_payment = mine.order_by('-date', '-id').first()
        member.last_paid = last_payment.amount if last_payment else 0

        member.left_to_pay = max(price - member.total_paid, 0)

        member.expiry_date = None
        member.days_left = None
        if member.plan_id and member.join_date:
            member.expiry_date = member.join_date + timedelta(days=member.plan.duration_days)
            member.days_left = (member.expiry_date - today).days

        if not member.is_active:
            member.plan_status = 'inactive'
        elif member.days_left is None:
            member.plan_status = 'none'
        elif member.days_left < 0:
            member.plan_status = 'expired'
        elif member.days_left <= 7:
            member.plan_status = 'expiring'
            expiring_soon += 1
        else:
            member.plan_status = 'active'

        if member.left_to_pay > 0:
            member.status_key = 'pending'
            pending_members += 1
            total_pending += member.left_to_pay
        elif member.plan_id and member.total_paid > 0:
            member.status_key = 'paid'
        else:
            member.status_key = 'none'

        rows.append(member)

    if q:
        rows = [m for m in rows if q.lower() in m.name.lower()]

    rows.sort(key=lambda m: (m.status_key != 'pending', -m.left_to_pay, m.name))

    context = {
        'members': rows,
        'collected_this_month': collected_this_month,
        'pending_members': pending_members,
        'total_pending': total_pending,
        'total_payment': total_payment,
        'expiring_soon': expiring_soon,
        'search': q,
    }
    return render(request, 'payment_list.html', context)


@login_required(login_url='login_')
def add_payment(request):
    members = Member.objects.filter(
        owner=request.user, is_active=True, plan__isnull=False
    ).select_related('plan')

    for member in members:
        member.left_to_pay = max(Decimal(str(member.plan.price)) - get_paid_total(member), Decimal('0'))

    if request.method == 'POST':
        member = get_object_or_404(
            Member.objects.select_related('plan'),
            id=request.POST['member'],
            owner=request.user,
            plan__isnull=False,
        )
        amount = Decimal(request.POST['amount'])
        left_to_pay = Decimal(str(member.plan.price)) - get_paid_total(member)

        if amount > left_to_pay:
            return render(request, 'add_payment.html', {
                'members': members,
                'error': f'Only ₹{int(left_to_pay)} is left to pay.',
                'selected_member': str(member.id),
            })

        Payment.objects.create(owner=request.user, member=member, amount=amount, status='Paid')
        return redirect('payment_list')

    return render(request, 'add_payment.html', {
        'members': members,
        'selected_member': request.GET.get('member'),
    })


@login_required(login_url='login_')
def update_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, owner=request.user)
    members = Member.objects.filter(owner=request.user, plan__isnull=False).filter(
        Q(is_active=True) | Q(id=payment.member_id)
    )

    if request.method == 'POST':
        member = get_object_or_404(
            Member.objects.select_related('plan'),
            id=request.POST['member'],
            owner=request.user,
            plan__isnull=False,
        )
        amount = Decimal(request.POST['amount'])
        left_to_pay = Decimal(str(member.plan.price)) - get_paid_total(member, exclude_payment_id=payment.id)

        if amount > left_to_pay:
            return render(request, 'update_payment.html', {
                'payment': payment,
                'members': members,
                'error': f'Only ₹{int(left_to_pay)} is left to pay for this member.',
            })

        payment.member = member
        payment.amount = amount
        payment.status = 'Paid'
        payment.save()
        return redirect('payment_list')

    return render(request, 'update_payment.html', {'payment': payment, 'members': members})


@login_required(login_url='login_')
def mark_as_paid(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, owner=request.user)
    payment.status = 'Paid'
    payment.save()
    return redirect('payment_list')


@login_required(login_url='login_')
def attendance_list(request):
    q = request.GET.get('search', '').strip()
    today = timezone.localdate()

    all_attendances = Attendance.objects.filter(owner=request.user).select_related('member').order_by('-check_in')
    attendances = all_attendances
    if q:
        attendances = all_attendances.filter(member__name__icontains=q)

    return render(request, 'attendance_list.html', {
        'attendances': attendances,
        'checked_in_today': all_attendances.filter(date=today).count(),
        'inside_now': all_attendances.filter(check_out__isnull=True).count(),
        'total_records': all_attendances.count(),
        'search': q,
    })


@login_required(login_url='login_')
def add_attendance(request):
    members = Member.objects.filter(owner=request.user, is_active=True)
    if request.method == 'POST':
        member = Member.objects.get(id=request.POST['member'],owner=request.user)
        existing = Attendance.objects.filter(owner=request.user,member=member,check_out__isnull=True).exists()
        if not existing:
            Attendance.objects.create(
                owner=request.user,
                member=member
            )
        return redirect('attendance_list')
    return render(request,'add_attendance.html',{'members': members})

@login_required(login_url='login_')
def checkout_attendance(request, attendance_id):
    if request.method == 'POST':
        attendance = Attendance.objects.get(id=attendance_id,owner=request.user)
        attendance.check_out = timezone.now()
        attendance.save()
    return redirect('attendance_list')


@login_required(login_url='login_')
def plan_list(request):
    plans = list(MemberShipPlan.objects.filter(owner=request.user).order_by('duration_days'))
    for plan in plans:
        plan.member_count = Member.objects.filter(owner=request.user, plan=plan).count()

    context = {
        'plans': plans,
        'total_plans': len(plans),
        'total_members': Member.objects.filter(owner=request.user, plan__in=plans).count(),
    }
    return render(request, 'membershipPlan_list.html', context)


@login_required(login_url='login_')
def add_plan(request):
    if request.method == 'POST':
        name = request.POST['name'].strip()
        price = request.POST['price']
        duration_days = request.POST['duration_days']

        if int(price) <= 0 or int(duration_days) <= 0:
            return render(request, 'add_plan.html', {
                'error': 'Price and duration must be greater than 0.',
                'form': request.POST,
            })

        if MemberShipPlan.objects.filter(owner=request.user, name__iexact=name).exists():
            return render(request, 'add_plan.html', {
                'error': 'A plan with this name already exists.',
                'form': request.POST,
            })

        MemberShipPlan.objects.create(
            name=name,
            price=price,
            duration_days=duration_days,
            owner=request.user,
        )
        return redirect('plan_list')
    return render(request, 'add_plan.html')


@login_required(login_url='login_')
def update_plan(request, plan_id):
    plan = get_object_or_404(MemberShipPlan, id=plan_id, owner=request.user)

    if request.method == 'POST':
        name = request.POST['name'].strip()
        price = request.POST['price']
        duration_days = request.POST['duration_days']

        if int(price) <= 0 or int(duration_days) <= 0:
            return render(request, 'update_plan.html', {
                'plan': plan,
                'error': 'Price and duration must be greater than 0.',
            })
        plan.name = name
        plan.price = price
        plan.duration_days = duration_days
        plan.save()
        return redirect('plan_list')

    return render(request, 'update_plan.html', {'plan': plan})

from django.views.decorators.http import require_POST

@login_required(login_url='login_')
@require_POST
def delete_member(request, id):
    member = get_object_or_404(Member, id=id, owner=request.user)
    member.delete()
    return redirect('member_list')

@login_required(login_url='login_')
@require_POST
def delete_trainer(request, id):
    trainer = get_object_or_404(Trainer,id=id, owner=request.user)
    trainer.delete()
    return redirect('trainer_list')

@login_required(login_url='login_')
@require_POST
def delete_payment(request, id):
    payment =get_object_or_404(Payment,id=id, owner=request.user)
    payment.delete()
    return redirect('payment_list')

@login_required(login_url='login_')
@require_POST
def delete_attendance(request, id):
    attendance = get_object_or_404(Attendance,id=id, owner=request.user)
    attendance.delete()
    return redirect('attendance_list')

@login_required(login_url='login_')
@require_POST
def delete_plan(request, id):
    plan = get_object_or_404(MemberShipPlan,id=id, owner=request.user)
    plan.delete()
    return redirect('plan_list')
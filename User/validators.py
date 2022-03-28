import datetime
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import CustomUser, Block, WrongPass, IP


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def login_username_validator(request, phone_number, password):
    user = authenticate(phone_number=phone_number, password=password)
    if user is not None:
        if user.is_active and not user.is_locked:
            login(request, user)
            return HttpResponse('done')
        else:
            pass  # verify user and unlock account
    else:
        ip = get_ip(request)
        faild_login, created = IP.objects.get_or_create(ip=ip)
        user = get_object_or_404(CustomUser, phone_number=phone_number)
        if Block.objects.filter(user=user).exists():
            block = Block.objects.get(user=user)
            block.count_of_wrong_pass += 1
            block.save()
            ip = get_ip(request)
            ip_obj, created = IP.objects.get_or_create(ip=ip)
            print(ip_obj,'11111111111111111111111111111')
            wrong_pass = WrongPass.objects.create(user=user,
                                                  state=block.count_of_wrong_pass, ip=ip_obj)
            active_wpass_counts = WrongPass.objects.filter(user=user, is_active=True).count()
            if active_wpass_counts == 10:
                first_active_wpass = WrongPass.objects.get(user=user, state=(wrong_pass.state - 9))
                tenth_active_wpass = wrong_pass
                time_delta = tenth_active_wpass.date - first_active_wpass.date
                if time_delta.seconds <= 3600:
                    for i in range(10):
                        deactivate_wrong_p = WrongPass.objects.get(user=user, state=(wrong_pass.state - i))
                        deactivate_wrong_p.is_active = False
                        deactivate_wrong_p.save()
                        user.is_locked = True  # lock the account
                    user.number_of_user_blocking += 1
                    user.save()
                else:
                    first_active_wpass = WrongPass.objects.get(user=user, state=(wrong_pass.state - 9))
                    first_active_wpass.is_active = False
                    first_active_wpass.save()
        else:
            block = Block.objects.create(user=user)
            wrong_pass = WrongPass.objects.create(user=user, state=block.count_of_wrong_pass)


def ip_validator(request):
    ip = get_ip(request)
    ip_obj, created = IP.objects.get_or_create(ip=ip)
    if not ip_obj.is_locked:
        time_threshold = datetime.datetime.now(timezone.utc) - datetime.timedelta(hours=1)
        results_count = WrongPass.objects.filter(date__gt=time_threshold, ip=ip_obj).count()
        if results_count > 4:
            ip_obj.is_locked = True
            ip_obj.save()
            raise ValidationError("too many wrong try")
    else:
        raise ValidationError("IP is locked")







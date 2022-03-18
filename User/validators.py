from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils import timezone

from .utils import get_client_ip
from .models import CustomUser, Block, WrongPass, IP
from .decoretors import ip_checker


# @ip_checker
def login_validator(request, phone_number, password):
    ip = get_client_ip(request)
    if WrongPass.objects.filter(user_IP=ip).count() >= 5:
        last_wrong_pass = WrongPass.objects.get(user_IP=ip).order_by('-id')[0]  # end of range
        first_of_range = WrongPass.objects.get(pk=(last_wrong_pass.pk - 4))
        time_delta = last_wrong_pass.date - first_of_range.date
        if time_delta.seconds <= 3600:
            raise ValueError('?')
        else:
            user = authenticate(phone_number=phone_number, password=password)
            if user is not None:
                if user.is_active and not user.is_locked:
                    login(request, user)
                    return HttpResponse('done')
                else:
                    pass  # verify user and unlock account
            else:
                faild_login = IP.objects.create(username=phone_number, ip=ip)
                user = get_object_or_404(CustomUser, phone_number=phone_number)
                if Block.objects.filter(user=user).exists():
                    block = Block.objects.get(user=user)
                    block.count_of_wrong_pass += 1
                    block.save()
                    wrong_pass = WrongPass.objects.create(user=user,
                                                          state=block.count_of_wrong_pass,
                                                          user_IP=get_client_ip(request))
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






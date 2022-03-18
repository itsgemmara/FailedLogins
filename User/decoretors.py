from .utils import get_client_ip
from .models import WrongPass


def ip_checker(func):
    pass
    # def inner():
    #     ip = get_client_ip(request)
    #     if WrongPass.objects.filter(user_IP=ip).count() >= 5:
    #         last_wrong_pass = WrongPass.objects.get(user_IP=ip).order_by('-id')[0]  # end of range
    #         first_of_range = WrongPass.objects.get(pk=(last_wrong_pass.pk-4))
    #         time_delta = last_wrong_pass.date - first_of_range.date
    #         if time_delta.seconds <= 3600:
    #             raise ValueError('?')
    #         else:
    #             func()
    # return inner

import random
from django.utils import timezone
import threading
from rest_framework.generics import GenericAPIView

from .serializer import *
from .models import UnBlockCode


def activate_user_account( user, main_code, verify_code):
    if main_code.code == verify_code:
        user.is_locked, user.is_active = False, True
        main_code.is_expired, main_code.used = True, True
        main_code.save()
        user.save()
    else:
        raise Exception('invalid code')


class UnblockCodeGeneratorApi(GenericAPIView):
    """
    generating unblock code.
    """
    serializer_class = UnBlockCodeSerializer

    def __init__(self, code=None, verify_code=None):
        self.code = code
        self.verify_code = verify_code

    def set_is_expired(self):
        self.code.is_expired = True
        self.code.expired_at = timezone.now()
        self.code.save()
        return self.code

    def post(self, request):
        serializer = UnBlockCodeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        new_code_status = serializer.validated_data["new_code"]
        unexpired_codes = UnBlockCode.objects.filter(user=user, used=False, is_expired=False)
        if unexpired_codes.count() == 0 or new_code_status:
            print('hiiiiiii')
            self.verify_code = random.randint(10000, 99999)
            print('self.verify_codeeeeee',self.verify_code)
            if unexpired_codes.count() != 0:
                for i in unexpired_codes:
                    i.is_expired = True
                    i.save()
            self.code = UnBlockCode.objects.create(code=self.verify_code, user=user)
            t = threading.Timer(interval=120, function=self.set_is_expired)
            t.start()
        elif unexpired_codes.count() == 1 and not new_code_status:
            self.verify_code = UnBlockCode.objects.get(user=user, used=False, is_expired=False).code
        return self.verify_code


class UnBlockApi(GenericAPIView):
    """
    unblocking accounts by verify code.
    """
    serializer_class = UnBlockSerializer

    def post(self, request):
        serializer = UnBlockSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception= True)
        user = serializer.validated_data["user"]
        verify_code = serializer.validated_data["verify_code"]
        try:
            main_code = UnBlockCode.objects.get(user=user, used=False, is_expired=False)
            activate_user_account(user, main_code, verify_code)
            msg = 'your account is active and unlocked now!'
        except Exception as ex:
            raise Exception('invalid code. Enter the code correctly or request a new code.')

        return {'massage': msg}

from typing import List, Dict, Union, Tuple
import logging

from django.http import HttpRequest, JsonResponse
from django.contrib.auth.models import Group

import jwt
from dateutil import parser

from backend.settings import SECRET_KEY
from user.models import User


logger = logging.getLogger('django')


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def get_user(data: Dict) -> Union[Tuple[User, List[Group]], object]:
        try:
            user = User.objects.get(username=data.get('username'))
            return user
        except User.DoesNotExist as err:
            logger.error(f'error creating or retrieving user. reason: {err}')
            return

    def __call__(self, request: HttpRequest):
        setattr(request, '_dont_enforce_csrf_checks', True)
        auth_header: str = request.headers.get('authorization')
        if auth_header:
            token_obj: List[str] = auth_header.split(' ')
            if token_obj[0].lower() != 'bearer':
                return JsonResponse(data={
                        'message': 'invalid token type',
                        'success': False,
                    }, status=400)
            try:
                payload: Dict = jwt.decode(jwt=token_obj[1], key=SECRET_KEY, algorithms='HS256', verify=True)
                print(payload)
                user_obj = self.get_user(data=payload)
                if not user_obj:
                    return JsonResponse(data={
                        'message': 'cannot retrieve user information',
                        'success': False
                    }, status=401)
                setattr(request, 'user', user_obj)
            except Exception as err:
                return JsonResponse(data={
                    'message': f'auth exception {str(err)}',
                    'success': False,
                }, status=401)
        response = self.get_response(request)
        return response
import json

from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from django_redis import get_redis_connection

from apps.utils.decorator import RequiredMethod, Protect, LoginRequired
from apps.utils.validator import validate_username, validate_password, validate_email
from apps.utils.response_status import ResponseStatus
from apps.utils.response_processor import process_response

from apps.account import models as account_models
from apps.account.models import AccountRole


@Protect
@RequiredMethod('POST')
def register(request):
    request_data = json.loads(request.body)

    verification_code = request_data.get('verification_code')
    if not verification_code:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)

    username = request_data.get('username')
    if not username:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)
    status = validate_username(username)
    if status is not None:
        return process_response(request, status)

    password = request_data.get('password')
    if not password:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)
    status = validate_password(password)
    if status is not None:
        return process_response(request, status)

    email = request_data.get('email')
    if not email:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)
    status = validate_email(email)
    if status is not None:
        return process_response(request, status)

    role = request_data.get('role')
    if not role:
        return process_response(request_data, ResponseStatus.MISSING_PARAMETER_ERROR)
    if not role.isdigit():
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)
    role = int(role)
    if role != AccountRole.Buyer and role != AccountRole.Seller:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    if account_models.Account.objects.filter(username=username):
        return process_response(request, ResponseStatus.USERNAME_EXISTED_ERROR)

    if account_models.Account.objects.filter(email=email):
        return process_response(request, ResponseStatus.EMAIL_EXISTED_ERROR)

    cache = get_redis_connection()
    stored_code = cache.get('verification_code_' + email)
    if verification_code != stored_code:
        return process_response(request, ResponseStatus.VERIFICATION_CODE_NOT_MATCH_ERROR)
    cache.delete('verification_code_' + email)

    account = account_models.Account(username=username,
                                     password=make_password(password),
                                     email=email,
                                     role=role)
    account.save()

    account_info = account_models.AccountInfo(account=account)
    account_info.save()

    return process_response(request, ResponseStatus.OK)


@Protect
@RequiredMethod('POST')
def login(request):
    request_data = json.loads(request.body)

    username = request_data.get('username')
    if not username:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)

    password = request_data.get('password')
    if not password:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)

    if request.session.get('username', None):
        return process_response(request, ResponseStatus.OK)

    account = account_models.Account.objects.filter(Q(username=username) | Q(email=username)).first()
    if not account:
        return process_response(request, ResponseStatus.USERNAME_NOT_EXISTED_ERROR)

    if check_password(password, account.password) is False:
        return process_response(request, ResponseStatus.PASSWORD_NOT_MATCH_ERROR)

    request.session['username'] = account.username

    return process_response(request, ResponseStatus.OK)


@Protect
@RequiredMethod('POST')
@LoginRequired
def logout(request):
    del request.session['username']

    return process_response(request, ResponseStatus.OK)


@Protect
@RequiredMethod('GET')
def get_status(request):
    if request.session.get('username') is not None:
        username = request.session.get('username')

        account = account_models.Account.objects.filter(username=username).first()
        if not account:
            return process_response(request, ResponseStatus.UNEXPECTED_ERROR)

        request.data = {
            'login': True,
            'username': account.username,
            'email': account.email,
            'role': account.role,
            'nickname': account.info.nickname,
            'avatar': account.info.avatar,
        }

        if int(account.role) == AccountRole.Seller:
            request.data['balance'] = '{}.{}'.format(account.info.balance_integer, account.info.balance_decimal)

        return process_response(request, ResponseStatus.OK)
    else:
        request.data = {
            'login': False,
        }

        return process_response(request, ResponseStatus.OK)

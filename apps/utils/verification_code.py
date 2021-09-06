import json

from django_redis import get_redis_connection

from apps.utils.decorator import Protect, RequiredMethod
from apps.utils.response_status import ResponseStatus
from apps.utils.response_processor import process_response
from apps.utils.validator import validate_email
from apps.utils.random_string_generator import generate_random_string, Pattern
from apps.utils.email_sender import send
from apps.account import models as account_models
from shop import settings


@Protect
@RequiredMethod('POST')
def verification_code(request):
    request_data = json.loads(request.body)

    email = request_data.get('email')
    if not email:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)
    status = validate_email(email)
    if status is not None:
        return process_response(request, status)

    check = request_data.get('check')
    if check:
        account = account_models.Account.objects.filter(email=email).first()
        if account:
            return process_response(request, ResponseStatus.USERNAME_EXISTED_ERROR)

    code = generate_random_string(6, Pattern.Digits)
    message = settings.VERIFICATION_CODE_MAIL_MESSAGE.format(code=code, email=email)

    send(email, message)

    cache = get_redis_connection()
    cache.set('verification_code_' + email, code, 10 * settings.MINUTE)

    return process_response(request, ResponseStatus.OK)

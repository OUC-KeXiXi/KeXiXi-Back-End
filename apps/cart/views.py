import json

from apps.utils.decorator import RequiredMethod, Protect, LoginRequired
from apps.utils.response_status import ResponseStatus
from apps.utils.response_processor import process_response
from shop import settings

from apps.account import models as account_models
from apps.account.models import AccountRole
from apps.course import models as course_models
from apps.cart import models as cart_models


@Protect
@RequiredMethod('POST')
@LoginRequired
def add_course(request):
    request_data = json.loads(request.body)

    account = account_models.Account.objects.filter(username=request.session.get('username')).first()
    if int(account.role) != AccountRole.Buyer:
        return process_response(request, ResponseStatus.PERMISSION_DENIED)

    course_id = request_data.get('course_id')
    if not course_id:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)

    course = course_models.Course.objects.filter(id=course_id, deleted=False, published=True).first()
    if not course:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    cart = cart_models.Cart.objects.filter(buyer=account, course=course)
    if cart:
        return process_response(request, ResponseStatus.ALREADY_IN_CART)

    cart = cart_models.Cart(buyer=account, course=course)
    cart.save()

    return process_response(request, ResponseStatus.OK)


@Protect
@RequiredMethod('GET')
@LoginRequired
def get_my_cart(request):
    account = account_models.Account.objects.filter(username=request.session.get('username')).first()
    if int(account.role) != AccountRole.Buyer:
        return process_response(request, ResponseStatus.PERMISSION_DENIED)

    carts = cart_models.Cart.objects.filter(buyer=account)

    request.data = {
        'courses': []
    }

    for cart in carts:
        request.data['courses'].append(cart.course.id)

    return process_response(request, ResponseStatus.OK)


@Protect
@RequiredMethod('POST')
@LoginRequired
def delete_course(request):
    request_data = json.loads(request.body)

    account = account_models.Account.objects.filter(username=request.session.get('username')).first()
    if int(account.role) != AccountRole.Buyer:
        return process_response(request, ResponseStatus.PERMISSION_DENIED)

    course_id = request_data.get('course_id')
    if not course_id:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)

    cart = cart_models.Cart.objects.filter(buyer=account, course=course_id)
    if not cart:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    cart.delete()

    return process_response(request, ResponseStatus.OK)

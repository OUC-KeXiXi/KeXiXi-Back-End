import json

from apps.utils.decorator import RequiredMethod, Protect, LoginRequired
from apps.utils.response_status import ResponseStatus
from apps.utils.response_processor import process_response
from shop import settings

from apps.account import models as account_models
from apps.account.models import AccountRole
from apps.course import models as course_models
from apps.cart import models as cart_models
from apps.order import models as order_models


def calculate(a_integer, a_decimal, b_integer, b_decimal):
    integer = a_integer + b_integer
    decimal_part = a_decimal + b_decimal
    integer += decimal_part // 100
    decimal = decimal_part % 100

    return integer, decimal


@Protect
@RequiredMethod('POST')
@LoginRequired
def place_order(request):
    request_data = json.loads(request.body)

    account = account_models.Account.objects.filter(username=request.session.get('username')).first()
    if int(account.role) != AccountRole.Buyer:
        return process_response(request, ResponseStatus.PERMISSION_DENIED)

    courses_id = request_data.get('courses_id')
    if not courses_id:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)

    if type(courses_id) is not list:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    courses = []
    for one in courses_id:
        cart = cart_models.Cart.objects.filter(buyer=account, course=one).first()
        if not cart:
            return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

        courses.append(cart.course)

    order = order_models.Order(buyer=account)
    order.save()

    price_integer = 0
    price_decimal = 0
    for one in courses:
        snapshot = one.get_latest_course()
        price_integer, price_decimal = calculate(price_integer, price_decimal, snapshot.price_integer, snapshot.price_decimal)

        order_detail = order_models.OrderDetail(order=order, snapshot=snapshot)
        order_detail.save()

        cart = cart_models.Cart.objects.filter(buyer=account, course=one).first()
        cart.delete()

    order.price_integer = price_integer
    order.price_decimal = price_decimal
    order.save()

    request.data = {
        'order_id': order.id
    }

    return process_response(request, ResponseStatus.OK)


@Protect
@RequiredMethod('GET')
@LoginRequired
def get_order_detail(request):
    account = account_models.Account.objects.filter(username=request.session.get('username')).first()
    if int(account.role) != AccountRole.Buyer:
        return process_response(request, ResponseStatus.PERMISSION_DENIED)

    order_id = request.GET.get('order_id')
    if not order_id:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)

    order = order_models.Order.objects.filter(id=order_id, buyer=account).first()
    if not order:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    request.data = {
        'order_id': order_id,
        'price': '.'.join([str(order.price_integer), str(order.price_decimal)]),
        'paid': order.paid,
        'create_time': order.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        'snapshots': []
    }

    snapshots = order.get_detail()
    for one in snapshots:
        request.data['snapshots'].append(one.id)

    return process_response(request, ResponseStatus.OK)


@Protect
@RequiredMethod('GET')
def pay_order(request):
    order_id = request.GET.get('order_id')
    if not order_id:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)

    order = order_models.Order.objects.filter(id=order_id, paid=False).first()
    if not order:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    order.paid = True
    order.save()

    details = order.get_detail()
    for one in details:
        seller = one.snapshot.root.seller
        seller_info = seller.info
        seller_info.gain(one.snapshot.price_integer, one.snapshot.price_decimal)
        seller_info.save()

    return process_response(request, ResponseStatus.OK)

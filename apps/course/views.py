import json
import re
import os

from apps.utils.decorator import RequiredMethod, Protect, LoginRequired
from apps.utils.response_status import ResponseStatus
from apps.utils.response_processor import process_response
from shop import settings

from apps.account import models as account_models
from apps.account.models import AccountRole
from apps.course import models as course_models


@Protect
@RequiredMethod('POST')
@LoginRequired
def create_new_course(request):
    account = account_models.Account.objects.filter(username=request.session.get('username')).first()
    if int(account.role) != AccountRole.Seller:
        return process_response(request, ResponseStatus.PERMISSION_DENIED)

    request_data = json.loads(request.body)

    title = request_data.get('title')
    if not title:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)
    if len(title) > 100:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    content = request_data.get('content')
    if not content:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)

    cover = request_data.get('cover')
    if not cover:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)
    if len(cover) > 50 or cover[:7] != '/media/' or re.search(r'\.\.', cover) \
            or not os.path.exists('.' + cover):
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    price = request_data.get('price')
    if not price:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)
    price = price.split('.')
    if len(price) != 2:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)
    integer, decimal = price[0], price[1]
    if len(decimal) != 2:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)
    if not integer.isdigit() or not decimal.isdigit():
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    tags = request_data.get('tags')
    if tags:
        if type(tags) is not list:
            return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    course = course_models.Course(title=title, seller=account)
    course.save()
    course.tags.add(*course_models.CourseTag.objects.filter(id__in=tags))

    snapshot = course_models.CourseSnapshot(root=course,
                                            title=title,
                                            content=content,
                                            cover=cover,
                                            price_integer=integer,
                                            price_decimal=decimal,
                                            )
    snapshot.save()

    request.data = {
        'course_id': course.id,
        'snapshot_id': course.get_latest_course().id
    }

    return process_response(request, ResponseStatus.OK)


@Protect
@RequiredMethod('GET')
def get_course_detail(request):
    course_id = request.GET.get('course_id')
    if not course_id:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)

    course = course_models.Course.objects.filter(id=course_id).first()
    if not course:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    snapshot = course.get_latest_course()

    request.data = {
        'title': course.title,
        'seller_id': course.seller.id,
        'seller_name': course.seller.info.nickname if course.seller.info.nickname else course.seller.username,
        'published': course.published,
        'tags': [{'tag_id': tag.id, 'tag_name': tag.name} for tag in course.tags.all()],
        'deleted': course.deleted,
        'sales': course.sales,
        'snapshot_id': snapshot.id,
        'content': snapshot.content,
        'cover': snapshot.cover,
        'price': '.'.join([str(snapshot.price_integer), str(snapshot.price_decimal)]),
        'create_time': snapshot.create_time.strftime('%Y-%m-%d %H:%M:%S')
    }

    return process_response(request, ResponseStatus.OK)


@Protect
@RequiredMethod('GET')
def get_snapshot_detail(request):
    snapshot_id = request.GET.get('snapshot_id')
    if not snapshot_id:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)

    snapshot = course_models.CourseSnapshot.objects.filter(id=snapshot_id).first()
    if not snapshot:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    course = snapshot.root

    request.data = {
        'title': course.title,
        'seller_id': course.seller.id,
        'seller_name': course.seller.info.nickname if course.seller.info.nickname else course.seller.username,
        'published': course.published,
        'tags': [{'tag_id': tag.id, 'tag_name': tag.name} for tag in course.tags.all()],
        'deleted': course.deleted,
        'sales': course.sales,
        'snapshot_id': snapshot.id,
        'content': snapshot.content,
        'cover': snapshot.cover,
        'price': '.'.join([str(snapshot.price_integer), str(snapshot.price_decimal)]),
        'create_time': snapshot.create_time.strftime('%Y-%m-%d %H:%M:%S')
    }

    return process_response(request, ResponseStatus.OK)


@Protect
@RequiredMethod('POST')
@LoginRequired
def edit_course(request):
    account = account_models.Account.objects.filter(username=request.session.get('username')).first()
    if int(account.role) != AccountRole.Seller:
        return process_response(request, ResponseStatus.PERMISSION_DENIED)

    request_data = json.loads(request.body)

    course_id = request_data.get('course_id')
    if not course_id:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)

    course = course_models.Course.objects.filter(id=course_id, deleted=False).first()
    if not course:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    if account.id != course.seller.id:
        return process_response(request, ResponseStatus.PERMISSION_DENIED)

    title = request_data.get('title')
    if not title:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)
    if len(title) > 100:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    content = request_data.get('content')
    if not content:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)

    cover = request_data.get('cover')
    if not cover:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)
    if len(cover) > 50 or cover[:7] != '/media/' or re.search(r'\.\.', cover) \
            or not os.path.exists('.' + cover):
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    price = request_data.get('price')
    if not price:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)
    price = price.split('.')
    if len(price) != 2:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)
    integer, decimal = price[0], price[1]
    if len(decimal) != 2:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)
    if not integer.isdigit() or not decimal.isdigit():
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    tags = request_data.get('tags')
    if tags:
        if type(tags) is not list:
            return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    course.title = title
    course.save()
    course.tags.clear()
    course.tags.add(*course_models.CourseTag.objects.filter(id__in=tags))

    snapshot = course_models.CourseSnapshot(root=course,
                                            title=title,
                                            content=content,
                                            cover=cover,
                                            price_integer=integer,
                                            price_decimal=decimal,
                                            )
    snapshot.save()

    request.data = {
        'course_id': course.id,
        'snapshot_id': course.get_latest_course().id
    }

    return process_response(request, ResponseStatus.OK)


@Protect
@RequiredMethod('POST')
@LoginRequired
def delete_course(request):
    account = account_models.Account.objects.filter(username=request.session.get('username')).first()
    if int(account.role) != AccountRole.Seller:
        return process_response(request, ResponseStatus.PERMISSION_DENIED)

    request_data = json.loads(request.body)

    course_id = request_data.get('course_id')
    if not course_id:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)

    course = course_models.Course.objects.filter(id=course_id, deleted=False).first()
    if not course:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    if account.id != course.seller.id:
        return process_response(request, ResponseStatus.PERMISSION_DENIED)

    course.deleted = True
    course.published = False
    course.save()

    return process_response(request, ResponseStatus.OK)


@Protect
@RequiredMethod('POST')
@LoginRequired
def publish_course(request):
    account = account_models.Account.objects.filter(username=request.session.get('username')).first()
    if int(account.role) != AccountRole.Seller:
        return process_response(request, ResponseStatus.PERMISSION_DENIED)

    request_data = json.loads(request.body)

    course_id = request_data.get('course_id')
    if not course_id:
        return process_response(request, ResponseStatus.MISSING_PARAMETER_ERROR)

    course = course_models.Course.objects.filter(id=course_id, deleted=False).first()
    if not course:
        return process_response(request, ResponseStatus.BAD_PARAMETER_ERROR)

    if account.id != course.seller.id:
        return process_response(request, ResponseStatus.PERMISSION_DENIED)

    course.published = True
    course.save()

    return process_response(request, ResponseStatus.OK)


@Protect
@RequiredMethod('GET')
def get_latest_courses_list(request):
    courses = course_models.Course.objects.filter(published=True, deleted=False).order_by('-id')

    request.data = {
        'courses': []
    }

    for course in courses:
        snapshot = course.get_latest_course()

        request.data['courses'].append({
            'title': course.title,
            'seller_id': course.seller.id,
            'seller_name': course.seller.info.nickname if course.seller.info.nickname else course.seller.username,
            'published': course.published,
            'tags': [{'tag_id': tag.id, 'tag_name': tag.name} for tag in course.tags.all()],
            'deleted': course.deleted,
            'sales': course.sales,
            'snapshot_id': snapshot.id,
            'content': snapshot.content,
            'cover': snapshot.cover,
            'price': '.'.join([str(snapshot.price_integer), str(snapshot.price_decimal)]),
            'create_time': snapshot.create_time.strftime('%Y-%m-%d %H:%M:%S')
        })

    return process_response(request, ResponseStatus.OK)


@Protect
@RequiredMethod('GET')
def get_hottest_courses_list(request):
    courses = course_models.Course.objects.filter(published=True, deleted=False).order_by('-sales', '-id')

    request.data = {
        'courses': []
    }

    for course in courses:
        snapshot = course.get_latest_course()

        request.data['courses'].append({
            'title': course.title,
            'seller_id': course.seller.id,
            'seller_name': course.seller.info.nickname if course.seller.info.nickname else course.seller.username,
            'published': course.published,
            'tags': [{'tag_id': tag.id, 'tag_name': tag.name} for tag in course.tags.all()],
            'deleted': course.deleted,
            'sales': course.sales,
            'snapshot_id': snapshot.id,
            'content': snapshot.content,
            'cover': snapshot.cover,
            'price': '.'.join([str(snapshot.price_integer), str(snapshot.price_decimal)]),
            'create_time': snapshot.create_time.strftime('%Y-%m-%d %H:%M:%S')
        })

    return process_response(request, ResponseStatus.OK)


def get_pinned_courses_list(request):
    courses = course_models.Course.objects.filter(published=True, deleted=False, pinned=True).order_by('-sales', '-id')

    request.data = {
        'courses': []
    }

    for course in courses:
        snapshot = course.get_latest_course()

        request.data['courses'].append({
            'title': course.title,
            'seller_id': course.seller.id,
            'seller_name': course.seller.info.nickname if course.seller.info.nickname else course.seller.username,
            'published': course.published,
            'tags': [{'tag_id': tag.id, 'tag_name': tag.name} for tag in course.tags.all()],
            'deleted': course.deleted,
            'sales': course.sales,
            'snapshot_id': snapshot.id,
            'content': snapshot.content,
            'cover': snapshot.cover,
            'price': '.'.join([str(snapshot.price_integer), str(snapshot.price_decimal)]),
            'create_time': snapshot.create_time.strftime('%Y-%m-%d %H:%M:%S')
        })

    return process_response(request, ResponseStatus.OK)
import re

from typing import Union

from apps.utils.response_status import ResponseStatus


def validate_username(username: str) -> Union[ResponseStatus, None]:
    """
    1. 长度大于等于 4
    2. 长度小于等于 30
    3. 仅含有字母、数字、下划线

    :param username: 用户名
    :return: 返回状态枚举
    """
    if len(username) < 4:
        return ResponseStatus.USERNAME_TOO_SHORT_ERROR
    if len(username) > 30:
        return ResponseStatus.USERNAME_TOO_LONG_ERROR
    if re.search(r'[^A-Za-z0-9_]', username):
        return ResponseStatus.USERNAME_FORMAT_ERROR

    return None


def validate_password(password: str) -> Union[ResponseStatus, None]:
    """
        1. 长度大于等于 6
        2. 长度小于等于 20
        3. 仅含合法字符 ASCII 33 ~ 126
        4. 需含有数字
        5. 需含有字母

        :param password: 密码
        :return: 返回状态枚举
        """
    if len(password) < 6:
        return ResponseStatus.PASSWORD_TOO_SHORT_ERROR
    if len(password) > 20:
        return ResponseStatus.PASSWORD_TOO_LONG_ERROR
    if not all(32 < ord(c) < 128 for c in password):
        return ResponseStatus.PASSWORD_FORMAT_ERROR
    if not re.search(r'[0-9]', password):
        return ResponseStatus.PASSWORD_LACK_NUMBER_ERROR
    if not re.search(r'[A-Za-z]', password):
        return ResponseStatus.PASSWORD_LACK_LETTER_ERROR

    return None


def validate_email(email: str) -> Union[ResponseStatus, None]:
    """
    1. 邮箱格式错误

    :param email: 邮箱
    :return: 返回状态码
    """
    if not re.search(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
        return ResponseStatus.EMAIL_FORMAT_ERROR

    return None

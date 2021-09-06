from enum import Enum


class ResponseStatus(Enum):
    """
    响应状态的枚举类

    状态类型格式形如:
    Status_Name = (code: int, message: str)
    """
    # Debug
    DEBUG = (10000, 'Debug')

    # 成功
    OK = (20000, '成功')

    # 禁止访问
    FORBIDDEN = (50403, 'Forbidden')

    # 意外错误
    UNEXPECTED_ERROR = (50000, '意外错误')

    # 正常错误
    REQUEST_METHOD_ERROR = (40000, '请求方法错误')
    JSON_DECODE_ERROR = (40001, 'JSON 解析错误')
    MISSING_PARAMETER_ERROR = (40002, '缺少参数')
    BAD_PARAMETER_ERROR = (40003, '参数错误')

    UNSUPPORTED_IMAGE_FORMAT = (41001, '不支持当前图片格式')

    USERNAME_TOO_SHORT_ERROR = (42001, '用户名应不少于 4 位')
    USERNAME_TOO_LONG_ERROR = (42002, '用户名应不多于 20 位')
    USERNAME_FORMAT_ERROR = (42003, '用户名仅能含有字母、数字和下划线')
    PASSWORD_TOO_SHORT_ERROR = (42004, '密码应不少于 6 位')
    PASSWORD_TOO_LONG_ERROR = (42005, '密码应不多于 20 位')
    PASSWORD_FORMAT_ERROR = (42006, '密码应仅包含合法字符')
    PASSWORD_LACK_NUMBER_ERROR = (42007, '密码必须包含数字')
    PASSWORD_LACK_LETTER_ERROR = (42008, '密码必须包含字母')
    EMAIL_FORMAT_ERROR = (42009, '邮箱格式错误')
    USERNAME_EXISTED_ERROR = (42010, '用户名已存在')
    EMAIL_EXISTED_ERROR = (42011, '邮箱已存在')
    USERNAME_NOT_EXISTED_ERROR = (42012, '用户名不存在')
    PASSWORD_NOT_MATCH_ERROR = (42013, '密码错误')
    VERIFICATION_CODE_NOT_MATCH_ERROR = (42014, '验证码不匹配')

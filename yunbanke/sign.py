from datetime import datetime
from hashlib import sha1, md5
import hmac
from typing import Tuple

GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT+00:00'
KEY = '526EBA802E6FCF44661DE4393A82ABDA'


def get_time():
    return datetime.utcnow().strftime(GMT_FORMAT)


def hash_string(url, time_str, form=None, user_id: str = None, login_form=True):
    """
    获取签名串
    :param url
    :param time_str 请用get_time获取
    :param form 数据表单
    :param user_id
    :param login_form 是否是登录表单
    """
    if user_id is not None:
        user_id = user_id.upper()
        result = "|".join((url, user_id, time_str))
    else:
        result = "|".join((url, time_str))
    if form is None:
        return result

    form_str = ""
    for i, a in form.items():
        form_str += f"{i}={a}"
        form_str += "|"
    form_str = form_str[:-1]
    if login_form:
        result += "|"
        result += form_str
    else:
        result += "|"
        result += form_sign(form_str).upper()
    return result


def form_sign(form_str):
    form_str = bytes(form_str, "utf-8")
    hl = md5()
    hl.update(form_str)
    return hl.hexdigest()


def make_digest(message, key=KEY):
    key = bytes(key, 'UTF-8')
    message = bytes(message, 'UTF-8')
    digester = hmac.new(key, message, sha1)
    return digester.hexdigest()


def sign_request(url, form=None, user_id=None, access_secret=None, login_form=False) -> Tuple[str, str]:
    time = get_time()
    if user_id is not None:
        string = hash_string(url, time, form, user_id, login_form=login_form)
        return time, make_digest(string, access_secret)
    string = hash_string(url, time, form, login_form=login_form)
    return time, make_digest(string)

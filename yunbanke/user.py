from yunbanke import sign
from requests import Session
from typing import Tuple
from yunbanke.apis import *
import requests

BASE_HEADERS = headers = {
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 8.1.0; ONE A2001 Build/OPM7.181205.001)', 'X-scheme': 'https',
    'X-app-id': 'MTANDROID', 'X-app-version': '5.1.1', 'X-dpr': '2.7', 'X-app-machine': 'ONE A2001',
    'X-app-system-version': '8.1.0', 'Host': 'api.mosoteach.cn',

}


class User:
    def __init__(self, ):
        self._session = Session()
        self._session.headers = BASE_HEADERS
        self._access_secret = ""
        self._user_id = ""
        self._access_id = ""
        self._last_sec_update_ts_s = ""

    def login_user(self, user: str, pwd: str) -> Tuple[dict, bool, str]:
        """
        登录用户
        :param user 用户名
        :param pwd 密码
        :return 第一个参数为是否成功，第二个参数为信息，第三个参数为返回的信息
        """

        login_data = {'account_name': user, 'app_id': 'MTANDROID', 'app_version_name': '5.1.1',
                      'app_version_number': '111',
                      'device_type': 'ANDROID', 'dpr': '2.7',
                      'system_version': '8.1.0', 'user_pwd': pwd}

        time, signature = sign.sign_request(URL_LOGIN, login_data, login_form=True)
        self._session.headers["Date"] = time
        self._session.headers["X-mssvc-signature"] = signature
        rep = self._session.post(URL_LOGIN, data=login_data).json()
        if rep["result_code"] == 0:
            user_data = rep["user"]
            self._access_secret = user_data["access_secret"]
            self._user_id = user_data["user_id"]
            self._access_id = user_data["access_id"]
            self._last_sec_update_ts_s = user_data["last_sec_update_ts_s"]
            return user_data, True, rep["result_msg"]
        return rep, False, rep["result_msg"]

    def list_course(self) -> Tuple[dict, bool, str]:
        """
        班课列表
        """
        time, signature = sign.sign_request(URL_CC_LIST_JOINED, user_id=self._user_id,
                                            access_secret=self._access_secret)
        self._session.headers["Date"] = time
        self._session.headers["X-mssvc-access-id"] = self._access_id
        self._session.headers["X-mssvc-signature"] = signature
        self._session.headers["X-mssvc-sec-ts"] = self._last_sec_update_ts_s
        rep = self._session.post(URL_CC_LIST_JOINED).json()
        if rep["result_code"] == 0:
            return rep["rows"], True, rep["result_msg"]
        return rep, False, rep["result_msg"]

    def list_checkin(self, id, page=1, role_id=2) -> Tuple[dict, bool, str]:
        """
        签到任务列表
        :param id 班课id
        """
        form = {"clazz_course_id": id, "page": page, "role_id": role_id}

        time, signature = sign.sign_request(URL_CHECKIN_INDEX, form, user_id=self._user_id,
                                            access_secret=self._access_secret, login_form=False)
        self._session.headers["Date"] = time
        self._session.headers["X-mssvc-access-id"] = self._access_id
        self._session.headers["X-mssvc-signature"] = signature
        self._session.headers["X-mssvc-sec-ts"] = self._last_sec_update_ts_s
        rep = self._session.post(URL_CHECKIN_INDEX, data=form).json()
        if rep["result_code"] == 0:
            return rep["data"], True, rep["result_msg"]
        return rep, False, rep["result_msg"]

    def checkin(self, checkin_id, report_pos_flag="Y", lat="", lng="") -> Tuple[bool, str]:
        """
        签到
        后三个参数可能与签到位置有关
        :param checkin_id
        :param report_pos_flag
        :param lat
        :param lng
        """
        form = {"checkin_id": checkin_id, "report_pos_flag": report_pos_flag, "lat": lat, "lng": lng}
        time, signature = sign.sign_request(URL_CHECKIN, None, user_id=self._user_id,
                                            access_secret=self._access_secret, login_form=False)
        self._session.headers["Date"] = time
        self._session.headers["X-mssvc-access-id"] = self._access_id
        self._session.headers["X-mssvc-signature"] = signature
        self._session.headers["X-mssvc-sec-ts"] = self._last_sec_update_ts_s
        # 设置host
        self._session.headers["Host"] = "checkin.mosoteach.cn:19528"
        rep = self._session.post(URL_CHECKIN, data=form).json()
        if rep["result_code"] == 0:
            # 还原host
            self._session.headers["Host"] = "api.mosoteach.cn"
            return True, rep["result_msg"]
        self._session.headers["Host"] = "api.mosoteach.cn"
        return False, rep["result_msg"]

    def is_check_open(self, id) -> Tuple[bool, dict, str]:
        """
        当前是否开启签到
        :param id
        """
        form = {"clazz_course_id": id}
        time, signature = sign.sign_request(URL_CHECKIN_OPEN, form, user_id=self._user_id,
                                            access_secret=self._access_secret, login_form=False)
        self._session.headers["Date"] = time
        self._session.headers["X-mssvc-access-id"] = self._access_id
        self._session.headers["X-mssvc-signature"] = signature
        self._session.headers["X-mssvc-sec-ts"] = self._last_sec_update_ts_s
        rep = self._session.post(URL_CHECKIN_OPEN, data=form).json()
        if rep["result_code"] == 0:
            return True, rep, rep["result_msg"]
        return False, rep, rep["result_msg"]

    def list_interaction(self, id, dpr=2.7, role_id=2) -> Tuple[dict, bool, str]:
        """
        获取任务列表
        :param id
        """
        form = {"clazz_course_id": id, "dpr": dpr, "role_id": role_id}
        time, signature = sign.sign_request(URL_INTERACTION_LIST, form, user_id=self._user_id,
                                            access_secret=self._access_secret, login_form=False)
        self._session.headers["Date"] = time
        self._session.headers["X-mssvc-access-id"] = self._access_id
        self._session.headers["X-mssvc-signature"] = signature
        self._session.headers["X-mssvc-sec-ts"] = self._last_sec_update_ts_s
        rep = self._session.post(URL_INTERACTION_LIST, data=form).json()
        if rep["result_code"] == 0:
            return rep["data"], True, rep["result_msg"]
        return rep, False, rep["result_msg"]

    def list_member(self, id, dpr=2.7) -> Tuple[dict, bool, str]:
        """
        获取班级成员列表
        :param id
        """
        form = {"clazz_course_id": id, "dpr": dpr}
        time, signature = sign.sign_request(URL_MEMBER_LIST, form, user_id=self._user_id,
                                            access_secret=self._access_secret, login_form=False)
        self._session.headers["Date"] = time
        self._session.headers["X-mssvc-access-id"] = self._access_id
        self._session.headers["X-mssvc-signature"] = signature
        self._session.headers["X-mssvc-sec-ts"] = self._last_sec_update_ts_s
        rep = self._session.post(URL_MEMBER_LIST, data=form).json()
        if rep["result_code"] == 0:
            return rep["data"], True, rep["result_msg"]
        return rep, False, rep["result_msg"]

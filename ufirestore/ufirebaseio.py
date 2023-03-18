

access_token = 'ya29.c.b0Aaekm1LE9QUFBay18QmxOq4s0B1sj_CLI5X51UTEGFuuQaGwH_XnGXhKVgqXkBr53QW8dex9jvKudSmOmtwWgVKIPDiB8AN5qYXXt-eN7gt_OfWkC93jz2yEg9O55CFgPTSX6e_hJs-egI6V4uWgCIMmk-vB1sYCGOrw494ku60IiL5eFoyC7Qdxt56ukP2o3kHchYoOJIzDuVU-56NerOJ66doC47heunRisXcO5kKZwfy7NAyQ04g8vCTCERjpxwITIXTOfqhz0DNED7zmltm-xPJKuOtvHUPTDnbFjTqKIzq0HanwMXgxTH8MoEzK9oopNUsK--gAL341CWX5I6QfB4sYb_-xRbm13FktdwVgltMo444cjomt8pyo8rWicgJIdbJ3a6qanO89ebgXmRmhQfBkf9pyFV_Yu16YRZfe6k1v-wxtIqM625csFhogzBcXYrSJfYg2wef4tYh0RpB4q8mvd5oZhbkFXrQcXJXeuYU4k93xS8q52Rv3YhnUisp_at6Zf4dfM2dRUVXYZuY0B6av4kz_qxMYQn8Fw6bt-JX_lQSs1tw8nBYW2jyxX3o-OezZYgz_4pWRb97gtx4hVp-9dcFszWe1p_WyM9h1QYyRj7qFvpQW30OQORewiX5YBOkp419XOYarvi6u6gWygSa4i7bx6sFFuduwRcznRsyhX7l2ZstaFVM0bI16oVmtvBqJ7Bl2ri2VUcYRIxdoQpa7-vV53u15oQ5uWo9_pepxzywvr1FxUZphnxf6-u1tgp-Ug752rn6cSr5ck0s1Sb9Ouj_uxYc_UM7R4SWYlz_VqclX4JrykhzObwzcZqc2251g2FYoqIXxs2zp3czsMizRr7hweumYr6ojqQpdM-peB_iIn2tIg5rBX58_xRztod3vyUvs4Qjuq4B29VoBxFOM76OQ-8iu4WOf4Qm1wbQBu1lvn-oeymWeUXcSZq_jrBMSdtc0M39vR-QYtUX9pJaeJQ2rfdFzaSr1jxsq7MdyrlU50Qa'
project_id = 'rn5notifications-default-rtdb'


class FirestoreException(Exception):
    def __init__(self, message, code=400):
        super().__init__()
        self.message = message
        self.code = code

    def __str__(self):
        return f"{self.code}: {self.message}"


class FirebaseGlobal:
    GLOBAL_URL_HOST = f"https://{project_id}.firebaseio.com/"
    PROJECT_ID = project_id
    ACCESS_TOKEN = access_token


def construct_url(resource_path):
    return "%s/%s" % (FirebaseGlobal.GLOBAL_URL_HOST, resource_path)


def send_request(path, method="get", data=None, dump=True):
    headers = {}

    if FirebaseGlobal.ACCESS_TOKEN:
        headers["Authorization"] = "Bearer " + FirebaseGlobal.ACCESS_TOKEN

    response = urequests.request(method, path, headers=headers, json=data)

    if dump == True:
        if response.status_code < 200 or response.status_code > 299:
            print(response.text)
            raise FirestoreException(response.reason, response.status_code)

        json = response.json()
        if json.get("error"):
            error = json["error"]
            code = error["code"]
            message = error["message"]
            raise FirestoreException(message, code)
        return json


def set_project_id(proj_id):
    FirebaseGlobal.GLOBAL_URL_HOST = f"https://{proj_id}.firebaseio.com/"
    FirebaseGlobal.PROJECT_ID = proj_id


def set_access_token(token):
    FirebaseGlobal.ACCESS_TOKEN = token

import urequests
import config
import utime
import mynetwork


class FirebaseException(Exception):
    def __init__(self, message=None, code=200, reason=None):
        super().__init__()
        self.message = message
        self.code = code
        self.reason = reason

    def __str__(self):
        return f"{self.code} {self.reason}: {self.message}"


class FirebaseGlobal:
    GLOBAL_URL_HOST = f"https://{config.project_id}.firebaseio.com"
    GLOBAL_URL_SIGNIN = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    GLOBAL_URL_TOKEN = "https://securetoken.googleapis.com/v1/token"
    ID_TOKEN = ""
    REFRESH_TOKEN = ""
    EXPIRES = 0


def construct_url(resource_path):
    return "%s/%s" % (FirebaseGlobal.GLOBAL_URL_HOST, resource_path)


def add_params(path, params):
    first = True
    for param in params:
        if len(param) > 0:
            if first:
                path += "?"
            else:
                path += "&"
            path += f"{param[0]}={param[1]}"
        first = False
    return path


def login():
    params = [["key", config.api_key]]
    data = {"email": config.email, "password": config.password, "returnSecureToken": True}
    headers = {}
    path = add_params(FirebaseGlobal.GLOBAL_URL_SIGNIN, params)
    response = send_request(path, "POST", headers, data, dump=True, debug=True)
    FirebaseGlobal.ID_TOKEN = response['idToken']
    FirebaseGlobal.REFRESH_TOKEN = response['refreshToken']
    FirebaseGlobal.EXPIRES = utime.time() + int(response['expiresIn'])
    #mynetwork.complete_job()


def ping():
    path = construct_url("hotbox/ping.json")
    value = send_request(path, headers={}, debug=True)


def get(endpoint, cb, debug=False):
    path = construct_url(endpoint)
    params = [["auth", FirebaseGlobal.ID_TOKEN], ["timeout", "300ms"]]
    path = add_params(path, params)
    headers = {}
    value = send_request(path, headers=headers, debug=debug)
    cb(value)


def send_request(path, method="GET", headers=None, data=None, dump=True, debug=False):
    if debug:
        print(path)

    response = urequests.request(method, path, headers=headers, json=data)

    if debug:
        print(response.content)

    if dump:
        try:
            firebase_exception = FirebaseException()
            if response.status_code < 200 or response.status_code > 299:
                firebase_exception = FirebaseException(reason=response.reason.decode(),
                                                       code=response.status_code)

            json = response.json()
            if "error" in json:
                error = json["error"]
                firebase_exception.message = error
            if firebase_exception.code != 200:
                raise firebase_exception
            return json
        except FirebaseException as e:
            print("HTTP Error:", str(e))
            return {}


def set_project_id(proj_id):
    FirebaseGlobal.GLOBAL_URL_HOST = f"https://{proj_id}.firebaseio.com/"
    FirebaseGlobal.PROJECT_ID = proj_id


class Request:
    """
    Request object to store parameters, headers, etc.
    """

    def __init__(self, body=None, params=None, headers=None, request=None, raw=None):
        self.body = body if body is not None else None
        self.params = params if params is not None else {}
        self.queries = {}
        self.headers = headers if headers is not None else {}
        self.request = request if request is not None else {}
        self.cookies = {}
        self.session = {}
        self.files = {}
        self.raw = raw if raw is not None else None

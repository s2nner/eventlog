from urllib.parse import urlparse

from csv_reader import RowObject


class Request:
    id = None
    group_requests = {}

    def __init__(self, data: RowObject):
        self.id = data.id_request

    def finish(self, data: RowObject) -> None:
        pass

    def process(self, data: RowObject) -> None:
        """processing log data"""
        if data.event_type == 'BackendConnect':
            backend_name = urlparse(data.args).netloc
            backends = self.group_requests.get(data.gr, {})
            backend_obj = backends.get(data.gr, Backend(backend_name))
            backends[backend_name] = backend_obj
            self.group_requests[data.gr] = backends

        if data.event_type in ('BackendRequest', 'BackendError'):
            backend_obj = list(self.group_requests.get(data.gr).values())[-1]
            backend_obj(data)


class Backend:
    name = None
    requests = 0

    def __init__(self, name: str):
        self.name = name
        self.errors = []

    def __call__(self, data: RowObject) -> None:
        self.update(data)

    def update(self, data: RowObject) -> None:
        if data.event_type == 'BackendError':
            self.errors.append(data.args)
        elif data.event_type == 'BackendRequest':
            self.requests += 1

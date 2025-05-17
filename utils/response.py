import flask
import typing


class Response:
    def __init__(
        self,
        status_code: int,
        msg: str,
        data: typing.Optional[typing.Any] = None
    ):
        self.status_code = status_code
        self.msg = msg
        self.data = data

    def to_dict(self) -> dict:
        response = {"status_code": self.status_code, "msg": self.msg}
        if self.data is not None:
            response["data"] = self.data
        return response

    def to_json(self):
        return flask.jsonify(self.to_dict())

    def send(self):
        return self.to_json(), self.status_code

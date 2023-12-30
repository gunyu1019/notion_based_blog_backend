from typing import Any


class NotionException:
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        request_id: str,
        developer_survey: str = None,
    ):
        self.status_code = status_code
        self.code = code

        self.message = message
        self.developer_survey = developer_survey
        self.request_id = request_id
        super().__init__(self.__str__())

    @classmethod
    def from_payload(cls, data: dict[str, Any]):
        return cls(
            status_code=int(data["status"]),
            code=data["code"],
            message=data["message"],
            developer_survey=data.get("developer_survey", None),
            request_id=data["request_id"],
        )

    def __str__(self) -> str:
        return "{code}: {message}".format(code=self.code, message=self.message)

    def __eq__(self, other):
        return (
            isinstance(other, NotionException)
            and self.code == other.code
            and self.request_id == other.request_id
        )

    def __ne__(self, other):
        return not self.__eq__(other)

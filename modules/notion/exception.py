from models.notion import error


class BadRequest(error.NotionException, Exception):
    status_code: int = 400


class Unauthorized(error.NotionException, Exception):
    status_code: int = 401


class Forbidden(error.NotionException, Exception):
    status_code: int = 403


class NotFound(error.NotionException, Exception):
    status_code: int = 404


class Conflict(error.NotionException, Exception):
    status_code: int = 409


class RateLimited(error.NotionException, Exception):
    status_code: int = 429


class InternalServerError(Exception):
    status_code: int = 500


class BadGateway(Exception):
    status_code: int = 502


class ServiceUnavailable(Exception):
    status_code: int = 503


class GatewayTimeout(Exception):
    status_code: int = 504


CLIENT_ERROR_RESPONSE = (
    BadRequest | Unauthorized | Forbidden | NotFound | Conflict | RateLimited
)
SERVER_ERROR_RESPONSE = (
    InternalServerError | BadGateway | ServiceUnavailable | GatewayTimeout
)

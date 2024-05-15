from pydantic import BaseModel
from fastapi import status


class UnauthorizedErrorResponse(BaseModel):
    detail: str


class ForbiddenErrorResponse(BaseModel):
    detail: str


class NotFoundErrorResponse(BaseModel):
    detail: str


class InternalServerErrorResponse(BaseModel):
    detail: str


response_dic = {
    status.HTTP_401_UNAUTHORIZED: {
        "model": UnauthorizedErrorResponse,
        "description": "Access token is missing or invalid.",
    },
    status.HTTP_403_FORBIDDEN: {
        "model": ForbiddenErrorResponse,
        "description": "You do not have permission to perform this action.",
    },
    status.HTTP_404_NOT_FOUND: {
        "model": NotFoundErrorResponse,
        "description": "The requested resource was not found.",
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": InternalServerErrorResponse,
        "description": "Internal server error.",
    },
}

unauthorized_error_response = {
    "model": UnauthorizedErrorResponse,
    "description": "Access token is missing or invalid.",
}

forbidden_error_response = {
    "model": ForbiddenErrorResponse,
    "description": "You do not have permission to perform this action.",
}

not_found_error_response = {
    "model": NotFoundErrorResponse,
    "description": "The requested resource was not found.",
}

internal_server_error_response = {
    "model": InternalServerErrorResponse,
    "description": "Internal server error.",
}

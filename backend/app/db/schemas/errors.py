from pydantic import BaseModel, Field

class BadRequestError(BaseModel):
    detail: str = Field(..., description="Details of the bad request.")

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Invalid Request."
            }
        }

class UnauthorizedError(BaseModel):
    detail: str = Field(..., description="Details of the unauthorized request.")

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Invalid authentication credentials."
            }
        }

class NotFoundError(BaseModel):
    detail: str = Field(..., description="Details of the resource not found.")

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Book with ID 123 not found."
            }
        }

class ValidationError(BaseModel):
    detail: list = Field(..., description="Details of validation errors.")

    class Config:
        json_schema_extra = {
            "example": {
                "detail": [
                    {
                        "loc": ["body", "title"],
                        "msg": "field required",
                        "type": "value_error.missing"
                    }
                ]
            }
        }

class InternalServerError(BaseModel):
    detail: str = Field(..., description="Details of the unexpected server error.")

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "An unexpected server error occurred."
            }
        }

from fastapi.openapi.utils import get_openapi

def custom_openapi(app):
    """
    Generate a custom OpenAPI schema for the FastAPI application.
    :param app: The FastAPI application instance.
    :return: The OpenAPI schema.
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Books API",
        version="1.0.0",
        description="APIs for managing books with JWT authentication.",
        routes=app.routes,
        contact={
            "name": "Support Team",
            "email": "support@example.com",
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
    )

    # Additional OpenAPI customizations
    openapi_schema["info"]["x-logo"] = {
        "url": "https://example.com/logo.png"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

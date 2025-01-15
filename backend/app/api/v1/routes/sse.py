from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.core.sse import generate_stream, add_event
from app.core.security import verify_access_token
from app.db.schemas.errors import (
    BadRequestError,
    UnauthorizedError,
    InternalServerError,
)
router = APIRouter(dependencies=[Depends(verify_access_token)])

@router.get(
    "/",
    response_class=StreamingResponse,
    responses={
        200: {"description": "Stream started successfully. Sends real-time updates."},
        401: {"description": "Unauthorized (Invalid or expired token).", "model": UnauthorizedError},
        500: {"description": "Internal Server Error (Issue with the stream).", "model": InternalServerError},
    },
)
def stream_updates():
    """
    SSE endpoint for streaming real-time updates.
    Sends events whenever there is an update in the system.
    """
    try:
        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream"
        )
    except Exception as e:
        add_event("error", "Stream failed to initialize", {"error": str(e)})
        raise HTTPException(
            status_code=500,
            detail="An internal server error occurred while initializing the stream."
        )

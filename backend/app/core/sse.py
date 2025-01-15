from queue import Queue, Empty
import json

# Event queue with a maximum size to prevent unbounded growth
event_queue = Queue(maxsize=100)

def add_event(event_type: str, message: str, data: dict = None):
    """
    Add an event to the queue with type and optional data.
    :param event_type: The type of event (e.g., 'book-created', 'error').
    :param message: A message describing the event.
    :param data: Additional data for the event (optional).
    """
    try:
        event = {
            "type": event_type,
            "message": message,
            "data": data or {}
        }
        event_queue.put(event, timeout=2)  # Timeout ensures no indefinite blocking
    except Exception as e:
        print(f"Failed to add event to queue: {str(e)}")

def generate_stream():
    """
    Generator function for streaming events from the queue.
    Yields events in SSE format.
    """
    try:
        while True:
            try:
                # Wait for an event with a timeout
                event = event_queue.get(timeout=10)
                yield f"event: {event['type']}\ndata: {json.dumps(event)}\n\n"
            except Empty:
                # Send a keep-alive message to prevent client timeouts
                yield ": keep-alive\n\n"
    except GeneratorExit:
        # Handle client disconnection gracefully
        print("Client disconnected from SSE stream.")
    except Exception as e:
        # Log unexpected errors
        print(f"Error in SSE stream: {str(e)}")

def success(message, data=None):
    """Standard success response"""
    response = {"status": "success", "message": message}
    if data is not None:
        response["data"] = data
    return response, 200

def error(message, code=400):
    """Standard error response"""
    return {"status": "error", "message": message}, code

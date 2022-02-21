from flask import jsonify, make_response


def __format_error_json(messages):
    if isinstance(messages, dict) and "json" in messages:
        return {
            "error": True,
            "messages": {key: item[0] for key, item in messages["json"].items()},
        }
    return messages


def handle_error_422(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return jsonify(__format_error_json(messages)), err.code, headers
    else:
        return jsonify(__format_error_json(messages)), err.code

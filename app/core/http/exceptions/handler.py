from flask import jsonify


def __format_error_json(messages):
    if isinstance(messages, dict) and "json" in messages:
        return {
            "error": True,
            "messages": {key: item[0] for key, item in messages["json"].items()}
            if isinstance(messages["json"], dict)
            else {"body": messages["json"]},
        }
    return messages


def handle_error_422_400(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return jsonify(__format_error_json(messages)), err.code, headers
    else:
        return jsonify(__format_error_json(messages)), err.code


def handle_api_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

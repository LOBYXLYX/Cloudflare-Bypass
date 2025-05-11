import loguru
from flask import Flask, jsonify, request
import sys
from aqua import CF_Solver

app = Flask(__name__)

loguru.logger.remove()
log_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> - <level>{message}</level>"
loguru.logger.add(sys.stderr, format=log_format, level="TRACE", colorize=True)
loguru.logger = loguru.logger.opt(colors=True)

### ToDo :: Move to a separate file
def validate_payload(payload):
    if "url" not in payload:
        return {
            "error": "no url provided"
        }
    if "proxy" not in payload:
        payload["proxy"] = None
    if "headers" not in payload:
        payload["headers"] = {}
    if "insecure_skip_verify" not in payload:
        payload["insecure_skip_verify"] = False
    if "cookie_only" not in payload:
        payload["cookie_only"] = False

    try:
        payload["homepage"] = "/".join(payload["url"].split('/')[:3])
    except Exception as e:
        return {
            "error": f"invalid URL: {str(e)}"
        }
    return payload


@app.route('/process', methods=['POST'])
def process():
    payload = validate_payload(request.json)
    if "error" in payload:
        loguru.logger.error(payload["error"])
        return jsonify(payload)

    try:
        cf = CF_Solver(
            domain=payload['homepage'],
            proxy=payload['proxy'],
            insecure_skip_verify=False if payload['insecure_skip_verify'] is None else payload["insecure_skip_verify"],
            headers={} if payload['headers'] is None else payload["headers"],
        )
        cookie = cf.cookie()

        solver_response = {
            "cookie": cookie,
            "status": 200,
        }

        # Skip the get if its only for the cookies
        if payload["cookie_only"] is not True:
            response = cf.client.get(payload["url"])
            solver_response["html"] = response.text
            solver_response["status"] = response.status_code
    except Exception as e:
        loguru.logger.error(e)
        return jsonify({
            "error": str(e)
        })
    return jsonify(solver_response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1180, debug=True)

import azure.functions as func
import logging
import json
import math

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="CalculateArea", methods=["POST"])
def CalculateArea(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('CalculateArea function triggered.')

    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON body"}),
            status_code=400,
            headers=headers,
            mimetype="application/json"
        )

    shape = req_body.get('shape')
    area = None

    try:
        if shape == 'circle':
            radius = float(req_body.get('radius'))
            area = math.pi * radius ** 2

        elif shape == 'rectangle':
            width = float(req_body.get('width'))
            height = float(req_body.get('height'))
            area = width * height

        elif shape == 'triangle':
            base = float(req_body.get('base'))
            height = float(req_body.get('height'))
            area = 0.5 * base * height

        else:
            return func.HttpResponse(
                json.dumps({"error": f"Unknown shape: {shape}"}),
                status_code=400,
                headers=headers,
                mimetype="application/json"
            )

    except (TypeError, ValueError):
        return func.HttpResponse(
            json.dumps({"error": "Invalid or missing numeric dimensions"}),
            status_code=400,
            headers=headers,
            mimetype="application/json"
        )

    return func.HttpResponse(
        json.dumps({"shape": shape, "area": round(area, 2)}),
        status_code=200,
        headers=headers,
        mimetype="application/json"
    )

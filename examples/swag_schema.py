from flask import Flask
from flasgger import Swagger, Schema, fields
from marshmallow.validate import Length, OneOf

app = Flask(__name__)
Swagger(app)

swag = {"swag": True,
        "tags": ["demo"],
        "responses": {200: {"description": "Success request"},
                      400: {"description": "Validation error"}}}


class Body(Schema):
    color = fields.List(fields.String(), required=True, validate=Length(max=5), example=["white", "blue", "red"])


class Query(Schema):
    color = fields.String(required=True, validate=OneOf(["white", "blue", "red"]))
    swag_in = "query"


@app.route("/color/<id>/<name>", methods=["POST"], **swag)
def index(body: Body, query: Query, id: int, name: str):
    return {"body": body, "query": query, "id": id, "name": name}


def test_swag(client, specs_data):
    """
    This test is runs automatically in Travis CI

    :param client: Flask app test client
    :param specs_data: {'url': {swag_specs}} for every spec in app
    """
    payload = {"color": ["white", "blue", "red"]}

    test_case = [
        {"url": '/color/100/putin?color=white', "status_code": 200},
        {"url": '/color/100/putin?color=black', "status_code": 400}
    ]
    for case in test_case:
        response = client.post(case["url"], json=payload)
        assert response.status_code == case["status_code"]


if __name__ == "__main__":
    app.run(debug=True)

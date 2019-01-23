from flask import Flask, Response, request
import os
import json
import logging

import pika

from entity_json import entities_to_json
import xmltodict

app = Flask(__name__)

logger = logging.getLogger('service')
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

config = json.loads(os.environ["CONFIG"])

queue = config["queue"]
decode_json_body = config.get("decode_json_value", False)
decode_xml_body = config.get("decode_xml_body", False)
timeout = config.get("inactivity_timeout_seconds", 1)

username = config.get("username", "guest")
password =config.get("password", "guest")

hostname = config.get("hostname", "localhost")
port = config.get("port", 5672)

virtual_host = config.get("virtual_host", "/")

credentials = pika.PlainCredentials(username, password)
parameters = pika.ConnectionParameters(hostname,
                                       port,
                                       virtual_host,
                                       credentials)

@app.route('/', methods=["GET"])
def get():
    limit = request.args.get("limit")

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    def generate():
        yield "["
        index = 0
        for method_frame, properties, body in channel.consume(queue, inactivity_timeout=timeout):
            if method_frame is None:
                break
            if index > 0:
                yield ","
            body_result = body
            if decode_json_body:
                body_result = json.loads(body.decode('utf-8'))
            elif decode_xml_body:
                body_result = xmltodict.parse(body.decode('utf-8'))
            result = {
                # dummy to prevent full sync deletion tracking
                "_updated": 0,
                "properties": properties.__dict__,
                "body": body_result,
            }
            yield entities_to_json(result)
            # TODO unsafe ack
            channel.basic_ack(method_frame.delivery_tag)
            index = index + 1
            if limit and index >= int(limit):
                break
        yield "]"
        channel.close()
        connection.close()
    return Response(generate(), mimetype='application/json', )

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

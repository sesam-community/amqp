# Read AMQP 0.9 messages as a json source

[![Build Status](https://travis-ci.org/sesam-community/amqp.svg?branch=master)](https://travis-ci.org/sesam-community/amqp)

Example system config:
```
{
  "_id": "rabbitmq-trafikkdata",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "CONFIG": {
        "queue": "myqueue",
        "decode_xml_body": true,
        "inactivity_timeout_seconds": 5,
        "hostname": "localhost",
        "port": 5672,
        "username": "guest",
        "password": "guest
      }
    },
    "image": "sesamcommunity/amqp",
    "port": 5000
  }
}

```

Example source pipe:
```
{
  "source": {
    "type": "json",
    "system": "rabbitmq-trafikkdata",
    "is_chronological": true,
    "supports_since": true,
    "url": "/"
  }
}

```

Example output from Cloudamqp:
```
$ curl localhost:5000/?limit=1 | jq .
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  4450    0  4450    0     0   101k      0 --:--:-- --:--:-- --:--:--  101k
[
  {
    "_updated": 0,
    "properties": {
      "content_type": "application/xml",
      "content_encoding": null,
      "headers": null,
      "delivery_mode": 2,
      "priority": null,
      "correlation_id": null,
      "reply_to": null,
      "expiration": null,
      "message_id": null,
      "timestamp": null,
      "type": null,
      "user_id": null,
      "app_id": null,
      "cluster_id": null
    },
    "body": {
      "d2LogicalModel": {
        "@xmlns": "http://datex2.eu/schema/2/2_0",
        "@modelBaseVersion": "2"
        [..]
      }
    }
  }
]
```

## Limitations

* One microservice pr queue
* Acknowledges message before guaranteed delivery (!)

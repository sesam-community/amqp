# Read AMQP messages as a json source

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
    "image": "sesamcommunity/kafka",
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

## Limitations

* One microservice pr queue
* Acknowledges message before guaranteed delivery (!)
# Kong Plugin - Schema to Markdown

Simple tool to get a Kong Schema and create Markdown output to be use at README.md files.


## Usage

Start Kong, then execute:

```bash
docker run --rm leandrocarneiro/kong-plugin-schema-to-markdown:python <pluginName> <kongSchemaEndpoint>
```

Example:

- Kong running and opening the admin port 8001 for my docker network 172.17.0.0/24

```bash
docker run --rm leandrocarneiro/kong-plugin-schema-to-markdown:python zipkin http://172.17.0.1:8001/schemas/plugins/
```

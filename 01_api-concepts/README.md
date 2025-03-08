# API concepts
> misc API related concepts

## Communication patterns

+ **Request-Response** &mdash; 1:1, like a browser calling a web server.

+ **Publish-Subscribe** &mdash; a publisher emits a message and subscribers act on it according to some data in the message.

+ **Queues** &mdash; a publisher emits a message but only one out of a pool of subscribers grabs the message and acts on it.

## API fundamental concepts

> A **resource** is data you can distinguish and perform operations on.

> An **endpoint** is a distinct URL and HTTP *verb* (sometimes called action) a web service provides for each feature it wants to expose.<br>An endpoint is sometimes called a route, because it routes the URL to a *function* that performs some logic.

The API of a service can be written in a standard format for documenting REST APIs called [OpenAPI document](https://swagger.io/specification/v3#openapi-document) or API spec document.

The API spec (OpenAPI document) describes a REST API with the different paths, and within each path all the different capabilities that are available.

That document also includes an `schema` section that is used to describe the shape of the data exchanged over those endpoints.

## REST APIs Design Principles

REST is an architectural style for loosely coupled and highly scalable applications that communicate over a network.

| NOTE: |
| :---- |
| REST stands for **RE**presentational **S**tate **T**ransfer. That is, REST refers to the ability to transfer the representation of a resource's state. |

REST APIs are structured around resources. Resources are entities that can be manipulated through the API and that are referenced by a unique URL.

There are two types of resources:
+ singletons: represent a single entity. For example, `/orders/{order_id}` represents the URL path of a *singleton resource*.
+ collections: represent lists of entities. For example, `/orders` represents the URL path of a *collection resource*.

Resources can be nested within another resource. For example, an order may contain a list of several items:

```json
{
  "id": "624f25f2-3d35-4cfc-b710-b64b2ed2942d",
  "status": "delivered",
  "created": "2023-12-20",
  "order": [
    {
      "product": "capuccino",
      "size": "small",
      "quantity": 1
    },
    {
      "product": "machiato",
      "size": "small",
      "quantity": 2
    }
  ]
}
```

Nested endpoints can be created to represent nested resources. For example, to retrieve the status of a particular order we could expose a `GET /orders/{order_id}/status` to retrieve the `status` value associated to a given `order_id`.

| NOTE: |
| :---- |
| Nested options is a popular optimization technique when resources are represented by large payloads, as the requestor won't have to process that large payload and can receive the specific field it is interested in. |

The resource oriented nature of REST APIs is limiting when you need to model actions, such as cancelling an order. A common *pragmatic* approach is to represent those actions as nested resources, as in `POST /orders/{order_id}/cancel` to cancel an order.

### Architectural constraints of REST applications

The following list describes the characteristics a REST API server must satisfy to process and respond to a client request:

+ **Client-Server architecture**: The UI must be decoupled from the backend.

+ **Statelessness**: The server must not manage states between requests. In other words, every request to the server must contain all the information necessary to process it.

+ **Cacheability**: Requests that always returns the same response must be cacheable.

+ **Layered**: The API may be architected in layers, but such complexity must be hidden from the user. This includes not only how you build each of the services powering the REST API, but also extends to the set microservices that might constitute the backend. You will typically use an API gateway which provides a single entry point to all those different microservices no matter their technology stack and how they are built.

+ **Code on demand**: The server should be able to inject code into the UI on demand.

+ **Uniform interface**: The API must provide a consistent interface for accessing and manipulating resources.

The following picture illustrates the *layered* capability described above, in which the API gateway hides away the complexities of the backend as the client sees a uniform interface exposed on the gateway and it is completely unaware of the different services running on the backend.

This is known as the API Gateway pattern:

![API Gateway pattern](pics/api-gateway.png)

### Hypermedia as the engine of application state (HATEOAS)

HATEOAS is a paradigm in the design of REST APIs that emphasizes the concept of discoverability.

HATEOAS makes APIs easier to use by enriching responses with all the information users need to interact with a given resource.

For example, if a client request the details of an order, the response includes the links to cancel and pay for such order:

```json
{
  "id": 8,
  "status": "progress",
  "created": "2023-12-20",
  "order": [
    {
      "product": "capuccino",
      "size": "medium",
      "quantity": 1
    }
  ],
  "links": [
    {
      "href": "/orders/8/cancel",
      "description": "Cancels the order",
      "type": "POST"
    },
    {
      "href": "/orders/8/pay",
      "description": "Pays an order",
      "type": "POST"
    },
  ]
}
```

In practice, not many APIs are built this way because:

+ The information in the links should be readily available in the API documentation.
+ It's not clear what should be returned. For example, I might not have permissions to cancel an order, should I include the link to cancel the order in the links section?
+ Certain actions might not be available depending on the state on the system, which is continuously changing. Generating the links is a large overhead, and might not be relevant when the user tries to use those links if the system has changed.
+ It makes the payloads bulkier.

### The Richardson maturity model for a REST API

The maturity of an API can be evaluated using this model:

1. **Level 1: RPC over HTTP**

        The API supports remote procedure calls (that is, the invocation of some application business logic) over HTTP.

2. **Level 2: Availability of resources**

        Endpoints are structured around resources, as opposed to having a generic endpoint definition that triggers the corresponding business logic based on the information the endpoint receives.

3. **Level 3: Using HTTP methods and status codes**

        The API makes use of the HTTP verbs in a consistent and standard way (`GET` to retrieve, `POST` to create, etc.) and returns propert HTTP status codes (200 for OK, 201 for created,etc.)

4. **Level 4: API Discoverability**

        The API leverages the concept of discoverability, as described by the principles of [HATEOAS](#hypermedia-as-the-engine-of-application-state-hateoas)

### Structured resource URLs with HTTP methods

As described in the [Richardson maturity model](#the-richardson-maturity-model-for-a-rest-api), a mature API design makes a consistent use of HTTP methods (and status codes).

HTTP methods are special keywords used in HTTP requests to indicate the type of action we wish to perform.

The standard semantics are:

| HTTP method | Description |
| :---------- | :---------- |
| `GET` | Return information about the requested resource. |
| `POST` | Create a new resource. |
| `PUT` | Performs a full update by replacing a resource. |
| `PATCH` | Updates specific properties of a resource. |
| `DELETES` | Deletes a resource. |

#### `PUT` vs. `PATCH`

Both `PUT` and `PATCH` are used to perform updates, with the only difference being the `PUT` requires the API client to send a whole new representation of the resource, while `PATCH` allows the client only the properties that should be updated.

For example, the payload for a `PUT` request for an order looks like:

```json
{
  "id": "624f25f2-3d35-4cfc-b710-b64b2ed2942d",
  "status": "delivered",
  "created": "2024-09-08",
  "order": [
    {
      "product": "margherita",
      "size": "medium",
      "quantity": 1
    },
    {
      "product": "capuccino",
      "size": "large",
      "quantity": 1
    }
  ]
}
```

By contrast, a `PATCH` request used to update the size of the pizza could be:

```json
{
  "op": "replace",
  "path": "/order/0/size",
  "value": "large"
}
```

This approach follows the [JSON Patch](https://jsonpatch.com/). Simpler resources could be updated by sending in the payload only the fields that should be changed:

```bash
{
  "day": "2024-09-08",
  "remarks": "I finally wasn't feeling dizzy"
}
```

| NOTE: |
| :---- |
| While implementing `PATCH` endpoints is a good practice for public-facing APIs, most APIs tend to implement only `PUT` endpoints for updates because they're easier to handle. |

### Using HTTP status codes systematically

HTTP status codes are used to signal the result of processing an API request in the server.

When used properly, HTTP status code help us deliver expressive responses to our APIs' consumers.

HTTP status codes are organized into groups:

| Group | Description |
| :---- | :---------- |
| 1xx | An operation is in progress. |
| 2xx | A request was successfully processed. |
| 3xx | A resource has been moved to a new location. |
| 4xx | Something was wrong with the request. |
| 5xx | An error occurred processing a valid request. |

Let's assume that we have the following endpoints in an order processing API:

+ `/orders`
  + GET &mdash; retrieve a list of orders
  + POST &mdash; places an order
+ `/orders/{order_id}`
  + GET &mdash; returns an order
  + PUT &mdash; updates an order
  + DELETE &mdash; deletes an order
+ `/orders/{order_id}/cancel`
  + POST &mdash; cancels an order
+ `/orders/{order_id}/pay`
  + POST &mdash; pays for an order

We can map each of those endpoints to the corresponding HTTP status code signifying success in the operation:

| Endpoint | Success HTTP status code | Description |
| :------- | :----------------------- | :---------- |
| `POST /orders` | 201 (Created) | A resource (order) has been created. |
| `GET /orders` | 200 (OK) | A request (retrieve collection of orders) was successfully processed. |
| `GET /orders/{order_id}` | 200 (OK) | A request (retrieve order with id=`order_id`) was successfully processed. |
| `PUT /orders/{order_id}` | 200 (OK) | A resource (order with id=`order_id`) was successfully replaced. |
| `DELETE /orders/{order_id}` | 204 (No Content) | A resource (order with id=`order_id`) was successfully processed (order deleted), but no content was delivered in the response. |
| `POST /orders/{order_id}/cancel` | 200 (OK) | The request (cancellation of order with id=`order_id`) was successfully processed. |
| `POST /orders/{order_id}/pay` | 200 (OK) | The request (payment of order with id=`order_id`) was successfully processed. |

#### HTTP status codes to report client errors in the request

The following table details the HTTP status codes that should be used to inform the API client that the problem is on their end:

| Situation | Example | Status Code |
| :-------- | :------ | :---------- |
| Sending a malformed payload with invalid syntax | An invalid JSON document is sent | 400 (Bad Request) |
| Sending a malformed payload that is syntactically correct but misses a required parameter, or contains an invalid parameter, or assigns the wrong value or type to a parameter | An order request misses the `"product"` key | 422 (Unprocessable Entity) |
| Sending a request to a resource that doesn't exist | Sending a request to `/orders/1234` when `1234` is not an existing order | 404 (Not Found) |
| Sending a request using an HTTP method that is not supported | Using `PATCH /orders/{order_id}` when that operation is unavailable | 501 (Not Implemented), if you plan to implement support in the future<br>405 (Method Not Allowed), otherwise |
| Making a request without having authenticated first | Sending a request without the proper authentication information | 401 (Unauthorized) |
| Making a request to an endpoint I'm not authorized to access | Sending a request to `/orders/{order_id}/cancel` when only admins can cancel orders | 403 (Forbidden) |

#### HTTP status codes to report errors in the server

The following table details the HTTP status codes that should be used to inform the API client that the problem is on the server end. We use these codes to inform the client that the request was OK.

| Situation | Example | Status Code |
| :-------- | :------ | :---------- |
| An application error has prevented the request from completing. | A bug in the code that causes the request processing to crash. | 500 (Internal Server Error) |
| Server is unavailable to take on more requests | Server is overloaded, or down for maintenance | 503 (Service Unavailable) |
| Server is taking longer than expected to respond | Server is slow, for some reason | 504 (Gateway timeout) |

### Designing API payloads

Payloads represent the data exchanged between a client and the server through an HTTP request.

The usability of an API is very much dependent on good payload design, as poorly designed payloads make APIs difficult to use and result in bad user experience (UX).

An HTTP message body or payload is a message that contains the data exchanged in an HTTP request. Both HTTP requests and responses can contain a message body. The message body is encoded in one of the media types supported by HTTP, typically JSON.

The HTTP specification allows you to include payloads in all HTTP methods, but discourages their use in `GET` and `DELETE` requests. As it is not forbidden, you might find popular APIs (e.g., Elasticsearch) that sends information in the body of a `GET` request.

This specification also states that responses in the 1xx group, and responses returning 204 (No Content), and 304 (Not Modified) must not include a payload. All other payloads must include a response payload.

#### Error response payloads

Error payloads should include an `"error"` key detailing why the client is getting an error.

For example, for a 404 (Not Found) situation, we should return a payload such as:

```json
{
  "error": "Resource not found"
}
```

| NOTE: |
| :---- |
| You can also use similar keywords, such as `"detail"` or `"message"`. |

#### Response payloads for POST requests

It's a good practice to return a full representation of the resource that has been created in the response to a `POST` request. This representation will typically include additional information that was not sent on the request payload, such as the ID assigned to the resource created, the status, the creation timestamp, etc.

#### Response payloads for `PUT` and `PATCH` requests

It's a good practice to return a full representation of the resource being updated by a `PUT`/`PATCH` request, so that the client can validate the result of the update.

#### Response payloads for `GET` requests

There are two scenarios associated with `GET` requests:
+ when we are requested to return a collection of resources (e.g., `GET /orders`).
+ when we are requested to return a specific singleton (e.g., `GET /orders/{order_id}`)

The reponse to `GET /orders` must return a list of orders. You can either include a full representation of each order, or include only a partial representation.

The first strategy gives the API client all the information in one request, but may compromise the performance of the API when the list of items is big, as it will result in a large response payload:

```json
{
  "orders": [
    {
      "id": "624f25f2-3d35-4cfc-b710-b64b2ed2942d",
      "status": "delivered",
      "created": "2023-12-20",
      "order": [
        {
          "product": "capuccino",
          "size": "small",
          "quantity": 1
        },
        {
          "product": "machiato",
          "size": "small",
          "quantity": 2
        }
      ]
    },
    {
      // ... order 2 ...
    },
    {
      // ... order 3 ...
    }
  ]
}
```

When using the second strategy, the response only includes a partial representation of each order:

```json
{
  "orders": [
    {
      "id": "624f25f2-3d35-4cfc-b710-b64b2ed2942d",
    },
    {
      "id": "07a8cff9-5832-4166-8766-6c4d7079caf6",
    },
    {
      "id": "4d27ba66-8529-4291-96c7-17232714f76e"
    }
  ]
}
```

It is common practice when using this strategy to send only the list of `order_id`'s.

When using this strategy, the API client will have to submit a subsequent request to obtain the full information about the order, that is, a request to `GET /orders/{order_id}` for each `id` received.

The choice between returning the full or partial representation depends on the actual scenario to implement.

For singleton endpoints (e.g., `GET /orders/{order_id}`), a full representation of the resource must be returned.

### Designing URL query parameters

URL query parameters are key-value pairs that you encode in the URL to send additional information.

Query parameters come after a question mark `?`. You can combine multiple query parameters by separating them with ampersands `&`.

It's a best practice for endpoints returning a collection of resources to allow users to filter and paginate the results.

For example, when using the `GET /orders` endpoint, you may want to limit the results to only the five most recent orders, or to only the cancelled orders.

These sort of scenarios can be accomplished with URL query parameters.

For example, in our `GET /orders` endpoint you can define:
+ `cancelled` &mdash; if not specified, all results will be returned. If specified and true, only cancelled orders will be retrieved. If specified and false, only not cancelled orders will be retrieved.
+ `limit` &mdash; specifies the max number of orders to be retrieved.

URL query paramters should always be optional, and when appropriate, the server may assign default values for them (e.g., when paginating a large number of results, the server can decide to return only the first page even if the user has not send values for the pagination parameters).


#### A few words about pagination

When returning a large number of results, it is common practice to use a `page` and `per_page` combination of parameters:
+ `page`: represents the set of data to be retrieved.
+ `per_page`: identifies the number of items we want to be included in each response.

For example, to obtain the first ten items of a large result set, you would send the following request:

```
GET /orders?page=1&per_page=10
```

## Using OpenAPI to document REST APIs

OpenAPI is by far the most popular standard for describing RESTful APIs, with a rich ecosystem of tools for testing, validating, and visualizing APIs.

OpenAPI uses JSON Schema to describe the API's structure and models.

### Using JSON Schema to model data

OpenAPI uses an extended subset of the JSON Schema specification for defining the API's structure and models.

JSON Schema is a specification standard for defining the structure of a JSON document and the types and formats of its properties.

Creating a JSON schema for interfaces that use JSON has two main purposes:
+ Document for the interfaces that use JSON to represent data.
+ Validate that the data being exchanged is correct.

The following table describes a few JSON schema basic data types:

| JSON Schema type | Description |
| :--------------- | :---------- |
| `string`  | character values |
| `number`  | integer and decimal values |
| `object`  | associative arrays (i.e., Python dicts) |
| `array`   | collection of other data types (i.e., Python lists) |
| `boolean` | for `true` and `false` values |
| `null`    | for uninitialized data |

As an example, the following snippet defines the JSON Schema document for an `order` object that features the properties `product`, `quantity`, and `size`:

```json
{
    "order": {
        "type": "object",
        "properties": {
            "product": {
                "type": "string",
            },
            "quantity": {
                "type": "number"
            },
            "size": {
                "type": "string"
            }
        }
    }
}
```

And the following is a JSON document that complies with such specification:

```json
{
    "order": {
        "product": "margherita",
        "quantity": 1,
        "size", "big"
    }
}
```

The following snippet represents the JSON Schema document for an array of objects having `product`, `quantity`, and `size` properties:

```json
{
    "order": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "product": {
                    "type": "string"
                },
                "quantity": {
                    "type": "number",
                },
                "size": {
                    "type": "string"
                }
            }
        }
    }
}
```

An object can have any number of nested objects. However, when too many objects are nested, indentation makes the specification difficult to read. To mitigate this problem, JSON Schema allows you to define each object separately, and then use *JSON pointers* to reference them.

The following snippet illustrates the use of JSON pointers to simplify the specification found above:

```json
{
    "OrderItemSchema": {
        "type": "object",
        "properties": {
            "product": {
                "type": "string"
            },
            "quantity": {
                "type": "number"
            },
            "size": {
                "type": "string"
            }
        }
    },
    "Order": {
        "order": {
            "type": "array",
            "items": {
                "$ref": "#/OrderItemSchema"
            }
        }
    }
}
```

Note that the pointer uses JSONPath to identify the location of the referenced definition, with the root of the document represented by `#` and using `/` for navigation.

For example, the JSONPath expression that refers to the `size` property of our document above will be: `#/OrderItemSchema/properties/size`.

In addition to the type of the property, JSON Schema also allows you to specify the format of the property. For example, we could add a `created` property to identify when the order was created. Its JSON Schema snippet would be:

```json
{
    "created": {
        "type": "string",
        "format": "date"
    }
}
```

| NOTE: |
| :---- |
| While the native language for JSON Schame is JSON, it's more practical for humans to use YAML, as it is less verbose and lets you use comments. |

### Anatomy of an OpenAPI specification

OpenAPI is a standard specification format for documenting RESTful APIs, that relies on JSON Schema for the request and response payload specification.

An OpenAPI spec contains **everything** the consumer of the API needs to be able to interact with the API.

The document itself features five sections:

![OpenAPI spec sections](pics/openapi-sections.png)

| Section | Description |
| :------ | :---------- |
| `openapi` | Indicates the version of OpenAPI the document conforms to. |
| `info` | Contains general information such as the title and version of the API. |
| `servers` | Contains a list of URLs where the API is available.<br>It is common to include the URLs for *production*, *staging*, *development*, etc. |
| `paths` | Describes the endpoints exposed by the API, including information about the expected payloads, allowed path parameters, and the format of the responses.<br>This section represent the API interface, and it's the section that consumers will inspect to understand how to integrate with the API. |
| `components` | Defines reusable elements that are referenced in other parts of the specification, such as schemas, parameters, security schemes, request bodies, and responses.<br>A schema is a definition of the expected attributes and types in your request and response objects. OpenAPI schemas are defined using JSON Schema syntax. |

### The `paths` section: documenting the API endpoints

The `paths` section of the OpenAPI schema spec document lists the URL paths exposed by the API, with the HTTP methods they implement, the types of requests they expect, and the responses they return, including the status codes.

When writing this section, it is recommended to start with a textual representation of your endpoints and their responsibilities.

The following table describes the endpoints of an ordering system:

| Endpoint | Responsibility |
| :------- | :------------- |
| `GET /orders` | Retrieve a list of orders. |
| `POST /orders` | Place an order. Requires a full representation of the order. |
| `GET /orders/{order_id}` | Return an order. |
| `PUT /orders/{order_id}` | Replace an order. Requires a full representation of the order. |
| `DELETE /orders/{order_id}` | Delete an order. |
| `POST /orders/{order_id}/cancel` | Cancel an order. |
| `POST /orders/{order_id}/pay` | Pay an order. |

Then, you can start creating the *skeleton* definition of the `paths` section using YAML. It is recommended to include an `operationId` property for each of the endpoints so that we can reference the operation in other sections of the document.

```yaml
paths:
  /orders:
    get:
      operationId: getOrders
    post:
      operationId: createOrder

  /orders/{order_id}:
    get:
      operationId: getOrder
    put:
      operationId: replaceOrder
    delete:
      operationId: deleteOrder

  /orders/{order_id}/cancel:
    post: cancelOrder

  /orders/{order_id}/pay:
    post: payOrder
```

With the *skeleton* in place, you can start detailing the parameters the endpoint accepts, the request payloads, query parameters, responses and their status codes, etc.

#### Documenting URL query parameters

It is common for endpoints returning a collection of resources to use URL query parameters to tailor the results it returns.

Let's assume that we want the `GET /orders` endpoint described above to be able to filter orders using URL query parameters:

+ `cancelled`: specifies whether we want to filter the cancelled orders, so that only cancelled orders will be returned. This parameter will accept boolean values.

+ `limit`: specifies the max number of orders to be returned to the client. The value will be a number.

Therefore, we want to support requests such as `GET /orders?cancelled=true&limit=5` to return the list of the five most recent orders that have been cancelled.

```yaml
paths:
  /orders:
    get:
      operationId: getOrders
      parameters:
        - name: cancelled   # Parameter name
          in: query         # URL query parameter
          required: false   # Optional
          schema:
            type: boolean   # Boolean
        - name: limit
          in: query:
          required: false
          schema:
            type: integer
```

#### Documenting URL path parameters

Path parameters are common in the endpoint specification. Those are described in a `parameters` section that hangs directly from the path specification as seen below:


```yaml
paths:
  /orders/{order_id}:
    parameters:
      - name: order_id    # Parameter name
        in: path          # URL path parameter
        required: true    # Mandatory
        schema:
          type: string
          format: uuid
    get:
      operationId: getOrder
    ...
```


#### Documenting request payloads

When dealing with the specification of request payloads, you should start with an instance of the payload you want to model.

For example, for our Order service could be:

```json
"order": [
  {
    "product": "margherita",
    "size": "medium",
    "quantity": 1
  }
]
```

We can then write a short textual representation describing each field:

| Payload property | Description |
| :--------------- | :---------- |
| `product` | The type of product the user is ordering. |
| `size` | The size of the product the user is ordering. It has to be one of: `small`, `medium`, `big`. |
| `quantity` | The number of instances of the product the user is ordering. It can be any integer number equal to or greater than 1. |

With all the required information in place, we can define the schem for this payload. This will be defined under the `content` property of the method's `requestBody` property.

```yaml
paths:
  /orders:
    get:
      operationId: getOrders
      parameters:
        # ...URL query params spec...
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                order:
                  type: array
                  items:
                    type: object
                    properties:
                      product:
                        type: string
                      size:
                        type: string
                        enum:
                          - small
                          - medium
                          - big
                      quantity:
                        type: integer
                        required: false
                        default: 1
                    required:
                      - product
                      - size
```

### The `components` section: refactoring schema definitions to avoid repetition

While the previous snippet is valid, you can see that embedding payload schemas in the endpoint definition makes it very difficult to read.

It is considered a good practice to refactor such schemas to keep the API spec clean and readable.

The following snippet illustrates how to do so by leveraging the `components` section of the OpenAPI spec:

```yaml
paths:
  /orders:
    post:
      operationId: createOrder
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateOrderSchema" # JSON pointer
components:
  schemas:
    CreateOrderSchema:
      type: object
      properties:
        order:
          type: array
          items:
            type: object
            properties:
              product:
                type: string
              size:
                type: string
                enum:
                  - small
                  - medium
                  - big
              quantity:
                type: integer
                required: false
                default: 1
            required:
              - product
              - size
```

This refactoring let us keep the `paths` section clean and focused on the higher-level details of the endpoint.

Refactoring using JSON pointers can be taken a bit further. Our `CreateOrderSchema`contains an array of nested objects. It will be easier to understand and maintain if we keep them separate.

```yaml
components:
  schemas:
    OrderItemSchema:
      type: object
      properties:
        product:
          type: string
        size:
          type: string
          enum:
            - small
            - medium
            - big
        quantity:
          type: integer
          required: false
          default: 1
      required:
        - product
        - size

    CreateOrderSchema:
      type: object
      properties:
        order:
          type: array
          items:
            $ref: "#/components/schemas/OrderItemSchema"
```

Now it has become easier to define the rest of the endpoints by referring to schemas already defined.

For example, the following snippet illustrates the specification of the `PUT /orders/{order_id}`:

```yaml
paths:
  /orders/{order_id}:
    parameters:
      - in: path
        name: order_id
        required: true
        schema:
          type: string
          format: uuid
    put:
      operationId: replaceOrder
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schema/CreateOrderSchema"
```

### Documenting API responses

When documenting the responses in an OpenAPI spec document, it is recommended to start from a sample response payload:

```json
{
  "id": "624f25f2-3d35-4cfc-b710-b64b2ed2942d",
  "status": "delivered",
  "created": "2024-09-10",
  "order": [
    {
      "product": "margherita",
      "size": "medium",
      "quantity": 1,
    },
    {
      "product": "gelato",
      "size": "small",
      "quantity": 2
    }
  ]
}
```

Then, you have to create the corresponding schema definition within the `#/components/schema` section:

```yaml
components:
  schema:
    GetOrderSchema:
      type: object
      properties:
        id:
          type: string
          format: uuid
        status:
          type: string
          enum:
            - created
            - paid
            - progress
            - cancelled
            - dispatched
            - delivered
        created:
          type: string
          format: date-time
        order:
          type: array
          items:
            $ref: "#/components/schemas/OrderItemSchema"
```

Note how we've used JSON pointers to reuse the definition of the items that are part of the `"order"` array.

An alternative way of reusing schemas is to use a strategy called *model composition*, which allows you to combine the properties of different schemas into a single object definition.

This is achieved using the keyword `allOf` to indicate that the object requires all the properties in the listed schemas.

You can see the *model composition* technique in the following snippet:

```yaml
components:
  schema:
    GetOrderSchema:
      allOf:
        - $ref: "#/components/schemas/CreateOrderSchema"
        - type: object
          properties:
            id:
              type: string
              format: uuid
            status:
              type: string
              enum:
                - created
                - paid
                - progress
                - cancelled
                - dispatched
                - delivered
            created
              type: string
              format: date-time
```

Because `CreateOrderSchema` already included the array information we need, we are only required to specify the added properties for the `GetOrderSchema`.

| NOTE: |
| :---- |
| Model composition results in a cleaner and more succinct specification, but it requires the models to be created to be strictly compatible. If we look at the example above, if the definition of `CreateOrderSchema` was to be updated in the future, we would need to revert back to the previous approach, which will be additional work. |

#### Preventing unknown fields in your payload

In general, it is considered a good practice to force a validation error when a payload includes fields that haven't been defined in your schemas.

This can be stated by including the property `additionalProperties` of your schemas set to `false`:

```yaml
OrderItemSchema:
  type: object
  properties:
    product:
      type: string
    size:
      type: string
      enum:
        - small
        - medium
        - large
  required:
    - product
    - size
    - quantity
  additionalProperties: false
```

#### Referencing your schemas in the `paths` section

With the schema in place, we can then complete the `paths` specification, which will include the response's status code, content type, and schema:

```yaml
paths:
  /orders/{order_id}:
    parameters:
      - in: path
        name: order_id
        required: true
        schema:
          type: string
          format: uuid
    get:
      summary: Return the details of a specific order
      operationId: getOrder
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/GetOrderSchema"
```

### Creating generic responses

APIs will feature also more generic responses, for example, when signaling an error to the API consumer.

Such responses can also be modeled so that they are reused in different sections of the specification. You just need to define them in the `#/components/responses` subsection.

For example, the following snippet illustrates how to model the *404 (Not Found)* using an `Error` schema:

```yaml
components:
  responses:
    NotFound:
      description: The specified resource was not found
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"

  schemas:
    Error:
      type: object
      properties:
        detail:
          type: string
      required:
        - detail
```

With the response information in place, you can start referring to it in the corresponding `paths` spec:

```yaml
paths:
  /orders/{order_id}:
    parameters:
      - in: path
        name: order_id
        required: true
        schema:
          type: string
          format: uuid
    get:
      summary: Return the details of a specific order
      operationId: getOrder
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/GetOrderSchema"
        "404":
          $ref: "#/components/responses/NotFound"
```

### Defining the authentication scheme of the API

While we haven't discussed API security aspects yet, you are surely aware of the importance of how your APIs are protected.

The API spec must describe how users need to authenticate and authorize their requests.

The security related definitions go within the `#/components/securitySchemes` section.

The following snippet illustrates how to configure three security schemes: one for OpenID Connect (OIDC), one for OAuth2, and another for bearer authorization.

OIDC might be primarily used to authenticate *human* users through a frontend application, while for API integrations, OAuth2 is typically used. The bearer authorization is commonly used for point-to-point integration with our APIs (such as the ones a user operating a SPA will use):

```yaml
components:
  securitySchemes:
    openId:
      type: openIdConnect
      openIdConnectUrl: https://<my-site>.com/known/open-id-configuration
    oauth2:
      type: oauth2
      flows:
        clientCredentials:
          tokenUrl: https://<my-site>.com/oauth2/token
          scopes: {}
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - oauth2:
    - getOrders
    - createOrder
    - getOrder
    - updateOrder
    - deleteOrder
    - payOrder
    - cancelOrder
  - bearerAuth:
    - getOrders
    - createOrder
    - getOrder
    - updateOrder
    - deleteOrder
    - payOrder
    - cancelOrder
```

### Summary: manually writing OpenAPI spec to document your REST APIs

Even when using a framework that doesn't require you to write an OpenAPI spec document (or that can even generate such document from your code, as FastAPI does), it's often recommended to manually write it, as it will give you and your API consumers some vital insights using standard documentation.

When doing so, it is recommended to follow these steps:

1. Get your APIs designed, as discussed in [REST APIs Design Principles](#rest-apis-design-principles) section.

1. Create a YAML file with the five required OpenAPI spec sections:
  - `openapi`: version of OpenAPI the document adheres to.
  - `info`: general information about the API.
  - `servers`: list of URLs where the API is available.
  - `paths`: endpoints exposed by the API.
  - `components`: reusable elements referenced in other sections.

1. Populate the `openapi`, `info`, and `servers` sections.

1. Create a table describing your endpoints, and use it as an input for populating the `paths` section. Include an `operationId` and `summary` for each endpoint.

1. Document your query parameters (if needed).

1. Document your path parameters.

1. Describe your input payloads in the `components` section. Start by writing example input payloads and some textual information describing the shape of each element of the payload and use it as a guidance for writing the corresponding schemas in the aforementioned section. Reference the created schemas in the corresponding `path` section under the `requestBody` key.

1. Describe your response payloads in the `components` section. Start by writing example output payloads. Reference those schemas in your corresponding endpoints documented in the `paths` section under the `responses` key. Each response should be prefixed by the corresponding HTTP status code.

1. Create schemas for your generic response payloads (e.g., error messages) and complete the `paths` spec describing your non-success situations.

1. Define the authentication scheme of the API in the `#/components/securitySchemes` section.
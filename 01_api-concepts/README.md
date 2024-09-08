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

When used propertly, HTTP status code help us deliver expressive responses to our APIs' consumers.

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

URL query paramters should always be optional, and when appropriate, the server may assign default values for them (e.g., when paginating a large number of results, the server can decide to return only the first page even if the user has not send values for the pagination parameters).


#### A few words about pagination

When returning a large number of results, it is common practice to use a `page` and `per_page` combination of parameters:
+ `page`: represents the set of data to be retrieved.
+ `per_page`: identifies the number of items we want to be included in each response.

For example, to obtain the first ten items of a large result set, you would send the following request:

```
GET /orders?page=1&per_page=10
```

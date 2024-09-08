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

## High-Level application architecture

A high-level application architecture enforces the boundaries and allows you to apply the principle of separation of concerns between the application layers.

In a web application, you'll typically find:
+ The API layer

    An adapter on top of the application logic that exposes the service's capabilities to its consumers.

+ The Business/Application logic layer

    Implements the service's capabilities. It controls the interactions between the API layer and the Data layer.

    This is the part that knows what to do to effectively carry out an action such as registering a new dizzines episode, or adding a new tv show you've recently watched. The API layer only exposes such capabilities, but doesn't know what the action really means.

+ The Data layer

    Implements the data models required for interfacing with our sources of data and the persistence storage systems.

![HL architecture](pics/hl-app-arch.png)

## Implementing the API spec with FastAPI

With the first version of the API spec in place, and the high-level architecture view, we can start implementing the API endpoints in an iterative fashion.

We should start with a minimalist approach that returns *canned* responses, and then start enhancing it adding additional capabilities such as data validation, dynamic responses, etc.

[FastAPI](https://github.com/tiangolo/fastapi) is a web application framework built on top of [Starlette](https://github.com/encode/starlette) &mdash; a high-performance, lightweight, async server gateway interface (ASGI).

In addition, FastAPI relies on [pydantic](https://github.com/samuelcolvin/pydantic/) for data validation.

![FastAPI - Starlette architecture](pics/fastapi-starlette.png)

| NOTE: |
| :---- |
| As opposed to the Web Server Gateway Interface (WSGI), which is a Python standard specification to connect application code to servers in an sync fashion, ASGI does that asynchronously to foster concurrency. |
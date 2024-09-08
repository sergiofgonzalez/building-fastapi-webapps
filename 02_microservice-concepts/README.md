# Microservice concepts
> microservices related concepts

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


## Microservices design principles

There are three fundamental microservices design principles:
+ Database-per-service principle
+ Loose coupling principle
+ Single Responsibility principle

Following these three principles will ensure you build a sound microservices solution instead of a distributed monolith.

### Database-per-service Principle

Each microservice must own a specific set of data, and no other service should have access to such data except through an API.

This principle does not necessarily mean that each microservice should be connected to a different database, only that the data in control of the microservice must not be accessed by another microservice.

The following diagram illustrates this principle in the context of an app that allows a registered user to place an order.

![DB per service](pics/db-per-service.png)

### Loose coupling principle

Microservices should be designed with a clear separation of concerns.

Two implications can be derived from this principle:
+ Each service must be able to work independently from others. If you have a service that can't fulfill a single request without calling another service, they belong together.

+ Each service must be able to be updated without impacting other services. If changes to a service require updates to other services, there is a tight-coupling between and they need to be redesigned.

### Single Responsibility Principle (SRP)

A microservice should be designed around a single business capability or subdomain.

## Service Decomposition Techniques

When dealing with a microservices architecture design, there are two main techniques you can follow to identify what microservices you should be working on:

1. [Decomposition by business capability](#service-decomposition-by-business-capability)
2. Decomposition by subdomain

### Service decomposition by business capability

Decomposition by business capability generally results in an architecture that maps every business team to a microservice.

In this strategy, we look into the activities a business organization performs and how the organization is structured to undertake them, to then creates microservices that mirror that organizational structure.

For example, if an organization has three departments: *Customers*, *Claims*, and *Kitchen*, the service decomposition would be as follows:

![Service Decomposition by business capability](pics/service-decomposition-by-business-capability.png)

However, most of the scenarios require a little bit more of analysis fieldwork to understand the underlying responsibilities of each department and how they interact together.

#### Analyzing the business structure of an organization

Let's consider a fictitious company called *Mama Jane's Pizza*.

*Mama Jane's Pizza* is a Pizza delivery and carryout restaurant chain that allows you to order Pizza wherever you are and get it delivered to your door, or picked up in the restaurant closer to you.

The organization of the company is as follows:

+ **Products department** &mdash; Customers can order different types of Pizzas and related products out of a catalog managed by the Products department.

+ **Inventory department** &mdash; Availability of products and ingredients at the time of order are managed by the Inventory department.

+ **Finance department** &mdash; This department ensures that the company is profitable and looks after the financial infrastructure required to process customer payments.

+ **Kitchen department** &mdash; Once a user places an order, the Kitchen team is in charge of picking up its details and process it until it is ready to be delivered or picked up.

+ **Delivery department** &mdash; when the order is ready for delivery, a team of riders is in charge of picking it up and take it to the end customer.

#### Associating microservices to business capabilities

With the organization analysis in place, we start doing a 1:1 mapping of each of the relevant business teams to a microservice, identifying also the service's responsibilities.

| SPOILER ALERT: |
| :---- |
| This mapping will not be the final one. |

| Microservice | Aligned Team | Responsibilities |
| :----------- | :----------- | :--------------- |
| Products | Products Team | Owns the product catalog data.<br>The Products team will use this service to maintain the catalog: add new products, update existing ones, etc. |
| Ingredients | Inventory Team | Owns the data about the ingredients stock.<br>The ingredients team is in charge of keeping the ingredients DB in sync with the warehouse stock. |
| Sales | Sales Team | Guides customers through the journey of placing orders and keeps track of them.<br>This service owns the customer data (e.g., orders, registrations, etc.) and the lifecycle of each order.
| Finance | Finance Team | Implements the payment processing activities.<br>Owns the data about user payment details and payment history.<br>The Finance team uses this service to keep the company accounts up to date and to ensure payments work correctly. |
| Kitchen | Kitchen Team | Sends orders to the restaurants' kitchens and keeps track of their progress. It also monitors the performance of the different kitchen systems. |
| Delivery | Delivery Team | Arranges the delivery of the order to the customer once it has been produced by the kitchen. It provides additional services, such as the translation of the user location to coordinates to choose the closest restaurant, and chooses the best route for the rider. It owns the data about each delivery made. |

Right after that, we must evaluate whether each of the microservices satisfy the three principles mentioned at the beginning of the document:

1. Database per service Principle
    + Each microservice must own a specific set of data.
    + No other service should have access to the data owned by the microservice except through an API.

2. Loose coupling Principle
    + Each service must be able to work independently from the others. If a service can't fulfill a single request without calling another service, they belong together.

    + Each service must be able to be updated without impacting other services. Otherwise, there's tight coupling and the services need to be redesigned.

3. Single Responsibility Principle

    + Each service should be designed around a single business capabilitiy or subdomain.

All of the services seem to comply with the *database-per-service principle* as all of them owned a defined set of data with no intersection between them.

However, the *Products* and *Ingredients* services are so tightly coupled. For example, the Products service won't be able to do anything by itself without contacting first the Ingredients service, as it needs to check if the ingredients of the selected product are available, and send a signal to update the stock as soon as the cooking process begins.

As a result, it'll be recommended to have a single Products service that both the Products and Ingredients team own.

### Service decomposition by subdomains

A stronger technique, and one that can be applied to scenarios not aligned to organizations is the *Decomposition by Subdomains* strategy.

This strategy draws inspiration from the field of domain-driven design (DDD) &mdash; an approach to software development that focuses on modeling the processes and flows of the business with software using the same language business users employ.

When applied to a microservice architecture, DDD helps us define the core responsibilities of each service and its boundaries.

#### What is domain-driven design (DDD)?

DDD is an approach to sw development that focuses on modeling the processes and flows of the business users. DDD offers an approach to software development that tries to reflect as accurately as possible the ideas and the language that businesses, or end-users of the software, use to refer to their processes and flows.

To do so, DDD encourages the creation of a rigorous, model-based language that software developers can share with the users. This language is called *ubiquitious language*.

First you need to identify the core domain of a business:

+ *Mama Jane's Pizza* &mdash; delivery of high-quality pizza to customers as quickly as possible regardless of their location.

+ Logistics company &mdash; shipment of products.

Once the core domain is identified, you continue with the discovery of subdomains and generic subdomains:

A subdomain will be an area of the business that is not directly related to value generation, but it is fundamental to support it. For *Mama Jane's* it might be the riders management; for a logistics company, it might customer support for the users shipping their products.

The core domain gives you a definition of the problem space: it will describe what you try to solve with software.

The solution consists of a model (set of abstractions that describe the domain and solves the problem).

In practice, most problems require the collaboration of different models, with their own *ubiquitious languages*. The process of defining such models is called *strategic design*.

#### Applying strategic design to *Mama Jane's Pizza*

To break down a system into subdomains, it helps to think about the operations the system has to perform to accomplish its goal.

In the case under study, we want to model the process of taking an order and delivering it to the customer.

This can be broken down into the following steps:

1. When the customer lands on the website, we show them the product catalog. Each product is marked as available or unavailable. The customer can filter the list by availability and sort it by price (ascending and descending).

1. The customer selects one or more products.

1. The customer pays for their order.

1. Once the customer has paid, we pass on the details of the order to the kitchen.

1. The kitchen picks up the order and produces it.

1. The customer monitors progress on their order.

1. Once the order is ready, we arrange its delivery with a rider.

1. The customer tracks the delivery itinerary until it is deliverd to their door.


Those steps can be pictured in a user journey:

![Mama Jane's user journey](pics/user_journey_mama_janes.png)

The user journey is a useful artifact for discovering the business subdomains:

![Subdomain identification](pics/subdomain_identification_mama_janes.png)

The diagram leads us to the following subdomains:

+ **Products** &mdash; Tells us which products are available and which aren't. To do so, the products subdomain needs to be able to track the amount of each product and ingredient in stock.

+ **Orders** &mdash; Manages the lifecycle of each order. This subdomain owns data about the users' orders, and exposes an interface to manage orders and check their status. This subdomain also needs to take care of passing the order details to the kitchen once the payment is done. It also needs to allow the user to check the status of the order while it is being processed. Finally, it also needs to interact with the delivery system to arrange the delivery and expose the status of the delivery.

+ **Payments** &mdash; Handles user payments. Contains all the logic needed for payment processing (card validation, integration with 3rd party payment systems, ...). This subdomains owns all the data related to user payments.

+ **Kitchen** &mdash; Manages the production of the customer's order. This subdomain owns data related to the production of the customer's order, exposing an interface to enable receiving orders and exposing their status. It also notifies the orders subdomain when the order is ready so that it can be delivered.

+ **Delivery** &mdash; Contains specialized logic to resolve the geolocation of the customer and calculate the optimal route. It manages the fleet of riders. It owns data related to all the deliveries. The orders subdomain interfaces with this subdomain to update the itinerary of the customer's order.

Not how each subdomain can be mapped 1:1 to a microservice, as each subdomain encapsulates a well-define and clearly differentiated area of logic that own some portial of the overall application data.

As a result, when applying strategic analysis to an application as defined in DDD, we guarantee that each subdomain can be represented by a microservice that comply with the three microservices principles: database per service, loose coupling, and single responsibility.

The strategic analysis process can be therefore summarized as follows:

1. Describe in text an operation the user needs to perform, as a sequence of steps (e.g., successful delivery of a customer's order).

1. Create a user-journey diagram, depicting in broad lines what happens in each step.

1. Create a subdomain-discovery diagram, identifying the subdomains that play a role in each step.

1. For each subdomain, elaborate on the following aspects:
    + what is the subdomain's main responsibility (e.g., Handle user payments).
    + what is the data that the subdomain owns.
    + what inbound and outbound interactions will be expected in this subdomain (i.e., this will be an indication of the service's interface).

1. Map each subdomain to a microservice.

#### 'Decomposition by business capability' vs. 'decomposition by subdomain'

Both approaches give us different perspectives on the business problem. While *decomposition by subdomain* strategy is more generally applicable, when using *decomposition by business capability* you will end up with an architecture that resembles the existing organizational structure, which might facilitate the collaboration between the business and the technical teams.

The downside of the *decomposition by business capability* is that in general the organizational structure of a company is not necessarily the most efficient from the software development perspective, and in many companies that structure changes frequently. Also, not all the software problems are aligned to a company problem (especially for small-medium software apps).

In summary, if you must choose a single approach, use *decomposition by subdomain*. If you have sufficient time to do a thorough analysis, combine both strategies.
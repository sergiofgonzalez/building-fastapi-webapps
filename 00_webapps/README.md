# The web apps
> design and other info about the web apps to build

## Intro

To illustrate concepts about microservice architectures, API design and FastAPI implementation, I will be building a couple of web apps with different level of complexity.

+ **simple** &mdash; A *'Dizziness Tracker'* application that allows a user to create a journal of their dizziness episodes (duration, when did it start, how strong it was, etc.) and get some statistics about the recorded data (how many episodes were recorded in the past x months, etc.).

+ **complex** &mdash; A *'MovieDB'* application that allows a user to record the movies and tv shows they've watched and get some statistics about them. This example opens up interesting capabilities such as scraping of information from movie sites to populate the information about the cast, exporting information to spreadsheets for review, etc.


## Step 1: Discovery phase: Description of the functionality

The process begins with a discovery phase that describes, in broad strokes, the software application we want to build. Because it is a discovery stage, functionality and technical topics might be mixed together: there are no rules!

You should expect this description to be updated as the software project evolves and new aspects are unveiled in the subsequent phases.

### Dizziness Tracker

The Dizziness Tracker application allows a user to record in a journal their dizziness episodes.

Typically, a user will create a journal entry specifying the date, the level of dizziness they feel, and any remarks associated to that entry. When a user feels dizziness, it typically spans several days. An episode will therefore include several journal entries.

After having recorded journal entries, the user would like to gather certain statistics about their dizziness episodes, and search by different criteria (by date range, by the degree, count the episodes, or understand the average duration of their episodes).

#### Data Model

In the data model, the fundamental entity is the `JournalEntry` which describes a record in the Dizziness Tracker.

The data is very simple:
+ date of the journey
+ level of dizziness the user feels
+ any relevant remarks

The level of dizziness is a value in the range 0-5 that has certain associated symptoms. For example, level 0 is 'not feeling dizzy at all', level 1 is 'feeling a little light-headed but completely functional'.

A few other relevant entities are:
+ LevelSymptoms: a set of symptoms associated to a given level.
+ Episode: a list of associated journal entries that identifies records that go together.

In particular, the episode is a calculated entity that is composed of a sequence of back-to-back journal entries, typically encompassing several days.

![Dizziness Tracker Data Model](pics/dizziness-tracker_data-model.png)

## Step 2: Prototyping: initial scaffolding

It's too early to do a thorough API specification at this stage, as we only have a short description of the application and a few high-level notes about the data model.

However, creating a small prototype of a portion of the application will give us some early hands-on experience, and will allow us unveil challenges we will have to solve on the subsequent phases.

We can start by creating a simple application exposing a REST interface for some portion of the application, with some payload validation, and a fake data layer that we could directly use from the web layer.

### Dizziness Tracker

We create the prototype [Dizziness Tracker](./dizziness-tracker/03_dizziness-tracker_fakes-web/README.md) with a web data layer, payload validation, and a fake data layer that allow a sort of poor-man's in-memory database.

We define the boundaries around the journal entries (which is the main entity of the application), and the related symptoms.


#### API specification

For this initial prototype, as we only we want to get some hands-on experience with FastAPI, Pydantic, and the most relevant entities, we expose only the interface to maintain the journal entries. The associated symptoms will be managed internally (as if they were preloaded), and there will be no management of episodes.

As a result, we will define an  `/entries` resource with the following capabilities:

+ `/entries`
  + `GET` &mdash; retrieves the full list of journal entries.
  + `POST` &mdash; creates a new journal entry.

+ `/entries/{entry_id}`
  + `GET` &mdash; returns an entry
  + `PUT` &mdash; replaces an entry
  + `PATCH` &mdash; modifies an entry
  + `DELETE` &mdash; deletes an entry

| NOTE: |
| :---- |
| We will not have at this point any modeled action, such as `/episodes/{episode_id}/close`. |

##### A few words about creating the API spec in FastAPI

Doing an API-first design is strongly encouraged, and the standard way to do so is through an OpenAPI spec document in either YAML or JSON.

Traditionally, you would write the OpenAPI spec document, and then implement your services to fulfill such spec (maybe with the help of some code generation tools).

FastAPI follows the inverse approach: it lets you define your API interface using Python, and then generates the OpenAPI spec for you. This ensures that your OpenAPI documentation always reflects the code.

You can test your app using the generated OpenAPI spec visiting http:<your-app-url>/docs.

#### Concepts realized in the scaffolding

In the final scaffolding found in [Dizziness Tracker](./dizziness-tracker/03_dizziness-tracker_fakes-web/README.md) we validate the following topics:

+ REST API for the `/entries` resource, with the correct response status codes.

+ Input payload validation and output response validation using Pydantic models.

+ Fake data layer, used from the web layer, that allows the user to maintain entries.

+ Management of duplicated journal entries (by date), and not found entries (by id).

+ Management of custom validators to prevent sending JSON nulls, as `remarks: null`.

## Step 3: Applying strategic design

In this step, you go further in the analysis of the application, trying to unveil the core domain and subdomains of the application.

The goal is to end up with one or more microservices that fulfill the application's functionalities, and each of the microservices following the fundamentals design principles:

1. **Database per service principle**

    Each microservice must own a specific set of data, and no other service should have access to such data except through an API.

1. **Loose coupling principle**

    Each microservice must be able to work independently from others. If a service can't fulfill a single request without calling another service, they belong together.

    Additionally, each microservice must be able to be updated without impacting other services. If changes to a service require updates to other services there is a tight coupling that must be removed by applying more design work.

1. **Single responsibility principle**

    A microservice should be designed around a single business capability or subdomain.

The **strategic analysis** process we will follow can be summarized as folows:

1. Describe in text an operation the user needs to perform, as a sequence of steps (e.g., successful delivery of a customer's order).

1. Create a user-journey diagram, depicting in broad lines what happens in each of the operation steps (e.g., [user journey](../02_microservice-concepts/pics/user_journey_mama_janes.png))

1. Create a subdomain discovery diagram that identifies the subdomains that play a role in each step.

1. For each subdomain, do a textual elaboration of the following aspects:
  + What is the subdomain's main responsibility.
  + What is the data the subdomain owns.
  + What inbound and outbound interactions are expected in the subdomain (i.e., the interface).

1. Map each subdomain to a microservice and confirm the identified microservices fulfill the three microservices principles.

Let's do so for our applications

### Dizziness Tracker: Applying strategic design

In this section we will follow the strategic design process to the Dizziness Tracker. Note that because the app is simple, many of the steps will be trivial.

#### Step 3.1: Describing the operation

We will model the process of a user recording journal entries of their dizziness episodes in the application, and receiving information about it.

The process can be broken down into the following steps:

1. When the user hits the application URL, they are presented with a form allowing the user to enter a new entry, and a table displaying most recent entries and episodes. For each entry, the different symptoms are also displayed. Some statistics are also displayed.

1. The user enters a new journal entry.

1. Once the entry has been added, the new entry details are passed on, so that episodes can be kept up to date.

1. The episodes portion picks up the details of the new entry and updates the status: is it a new episode, is the continuation of an existing one?

1. Once the episodes portion is completed, the user is presented with an updated view of the journal entries and some statistics.

#### Step 3.2: The user-journey diagram

The steps from the previous section can be roughly pictured in a user journey.

![Dizziness Tracker User Journey](pics/dizziness-tracker_user-journey.png)

Because of the simplicity of the application, the user journey is nothing fancy. It just shows the different steps involved in the operation.

#### Step 3.3: The subdomain discovery diagram

The user-journey leads us to the discovery of the application subdomains that pay a role in each step:

![Subdomain discovery diagram](pics/dizziness-tracker_subdomain-identification-diagram.png)

#### Step 3.4: Elaborating on the subdomains

In this step, we elaborate on the following aspects:
+ What is the subdomain main responsibility.
+ What is the data the subdomain owns.
+ What inbound and outbound interactions will be expected in this subdomain

This will let us map each subdomain to a microservice:

+ **Application** &mdash; It will coordinate the display of the dizziness related information (entries, episodes, statistics) and manage the UI interaction. It will not own any data. It will interact with the other subdomains to retrieve the required information to be displayed to the user.

+ **Journal Entries** &mdash; Handles the journal entries of the 'Dizziness Tracker'. It will own the individual journal entries that describe what the user feels in a particular day. It will expose an interface to perform CRUD operations on those entries.

+ **Episodes** &mdash; Manages the dizziness episodes, which groups one or more consecutive journal entries. It will own the episode related data. It will expose an interface to be able to read the episode information, but will not expose any create/update/delete as this information is calculated. It also exposes an operation to process a newly requested journal entry, to be able to pick up its detail and update the episodes data.

+ **Statistics** &mdash; Manages statistics of journal entries and episodes. It will own the statistics related data (if stored). It will expose an interface to to expose the different statistic that are generated, and will interact with the 'Journal Entries' and 'Episodes' subdomains to read their current and be able to calculate the statistics.

#### Step 3.5: Identifying the microservices

In this step we simply do a 1:1 mapping between the identified subdomains and the microservices/services we will build. Because this is a small app, we could opt for joining together a few subdomains in a single project using different routers.

However, for illustration purposes, we will create a microservice per subdomain, even if that design leads us to very small microservices.

The microservices, along with certain technical details, associated with them will be:

+ **Application** &mdash; A Streamlit application that will manage user interaction and coordinate the invocation of the other services. It will show a form, a table with the journal entries, and some statistics.

+ **Journal Entries** &mdash; A FastAPI microservice to manage journal entries and symptoms. It will expose a full CRUD API and own all the journal entries and symptoms data.

+ **Episodes** &mdash; A FastAPI microservice to manage episodes, which is a computed domain model concept not managed by the user. It will expose a read REST API to retrieve episodes and an operation to receive the notification that a new journal entry has been created.

+ **Statistics** &mdash; a FastAPI microservice to manage statistics about journal entries and episodes. It will expose a read REST API to get the latest statistics. Depending on the performance, it might need to own a piece of data with certain precomputed values.
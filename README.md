This is a personal prject I am using to learn / relearn a few different concepts.

I am looking to ingest data from an api, in this instance I am using the POS system [Square]['https://developer.squareup.com/reference/square]. 
The main frameworks or packages I am using are:
- Square Python SDK
- Pydanitc
- SQLModel / SQLAlchemy
- FastAPI (In future for webhooks)


What I am planning on doing: 

Extracting data from API endpoints
Normalizing the JSON response into individual objects in the database
Building dimensional data model - I'm think maybe around line items (line item fact)

Next few things arent as clear as to how Ill do them: 
Building a semantic layer in some tool - maybe snowflake, dbt or pbi. 
Then connecting claude via MCP to be able to have a conversational BI.

If I choose to use something like dbt for my semantic layer then I will probably do all my transformations and build my dimesnsional model using dbt.


Key things I've been learning and exporing:

- Asynchronous programming
    Understanding that a program which depends on I/O bound tasks (reads / writes from DB) are whats slow and not the actual compute required.
- Concurrecncy 
    How can I concurrently run code to improve speed of my program. In this instance I am looking to extract data from the API concurrently.
    I'll need to consider things like, API rate limits, memeory, checkpointing strategy for failures (how can I ensure tasks run concurrently are idempotent), deadlocks, etc.
- 


Architecture flow:

    Check cursor table if any cursur values exists
    Update the base query params if cursor value exists
    Concurrently make request to each of the API endpoints
    Pass the result to each of the processors where data will be validated and written to the db
    Write the cursor to table in db
    Repeat until there is no more cursors returned from the endpoint

Based on the square api documentation, each result will be paginated for things like payments or orders so keeping track of the cursor will be a way for me to checkpoint where I am up to for writing data into the database. I will only update the cursor values if the result has been successfully written to the db.


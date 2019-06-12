## Bugs Found in the Broken HashServe API

Each bug has a unique ID.
Test failures related to each bug are tagged with this ID.

#### BUG-1: Asynchronous functionality non-existent

The API specifications say this:

> A POST to /hash should accept a password. It should return a job identifier
immediately. It should then wait 5 seconds and compute the password hash.

However, `POST /hash` is not returning a Job ID immediately.
It is working synchronously, waiting 5 seconds for the process to complete,
_then_ returning the Job ID.
When the hash is retrieved with the Job ID,
it is immediately available.

I expected get a Job ID from the `POST` call immediately,
then have to poll the `GET /hash` endpoint until the hash is created.


#### BUG-2 Average time is not being calculated correctly

After creating any number of hashes successfully,
a call to `GET /stats` provides some odd results.
The tests show that the `AverageTime` value is considerably higher
than the actual average time.
There doesn't seem to be any immediately obvious rhyme or reason to the values it gives.


#### BUG-3 The `shutdown` feature shuts down the server prematurely

The API specifications say this:

> The software should support a graceful shutdown request. Meaning, it should allow any
in-flight password hashing to complete, reject any new requests, respond with a 200 and
shutdown.

The tests have revealed that intermittently,
when a `POST /hash` call with `shutdown` as the payload is made,
the server shuts down before the response for the `POST /hash` call can even be made.


#### BUG-4 400 Bad Request being used when 404 Not Found is obvious

When making a call to `GET /hash/{jobID}` with a non-existent job ID,
a 400 Bad Request response is returned.
While it is good that a client error is returned,
404 Not Found is specifically intended for cases like this.

## JumpCloud SDET Assignment
**Ryan Casperson**

For this coding assignment, I wrote tests using Python's [behave](https://behave.readthedocs.io/en/latest/) test framework.
In general, I've plenty of thoughts on why BDD is an excellent testing process,
but those conversations can perhaps be saved for the interviews.

Though I was given an API that is known to have issues,
I attempted to write the tests based on how it _should_ work.

In the cases where a test fails because of a bug,
I have left that test case failing,
tagged the test as `@quarantined` to demonstrate that the test is broken due to a bug,
and linked the bug's identifier on the test case.

Details on the bugs I've found are documented [here](./BUGS.md).

### My Approach

I want to highlight a couple things in regard to my approach to testing this application,
as they apply to my approach to testing in general.

One important idea for me is the **isolation of tests**.
It is crucial that each test case be as limited in scope as reasonably possible.
By doing this, we can isolate issues,
and ensure that we have all the information a test run can give,
even if there are failures.

For example, if a test has multiple assertions that aren't directly correlated,
if the first assertion fails, we can't know if the second one would or not,
until the first failure is resolved.

Another thing you might notice is that I strive to **keep the test framework layer as small as possible**.
In these `behave` tests, you can see that often I have something like this:

```py
@when("Something is done")
def step_do_something(context):
    do_something(context.client, context.something)


def do_something(client, something):
    ...
```

The idea behind this extra layer is to make it much easier to move and reuse test logic.
If these tests ever needed to be switch to another test framework,
the `do_something` helper function is already ready to be moved.
The only thing that would change would be where the `client` and `something` params come from,
which depends on the framework.

Also, `do_something` could be easily reused if needed elsewhere.
If you follow my commit history closely,
you might find a case or two where a helper was moved from a step file to a common file,
so that is could be used in multiple step files.


### Running Tests

I didn't put much work in trying automate the creation of the environment,
so I checked everything into this GitHub repo.
The executable I was using for the API is in `./bin`,
and that path is hard coded into the tests.

In order to test the `/stats` values, as well as shutting down the API,
the client handles turning the API server on and off within the tests.
So if you're running tests on Mac OS as I have been,
you shouldn't need any environment setup at all besides cloning this repo,
and changing into the working directory.
Otherwise, you can put the correct executable file need into `./bin` or wherever,
and manually change the path stored as a constant in `tests/environment.py`.

From there here are the commands you need in order to get properly set up, and to run tests:

- `curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python`
- `poetry install`
- `poetry run behave tests`

The `behave` CLI will let you run different combinations of tests if you so choose.

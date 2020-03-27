## Documentation

### Stack

- Language: Python 3.7
- Framework: [Starlette](https://www.starlette.io)
- Templating: [Jinja](https://jinja.palletsprojects.com/en/2.11.x/) (with [jQuery](https://jquery.com) support)

Apart from having [Starlette](https://www.starlette.io) as a web server, `Ledis` is written in pure Python.

### Language Choice

1. Creator familiarity with Python syntax and library system.
2. Basic requirements were to replicate common data stored in `Redis` such as String and Set, leading to choice of language to be Python:
    * Python dictionary data structure has pre-built method that support key-value pair store and retrieve functions.

### Implementation

1. Data structure:
    - 1.1. Why dictionary is used:
        - Suitable for storing bivariate data
        - Almost constant time for look up process
        - Unique and immutable pre-built data structure with lots of helper methods
    - 1.2. Class `BaseDataStructure`
        - Base class for all the required functionalities in other data types
        - Reduce repetitive code in String and Set wrapper classes
        - Each data type has `type` property correspond to either `String` or `Set` enum type, `expire_at` to store data's expiration date and the `data` itself.

2. How TTL is implemented
    - Each data types in Ledis has a property called `expire_at` to store the future date for data to expire which is pre-set to `None`
    - When user calls `EXPIRE` with an amount time in seconds, Ledis appends to the data with corresponding key `expire_at` value calculated at that moment.
    - Data is design to be *lazily deleted* whenever a method is called (each method checks if data has been expired when getting value from a key)


3. Snapshots
    - Used module `shelve` in Python for data persistence
    - Since the goal was to make Redis lightweight, `shelve` basic functionality to serialize object into bytes on disk and can recreate it from the bytes later on fufills with the project need.
    - Any Python objects can be stored arbitrarily in a shelf

4. Web server - Starlette

    * [Starlette](https://www.starlette.io) is used as a web server to serve HTML templates and CLI for `Ledis`.

5. Templates
    * 5.1. jQuery - create ajax request to server
    * 5.2. TailwindCSS - front-end styling framework
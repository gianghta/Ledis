# Ledis

A lightweight version of Redis. Try out demo [here](https://ledis-app-proj.herokuapp.com/)

> Written in Python 3.7

## Installation

### 1. Install Python 3.7 (and pip)

### 2. Install the dependencies for Python

```
pip install poetry

# Install the dependencies
poetry install
```

## Usage

Run the application:
```
poetry run uvicorn ledis.app:app
```

The application will be running at http://localhost:8000

#### Commands

1. String:
    * __SET__ _key value_: set a string value, always overwriting what is saved under key
    * __GET__ _key_: get a string value at key

2. Set:
    * __SADD__ _key value1 [value2...]_: add values to set stored at key
    * __SREM__ _key value1 [value2...]_: remove values from set
    * __SMEMBERS__ _key_: return array of all members of set
    * __SINTER__ _[key1] [key2] [key3] ..._: (bonus) set intersection among all set stored in specified keys. Return array of members of the result set

3. Data Expiration:
    * __KEYS__: List all available keys
    * __DEL__ _key_: delete a key
    * __EXPIRE__ _key seconds_: set a timeout on a key, seconds is a positive integer (by default a key has no expiration). Return the number of seconds if the timeout is set
    * __TTL__ _key_: query the remaining time-to-live of a key

4. Snapshot:
    * __SAVE__: save current state in a snapshot
    * __RESTORE__: restore from the last snapshot,

5. Error Handling:
When an error occurs, the error message is returned as `[ERROR] <error_message>`.


## Testing

```
poetry run pytest
```

## Documentation

[Read docs here](/docs/README.md)
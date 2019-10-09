# Intro [![Build Status](https://travis-ci.org/triplepoint/ansible-self-signed-certificates.svg?branch=master)](https://travis-ci.org/triplepoint/ansible-self-signed-certificates)
Install and configure self-signed certificates for multiple domains.

there's one variable defined that isn't namespaced with this role and that's `certbot_certs`.  This variable is intended to duplicate the interface of the `geerlingguy.certbot` role, so that this role can be smoothly substituted for `geerlingguy.certbot` during testing.  See the role variables for more details.

## Requirements
None.

## Role Variables
See the [comment in the default variables file](defaults/main.yml) for information on configuration.

## Dependencies
None.

## Example Playbook
    - hosts: whatever
      roles:
        - triplepoint.self_signed_certificates

## Role Testing
This role is tested with `molecule`, using `pipenv` to handle dependencies and the Python testing environment.

### Setting Up Your Execution Environment
``` sh
pip install pipenv
```

Once you have `pipenv` installed, you can build the execution virtualenv with:
``` sh
pipenv install --dev
```

### Running Tests
Once you have your environment configured, you can execute `molecule` with:
``` sh
pipenv run molecule test
```

### Regenerating the Lock File
You shouldn't have to do this very often, but if you change the Python package requirements using `pipenv install {some_package}` commands or by editing the `Pipfile` directly, or if you find the build dependencies have fallen out of date, you might need to regenerate the `Pipfile.lock`.
``` sh
pipenv update --dev
```
Be sure and check in the regenerated `Pipfile.lock` when this process is complete.

## License
MIT

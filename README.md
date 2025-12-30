# Intro

Install and configure self-signed certificates for multiple domains.

there's one variable defined that isn't namespaced with this role and that's `certbot_certs`. This variable is intended to duplicate the interface of the `geerlingguy.certbot` role, so that this role can be smoothly substituted for `geerlingguy.certbot` during testing. See the role variables for more details.

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

## License

MIT

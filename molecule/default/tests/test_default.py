import os
from os.path import join
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


cert_dir = '/etc/self-signed-certs/live/'


@pytest.mark.parametrize('domain', ['example1.com', 'example3.com'])
def test_domain_cert_directories_exist(host, domain):
    assert host.file(join(cert_dir, domain)).exists
    assert host.file(join(cert_dir, domain)).is_directory
    assert host.file(join(cert_dir, domain, 'ca')).exists
    assert host.file(join(cert_dir, domain, 'ca')).is_directory


@pytest.mark.parametrize('domain', ['example1.com', 'example3.com'])
@pytest.mark.parametrize('finfo', [
    ('ca/privkey.pem', '0600'),
    ('ca/crt.pem', '0644'),
    ('privkey.pem', '0600'),
    ('cert.pem', '0644'),
    ('chain.pem', '0644'),
    ('fullchain.pem', '0644'),
])
def test_domain_certificate_files_exist(host, domain, finfo):
    assert host.file(join(
            cert_dir, domain, finfo[0])).exists

    assert oct(host.file(join(cert_dir, domain, finfo[0])).mode) == finfo[1]


@pytest.mark.parametrize('domain', ['example1.com', 'example3.com'])
def test_domains_represented_in_cert_pem(host, domain):
    """
    #  - assert that the domains specified are present in the cert.pem file
    #    openssl x509 -noout -text -nameopt multiline -in <cert file>

    # ca/crt.pem has all of :
    #country_name: "{{ self_signed_certs_subject_country }}"
    #locality_name: "{{ self_signed_certs_subject_city }}"
    #organization_name: "{{ self_signed_certs_subject_org_name }}"
    #organizational_unit_name: "{{ self_signed_certs_subject_org_unit }}"
    # common_name: "{{ self_signed_certs_subject_org_name }}"


    # cert.pem cert has all of :
    # country_name: "{{ self_signed_certs_subject_country }}"
    # locality_name: "{{ self_signed_certs_subject_city }}"
    # organization_name: "{{ self_signed_certs_subject_org_name }}"
    # organizational_unit_name: "{{ self_signed_certs_subject_org_unit }}"
    # common_name: "{{ cert_item.domains | first }}"
    # subject_alt_name: "DNS:{{ cert_item.domains | join(',DNS:') }}"
    """

    pass


@pytest.mark.parametrize('domain', ['example1.com', 'example3.com'])
def test_content_of_chainfiles(host, domain):
    cacert = host.file(join(cert_dir, domain, 'ca/crt.pem')).content

    domaincert = host.file(join(cert_dir, domain, 'cert.pem')).content

    chainfile = host.file(join(cert_dir, domain, 'chain.pem')).content

    assert chainfile == cacert

    fullchainfile = host.file(join(cert_dir, domain, 'fullchain.pem')).content

    test_fullchain_val = domaincert + "\n" + cacert
    assert fullchainfile == test_fullchain_val

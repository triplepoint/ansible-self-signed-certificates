import os
from os.path import join
import pytest
import OpenSSL.crypto
from cryptography import x509
from cryptography.x509.oid import ExtensionOID
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
    assert host.file(join(cert_dir, domain, finfo[0])).exists
    assert oct(host.file(join(cert_dir, domain, finfo[0])).mode) == finfo[1]


@pytest.mark.parametrize('domain', ['example1.com', 'example3.com'])
def test_domains_represented_in_ca_cert_pem(host, domain):
    cfile = host.file(join(cert_dir, domain, 'ca/crt.pem')).content
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cfile)
    assert cert.get_subject().countryName == "US"
    assert cert.get_subject().localityName == "San Francisco"
    assert cert.get_subject().organizationName == "Self Signed"
    assert cert.get_subject().organizationalUnitName == \
        "Self Signed Certificates Department"
    assert cert.get_subject().commonName == "Self Signed"


@pytest.mark.parametrize('domain', [
    ('example1.com', ['example1.com', 'example2.com']),
    ('example3.com', ['example3.com'])
])
def test_domains_represented_in_domain_cert_pem(host, domain):
    cfile = host.file(join(cert_dir, domain[0], 'cert.pem')).content
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cfile)
    assert cert.get_subject().countryName == "US"
    assert cert.get_subject().localityName == "San Francisco"
    assert cert.get_subject().organizationName == "Self Signed"
    assert cert.get_subject().organizationalUnitName == \
        "Self Signed Certificates Department"
    assert cert.get_subject().commonName == domain[0]

    # Dealing with ASN.1 fields is a bit tricker, let's fall back
    # on the cryptography package
    csert = cert.to_cryptography()
    ext = csert.extensions.get_extension_for_oid(
        ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
    san_domains = ext.value.get_values_for_type(x509.DNSName)
    assert san_domains == domain[1]


@pytest.mark.parametrize('domain', ['example1.com', 'example3.com'])
def test_content_of_chainfiles(host, domain):
    cacert = host.file(join(cert_dir, domain, 'ca/crt.pem')).content

    domaincert = host.file(join(cert_dir, domain, 'cert.pem')).content

    chainfile = host.file(join(cert_dir, domain, 'chain.pem')).content

    assert chainfile == cacert

    fullchainfile = host.file(join(cert_dir, domain, 'fullchain.pem')).content

    test_fullchain_val = domaincert + "\n" + cacert
    assert fullchainfile == test_fullchain_val


@pytest.mark.parametrize('domain', ['example1.com', 'example3.com'])
def test_dhparams_file_exists(host, domain):
    assert host.file(join(cert_dir, domain, 'dhparams.pem')).exists
    assert oct(host.file(join(
        cert_dir, domain, 'dhparams.pem'
    )).mode) == '0644'

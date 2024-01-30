from cryptography import x509
from datetime import datetime

import os

def check_cert_validity(cert):
    not_valid_before = cert.not_valid_before
    not_valid_after = cert.not_valid_after

    current_date = datetime.utcnow()

    if not_valid_before <= current_date <= not_valid_after:
        return True
    else:
        return False


def load_certificate(file_path):
    with open(file_path, 'rb') as f:
        cert_data = f.read()
        cert = x509.load_pem_x509_certificate(cert_data)
        subject = cert.subject

    return cert, subject


def load_system_trusted_certificates():
    trusted_certs = {}
    certs = os.scandir("/etc/ssl/certs")
    for cert in certs:
        if cert.is_file():
            cert, subject = load_certificate(cert.path)
            if check_cert_validity(cert):
                trusted_certs[subject] = cert

    return trusted_certs


def validate_certificate_chain(cert, trusted_certs):
    chain = [cert]

    while chain[-1].issuer != chain[-1].subject:
        chain.append(trusted_certs[str(chain[-1].issuer)])

    for i in range(len(chain) - 1):
        if chain[i].issuer != chain[i + 1].subject:
            return False
        
    return True


def main():
    trusted_certs = load_system_trusted_certificates()
    for subject, cert in trusted_certs.items():
        print(subject)
        print(cert)
        print("Chain validity:", validate_certificate_chain(cert, trusted_certs))
        print("")


if __name__ == "__main__":
    main()
 

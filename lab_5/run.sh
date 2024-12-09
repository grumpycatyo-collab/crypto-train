#!/bin/bash

# Directory structure
mkdir -p ca/{certs,crl,newcerts,private}
mkdir -p users/{private,certs}
touch ca/index.txt
echo "1000" > ca/serial

# Generate CA private key (4096 bits)
openssl genrsa -out ca/private/ca.key 4096

# Generate CA self-signed certificate (valid for 10 years)
openssl req -new -x509 -days 3650 -key ca/private/ca.key -out ca/certs/ca.crt -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=RootCA"

# Configuration file for OpenSSL
cat > ca/openssl.cnf << EOL
[ ca ]
default_ca = CA_default

[ CA_default ]
dir               = ./ca
certs             = \$dir/certs
crl_dir           = \$dir/crl
new_certs_dir     = \$dir/newcerts
database          = \$dir/index.txt
serial            = \$dir/serial
RANDFILE          = \$dir/private/.rand

private_key       = \$dir/private/ca.key
certificate       = \$dir/certs/ca.crt

crl               = \$dir/crl/ca.crl
crlnumber         = \$dir/crlnumber
crl_extensions    = crl_ext
default_crl_days  = 30

default_md        = sha256
name_opt         = ca_default
cert_opt         = ca_default
default_days     = 365
preserve         = no
policy           = policy_strict

[ policy_strict ]
countryName             = match
stateOrProvinceName     = match
organizationName        = match
organizationalUnitName  = optional
commonName              = supplied
emailAddress           = optional

[ req ]
default_bits        = 2048
distinguished_name  = req_distinguished_name
string_mask         = utf8only
default_md          = sha256
x509_extensions     = v3_ca

[ req_distinguished_name ]
countryName                     = Country Name (2 letter code)
stateOrProvinceName             = State or Province Name
localityName                    = Locality Name
organizationName                = Organization Name
organizationalUnitName          = Organizational Unit Name
commonName                      = Common Name

[ v3_ca ]
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints = critical, CA:true
keyUsage = critical, digitalSignature, cRLSign, keyCertSign
EOL

create_user_certificate() {
    local username=$1

    if [ -f "users/certs/${username}.crt" ]; then
        echo "Error: Certificate for ${username} already exists"
        return 1
    fi

    local current_serial=$(cat ca/serial)
    echo $((current_serial + 1)) > ca/serial

    openssl genrsa -out users/private/${username}.key 2048

    openssl req -new \
        -key users/private/${username}.key \
        -out users/certs/${username}.csr \
        -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=${username}"

    openssl ca -config ca/openssl.cnf \
        -in users/certs/${username}.csr \
        -out users/certs/${username}.crt \
        -notext -batch
}

revoke_user_certificate() {
    local username=$1

    if [ ! -f "users/certs/${username}.crt" ]; then
        echo "Error: Certificate for ${username} not found"
        return 1
    fi

    echo "Revoking certificate for ${username}..."
    openssl ca -config ca/openssl.cnf -revoke users/certs/${username}.crt

    echo "Generating new Certificate Revocation List..."
    openssl ca -config ca/openssl.cnf -gencrl -out ca/crl/ca.crl

    rm -f users/certs/${username}.crt users/certs/${username}.csr users/private/${username}.key
    echo "Certificate for ${username} has been revoked and files cleaned up"
}

sign_file() {
    local username=$1
    local filename=$2

    if [ ! -f "users/private/${username}.key" ]; then
        echo "Error: User '${username}' does not exist or private key not found."
        return 1
    fi

    if [ ! -f "${filename}" ]; then
        echo "Error: File '${filename}' does not exist."
        return 1
    fi

    echo "=== Starting Digital Signature Process ==="
    echo "User: ${username}"
    echo "File to sign: ${filename}"
    echo "Using private key: users/private/${username}.key"

    echo "Creating signature..."
    if openssl dgst -sha256 -sign "users/private/${username}.key" -out "${filename}.sig" "${filename}"; then
        echo "✓ Signature created successfully"
        echo "Signature file: ${filename}.sig"
        echo "Signature size: $(stat -f %z "${filename}.sig") bytes"
        echo "Original file size: $(stat -f %z "${filename}") bytes"
        echo "Timestamp: $(date)"
        echo "=== Signature Process Complete ==="
        return 0
    else
        echo "✗ Failed to create signature"
        echo "=== Signature Process Failed ==="
        return 1
    fi
}

verify_signature() {
    local username=$1
    local filename=$2

    if [ ! -f "users/certs/${username}.crt" ]; then
        echo "Error: User certificate for '${username}' not found."
        return 1
    fi

    if [ ! -f "${filename}" ]; then
        echo "Error: Original file '${filename}' not found."
        return 1
    fi

    if [ ! -f "${filename}.sig" ]; then
        echo "Error: Signature file '${filename}.sig' not found."
        return 1
    fi

    echo "=== Starting Signature Verification Process ==="
    echo "User: ${username}"
    echo "File to verify: ${filename}"
    echo "Signature file: ${filename}.sig"
    echo "Using certificate: users/certs/${username}.crt"

    echo "Extracting public key from certificate..."
    echo "Certificate details:"
    openssl x509 -in "users/certs/${username}.crt" -text -noout | grep "Subject:" || true

    echo "Verifying signature..."
    if openssl dgst -sha256 -verify <(openssl x509 -in "users/certs/${username}.crt" -pubkey -noout) \
        -signature "${filename}.sig" "${filename}"; then
        echo "✓ Signature verification SUCCESSFUL"
        echo "The signature is valid and the file has not been tampered with."
    else
        echo "✗ Signature verification FAILED"
        echo "The signature is invalid or the file has been modified!"
        return 1
    fi

    echo "Verification timestamp: $(date)"
    echo "File hash (SHA256): $(openssl dgst -sha256 "${filename}" | cut -d' ' -f2)"
    echo "=== Verification Process Complete ==="
    return 0
}

show_file_info() {
    local file=$1
    echo "File: ${file}"
    echo "Size: $(stat -f %z "${file}") bytes"
    echo "Last modified: $(stat -f %Sm "${file}")"
    echo "SHA256 hash: $(openssl dgst -sha256 "${file}" | cut -d' ' -f2)"
}

while true; do
    echo "PKI Management System"
    echo "1. Create user certificate"
    echo "2. Revoke user certificate"
    echo "3. Sign a file"
    echo "4. Verify signature"
    echo "5. Exit"
    read -p "Choose an option: " choice

    case $choice in
        1)
            read -p "Enter username: " username
            create_user_certificate "$username"
            ;;
        2)
            read -p "Enter username to revoke: " username
            revoke_user_certificate "$username"
            ;;
        3)
            read -p "Enter username: " username
            read -p "Enter filename to sign: " filename
            sign_file "$username" "$filename"
            ;;
        4)
            read -p "Enter username: " username
            read -p "Enter filename to verify: " filename
            verify_signature "$username" "$filename"
            ;;
        5)
            exit 0
            ;;
        *)
            echo "Invalid option"
            ;;
    esac
done
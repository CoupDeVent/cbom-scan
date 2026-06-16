"""
Hardcoded secrets anti-pattern
WARNING: Scanner does NOT detect hardcoded keys/secrets.
This demonstrates what SHOULD be detected but isn't by current regex.
"""

# --- Hardcoded API Keys (SECURITY ANTI-PATTERN) ---

AWS_ACCESS_KEY = 'AKIAIOSFODNN7EXAMPLE'
AWS_SECRET_KEY = 'AbCdEfGhIjKlM/1324567/abcdefghijklmnopqr'

GITHUB_TOKEN = 'ghp_1234567890abcdefghijklmnopqrstuvwxyzABCD'
SLACK_WEBHOOK = 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX'

PRIVATE_KEY = '''-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA2a2j9Q1dBWsK8w8vK7x0L8v6L1w0K0w0L8v6L1w0K0w0L8v6
L1w0K0w0L8v6L1w0K0w0L8v6L1w0K0w0L8v6L1w0K0w0L8v6L1w0K0w0L8v6L1w0
K0w0L8v6L1w0K0w0L8v6L1w0K0w0L8v6L1w0K0w0L8v6L1w0K0w0L8v6L1w0K0w0
L8v6L1w0K0w0L8v6L1w0K0w0L8v6L1w0K0w0L8v6L1w0K0w0L8v6L1w0K0w0L8v6
-----END RSA PRIVATE KEY-----'''

DATABASE_PASSWORD = 'SuperSecret123!@#'
DB_CONNECTION_STRING = 'Server=db.example.com;User=admin;Password=MyP@ssw0rd!;Database=ProdDB'

API_SECRET = 'this-is-a-very-secret-api-key-12345'
ENCRYPTION_MASTER_KEY = '0123456789ABCDEF0123456789ABCDEF'  # 256-bit hex key

# --- Credentials in JSON format (sometimes missed) ---

CREDENTIALS = {
    'username': 'admin',
    'password': 'admin123',
    'api_key': 'sk_live_4eC39HqLyjWDarhtT657Gt9R',
    'private_key': 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC...',
}

# --- Certificate with private key (PEM format) ---

SSL_CERTIFICATE = '''-----BEGIN CERTIFICATE-----
MIIDXTCCAkWgAwIBAgIJALn5Q/c123/QMA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNV
BAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBX
aWRnaXRzIFB0eSBMdGQwHhcNMjMwMTAxMDAwMDAwWhcNMjQwMTAxMDAwMDAwWjBF
-----END CERTIFICATE-----'''

# --- Database credentials (common anti-pattern) ---

class DatabaseConfig:
    host = 'db.production.example.com'
    user = 'db_admin'
    password = 'Pas5w0rd!@#'
    port = 5432
    database = 'customer_data'
    ssl_cert = '/path/to/client-cert.pem'
    ssl_key = 'BEGIN PRIVATE KEY-----MIIEvQIBADANBgkqhkiG9w0BA...'


# --- OAuth tokens ---

OAUTH_CLIENT_ID = '123456789-abc.apps.googleusercontent.com'
OAUTH_CLIENT_SECRET = 'GOCSPX-abcdefghijklmnopqrstu_12345'
OAUTH_BEARER_TOKEN = 'ya29.a0AfH6SMBx1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p'

# --- API credentials ---

STRIPE_API_KEY = 'sk_live_4eC39HqLyjWDarhtT657Gt9R'
STRIPE_SECRET_KEY = 'rk_live_51234567890abcdefghijklmno'
TWILIO_AUTH_TOKEN = 'abcdef1234567890abcdef1234567890'

# --- Encryption key vault (anti-pattern) ---

ENCRYPTION_KEYS = {
    'master': '0123456789ABCDEF0123456789ABCDEF',
    'session': 'FEDCBA9876543210FEDCBA9876543210',
    'backup': 'aaaaaabbbbbbccccccddddddeeeeee00',
}

# --- SSH Private Keys ---

SSH_PRIVATE_KEY = '''-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUtAAAACWFlczI1Ni1jdHIAAAAgP1kKqFwL
m/dM3k5Q6v7z1234567890ABCDEFGHIJKLMNOPQRST=
-----END OPENSSH PRIVATE KEY-----'''

# --- Function that uses hardcoded key ---

def connect_database():
    """Attempts to use hardcoded credentials (VERY BAD)."""
    connection_string = f'postgresql://{DatabaseConfig.user}:{DatabaseConfig.password}@{DatabaseConfig.host}:{DatabaseConfig.port}/{DatabaseConfig.database}'
    # This would connect using hardcoded password - extremely insecure!
    return connection_string


def get_api_key():
    """Returns hardcoded API key (ANTI-PATTERN)."""
    return STRIPE_API_KEY  # Should use environment variables instead


# --- Comments that mention credentials (metadata leakage) ---

# Old backup key: abcdef0123456789abcdef0123456789
# Previous admin password: OldP@ssw0rd123
# Test API key: test_key_never_ever_use_this

import secrets

# Generate a 32-character random API key
api_key = secrets.token_hex(32)
print("Your secure API key:", api_key)

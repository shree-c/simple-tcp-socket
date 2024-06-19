from Crypto.PublicKey import RSA
from app.utils import generate_key_pair
import sys
if len(sys.argv) != 2:
    print("Usage: python rsa.py <key_name>")
    sys.exit(1)

# Generate RSA key pair
private_key, public_key = generate_key_pair()

with open(f'{sys.argv[1]}_private.pem', 'wb') as f:
    f.write(private_key)

with open(f'{sys.argv[1]}_public.pem', 'wb') as f:
    f.write(public_key)


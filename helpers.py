from hashlib import sha256


# This is the only password you'll need to remember,
# so better not have it hard-coded here.
MASTER_KEY = input('Please enter the master key: ')

# All available characters accepted in passwords.
all_chars = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'
             'abcdefghijklmnopqrstuvwxyz'
             '0123456789!@#$%^&*()-_')


def get_hexdigest(salt, plaintext):
    # In the latest versions of hashlib, you need to specify the encoding.
    return sha256(salt.encode('utf-8') + plaintext.encode('utf-8')).hexdigest()


def make_password(plaintext, service):
    # Use the master key in the salt for extra security.
    # The string is too long, the first 20 digits will suffice.
    salt = get_hexdigest(MASTER_KEY, service)[:20]
    hsh = get_hexdigest(salt, plaintext)
    return ''.join((salt, hsh))


def password(plaintext, service, length=10):
    # Make the hexdigest.
    raw_hexdigest = make_password(plaintext, service)
    # Convert it to decimal.
    num = int(raw_hexdigest, 16)
    num_chars = len(all_chars)
    chars = []
    # Build the final password.
    while len(chars) < length:
        num, idx = divmod(num, num_chars)
        chars.append(all_chars[idx])
    # Convert the password array to a string.
    return ''.join(chars)

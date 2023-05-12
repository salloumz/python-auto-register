import hashlib
import pyotp

def generate_2fa_code(secret):
    # Create a TOTP object with the given secret
    totp = pyotp.TOTP(secret, digits=6, digest=hashlib.sha1)

    # Get the current TOTP code
    code = totp.now()

    # Return the TOTP code as a string
    return str(code)

def main():
    # get the secret from the totpsecret.txt file
    totpsecret = open("totpsecret.txt", "r").read()
    code = generate_2fa_code(totpsecret)
    print(code)

main()
import random
from math import gcd
from sympy import isprime

def generate_prime():
    """Generates a random prime number between 1000 - 10000."""
    while True:
        num = random.randint(1000, 9999)
        if isprime(num):
            return num

def mod_inverse(e, phi):
    """Finds the modular inverse of e modulo phi using the extended Euclidean algorithm."""
    def egcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = egcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    gcd_val, x, _ = egcd(e, phi)
    if gcd_val != 1:
        raise ValueError("Modular inverse does not exist")
    return x % phi

def rsa_key_generation():
    """Generates RSA public and private keys."""
    p = generate_prime()
    q = generate_prime()
    while q == p:
        q = generate_prime()

    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose e such that 1 < e < phi and gcd(e, phi) == 1
    e = random.randint(2, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    d = mod_inverse(e, phi)

    return (e, n), (d, n)

def encrypt(plaintext, public_key):
    """Encrypts plaintext using the public key."""
    e, n = public_key
    ciphertext = [pow(ord(char), e, n) for char in plaintext]
    return ciphertext

def decrypt(ciphertext, private_key):
    """Decrypts ciphertext using the private key."""
    d, n = private_key
    plaintext = ''.join(chr(pow(char, d, n)) for char in ciphertext)
    return plaintext

def main():
    print("RSA Algorithm Implementation")

    public_key, private_key = rsa_key_generation()
    print(f"Public Key: {public_key}")
    print(f"Private Key: {private_key}")

    message = input("Enter a message to encrypt: ")
    encrypted_message = encrypt(message, public_key)
    print(f"Encrypted Message: {encrypted_message}")

    decrypted_message = decrypt(encrypted_message, private_key)
    print(f"Decrypted Message: {decrypted_message}")

if __name__ == "__main__":
    main()

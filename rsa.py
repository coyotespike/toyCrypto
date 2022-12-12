"""
Stolen in toto from https://github.com/garrethmcdaid/python-toy-encryption/blob/master/rsa/rsa.py

Typed to learn how it works

The reason the math is a little complex is we want to find two numbers that are inverse to each other, like reciprocals.

Raise a message to the power of the public key, then mod it by the modulus.
Raise the encrypted message to the power of the private key, then mod it by the modulus.

1. Why do we use Phi(F), and not just F? The README states that PHI is secret, and so it is, but F is just as secret and secure.
2. And I don't fully how the modular inverses work with exponentiation and modulo.

Nevertheless, I have a somewhat better understanding of RSA now.
"""

import random
from math import gcd

# https://stackoverflow.com/questions/48733714/smallest-coprime
def check_co_prime(first_number, second_number):
    '''
    Check if two numbers have different "atoms", i.e. made from different prime numbers
    '''
    return gcd(first_number, second_number) == 1


# https://stackoverflow.com/questions/48733714/smallest-coprime
def get_smallest_co_prime(number):
    '''
    Find the smallest coprime number for another number
    - You have to start at 2 because -1 and 1 are coprime to every other number

    For example, for 10, the smallest coprime number is 3
    '''
    for i in range(2, number): # for every number *i* starting from 2 up to M
        if check_co_prime(i, number): # check if *i* is coprime with M
            return i # if it is, return i as the result

def is_prime(num):
    '''
    Actually we only need to go up to the square root of a number
    to check if it is prime.
    '''
    if num == 0 or num == 1:
        return False
    for x in range(2, num):
        if num % x == 0:
            return False
    else:
        return True

# https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
def egcd(a, b):
    '''
    Python implementation of extended Euclidean algorithm
    - required to calculate the modular inverse
    '''
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


# https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
def modinv(a, m):
    '''
    Wrapper for egdc() to calculate modular inverse and find where it does not exist
    '''
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

######## End of Helper Functions ########

# Place a limit on the number of Primes we will consider
# in calculation to ensure we do not overburden the CPU
limit = 100

# Obtain a list of Prime numbers that exist in range from 7 to limit
# We chose 7 because RSA does not work with Primes below 7
primes = list(filter(is_prime, range(7,limit)))

# Step 1
# RSA starts with the selection of 2 Prime numbers
p1 = random.choice(primes)
p2 = random.choice(primes)

# We ensure that the 2 Prime numbers are not the same
while p2 == p1:
    p2 = random.choice(primes)

# Use this if you want to test with specific Primes
# Uncomment the lines below
p1 = 7
p2 = 11

# Step 2
# Multiply the 2 Prime numbers
factorOfPrimes = p1*p2

print(f'F: {factorOfPrimes}')


# Step 3
# Find the PHI value of the factor of the Primes
# This is the essential part of RSA. Only one party knows this value
phiOfFactorOfPrimes = (p1 - 1)*(p2 - 1)

print(f'PHI(F): {phiOfFactorOfPrimes}')


# Step 4
# Get a small exponent (to the power of) of the PHI value of the factor of Primes
# This value needs to be coprime with the PHI value of the factor of Primes
pubExp = get_smallest_co_prime(phiOfFactorOfPrimes)

print(f'Public Exponent: {pubExp}')

# Step 5
# The Private Key is the modular inverse of the exponent and the PHI value of the factor of Primes
# See the README for a more detailed explanation
priKey = modinv(pubExp, phiOfFactorOfPrimes)

print(f'Private Key: {priKey}')


# We now have what we need for the parties to exchange secure information

# Bob want to encrypt a message (we use a number for the message) and send it to Alice
# Alice sends Bob her Public Key (pubExp and factorOfPrimes)
# Bob performs calculation 75**pubExp%phiOfFactorOfPrimes
# This is the encrypted payload he sends to Alice

print(f'\nComplete the exchange')
print(f'#####################\n')

message = random.choice(range(1,10))
print(f'Plaintext message: {message}')

# This is the encrypted message Bob sends to Alice
encrypted_message = ( message ** pubExp ) % factorOfPrimes

print(f'\nEncrypted message: {encrypted_message}')

# Alice can now decrypt the message with her Private Key
decrypted_message = ( encrypted_message ** priKey ) % factorOfPrimes

print(f'\nDecrypted message: {decrypted_message}\n')

print(f'Bob successfully sent Alice a secure message: {decrypted_message == message}')


# Imagine taking a string, converting each letter to a number in a list
# and then encrypting each number in the list
# On other side, decrypting each number in the list and converting back to a string

# And vice versa
alice_encrypted_message = ( message ** priKey ) % factorOfPrimes
print(f'\nAlice encrypted message: {alice_encrypted_message}')
bob_decrypted_message = ( alice_encrypted_message ** pubExp ) % factorOfPrimes
print(f'\nBob decrypted message: {bob_decrypted_message}')

print(f'\nAlice successfully sent Bob an authenticated message: {bob_decrypted_message == message}')

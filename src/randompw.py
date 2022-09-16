import random
import string

# get random password pf length 8 with letters, digits, and symbols
characters = string.ascii_letters + string.digits
password = ''.join(random.choice(characters) for i in range(8))
print("Random password is:", password)
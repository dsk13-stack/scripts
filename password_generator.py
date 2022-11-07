#Генератор псевдо-случайных паролей для использования в терминале

import random
import argparse


ASCII_LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'
ASCII_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
DIGITS = '0123456789'
SPECIAL = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""

password_chars = ''
password = ''

parser = argparse.ArgumentParser(description='Password generator')
parser.add_argument('pass_len', help='Password len', type=int)
parser.add_argument('-u', '--uppercase', help='Use uppercase characters', action='store_true')
parser.add_argument('-l', '--lowercase', help='Use lowercase characters', action='store_true')
parser.add_argument('-d', '--digits', help='Use digits', action='store_true')
parser.add_argument('-s', '--special', help='Use special characters', action='store_true')
args = parser.parse_args()

if not args.uppercase and not args.lowercase and not args.digits and not args.special:
    password_chars += ASCII_LOWERCASE + ASCII_UPPERCASE + DIGITS + SPECIAL
else:
    if args.uppercase:
        password_chars += ASCII_UPPERCASE
    if args.lowercase:
        password_chars += ASCII_LOWERCASE
    if args.digits:
        password_chars += DIGITS
    if args.special:
        password_chars += SPECIAL

for i in range(args.pass_len):
    password += random.choice(password_chars)
print(password)

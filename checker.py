import hashlib
import urllib.request

def check_pwned(password):
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    with urllib.request.urlopen(url) as response:
        hashes = response.read().decode('utf-8').splitlines()

    for line in hashes:
        hash_suffix, count = line.split(':')
        if hash_suffix == suffix:
            return int(count)
    return 0

def check_strength(password):
    score = 0
    if len(password) >= 12:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(not c.isalnum() for c in password):
        score += 1
    levels = {0: "Very Weak", 1: "Weak", 2: "Moderate", 3: "Strong", 4: "Very Strong"}
    return levels[score]

password = input("Enter a password to check: ")
count = check_pwned(password)
strength = check_strength(password)

print(f"\nStrength: {strength}")
if count > 0:
    print(f"WARNING: This password has appeared in {count:,} known data breaches. Do not use it.")
else:
    print("Good news: this password was not found in known breaches.")
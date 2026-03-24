import secrets
import string
import math

SIMILAR = "il1Lo0O"

def build_charset(uppercase: bool, lowercase: bool, numbers: bool, symbols: bool, exclude_similar: bool) -> str:
    charset = ""
    if uppercase:
        charset += string.ascii_uppercase
    if lowercase:
        charset += string.ascii_lowercase
    if numbers:
        charset += string.digits
    if symbols:
        charset += string.punctuation
    if exclude_similar:
        charset = "".join(c for c in charset if c not in SIMILAR)
    return charset

def generate_password(length: int, uppercase: bool, lowercase: bool, numbers: bool, symbols: bool, exclude_similar: bool) -> str:
    charset = build_charset(uppercase, lowercase, numbers, symbols, exclude_similar)

    # Guarantee at least one char from each selected group
    required = []
    groups = []
    if uppercase:
        groups.append("".join(c for c in string.ascii_uppercase if c not in (SIMILAR if exclude_similar else "")))
    if lowercase:
        groups.append("".join(c for c in string.ascii_lowercase if c not in (SIMILAR if exclude_similar else "")))
    if numbers:
        groups.append("".join(c for c in string.digits if c not in (SIMILAR if exclude_similar else "")))
    if symbols:
        groups.append(string.punctuation)

    for group in groups:
        required.append(secrets.choice(group))

    remaining = [secrets.choice(charset) for _ in range(length - len(required))]
    password_list = required + remaining
    secrets.SystemRandom().shuffle(password_list)
    return "".join(password_list)

def calculate_strength(password: str) -> dict:
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    pool = 0
    if has_upper: pool += 26
    if has_lower: pool += 26
    if has_digit: pool += 10
    if has_symbol: pool += 32

    entropy = round(len(password) * math.log2(pool), 2) if pool else 0

    if entropy >= 80:
        strength = "very strong"
    elif entropy >= 60:
        strength = "strong"
    elif entropy >= 40:
        strength = "moderate"
    else:
        strength = "weak"

    return {"strength": strength, "entropy": entropy}

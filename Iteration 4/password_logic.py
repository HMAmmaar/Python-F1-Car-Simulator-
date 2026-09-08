import json
import os
import hashlib

USERS_FILE = 'users.json'


def load_users(path: str = USERS_FILE) -> dict:
    """
    Load the user database from JSON.
    Returns an empty dict if file is missing or invalid.
    """
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, PermissionError):
        return {}


def save_users(users: dict, path: str = USERS_FILE) -> None:
    """
    Save the user database to JSON with pretty formatting.
    """
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


def hash_text(text: str) -> str:
    """
    Hash any text (password or answer) using SHA-256.
    """
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def sign_up_user(username: str,
                 password: str,
                 confirm_password: str,
                 security_question: str,
                 security_answer: str) -> str:
    """
    Register a new user with a security question.
    
    Returns:
      - "user created" if successful,
      - "user exists" if username already taken,
      - "password mismatch" if passwords differ.
    """
    if password != confirm_password:
        return "password mismatch"

    users = load_users()

    if username in users:
        return "user exists"

    users[username] = {
        'password_hash': hash_text(password),
        'sec_question': security_question,
        'sec_answer_hash': hash_text(security_answer)
    }
    save_users(users)
    return "user created"


def validate_credentials(username: str,
                         password: str) -> str:
    """
    Verify a username/password pair.
    
    Returns:
      - "valid" if credentials match,
      - "password incorrect" if hash mismatches,
      - "no such user" otherwise.
    """
    users = load_users()

    if username not in users:
        return "no such user"

    if users[username]['password_hash'] == hash_text(password):
        return "valid"
    else:
        return "password incorrect"


def reset_via_security_question(username: str,
                                provided_answer: str,
                                new_password: str,
                                confirm_password: str) -> str:
    """
    Reset password by answering the security question.
    
    Returns:
      - "password reset successful" on success,
      - "no such user" if user not found,
      - "security answer incorrect" if answer hash mismatches,
      - "password mismatch" if new passwords differ.
    """
    users = load_users()

    if username not in users:
        return "no such user"

    correct_hash = users[username].get('sec_answer_hash')
    if not correct_hash or hash_text(provided_answer) != correct_hash:
        return "security answer incorrect"

    if new_password != confirm_password:
        return "password mismatch"

    users[username]['password_hash'] = hash_text(new_password)
    save_users(users)
    return "password reset successful"

sign_up_user("Admin", "Admin", "Admin", "Admin", "Admin")
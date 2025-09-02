from werkzeug.security import generate_password_hash

def generate_user_hash(password):
    return generate_password_hash(password, method='scrypt')

# Test
password = 'admin123'
hashed_password = generate_user_hash(password)
print(f"Hash généré : {hashed_password}")

# SQL pour insérer
print("\nRequête SQL :")
print(f"INSERT INTO users (username, email, password_hash)")
print(f"VALUES ('admin', 'admin@example.com', '{hashed_password}');")
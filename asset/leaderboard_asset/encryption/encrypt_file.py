import json
from cryptography.fernet import Fernet

# Load key
with open("C:/pythongame/pygame_projects/Wordles/asset/leaderboard_asset/encryption/key.key", "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

# Read and encrypt JSON
with open("C:/pythongame/pygame_projects/Wordles/asset/leaderboard_asset/leaderboard_data.json", "r", encoding="utf8") as file:
    data = file.read()

encrypted_data = fernet.encrypt(data.encode())

# Save encrypted file (overwrite original or new file)
with open("C:/pythongame/pygame_projects/Wordles/asset/leaderboard_asset/leaderboard_data.enc", "wb") as file:
    file.write(encrypted_data)
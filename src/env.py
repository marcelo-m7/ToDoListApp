from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv, set_key

def load_encryption_key():
    load_dotenv()
    key = os.getenv("FERNET_KEY")
    
    if not key:
        print("FERNET_KEY not found in environment variables. Checking .env file...")
        
        if not os.path.exists(".env"):
            print(".env file not found. Generating a new key...")
            key = Fernet.generate_key().decode()
            set_key(".env", "FERNET_KEY", key)
            print(f"New FERNET_KEY generated and saved to .env: {key}")
        else:
            with open(".env", "r") as f:
                for line in f:
                    if line.startswith("FERNET_KEY="):
                        key = line.split("=", 1)[1].strip()
                        break
            
            if not key:
                print("FERNET_KEY not found in .env file. Generating a new key...")
                key = Fernet.generate_key().decode()
                set_key(".env", "FERNET_KEY", key)
                print(f"New FERNET_KEY generated and saved to .env: {key}")
    
    print("Final key:", key)
    return key

load_encryption_key()

if "FERNET_KEY" in os.environ:
    print("FERNET_KEY está definida:", os.environ["FERNET_KEY"])
else:
    print("FERNET_KEY não está definida.")
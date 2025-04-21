import os
import time
import glob
from quantcrypt.sign import Sphincs

drive_path = input("Enter the path to your USB drive: ")
signer = Sphincs(variant="SMALL_SPHINCS")
print("SPHINCS+ initialized.")

print("Monitoring for new hashes from main1.py... Press Ctrl+C to stop.")
try:
    while True:
        hash_files = sorted(glob.glob("hash_*.txt"))
        for file_path in hash_files:
            snapshot_number = int(file_path.split("_")[1].split(".")[0])
            
            with open(file_path, 'r') as f:
                hash_hex = f.read().strip()
            
            unix_time = int(time.time())
            
            hash_bytes = bytes.fromhex(hash_hex)
            message = hash_bytes + str(unix_time).encode()
            signature = signer.sign(message)
            
            output_file = os.path.join(drive_path, f"signed_{snapshot_number}_{unix_time}.txt")
            
            # Save to flash drive
            with open(output_file, 'w') as f:
                f.write(f"Snapshot: {snapshot_number}\n")
                f.write(f"Time: {unix_time}\n")
                f.write(f"Hash: {hash_hex}\n")
                f.write(f"Signature: {signature.hex()}\n")
            
            print(f"Signed hash {snapshot_number} and saved to {output_file}")
            
            # Remove processed file
            os.remove(file_path)
        
        # Wait
        time.sleep(5)
        
except KeyboardInterrupt:
    print("\nProgram stopped.")

import os
import datetime

drive_path = None

def store_hash_on_drive(hash_value, snapshot_number):
    global drive_path
    
    if drive_path is None:
        drive_path = input("Enter the path to your USB drive: ")
    
    if isinstance(hash_value, bytes):
        hash_value = hash_value.hex()
        
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    filename = f"snapshot_{snapshot_number}_{timestamp}.txt"
    
    full_path = os.path.join(drive_path, filename)
    
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    with open(full_path, 'w') as f:
        f.write(f"Snapshot: {snapshot_number}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Hash: {hash_value}\n")
    
    print(f"Hash for snapshot {snapshot_number} stored at {full_path}")
    return True

def retrieve_hashes_from_drive():
    global drive_path
    
    if drive_path is None:
        drive_path = input("Enter the path to your USB drive: ")
    
    search_path = os.path.join(drive_path, "snapshot_*.txt")
    files = glob.glob(search_path)
    
    if not files:
        print(f"No hash files found at {drive_path}")
        return []
    
    hashes = []
    
    for file_path in files:
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                
                snapshot = None
                timestamp = None
                hash_value = None
                
                for line in lines:
                    if line.startswith("Snapshot:"):
                        snapshot = line.split(":", 1)[1].strip()
                    elif line.startswith("Timestamp:"):
                        timestamp = line.split(":", 1)[1].strip()
                    elif line.startswith("Hash:"):
                        hash_value = line.split(":", 1)[1].strip()
                
                if snapshot and hash_value:
                    hashes.append((int(snapshot), timestamp, hash_value))
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
    
    hashes.sort(key=lambda x: x[0])
  #I have no idea what this does but it does not work without it????????? kinda??????????           DELETE THIS LINE BEFORE SUBMISSION
    return hashes

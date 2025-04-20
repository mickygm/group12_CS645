# We Williams Beaumont, Hunter Forsythe, and McKinley Morris
# declare that We have completed this
# computer code in accordance with the UAB Academic Integrity
# Code and the UAB CS Honor Code. I/We have read the UAB
# Academic Integrity Code and understand that any breach of the
# Code may result in severe penalties.
# Student signature(s)/initials: WAB, MM, HF
# Date: 4/19/2025

import os
from cryptography.hazmat.primitives import hashes
import shutil
import schedule
import time

# Performs SHA-256 hash function
def sha256(data):
    h = hashes.Hash(hashes.SHA256())
    h.update(data)
    return h.finalize()

# Computes a Merkle hash from a list of files
def merkle_tree(leaves):
    #IF FOLDER IS EMPTY, RETURN HASH OF EMPTY STRING
    if not leaves:
        #print("\nEmpty directory.")
        return sha256(b'')
    #HASH ALL LEAVES
    nodes = [sha256(leaf) for leaf in leaves]
    #print("\nList of all node hashes: ", nodes)
    #COMBINE NODES UNTIL ROOT IS REACHED
    while len(nodes) > 1:
        level = 0
        next_level = []
        for i in range(0, len(nodes), 2): #combining hashes of every two nodes
            left = nodes[i]
            #if no right node, copy left node
            right = nodes[i + 1] if i + 1 < len(nodes) else left
            combined = sha256(left + right)
            next_level.append(combined)
        nodes = next_level
        level = level + 1
        #print("\nList of combined hashes for level ", level, nodes)
    #RETURN MERKLE ROOT
    return nodes[0]

# Creates a list of all files in a directory and passes that list to merkle_tree
def merkle_root_from_directory(path):
    leaves = []
    for root, _, files in os.walk(path):
        for f in files:
            try:
                with open(os.path.join(root, f), 'rb') as file:
                    leaves.append(file.read())
            except Exception as e:
                print(f"Error reading {f}: {e}")
    return merkle_tree(leaves)

# Creates a snapshot of the directory and hashes the digest of that directory with the previous snapshot's digest
def merkleSnap(dir, snap):
    global prevHash
    global snapIteration
    shutil.copytree(dir, snap, dirs_exist_ok=True)
    root = merkle_root_from_directory(snap)
    newHash = sha256(prevHash + root)
    prevHash = newHash
    print(f"\nHash of Snapshot {snapIteration}:", newHash.hex())
    snapIteration = snapIteration + 1

# Initializes first hash value to all 0s
prevHash = b"\x00" * 256

# Initializes the snapshot number
snapIteration = 1

# Main function
if __name__ == "__main__":
    # Gets information from the user on how they want to use the program
    dirName = input("\nEnter directory to hash: ")
    snapName = input("\nEnter name for snapshot directory: ")
    freq = int(input("\nChoose how often to take a snapshot:\n1. Every 30 seconds\n2. Every minute\n3. Every hour\n4. Every 24 hours\n"))
    goodInput = False
    while not goodInput: 
        if 1 <= freq <= 4: 
            goodInput = True
        else:
            key = int(input("\nInvalid selection. Please enter a valid selection: "))
    # Schedules the program to run based on the user's selection
    if freq == 1:
        schedule.every(30).seconds.do(merkleSnap, dir = dirName, snap = snapName)
    elif freq == 2:
        schedule.every().minute.do(merkleSnap, dir = dirName, snap = snapName)
    elif freq == 3:
        schedule.every().hour.do(merkleSnap, dir = dirName, snap = snapName)
    else:
        schedule.every(24).hours.do(merkleSnap, dir = dirName, snap = snapName)
    while True:
        schedule.run_pending()
        time.sleep(1)
    
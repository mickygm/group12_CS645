import os
from cryptography.hazmat.primitives import hashes

#SHA-256 fx
def sha256(data):
    h = hashes.Hash(hashes.SHA256())
    h.update(data)
    return h.finalize()

def merkle_tree(leaves):
    #IF FOLDER IS EMPTY, RETURN HASH OF EMPTY STRING
    if not leaves:
        return sha256(b'')
    #HASH ALL LEAVES
    nodes = [sha256(leaf) for leaf in leaves]
    #COMBINE NODES UNTIL ROOT IS REACHED
    while len(nodes) > 1:
        next_level = []
        for i in range(0, len(nodes), 2): #combining hashes of every two nodes
            left = nodes[i]
            #if no right node, copy left node
            right = nodes[i + 1] if i + 1 < len(nodes) else left
            combined = sha256(left + right)
            next_level.append(combined)
        nodes = next_level

    # The last remaining node is the Merkle root
    return nodes[0]

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

if __name__ == "__main__":
    root = merkle_root_from_directory("group12_GA3/Test Root")
    print("Merkle Root:", root.hex())
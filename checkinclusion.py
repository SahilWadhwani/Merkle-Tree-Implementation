import sys
import json
import hashlib

def hash_data(data):
    """Hashes a given string using SHA-256."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def load_merkle_tree(filename='merkle.tree'):
    """Loads the Merkle tree from a file."""
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("Error: Merkle tree file not found. Run buildmtree.py first.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in merkle tree file.")
        sys.exit(1)

def get_proof(merkle_tree, target_hash):
    """Generates a proof of inclusion for the target hash."""
    tree_levels = merkle_tree['tree_structure']
    proof = []
    
    # Locate the target hash in the leaf level (Level 0)
    level = 0
    nodes = tree_levels[f'Level {level}']
    index = next((i for i, node in enumerate(nodes) if node['hash'] == target_hash), -1)
    
    if index == -1:
        return None  # Target not found in Merkle tree
    
    # Traverse up the tree collecting proof nodes
    for level in range(len(tree_levels) - 1):
        nodes = tree_levels[f'Level {level}']
        
        # Find sibling node
        if index % 2 == 0:  # Even index (left child)
            sibling_index = index + 1 if index + 1 < len(nodes) else None
        else:  # Odd index (right child)
            sibling_index = index - 1
        
        if sibling_index is not None:
            proof.append(nodes[sibling_index]['hash'])
        
        # Move to the next level
        index //= 2  # Parent index
    
    return proof

def check_inclusion(target_string, filename='merkle.tree'):
    """Checks if a given string is included in the Merkle tree."""
    merkle_tree = load_merkle_tree(filename)
    target_hash = hash_data(target_string)
    
    proof = get_proof(merkle_tree, target_hash)
    if proof is None:
        print("no")
    else:
        print(f"yes {proof}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python checkinclusion.py <string>")
        sys.exit(1)
    
    target_string = sys.argv[1]
    check_inclusion(target_string)

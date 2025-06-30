import sys
import json
import hashlib
from buildmtree import MerkleTree

def hash_data(data):
    """Hashes a given string using SHA-256."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def calc_merkle_root(leaves):
    """Builds a Merkle root from a list of leaf hashes."""
    if not leaves:
        return None
    current = leaves[:]
    while len(current) > 1:
        temp = []
        for i in range(0, len(current), 2):
            left = current[i]
            right = current[i + 1] if i + 1 < len(current) else left
            temp.append(hash_data(left + right))
        current = temp
    return current[0]


def consistency_proof(m_leaves, n_leaves):
    """Generates a minimal consistency proof following RFC 6962 Section 2.1.3."""
    proof = []

    def calc_subtree_hash(leaves):
        """Calculate Merkle root of a subtree."""
        if len(leaves) == 1:
            return leaves[0]

        current = leaves[:]
        while len(current) > 1:
            next_level = []
            for i in range(0, len(current), 2):
                left = current[i]
                right = current[i + 1] if i + 1 < len(current) else current[i]
                next_level.append(hash_data(left + right))
            current = next_level
        return current[0]

    m = len(m_leaves)
    n = len(n_leaves)

    if m == n:
        # Same tree, no proof needed
        return []

    # Add the hash of the original tree (m_leaves)
    proof.append(calc_subtree_hash(m_leaves))

    # Add the subtree hash of the added data (suffix of new leaves)
    suffix = n_leaves[m:]
    if suffix:
        proof.append(calc_subtree_hash(suffix))

    return proof


def check_consistency(old_tree, new_tree):
    """Checks if the old tree is a consistent prefix of the new tree."""
    old_root = old_tree['merkle_root']
    new_root = new_tree['merkle_root']

    old_leaves = [node['hash'] for node in old_tree['tree_structure']['Level 0']]
    new_leaves = [node['hash'] for node in new_tree['tree_structure']['Level 0']]

    m = len(old_leaves)
    n = len(new_leaves)

    if old_leaves != new_leaves[:m]:
        return "no"

    proof = consistency_proof(old_leaves, new_leaves)

    # Always include old root at the beginning
    if not proof or proof[0] != old_root:
        proof.insert(0, old_root)

    # Always include new root at the end
    if proof[-1] != new_root:
        proof.append(new_root)

    return f"yes {proof}"


def load_merkle_tree(filename):
    """Loads a Merkle tree from a file."""
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Failed to load {filename}: {e}")
        sys.exit(1)


def main():
    """Main method to parse command-line arguments and check consistency."""
    if len(sys.argv) < 4 or "--" not in sys.argv:
        print("Usage: python checkconsistency.py <old list> -- <new list>")
        print("Example: python checkconsistency.py alice bob carol -- alice bob carol david eve")
        sys.exit(1)

    split_index = sys.argv.index("--")
    old_list = sys.argv[1:split_index]
    new_list = sys.argv[split_index + 1:]

    if not old_list or not new_list:
        print("Error: Both old and new lists must be provided.")
        sys.exit(1)

    # Generate Merkle trees for old and new lists
    MerkleTree(old_list).save_to_file("old_merkle.tree")
    MerkleTree(new_list).save_to_file("new_merkle.tree")

    # Load the Merkle tree structures
    old_tree = load_merkle_tree("old_merkle.tree")
    new_tree = load_merkle_tree("new_merkle.tree")

    # Check consistency
    result = check_consistency(old_tree, new_tree)
    print(result)


if __name__ == "__main__":
    main()

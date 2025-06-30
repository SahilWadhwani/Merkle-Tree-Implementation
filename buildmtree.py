import sys
import json
import hashlib

class MerkleTree:
    def __init__(self, data_list):
        self.leaves = [(data, self.hash_data(data)) for data in data_list]
        self.tree = []
        self.root = self.build_tree([leaf[1] for leaf in self.leaves])
    
    def hash_data(self, data):
        """Hashes a given string using SHA-256."""
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    
    def build_tree(self, leaves):
        """Builds the Merkle Tree and returns the Merkle Root."""
        tree_levels = [leaves]
        while len(tree_levels[-1]) > 1:
            current_level = tree_levels[-1]
            new_level = []
            for i in range(0, len(current_level), 2):
                if i + 1 < len(current_level):
                    new_hash = self.hash_data(current_level[i] + current_level[i+1])
                else: # If odd number of elements
                    
                    new_hash = self.hash_data(current_level[i] + current_level[i])
                new_level.append(new_hash)
            tree_levels.append(new_level)
        
        self.tree = tree_levels  # Store full tree structure
        return tree_levels[-1][0] if tree_levels else None
    
    
    def get_tree_structure(self):
        """Returns the Merkle Tree in a more readable structured format."""
        tree_structure = {}
        for level, nodes in enumerate(self.tree):
            formatted_nodes = []
            for i, node in enumerate(nodes):
                if level == 0:  # At the leaf level, show original data
                    formatted_nodes.append({
                        "hash": node,
                        "original_data": self.leaves[i][0] if i < len(self.leaves) else "None"
                    })
                else:
                    formatted_nodes.append({"hash": node})
            tree_structure[f'Level {level}'] = formatted_nodes
        return tree_structure

    
            
    def save_to_file(self, filename='merkle.tree'):
        """Saves the Merkle Tree structure to a file in JSON format."""
        with open(filename, 'w') as file:
            json.dump({"merkle_root": self.root, "tree_structure": self.get_tree_structure()}, file, indent=4)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./buildmtree.py alice bob carol david")
        sys.exit(1)
    
    try:
        data_list = sys.argv[1:]
        if not isinstance(data_list, list):
            raise ValueError("Input must be a JSON list of strings")
    except Exception as e:
        print("Error parsing input:", e)
        sys.exit(1)
    
    
    
    merkle_tree = MerkleTree(data_list)
    merkle_tree.save_to_file()
    
    print("Merkle Tree successfully built and saved to merkle.tree")

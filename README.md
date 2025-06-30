# Merkle Tree Implementation


##  Overview

This project implements **Merkle Trees** in Python, including proofs of **inclusion** and **consistency**. Merkle Trees are crucial in cryptography and blockchain for efficient and secure data verification.

-----

##  Files

  - `buildmtree.py`: Constructs a Merkle Tree and outputs `merkle.tree` in JSON format.
  - `checkinclusion.py`: Proves that an element exists in the Merkle Tree.
  - `checkconsistency.py`: Verifies that a new Merkle Tree version includes all elements of the old version, in the same order.
  - `merkle.tree`: JSON file representing the constructed Merkle Tree.
  - `old_merkle.tree` / `new_merkle.tree`: Sample files for consistency proof demonstration.

-----

## 🛠 Features

  - Uses **SHA-256** for all node hashes.
  - Handles an **odd number of leaves** by duplicating the last element.
  - Outputs trees in user-friendly **JSON structures**.
  - Provides **minimal, easy-to-verify** inclusion and consistency proofs.
  - Features a **command-line interface** for easy operation.

-----

##  Usage

### 1\. Build a Merkle Tree

Builds a tree from a list of strings and outputs `merkle.tree` in JSON.

```bash
python buildmtree.py alice bob carol david
```

### 2\. Proof of Inclusion

Checks if a given string is included in the tree and provides the inclusion proof.

```bash
python checkinclusion.py bob
```

### 3\. Proof of Consistency

Checks if a new Merkle Tree is a valid extension (prefix) of an old one.

```bash
python checkconsistency.py alice bob carol david -- alice bob carol david eve fred
```

-----

## Program Design

### 1\. `buildmtree.py` - Constructing the Merkle Tree

Accepts a list of strings as input. It computes the **SHA-256** hash of each string, builds a binary Merkle Tree structure, and handles odd elements by duplicating the last one. Finally, it saves the tree in `merkle.tree` as a JSON file.

**Example:**

```bash
python buildmtree.py alice bob carol david
# Output: merkle.tree (JSON format)
```

### 2\. `checkinclusion.py` - Proof of Inclusion

This script loads the Merkle Tree from `merkle.tree`, hashes the given string, and finds it in the tree. It then outputs the **minimal set of hashes** needed to verify the element’s presence.

**Example:**

```bash
python checkinclusion.py bob
# Output: Minimal proof hashes for "bob"
```

### 3\. `checkconsistency.py` - Proof of Consistency

This script loads two tree versions (`old_merkle.tree` and `new_merkle.tree`) and verifies that the old tree is a prefix of the new one. It outputs the required intermediate hashes for the proof.

**Example:**

```bash
python checkconsistency.py alice bob carol david -- alice bob carol david eve fred
# Output: Consistency proof hashes
```

-----

## Merkle Tree Structure

### Example: 4 Elements

```
        Merkle Root
        /         \
    Hash1        Hash2
   /    \       /    \
HashA  HashB  HashC  HashD
  |      |      |      |
alice   bob   carol  david
```

### Extended Example: Adding Eve and Fred

```
             New Merkle Root
           /                \
    Old Root              Hash3
   /      \              /     \
Hash1   Hash2       Hash5    Hash6 (dup)
 / \    /  \         / \      / \
A   B  C   D       E   F    F   F
alice bob carol david eve fred fred
```

-----

##  Example Output Files

  - `merkle.tree`: Contains the full Merkle Tree in JSON.
  - `old_merkle.tree`: The previous version for consistency checking.
  - `new_merkle.tree`: The updated version for consistency checking.

-----

## Screenshots

<img width="889" alt="image" src="https://github.com/user-attachments/assets/e0cee596-b301-4260-9c73-02a0299e3970" />


-----

##  Conclusion

  - Implements Merkle Tree construction with **SHA-256**.
  - Provides efficient, minimal proofs for **inclusion and consistency**.
  - The output is **well-structured** and **human-readable** (JSON).
  - Ideal for learning about cryptography, blockchains, and secure data structures.

-----

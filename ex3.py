## INFORMATION THEORY AND INFERENCE 
## ASSIGNMENT 3

# Gabriel Amorosetti
# Matricola N. 2107530

"""
Consider the given text (text_for_ex3.txt). 
Consider each character (including spaces, punctuation and newline) as independently sampled from a space of characters A_X with a given probability. 
Write a program to find a Huffman code for the characters; display the code and compute the code length. 
Encode the text (convert it into a binary string) and decode it. 
"""

#######################################################################################

import heapq                      # to efficiently extract the two characters with the smallest frequencies
from collections import Counter   # to count the frequency of each character


#####################

# We assume the text file 'text_for_ex3.txt' is located in the same directory as this .py code
with open("text_for_ex3.txt", "r", encoding="utf-8") as file :
    original_text = file.read()

# computing the frequency of each character
count = Counter(original_text)               # return a dict char : freq



# with the heap structure we create the priority pile of the charaters (associated with their respective frequencies)

pile = [] # list used as priority queue, respecting the order made by heap (where freq is the priority key)
id = 0    # we need to associated a unique id for each char (in case of equality of freq)

for char, freq in count.items() :

    heapq.heappush(pile, (freq, id, char))
    id += 1



# Huffman tree construction : 

if len(pile) == 1 :             # we consider the case where the text is composed of only one character (can appear multiple times but is the same, we can't build a tree)
    
    unique = pile[0][2]
    root = unique
    codes = {unique: "0"}

                                
else :                          # otherwise

    while len(pile) > 1 :       # as long as there's 2 nodes in the pile

        # we extract the two nodes with smallest frequencies
        freq1, id1, left = heapq.heappop(pile)
        freq2, id2, right = heapq.heappop(pile)

        # creation of in internal node (tuple)
        internal_node = (left, right)
        # we reinject this node with the total freq 
        heapq.heappush(pile, (freq1 + freq2, id, internal_node))
        id += 1
    
    # at the end only one element left in the pile, the root of the tree
    root = pile[0][2]



    # now we generate the codes based on the tree we built, by building a recursive function
    codes = {}

    def gen_code(node, prefix = "") : 
        # the function goes through the tree

        if isinstance(node, str):
            # if node is a leaf (character, is a str)
            codes[node] = prefix if prefix else "0" 

        else:
            # otherwise we keep going down the tree
            # internal node : tuple (left, right)
            gen_code(node[0], prefix + "0")
            gen_code(node[1], prefix + "1")

    gen_code(root)


#####################

# Huffman table 

print("Character --- Frequency --- Length --- Code")

for ch in sorted(codes.keys(), key = lambda c: (-count[c], c)) : # to print in order of decreasing frequency
    print(repr(ch), count[ch], len(codes[ch]), codes[ch])        # repr() to show characters like '\n'


#####################


# we encode the entire original text (joining the codes for each char in the original text to create the encoded text)
coded_text = "".join(codes[ch] for ch in original_text)


#####################

# decoding back to the original text :

if isinstance(root, str):                       # we consider the case where the text is composed of only one character
    decoded_text = root * len(original_text)

else:                                           # otherwise we go through the tree
    result = []
    n = root
    for bit in coded_text:
        if bit == "0":
            n = n[0]
        else:
            n = n[1]
        
        if isinstance(n, str):
            # at this point we reached a leaf
            result.append(n)
            n = root  # so we store the decoded code and go back to the root
    
    decoded_text = "".join(result)


#####################


print("\n")
print("Total length (bits) : ", len(coded_text))
print("Average lenght by character : ", len(coded_text) / len(original_text))


# Verifying that we decoded correctly
print("Correct decoding ? : ", decoded_text == original_text)
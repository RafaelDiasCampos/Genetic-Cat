import os
import cloudpickle
import argparse

from utils.Mask import Mask, MaskCharset
from utils.WordlistTree import WordlistTree

parser = argparse.ArgumentParser(description="Create a wordlist tree from a folder of wordlists.")
parser.add_argument("-i", "--input", help="The input wordlist folder.")
parser.add_argument("-o", "--output", help="The output wordlist folder.")
parser.add_argument("-d", "--depth", help="The maximum depth of the tree.", type=int, default=4)
args = parser.parse_args()

input_folder = args.input
output_folder = args.output
max_depth = args.depth
    
for filename in os.listdir(input_folder):
    if not filename.endswith(".txt"):
        continue
    
    depth = int(filename.split(".txt")[0])
    
    if depth > max_depth:
        continue
    
    print(f"Processing {filename}")
    
    with open(os.path.join(input_folder, filename), "r") as f:
        wordlist = f.read().splitlines()
        
    tree = WordlistTree(wordlist)
    
    with open(os.path.join(output_folder, filename.replace(".txt", ".pkl")), "wb") as f:
        cloudpickle.dump(tree, f)
        
    print(f"Processed {filename}")
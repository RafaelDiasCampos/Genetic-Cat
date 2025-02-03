import os
import re
import json
import argparse

parser = argparse.ArgumentParser(description="Sort wordlists in a folder and remove the duplicate elements.")
parser.add_argument("-i", "--input", help="The input wordlist folder.")
args = parser.parse_args()

wordlist_folder = args.input

print(f"Sorting wordlists in {wordlist_folder}...")

def sort_wordlist(lst):
    charsets = {
        "lowercase": "abcdefghijklmnopqrstuvwxyz",
        "uppercase": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "digits": "0123456789",
        "special": r" !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    }

    # Create a lookup table for sorting priority
    priority = {}
    for index, group in enumerate(charsets.values()):
        for char in group:
            priority[char] = index

    def sorting_key(word):
        return [priority.get(char, float('inf')) for char in word]

    lst.sort(key=sorting_key)

stats = {
    "total": 0,
    "lengths": {}
}

def sort_func(s: str) -> str:
    return s.lower()

for filename in os.listdir(wordlist_folder):
    if not filename.endswith(".txt"):
        continue
    
    print(f"Processing {filename}...")
    
    with open(os.path.join(wordlist_folder, filename), "r", encoding="utf8") as f:
        print(f"  Reading {filename}...")
        lines = f.readlines()
        
        print(f"  Removing duplicates from {filename}...")
        lines = list(set(lines))
        
        print(f"  Sorting {filename}...")
        sort_wordlist(lines)
        
        with open(os.path.join(wordlist_folder, filename), "w", encoding="utf8") as o:
            o.writelines(lines)
            
        line_len = len(lines[0].strip())
        line_count = len(lines)
                    
        stats["total"] += line_count
        stats["lengths"][line_len] = line_count
        
        
print(f"Total passwords: {stats['total']}")
print("Lengths:")
for length, count in stats["lengths"].items():
    print(f"  {length}: {count}")
    
with open(os.path.join(wordlist_folder, "stats.json"), "r") as f:  
    stats_original = json.load(f)
    
with open(os.path.join(wordlist_folder, "stats.json"), "w") as f:
    stats_dump = {
        "original": stats_original,
        "sorted": {
            "total": stats["total"],
            "lengths": stats["lengths"]
        }
    }
    json.dump(stats_dump, f, indent=2)
import os
import re
import json
import argparse

parser = argparse.ArgumentParser(description="Split a wordlist into multiple files based on password length.")
parser.add_argument("-i", "--input", help="The input wordlist file.")
parser.add_argument("-o", "--output", help="The output folder.")
args = parser.parse_args()

original_wordlist = args.input
output_folder = args.output

print(f"Splitting {original_wordlist} into {output_folder}...")

valid_regex = re.compile(r"^[a-zA-Z0-9 !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~]+$")

stats = {
    "total": 0,
    "lengths": {}
}

with open(original_wordlist, "r", encoding="utf8", errors="replace") as f:
    for line in f:
        line = line.strip()        
        line_length = len(line)
        
        if not valid_regex.match(line):
            continue
        
        stats["total"] += 1
        
        if line_length not in stats["lengths"]:
            output_file = os.path.join(output_folder, f"{line_length}.txt")
            o = open(output_file, "w", encoding="utf8")
            
            stats["lengths"][line_length] = {
                "count": 0,
                "file": o,
            }      
        
        stats["lengths"][line_length]["count"] += 1
        stats["lengths"][line_length]["file"].write(f"{line}\n")
        
print(f"Total passwords: {stats['total']}")
print("Lengths:")
for length, stat in stats["lengths"].items():
    stat["file"].close()
    print(f"  {length}: {stat["count"]}")
    
with open(os.path.join(output_folder, "stats.json"), "w") as f:  
    stats_dump = {
        "total": stats["total"],
        "lengths": {length: stat["count"] for length, stat in stats["lengths"].items()}
    }
    
    json.dump(stats_dump, f, indent=2)
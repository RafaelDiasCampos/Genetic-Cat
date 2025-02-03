from copy import deepcopy
from abc import abstractmethod

from .Mask import Mask, MaskCharset

class WordlistNode:
    @abstractmethod    
    def get_matches(self, mask: Mask) -> int:
        pass
    
    @abstractmethod
    def get_matching_nodes(self, mask: Mask) -> list["WordlistNode"]:
        pass
    
class WordlistNodeInternal(WordlistNode):
    def __init__(self, wordlist: list[str], start: int, end: int, partial_mask: Mask):
        self.partial_mask = partial_mask
        self.depth = len(partial_mask.mask)
        
        self.children = {}
        
        self.build_tree(wordlist, start, end)
    
    def build_tree(self, wordlist: list[str], start: int, end: int):
        for maskCharset in list(MaskCharset)[:-1]:
            # Binary search for the first word that doesn't match the mask
            left = start
            right = end
            
            partial_mask = Mask(self.partial_mask.mask + [maskCharset])
            
            while left < right:
                mid = (left + right) // 2
                if partial_mask.soft_match(wordlist[mid]):
                    left = mid + 1
                else:
                    right = mid
            
            # No words match the mask -> Create a leaf node
            if left == start:
                self.children[maskCharset] = WordlistNodeLeaf(0)
            
            # Mask matches the previous word perfectly -> Create a leaf node
            elif partial_mask.match(wordlist[left - 1].strip()):
                self.children[maskCharset] = WordlistNodeLeaf(left - start)
            
            # Mask is only a partial match -> Create a new internal node
            else:            
                self.children[maskCharset] = WordlistNodeInternal(wordlist, start, left, Mask(self.partial_mask.mask + [maskCharset]))   
            
            start = left
        
    def get_matches(self, mask: Mask) -> int:
        if len(mask.mask) < self.depth:
            raise ValueError(f"Mask length must be greater than or equal to {self.depth}")
        
        if mask.mask[self.depth] in self.children:
            return self.children[mask.mask[self.depth]].get_matches(mask)
        
        elif mask.mask[self.depth] == MaskCharset.ALL:
            return sum([child.get_matches(mask) for child in self.children.values()])
        
        else:
            raise ValueError(f"Invalid mask character at position {self.depth}")
        
    def get_matching_nodes(self, mask: Mask) -> list[WordlistNode]:
        if len(mask.mask) < self.depth:
            raise ValueError(f"Mask length must be greater than or equal to {self.depth}")
        
        if mask.mask[self.depth] in self.children:
            return self.children[mask.mask[self.depth]].get_matching_nodes(mask)
        
        elif mask.mask[self.depth] == MaskCharset.ALL:
            nodes = []
            for child in self.children.values():
                nodes.extend(child.get_matching_nodes(mask))
                
            return nodes
        
        else:
            raise ValueError(f"Invalid mask character at position {self.depth}")
    
class WordlistNodeLeaf(WordlistNode):
    def __init__(self, count: int):
        self.count = count
        
    def get_matches(self, mask: Mask) -> int:
        matches = self.count            
        return matches
    
    def get_matching_nodes(self, mask: Mask) -> list[WordlistNode]:
        return [self]
    
class WordlistTree:
    def __init__(self, wordlist: list[str]):
        self.root = WordlistNodeInternal(wordlist, 0, len(wordlist), Mask([]))
        self.wordlist_len = len(wordlist)
        self.word_len = len(wordlist[0].strip())
        
    def get_matches(self, mask: Mask) -> int:
        if len(mask.mask) != self.word_len:
            raise ValueError(f"Mask length must be equal to word length ({self.word_len})")
        return self.root.get_matches(mask)
    
    def get_combined_matches(self, masks: list[Mask]) -> int:        
        matching_nodes = []
        
        for mask in masks:
            matching_nodes.extend(self.root.get_matching_nodes(mask))
            
        matching_nodes_set = set(matching_nodes)
        
        matches = sum([node.count for node in matching_nodes_set])
        
        return matches
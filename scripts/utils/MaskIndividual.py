import numpy as np
from copy import deepcopy

from .Mask import Mask, MaskCharset
from .WordlistTree import WordlistTree

class MaskIndividual:
    def __init__(self, masks: list[Mask], max_masks: int):
        self.masks = masks
        self.max_masks = max_masks
        
        self.mask_len = len(masks[0].mask)
    
    def get_matches(self, wordlist_tree: WordlistTree) -> int:
        return wordlist_tree.get_combined_matches(self.masks)
    
    @property
    def cost(self) -> int:
        return sum([mask.cost for mask in self.masks])
    
    def __str__(self) -> str:
        return "\n".join([str(mask) for mask in self.masks])
    
    @staticmethod
    def from_string(masks_str: list[str], max_masks: int = None) -> "MaskIndividual":
        masks = [Mask.from_string(mask.strip()) for mask in masks_str]
        
        if max_masks is None:
            max_masks = len(masks)
        
        return MaskIndividual(masks, max_masks)
    
    @staticmethod
    def from_file(filename: str, max_masks: int = None) -> "MaskIndividual":
        with open(filename, "r") as f:
            lines = f.read().splitlines()
            
        return MaskIndividual.from_string(lines, max_masks)
    
    @staticmethod
    def crossover(parent1: "MaskIndividual", parent2: "MaskIndividual", n_children: int = 2) -> list["MaskIndividual"]:
        masks = parent1.masks + parent2.masks
        
        children = []
        
        for _ in range(n_children):
            # Randomly select the number of masks to keep
            # Using a normal distribution centered around the average number of masks
            n_selected_masks = np.random.normal(loc=len(masks)/2, scale=len(masks)/6)
            n_selected_masks = np.round(n_selected_masks).astype(int)
            n_selected_masks = np.clip(n_selected_masks, 1, parent1.max_masks)
            n_selected_masks = min(n_selected_masks, len(masks))
            
            selected_masks = np.random.choice(masks, n_selected_masks, replace=False).tolist()
            
            children.append(MaskIndividual(selected_masks, parent1.max_masks))
        
        return children
    
    @staticmethod
    def mutate(individual: "MaskIndividual") -> "MaskIndividual":
        new_individual = deepcopy(individual)
        
        # If the number of masks is less than the maximum, add a new mask with a 1/3 probability
        if len(new_individual.masks) < new_individual.max_masks:
            if np.random.rand() < 1/3:
                new_mask_list = np.random.choice(list(MaskCharset), new_individual.mask_len, replace=True).tolist()
                new_mask = Mask(new_mask_list)
                new_individual.masks.append(new_mask)
                
                return new_individual
        
        # If the number of masks is greater than 2, remove a random mask with a 1/2 probability
        if len(new_individual.masks) > 2:
            if np.random.rand() < 1/2:
                new_individual.masks.pop(np.random.randint(0, len(new_individual.masks)))
                
                return new_individual
            
        # Otherwise, mutate an existing mask
        mask_index = np.random.randint(0, len(new_individual.masks))
        mask_index_index = np.random.randint(0, new_individual.mask_len)
        
        new_individual.masks[mask_index].mask[mask_index_index] = np.random.choice(list(MaskCharset))
        
        return new_individual
    
    @staticmethod
    def generate_random(max_masks: int, mask_len: int) -> "MaskIndividual":
        n_masks = np.random.randint(1, max_masks + 1)
        masks = [Mask(np.random.choice(list(MaskCharset), mask_len, replace=True)) for _ in range(n_masks)]
        
        return MaskIndividual(masks, max_masks)
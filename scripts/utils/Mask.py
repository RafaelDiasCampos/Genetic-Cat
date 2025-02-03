from enum import Enum

class MaskCharset(Enum):
    LOWERCASE = 1
    UPPERCASE = 2
    DIGIT = 3
    SPECIAL = 4
    ALL = 5
    
    def __new__(cls, value):
        obj = object.__new__(cls)
        obj._value_ = value

        charsets = {
            1: ("abcdefghijklmnopqrstuvwxyz", "?l"),
            2: ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "?u"),
            3: ("0123456789", "?d"),
            4: (r" !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~", "?s")
        }
        
        charsets[5] = ("".join([v[0] for k, v in charsets.items()]), "?a")

        obj.charset, obj.str = charsets[value]

        return obj
    
    @property
    def cost(self) -> int:        
        return len(self.charset)
        
    def match(self, c: str) -> bool:
        return c in self.charset
        
    @classmethod
    def from_str(cls, s: str) -> "MaskCharset":
        for member in cls:
            if member.str == s:
                return member
        raise ValueError(f"'{s}' is not a valid MaskCharset string. Valid options are: {', '.join([m.str for m in cls])}")

    def __str__(self) -> str:
        return self.str
        
class Mask:
    def __init__(self, mask: list[MaskCharset]):
        self.mask = mask
        
    @property
    def cost(self) -> int:
        cost = 1
        for c in self.mask:
            cost *= c.cost
            
        return cost
    
    def soft_match(self, password: str) -> bool:
        return all([m.match(c) for c, m in zip(password, self.mask)])
    
    def match(self, password: str) -> bool:
        return len(password) == len(self.mask) and self.soft_match(password)
    
    @classmethod
    def from_str(cls, s: str) -> "Mask":
        mask = []
        for i in range(0, len(s), 2):
            mask.append(MaskCharset.from_str(s[i:i+2]))
        return cls(mask)
    
    def __str__(self) -> str:
        return "".join([str(m) for m in self.mask])
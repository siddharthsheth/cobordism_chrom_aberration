from collections import namedtuple
from segment import ChromSegment

ChromTransformation = namedtuple('ChromTransformation', ['forward', 'symbol', 'backward'])

# class ChromTransformation:
#     def __init__(self, transform, symbol):
#         self.transform = transform
#         self.symbol = symbol

def identity(s):
    return ChromSegment([c for c in s.chromatins])

def twist(s):
    return ChromSegment([c.reverse() for c in s.chromatins])

def braid(s, other):
    return ChromSegment([c for c in other.chromatins]), ChromSegment([c for c in s.chromatins])

def split(s, i=1):
    # Should raise TypeError if split does not work properly
    return None if i>len(s.chromatins) \
                   else ChromSegment([c for c in s.chromatins[:i]]), ChromSegment([c for c in s.chromatins[i:]])

def merge(s, other):
    return ChromSegment([c for c in s.chromatins].extend([c for c in other.chromatins]))

def death(s):
    pass

def birth():
    pass

chrom_transforms = {'I': identity, 'T': twist, 'W': braid, 'P': merge, 'C': split, 'D': death, 'B':birth}

IdentityTransform = ChromTransformation(identity, 'I')
TwistTransform = ChromTransformation(twist, 'T')
BraidTransform = ChromTransformation(braid, 'W')
PantTransform = ChromTransformation(merge, 'P')
CopantTransform = ChromTransformation(split, 'C')
DeathTransform = ChromTransformation(death, 'D')
BirthTransform = ChromTransformation(birth, 'B')
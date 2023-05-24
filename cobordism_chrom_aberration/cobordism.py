from segment import ChromSegment

def identity(s):
    pass
    # return ChromSegment([c for c in s.chromatins])

def twist(s):
    s.chromatins = [c.reverse() for c in reversed(s.chromatins)]
    # return ChromSegment([c.reverse() for c in reversed(s.chromatins)])

def braid(s, other):
    temp = s
    s = other
    other = temp
    # return ChromSegment([c for c in other.chromatins]), ChromSegment([c for c in s.chromatins])

def split(s, i=1):
    # Should raise ValueError if i is too big to split
    if i > len(s.chromatins):
        raise ValueError()
    else:
        new_segment = ChromSegment(s.chromatins[i:])
        s.chromatins = s.chromatins[:i]
        return new_segment

    # return None if i>len(s.chromatins) \
                #    else ChromSegment([c for c in s.chromatins[:i]]), ChromSegment([c for c in s.chromatins[i:]])

def merge(s, other):
    return ChromSegment([c for c in s.chromatins].extend([c for c in other.chromatins]))

def death(s):
    pass

def birth():
    pass

elementary_cobordisms = {'I': identity, 'T': twist, 'W': braid, 'P': merge, 'C': split, 'D': death, 'B':birth}

class Cobordism:
    def __init__(self, steps, initial, final):
        self.initial = initial
        self.final = final
        self.cob = [steps[0]]
        # check if first step can be applied to initial
        
        # check if each step composes with the next

        # check if the last step can produce final

    def composition(self, other):
        pass

    @staticmethod
    def check_configuration_compatibility(step, configuration):
        j = 0
        for i in range(len(step)):
            if j == len(configuration):
                return False
            if step[i] in {'I', 'T', 'D', 'C'}:
                # move to next segment of configuration
                pass
            elif step[i] in {'W', 'P'}:
                # jump two segments in configuration
                pass
            elif step[i] == 'B':
                # do not know what to do
                pass
            else:
                raise ValueError()
            
        
    def check_composability(self, configuration):
        pass

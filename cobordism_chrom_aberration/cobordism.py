from segment import ChromSegment

def identity(segment):
    new_segment = ChromSegment([c for c in segment.chromatins], labeled=segment.labeled, prev_segment=segment)
    segment.next_segment = new_segment
    return new_segment
    # return ChromSegment([c for c in s.chromatins])

def twist(segment):
    new_segment = ChromSegment([c.reverse() for c in reversed(segment.chromatins)], labeled=segment.labeled, prev_segment=segment)
    segment.next_segment = new_segment
    return new_segment

def braid(left_segment, right_segment):
    new_left_segment = ChromSegment([c for c in right_segment.chromatins], labeled=right_segment.labeled, prev_segment=right_segment)
    new_right_segment = ChromSegment([c for c in left_segment.chromatins], labeled=left_segment.labeled, prev_segment=left_segment)
    left_segment.next_segment = new_right_segment
    right_segment.next_segment = new_left_segment
    return new_left_segment, new_right_segment

def split(s, i=1):
    # Should raise Error if i is too big to split
    if s.labeled is True:
        if i > len(s.chromatins):
            raise ValueError()
        else:
            left_segment = ChromSegment([c for c in s.chromatins[:i]], prev_segment=s)
            right_segment = ChromSegment(s.chromatins[i:], prev_segment=s)
            s.next = left_segment
            return left_segment, right_segment
    else:
        pass

    # return None if i>len(s.chromatins) \
                #    else ChromSegment([c for c in s.chromatins[:i]]), ChromSegment([c for c in s.chromatins[i:]])

def merge(s, other):
    s.chromatins.extend(other.chromatins)
    # return ChromSegment([c for c in s.chromatins].extend([c for c in other.chromatins]))

def death(s):
    pass

def birth():
    pass

elementary_forward_cobordisms = {'I': identity, 'T': twist, 'W': braid, 'P': merge, 'C': split, 'D': death, 'B': birth}
elementary_reverse_cobordisms = {'I': identity, 'T': twist, 'W': braid, 'P': split, 'C': merge, 'D': birth, 'B': death}

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

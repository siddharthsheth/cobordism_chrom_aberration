from collections import Counter

class Label:
    def __init__(self, name:str, telomere:bool=False):
        self.name = name
        self.telomere = telomere

    def __hash__(self):
        return hash((self.name, self.telomere))
    
    def __str__(self):
        return f'_{self.name}_' if self.telomere is True else self.name
    
    def __eq__(self,other):
        return True if self.name==other.name else False
    
    @staticmethod
    def from_string(str):
        if str[0] == '_' and str[-1] == '_':
            return Label(str[1:-2], True)
        else:
            return Label(str, False)

class Chromatin:
    def __init__(self, start:Label, end:Label, color:str, centromere:bool=False):
        self.start = start
        self.end = end
        self.color = color
        self.centromere = centromere

    def reverse(self):
        return Chromatin(self.end, self.start, self.color, self.centromere)
    
    def __hash__(self):
        return hash((self.start, self.end, self.color, self.centromere))
    
    def __str__(self):
        return f'{self.start}*{self.color.upper()}*{self.end}' if self.centromere is True else f'{self.start}*{self.color}*{self.end}'
    
    @staticmethod
    def from_string(str):
        start, color, end = str.split('*')
        start = Label.from_string(start)
        end = Label.from_string(end)
        if color.isupper():
            return Chromatin(start, end, color.lower(), True)
        else:
            return Chromatin(start, end, color)

# Chromatin = namedtuple('Chromatin', ['start', 'end', 'color', 'centromere'], defaults=[False])
class Interval:
    def __init__(self, start, end, next_segment=None, prev_segment=None):
        self.labels = [start, end]
        self.next_segment = next_segment
        self.prev_segment = prev_segment
        pass


class ChromSegment:
    def __init__(self, chromatins, next_segment=None, prev_segment=None):
        if isinstance(chromatins, Chromatin):
            self.labeled = False
            self.chromatins = chromatins
        elif hasattr(chromatins, '__iter__'):
            self.labeled = True
            self.chromatins = [c for c in chromatins]
        self.next_segment = next_segment
        self.prev_segment = prev_segment

    @staticmethod
    def from_string(str):
        chromatins = str.split('--')
        return ChromSegment([Chromatin.from_string(c) for c in chromatins]) if len(chromatins) > 1 else ChromSegment(Chromatin())
        
    
    """
    1. telomere end cannot be connected to any free chromatin end in the segment.
    2. there cannot be duplicate centromeres of the same color in the segment.
    3. the start of the first chromatin and end of the last chromatin should be telomeres.????? at least in the terminal configurations
    4. at most 2 telomeres per color.
    5. Labels do not repeat                     ## NOT YET IMPLEMENTED/TESTED
    """
    def is_valid_terminal_segment(self, colors=None, centromeres=None, telomeres=None):
        if colors is None:
            colors = set()
        if centromeres is None:
            centromeres = Counter()
        if telomeres is None:
            telomeres = Counter()
        prev = None
        for c in self.chromatins:
            colors.add(c.color)
            if prev is None:
                if c.start.telomere is False:
                    print(f'{c}: segment start is not telomere')
                    return False
                else:
                    telomeres[c.color] += 1
            else:
                if prev.end.telomere is True:
                    print(f'{prev}: intermediate end is telomere')
                    return False
                if c.start.telomere is True:
                    print(f'{c}: intermediate start is telomere')
                    return False
            if c.centromere is True:
                centromeres[c.color] += 1
            prev = c
        if prev.end.telomere is False:
            print(f'{prev}: segment end is not telomere')
            return False
        else:
            telomeres[prev.color] += 1
        return True
    
    def __str__(self):
        return '--'.join(str(c) for c in self.chromatins)

    def __hash__(self):
        return hash()

    def __iter__(self):
        return iter(self.chromatins)
    
    def __len__(self):
        return len(self.chromatins)
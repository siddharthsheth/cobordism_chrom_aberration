from collections import Counter

class ChromConfiguration:
    def __init__(self, segments):
        self.segments = segments

    """
    1. every ChromSegment is individually valid
    2. there is exactly one centromere per color throughout the ChromConfiguration
    3. there are 2 telomeres per color throughout the ChromConfiguration
    4. Labels are unique                        # NOT YET TESTED/IMPLEMENTED
    """
    def is_valid_terminal_configuration(self):
        colors = set()
        centromeres = Counter()
        telomeres = Counter()
        for s in self.segments:
            if s.is_valid_terminal_segment(colors, centromeres, telomeres) is False:
                return False
        for color in colors:
            if telomeres[color] != 2:
                print(f'{color}: missing/extra telomeres')
                return False
            if centromeres[color] != 1:
                print(f'{color}: missing/extra centromere')
                return False
        return True
    
    def __str__(self):
        return '=='.join(str(s) for s in self.segments)
    
    def __len__(self):
        return len(self.segments)
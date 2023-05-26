from cobordism_chrom_aberration.segment import ChromSegment

class Interval:
    def __init__(self, labels, next_interval=None, prev_interval=None):
        self.labels = tuple(labels)
        self.next_interval = next_interval
        self.prev_interval = prev_interval

def identity(interval):
    new_interval = Interval(interval.labels, 
                            prev_interval=interval
                            )
    interval.next_interval = new_interval
    return (new_interval,)
    # return Interval([c for c in s.chromatins])

def twist(interval):
    new_interval = Interval([c for c in reversed(interval.labels)], 
                            prev_interval=interval)
    interval.next_interval = new_interval
    return (new_interval,)

def braid(left_interval, right_interval):
    new_left_interval = Interval(right_interval.labels, 
                                 prev_interval=right_interval
                                )
    new_right_interval = Interval(left_interval.labels, 
                                  prev_interval=left_interval
                                )
    left_interval.next_interval = new_right_interval
    right_interval.next_interval = new_left_interval
    return new_left_interval, new_right_interval

def copants(interval,  new_right_label=None, new_left_label=None):
    
    if interval.next_interval is not None:
        left_labels, right_labels = interval.next_interval['left'].labels, interval.next_interval['right'].labels
    else:
        left_labels = [interval.labels[0], new_right_label]
        right_labels = [new_left_label, interval.labels[-1]]

    new_left_interval = Interval(left_labels, 
                                 prev_interval=interval
                                )
    new_right_interval = Interval(right_labels, 
                                  prev_interval=interval
                                )
    interval.next_interval = {'left': new_left_interval, 'right': new_right_interval}
    return new_left_interval, new_right_interval
    # return None if i>len(s.chromatins) \
                #    else ChromSegment([c for c in s.chromatins[:i]]), ChromSegment([c for c in s.chromatins[i:]])

def pants(left_interval, right_interval):
    new_interval = Interval(left_interval.labels + right_interval.labels, 
                            prev_interval={'left':left_interval, 'right': right_interval}
                        )
    left_interval.next_interval = new_interval
    right_interval.next_interval = new_interval
    return (new_interval,)
    # return ChromSegment([c for c in s.chromatins].extend([c for c in other.chromatins]))

def death(s):
    pass

def birth():
    pass

elementary_forward_cobordisms = {'I': identity, 'T': twist, 'W': braid, 'P': pants, 'C': copants, 'D': death, 'B': birth}
elementary_reverse_cobordisms = {'I': identity, 'T': twist, 'W': braid, 'P': copants, 'C': pants, 'D': birth, 'B': death}

class Cobordism:
    def __init__(self, steps):
        if isinstance(steps[0], str) is True:
            self.steps = [steps]
            self.in_len, self.out_len = Cobordism.compute_in_out_len(steps)              # set in-boundary
        else:
            self = Cobordism(steps[0])
            self.in_len, self.out_len = Cobordism.compute_in_out_len(steps[0])              # set in-boundary
            for step in steps[1:]:
                step_cobord = Cobordism(step)
                self.composition(step_cobord)

    def composition(self, step):
        # check if each step composes with the next
        if self.out_len == step.in_len:
            self.steps.append(step)
            #update out-boundary
            self.out_len = step.out_len
        else:
            raise ValueError

    def generate_in_out_map(self):
        label_count = 0
        init_config = []
        # create intervals for each input
        for _ in range(self.in_len):
            init_config.extend(Interval([str(label_count), str(label_count+1)]))
            label_count += 2
        # forward pass
        configs = [tuple(init_config)]
        for step in self.steps:
            out_config = []
            in_config = configs[-1]
            input_index = 0
            for op in step:
                if op in {'I', 'T', 'D'}:
                    out_config.extend(elementary_forward_cobordisms[op](in_config[input_index]))
                    input_index += 1
                elif op in {'P', 'W'}:
                    out_config.extend(elementary_forward_cobordisms[op](in_config[input_index], in_config[input_index+1]))
                    input_index += 2
                else:
                    out_config.extend(elementary_forward_cobordisms[op](in_config[input_index], str(label_count), str(label_count+1)))
                    label_count += 2
                    input_index += 1
            configs.append(tuple(out_config))
        
        # backward pass
        for config in reversed(configs):
            for i in config:
                if i.prev_interval is not None:
                    if i.prev_interval.labels[0] == i.labels[0] and i.labels[-1] == i.prev_interval.labels[-1]:
                        i.prev_interval.labels = i.labels
                    elif i.prev_interval.labels[0] == i.labels[-1] and i.labels[0] == i.prev_interval.labels[-1]:
                        i.prev_interval.labels = tuple(reversed(i.labels))
                    elif len(i.prev_interval) == 2:
                        #split the current interval
                        left_child_right = i.prev_interval['left'].labels[-1]
                        # right_child_left = i.prev_interval['right'].labels[0]
                        left_labels = []
                        for l, j in enumerate(i.labels):
                            if l != left_child_right:
                                left_labels.append(l)
                            else:
                                right_labels = i.labels[j:]
                                break
                        i.prev_interval['left'].labels = tuple(left_labels)
                        i.prev_interval['right'].labels = tuple(right_labels)
                    elif i.prev_interval.labels[0] == i.labels[0]:
                        i.prev_interval.labels = i.labels
                    elif i.prev_interval.labels[-1] == i.labels[-1]:
                        i.prev_interval.labels += i.labels

        self.in_out_map = {configs[0]: configs[-1]}

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
    
    @staticmethod
    def compute_in_out_len(step):
        in_len, out_len = 0, 0
        for element in step:
            if element in {'I', 'T', 'C', 'D'}:
                in_len += 1
            elif element in {'P', 'W'}:
                in_len += 2
            elif element != 'B':
                raise ValueError
            if element in {'I', 'T', 'P', 'B'}:
                out_len += 1
            elif element in {'C', 'W'}:
                out_len += 2
            elif element != 'D':
                raise ValueError
        return in_len, out_len

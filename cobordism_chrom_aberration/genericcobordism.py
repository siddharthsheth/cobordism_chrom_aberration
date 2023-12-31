from cobordism_chrom_aberration.segment import ChromSegment

class Interval:
    def __init__(self, labels, next_interval=None, prev_interval=None, next_op=None, prev_op=None):
        self.labels = tuple(labels)
        self.next_interval = next_interval
        self.prev_interval = prev_interval
        self.next_op = next_op
        self.prev_op = prev_op
    
    def __str__(self):
        return str(self.labels)
    
    def __eq__(self, other):
        return True if all(l_s == l_o for l_s, l_o in zip(self.labels, other.labels)) else False

def identity(interval):
    new_interval = Interval(interval.labels, 
                            prev_interval=interval,
                            prev_op='I'
                            )
    interval.next_interval = new_interval
    interval.next_op = 'I'
    return (new_interval,)

def twist(interval):
    new_interval = Interval([c for c in reversed(interval.labels)], 
                            prev_interval=interval,
                            prev_op='T')
    interval.next_interval = new_interval
    interval.next_op = 'T'
    return (new_interval,)

def braid(left_interval, right_interval):
    new_left_interval = Interval(right_interval.labels, 
                                 prev_interval=right_interval,
                                 prev_op='W'
                                )
    new_right_interval = Interval(left_interval.labels, 
                                  prev_interval=left_interval,
                                  prev_op='W'
                                )
    left_interval.next_interval = new_right_interval
    left_interval.next_op = 'W'
    right_interval.next_interval = new_left_interval
    right_interval.next_op = 'W'
    return new_left_interval, new_right_interval

def copants(interval,  new_right_label=None, new_left_label=None):
    
    if interval.next_interval is not None:
        left_labels, right_labels = interval.next_interval['left'].labels, interval.next_interval['right'].labels
    else:                                                           # buggy. should do same as generate_final_config case 'P'
        left_labels = [interval.labels[0], new_right_label]
        right_labels = [new_left_label, interval.labels[-1]]

    new_left_interval = Interval(left_labels, 
                                 prev_interval=interval,
                                 prev_op='C'
                                )
    new_right_interval = Interval(right_labels, 
                                  prev_interval=interval,
                                  prev_op='C'
                                )
    interval.next_interval = {'left': new_left_interval, 'right': new_right_interval}
    interval.next_op = 'C'
    return new_left_interval, new_right_interval
    # return None if i>len(s.chromatins) \
                #    else ChromSegment([c for c in s.chromatins[:i]]), ChromSegment([c for c in s.chromatins[i:]])

def pants(left_interval, right_interval):
    new_interval = Interval(left_interval.labels + right_interval.labels, 
                            prev_interval={'left':left_interval, 'right': right_interval},
                            prev_op='P'
                        )
    left_interval.next_interval = new_interval
    left_interval.next_op = 'P'
    right_interval.next_interval = new_interval
    right_interval.next_op = 'P'
    return (new_interval,)
    # return ChromSegment([c for c in s.chromatins].extend([c for c in other.chromatins]))

def death(s):
    #TODO
    pass

def birth():
    #TODO
    pass

elementary_forward_cobordisms = {'I': identity, 'T': twist, 'W': braid, 'P': pants, 'C': copants, 'D': death, 'B': birth}
elementary_reverse_cobordisms = {'I': identity, 'T': twist, 'W': braid, 'P': copants, 'C': pants, 'D': birth, 'B': death}

class Cobordism:
    def __init__(self, steps):                              # ALLOW EMPTY COBORDISM?
        if steps is not None:
            if isinstance(steps, str) is True or isinstance(steps[0], str) is True:               # BUGGY STEP
                self.steps = [tuple(steps)]
                self.in_len, self.out_len = Cobordism.compute_in_out_len(steps)              # set in-boundary
            else:
                self.steps = [steps[0]]
                self.in_len, self.out_len = Cobordism.compute_in_out_len(steps[0])              # set in-boundary
                for step in steps[1:]:
                    step_cobord = Cobordism(step)
                    self.composition(step_cobord)
            # self.in_out_map = self.generate_terminal_config_map()

    def composition(self, step_cobord):
        # check if step_cobord composes with the next
        if len(self.steps) == 0 or self.out_len == step_cobord.in_len:
            self.steps.extend(step_cobord.steps)
            #update out-boundary
            self.out_len = step_cobord.out_len
        else:
            raise ValueError('Cobordisms cannot be composed.')

    def _generate_configs(self):
        label_count = 0
        init_config = []
        # create intervals for each input
        for _ in range(self.in_len):
            init_config.append(Interval([str(label_count), str(label_count+1)]))
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
        return configs
        
    def generate_terminal_configs(self):
        configs = self._generate_configs()
        # backward pass
        for config in reversed(configs):
            for i in config:
                if i.prev_op :
                    if i.prev_op == 'I' or i.prev_op == 'W':
                        i.prev_interval.labels = i.labels
                    elif i.prev_op == 'T':
                        i.prev_interval.labels = tuple(reversed(i.labels))
                    elif i.prev_op == 'P':
                        #split the current interval
                        left_child_right = i.prev_interval['left'].labels[-1]
                        left_labels = []
                        for j, l in enumerate(i.labels):
                            if l != left_child_right:
                                left_labels.append(l)
                            else:
                                left_labels.append(l)
                                right_labels = i.labels[j+1:]
                                break
                        i.prev_interval['left'].labels = tuple(left_labels)
                        i.prev_interval['right'].labels = tuple(right_labels)
                    elif i.prev_op == 'C' and i.prev_interval.next_interval['left'] == i:
                        i.prev_interval.labels = i.labels + i.prev_interval.next_interval['right'].labels
        self.in_config = configs[0]
        self.out_config = configs[-1]

    def generate_final_configuration(self, init):
        if hasattr(self, 'in_config') is False:
            self.generate_terminal_configs()
        # print([str(i) for i in init])
        # print([str(i) for i in self.in_config])
        if len(init) != len(self.in_config):
            raise ValueError('Input configuration does not match initial configuration.')
        init_map = dict()
        for init_i, self_i in zip(init, self.in_config):
            if len(init_i.labels) != len(self_i.labels):
                raise ValueError('Initial configuration inconsistent.')
            else:
                for init_label, self_label in zip(init_i.labels, self_i.labels):
                    if self_label in init_map:
                        if init_map[self_label] != init_label:
                            raise ValueError('Initial configuration inconsistent.')
                    else:
                        init_map[self_label] = init_label
        
        return [Interval([init_map[l] for l in final_i.labels]) for final_i in self.out_config]


    def is_cobordism(self, init, final):
        return True if self.generate_final_configuration(init) == final else False
    
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
                raise ValueError(f'Unknown cobordism: {step[i]}.')
    
    @staticmethod
    def compute_in_out_len(step):
        in_len, out_len = 0, 0
        for element in step:
            if element in {'I', 'T', 'C', 'D'}:
                in_len += 1
            elif element in {'P', 'W'}:
                in_len += 2
            elif element != 'B':
                raise ValueError(f'Unknown cobordism: {element}.')
            if element in {'I', 'T', 'P', 'B'}:
                out_len += 1
            elif element in {'C', 'W'}:
                out_len += 2
            elif element != 'D':
                raise ValueError(f'Unknown cobordism: {element}.')
        return in_len, out_len
    
    @staticmethod
    def load_from_file(file):
        c = None
        with open(file, 'r') as input:
            for line in input:
                elements = line.split()
                if c is None:
                    c = Cobordism([e for e in elements if e in elementary_forward_cobordisms])
                else:
                    c.composition(Cobordism([e for e in elements if e in elementary_forward_cobordisms]))

        return c

    def save_to_file(self, file):
        with open(file, 'w') as output:
            for step in self.steps:
                output.write(' '.join(step)+'\n')

    @staticmethod
    def from_string(s:str):
        steps = s.split('\n')
        c = None
        for step in steps:
            elements = step.split()
            if c is None:
                c = Cobordism([e for e in elements if e in elementary_forward_cobordisms])
            else:
                c.composition(Cobordism([e for e in elements if e in elementary_forward_cobordisms]))
        
        return c
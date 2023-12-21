from cobordism_chrom_aberration.genericcobordism import Interval, Cobordism

c = Cobordism.load_from_file('examples/fig_5.txt')

f = c.generate_final_configuration([Interval('abcd'), Interval('efgh')])

print([str(e) for e in f])


steps = '''C C C
            I W I I I
            I I W W
            I W W I
            I I I I W
            P P P'''
c = Cobordism.from_string(steps)
# print([str(i) for i in c.generate_final_configuration([Interval('abcd'), Interval('efgh'), Interval('ijkl')])])
f = c.generate_final_configuration([Interval('abcd'), Interval('efgh'), Interval('ijkl')])
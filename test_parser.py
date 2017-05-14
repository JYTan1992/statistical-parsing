import time
import sys
from _parser import *

def main(model_dir, heldout_gold):
    input_sents = list(read_ud_conll_pos(heldout_gold))
    parser = Parser(load=True, model_dir=model_dir)
    c = 0
    t = 0
    gold_sents = list(read_ud_conll(heldout_gold))
    t1 = time.time()
    for (words, tags), (_, _, gold_heads, gold_labels) in zip(input_sents, gold_sents):
        _, heads = parser.parse(words)
        for i, w in list(enumerate(words))[1:-1]:
            if gold_labels[i] in ('P', 'punct'):
                continue
            if heads[i] == gold_heads[i]:
                c += 1
            t += 1
    t2 = time.time()
    print 'Parsing took %0.3f ms' % ((t2-t1)*1000.0)
    print c, 'right of', t, 'dependencies - accuracy:', float(c)/t


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])


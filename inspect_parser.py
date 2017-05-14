import time
import sys
from _parser import *

def target_contexts(words, tags, i, n, stack, parse) :
    if len(stack) < 2:
        return False
    if i > n-1:
        return False
    if tags[i] not in ('NOUN', 'PRON', 'PROPN') :
        return False
    if tags[stack[-1]] not in ('NOUN', 'PRON', 'PROPN') :
        return False
    if tags[stack[-2]] not in ('VERB') :
        return False

    return True

class Stats(object) :
    pass

def main(model_dir, heldout_gold, target=target_contexts):
    parser = Parser(load=True, model_dir=model_dir)
    c = 0
    t = 0
    gold_sents = list(read_ud_conll(heldout_gold))
    t1 = time.time()
    stats = Stats()
    stats.targetn = 0
    stats.correctn = 0
    stats.features_seen = {}
    stats.features_unseen = {}
    for (words, tags, gold_heads, gold_labels) in gold_sents:
        _, heads = parser.instrumented_parse(words, gold_heads, target, stats)
    t2 = time.time()
    print 'Parsing took %0.3f ms' % ((t2-t1)*1000.0)
    print stats.correctn, 'right of', stats.targetn, 'target moves',
    print '' if not stats.targetn else ('accuracy: %f' % (float(stats.correctn)/stats.targetn))
    for k in set(stats.features_seen.keys() + stats.features_unseen.keys()):
        print 'Features of class ', k,
        print '' if k not in stats.features_seen.keys() else stats.features_seen[k],
        print 'seen and ', 
        print '' if k not in stats.features_unseen.keys() else stats.features_unseen[k],
        print 'new'
        
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])


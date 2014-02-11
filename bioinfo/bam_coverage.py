#! /usr/bin/env python
"""
Usage:

   bam-coverage.py reference.fa query.x.reference.bam minmatch query.fa mapq

bam-coverage calculates the fraction of bases in 'reference.fa' that are
covered by a BAM alignment file, for sequence in 'query.fa' that are
longer than 'minmatch'.
"""

from __future__ import print_function, division
import sys

DEPENDENCIES = {
    "pysam": False,
    "screed": False,
    "tqdm": False,
}

try:
    import pysam
    DEPENDENCIES['pysam'] = True
except ImportError:
    pass

try:
    import screed
    DEPENDENCIES['screed'] = True
except ImportError:
    pass

try:
    from tqdm import tqdm
    DEPENDENCIES['tqdm'] = True
except ImportError:
    pass


def check_dependencies():
    if all(DEPENDENCIES[d] for d in DEPENDENCIES):
        return True

    print("Missing dependencies, install before proceeding:")
    for dep, installed in DEPENDENCIES.items():
        if not installed:
            print(dep)

    sys.exit(1)


def bam_coverage(reference, alignments, min_match, query, min_mapq=30):
    check_dependencies()

    # load in the query sequences into a list
    print("reading query")
    query_seqs = set([r.name for r in tqdm(screed.open(query), leave=True)
                      if len(r.sequence) >= min_match])
    print()

    # create empty lists representing the total number of bases in the
    # reference
    print("creating empty lists")
    covs = {}
    for record in tqdm(screed.open(reference), leave=True):
        covs[record.name] = [0] * len(record.sequence)
    print()

    # run through the BAM records in the query, and calculate how much of
    # the reference is covered by the query.
    print('building coverage')
    with pysam.Samfile(alignments, "rb") as samfile:
        for record in tqdm(samfile, leave=True):

            if record.qname not in query_seqs:
                continue

            if record.mapq < min_mapq:
                continue

            cov = covs.get(samfile.getrname(record.tid))
            if not cov:
                continue

            for pos_read, pos_ref in record.aligned_pairs:
                if pos_ref:
                    cov[pos_ref] = 1
    print()

    # print out summary statistics for each of the reference.
    coved = 0
    total = 0
    print('Summing stats')
    for name in tqdm(covs, leave=True):
        this_cov = sum(covs[name])
        coved += this_cov
        total += len(covs[name])
        f = this_cov / float(len(covs[name]))
    print()

    print()
    print('total bases in reference:', total)
    print('total ref bases covered :', coved)
    print('fraction                :', coved / float(total))
    print('reference               :', reference)
    print('BAM alignment file      :', alignments)
    print('query sequences         :', query)


if __name__ == "__main__":
    reference = sys.argv[1]
    alignments = sys.argv[2]
    min_match = int(sys.argv[3])
    query = sys.argv[4]
    min_mapq = int(sys.argv[5])

    bam_coverage(reference, alignments, min_match, query, min_mapq=30)

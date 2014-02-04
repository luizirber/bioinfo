#! /usr/bin/env python
"""
Usage:

   calc-bwa-cover.py reference.fa query.x.reference.blastn minmatch query.fa

calc-blast-cover calculates the fraction of bases in 'reference.fa' that are
covered by BLAST matches from 'query.fa', for sequence in 'query.fa' that are
longer than 'minmatch'.
"""

import pysam
import screed
import tqdm


def calc_bwa_coverage(reference, bwa_alignments, min_match, query, min_mapq=30):

    # load in the query sequences into a list
    print "reading query"
    query_seqs = set([record.name for record in screed.open(query)
                      if len(record.sequence) >= minmatch])

    print "creating empty lists"

    # create empty lists representing the total number of bases in the
    # reference
    covs = {}
    for record in tqdm(screed.open(reference)):
        covs[record.name] = [0] * len(record.sequence)

    # run through the BAM records in the query, and calculate how much of
    # the reference is covered by the query.
    with pysam.Samfile(bwa_alignments, "rb") as samfile:
        for record in tqdm(samfile):

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

    print ''

    # print out summary statistics for each of the reference.
    coved = 0
    total = 0
    for name in covs:
        this_cov = sum(covs[name])
        coved += this_cov
        total += len(covs[name])
        f = this_cov / float(len(covs[name]))
        # print name, sum(covs[name]), len(covs[name]), f

    print 'total bases in reference:', total
    print 'total ref bases covered :', coved
    print 'fraction                :', coved / float(total)
    print 'reference               :', reference
    print 'bwa alignment file      :', bwa_alignment
    print 'query sequences         :', query

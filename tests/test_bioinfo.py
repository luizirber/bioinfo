# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import shutil
import unittest

from nose.tools import *  # PEP8 asserts
from scripttest import TestFileEnvironment

try:
    import coverage
    coverage.process_startup()
except ImportError:
    pass


class TestBamConverage(unittest.TestCase):

    '''Unit tests for bam_coverage.'''

    def setUp(self):
        self.env = TestFileEnvironment()
        shutil.copytree(os.path.join(os.path.dirname(__file__), 'data'),
                        os.path.join(self.env.base_path, 'data'))

    def tearDown(self):
        self.env.clear()

    def test_arguments(self):
        ret = self.env.run("bioinfo", "-h")
        self.assertEquals(ret.returncode, 0)
        self.assertIn('bam_coverage', ret.stdout)

    def test_complete_run(self):
        ret = self.env.run("bioinfo", "bam_coverage",
                           "data/bam_ref.fasta",
                           "data/bam_align.sorted.bam",
                           "10",
                           "data/bam_query.fasta",
                           "--mapq=30")
        self.assertEquals(ret.returncode, 0)

        self.assertIn('total bases in reference', ret.stdout)
        self.assertIn('total ref bases covered', ret.stdout)
        self.assertIn('fraction', ret.stdout)

        for line in ret.stdout.split('\n'):
            if 'total bases in reference' in line:
                self.assertIn('237', line)
            if 'total ref bases covered' in line:
                self.assertIn('57', ret.stdout)
            if 'fraction' in line:
                self.assertIn('0.24', ret.stdout)


if __name__ == '__main__':
    unittest.main()

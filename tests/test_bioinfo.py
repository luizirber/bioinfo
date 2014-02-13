# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import shutil
import unittest

from nose.tools import *  # PEP8 asserts
from scripttest import TestFileEnvironment


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

    def test_coverage(self):
        ret = self.env.run("bioinfo", "bam_coverage",
                           "data/bam_ref.fasta",
                           "data/bam_align.sorted.bam",
                           "10",
                           "data/bam_query.fasta",
                           "--mapq=30")
        self.assertEquals(ret.returncode, 0)
        self.assertIn('bam_coverage', ret.stdout)


if __name__ == '__main__':
    unittest.main()

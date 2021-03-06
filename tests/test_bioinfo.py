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
        self.total = 237
        self.coved = 154
        self.fraction = 0.6497
        self.min_match_coved = 115
        self.min_match_fraction = 0.485

    def tearDown(self):
        self.env.clear()

    def test_arguments(self):
        ret = self.env.run("bioinfo", "-h")
        self.assertEquals(ret.returncode, 0)
        self.assertIn('bam_coverage', ret.stdout)

    def test_complete_run_cli(self):
        ret = self.env.run("bioinfo", "bam_coverage",
                           "data/bam_ref.fasta",
                           "data/bam_align.sorted.bam",
                           "10",
                           "--mapq=30", expect_stderr=True)
        self.assertEquals(ret.returncode, 0)

        self.assertIn('total bases in reference', ret.stdout)
        self.assertIn('total ref bases covered', ret.stdout)
        self.assertIn('fraction', ret.stdout)

        self.assertNotIn('total bases in reference', ret.stderr)
        self.assertNotIn('total ref bases covered', ret.stderr)
        self.assertNotIn('fraction', ret.stderr)

        for line in ret.stdout.split('\n'):
            if 'total bases in reference' in line:
                self.assertIn(str(self.total), line)
            if 'total ref bases covered' in line:
                self.assertIn(str(self.coved), ret.stdout)
            if 'fraction' in line:
                self.assertIn(str(self.fraction), ret.stdout)

    def test_complete_run_module(self):
        from bioinfo import bam_coverage

        result = bam_coverage(
            os.path.join('tests', 'data', 'bam_ref.fasta'),
            os.path.join('tests', 'data', 'bam_align.sorted.bam'),
            10,
            30
        )
        self.assertEqual(result['total'], self.total)
        self.assertEqual(result['covered'], self.coved)
        self.assertAlmostEqual(result['fraction'], self.fraction, places=3)

    def test_min_match(self):
        from bioinfo import bam_coverage

        result = bam_coverage(
            os.path.join('tests', 'data', 'bam_ref.fasta'),
            os.path.join('tests', 'data', 'bam_align.sorted.bam'),
            45,
            30
        )
        self.assertEqual(result['total'], self.total)
        self.assertEqual(result['covered'], self.min_match_coved)
        self.assertAlmostEqual(result['fraction'],
                               self.min_match_fraction,
                               places=2)

    def test_check_dependencies(self):
        import bioinfo
        from bioinfo import bam_coverage

        bioinfo.bam_coverage_mod.DEPENDENCIES['pysam'] = False

        with self.assertRaises(SystemExit):
            bam_coverage(
                os.path.join('tests', 'data', 'bam_ref.fasta'),
                os.path.join('tests', 'data', 'bam_align.sorted.bam'),
                10,
                30
            )

        bioinfo.bam_coverage_mod.DEPENDENCIES['pysam'] = True


if __name__ == '__main__':
    unittest.main()

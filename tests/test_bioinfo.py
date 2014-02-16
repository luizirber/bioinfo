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
        self.coved = 57
        self.fraction = 0.24

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
                           "data/bam_query.fasta",
                           "--mapq=30", expect_stderr=True)
        self.assertEquals(ret.returncode, 0)

        self.assertIn('total bases in reference', ret.stdout)
        self.assertIn('total ref bases covered', ret.stdout)
        self.assertIn('fraction', ret.stdout)
        self.assertNotIn('elapsed', ret.stdout)

        self.assertNotIn('total bases in reference', ret.stderr)
        self.assertNotIn('total ref bases covered', ret.stderr)
        self.assertNotIn('fraction', ret.stderr)
        self.assertIn('elapsed', ret.stderr)

        for line in ret.stdout.split('\n'):
            if 'total bases in reference' in line:
                self.assertIn(str(self.total), line)
            if 'total ref bases covered' in line:
                self.assertIn(str(self.coved), ret.stdout)
            if 'fraction' in line:
                self.assertIn(str(self.fraction), ret.stdout)

    def test_complete_run_module(self):
        from bioinfo import bam_coverage

        total, coved, fraction = bam_coverage(
            os.path.join('tests', 'data', 'bam_ref.fasta'),
            os.path.join('tests', 'data', 'bam_align.sorted.bam'),
            10,
            os.path.join('tests', 'data', 'bam_query.fasta'),
            30
        )
        self.assertEqual(total, self.total)
        self.assertEqual(coved, self.coved)
        self.assertAlmostEqual(fraction, self.fraction, places=2)

    def test_check_dependencies(self):
        import bioinfo
        from bioinfo import bam_coverage

        bioinfo.bam_coverage_mod.DEPENDENCIES['pysam'] = False

        with self.assertRaises(SystemExit):
            bam_coverage(
                os.path.join('tests', 'data', 'bam_ref.fasta'),
                os.path.join('tests', 'data', 'bam_align.sorted.bam'),
                10,
                os.path.join('tests', 'data', 'bam_query.fasta'),
                30
            )

        bioinfo.bam_coverage_mod.DEPENDENCIES['pysam'] = True


if __name__ == '__main__':
    unittest.main()

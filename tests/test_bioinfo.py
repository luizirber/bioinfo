# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest

from nose.tools import *  # PEP8 asserts
from scripttest import TestFileEnvironment

class TestBamConverage(unittest.TestCase):

    '''Unit tests for bam_coverage.'''

    def setUp(self):
        self.env = TestFileEnvironment()

    def tearDown(self):
        pass

    def test_arguments(self):
        ret = self.env.run("bioinfo", "-h")
        self.assertEquals(ret.returncode, 0)
        self.assertIn('bam_coverage', ret.stdout)


if __name__ == '__main__':
    unittest.main()

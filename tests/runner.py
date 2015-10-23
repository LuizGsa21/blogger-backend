import unittest
import logging
import os

if '__main__' == __name__:
    # suppress warnings during test
    logging.getLogger().setLevel(logging.ERROR)
    # Discover and run tests.
    dirname = os.path.dirname
    suite = unittest.loader.TestLoader().discover(dirname(dirname(os.path.realpath(__file__))), pattern='test_*.py')
    unittest.TextTestRunner(verbosity=2).run(suite)

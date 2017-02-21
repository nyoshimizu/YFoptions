import unittest

from options import options


class TestPOSIXtime(unittest.TestCase):

    def test_datetoPOSIXtime(self):
        option = options.options('AAPL')
        date = "5/19/2017"
        POSIXtime = option.datetoPOSIXtime(date)
        self.assertEqual(POSIXtime, '1495152000')

if __name__ == '__main__':
    unittest.main()

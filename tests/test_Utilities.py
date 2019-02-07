
from unittest import TestCase
import sabersql.Utilities

class TestUtilities(TestCase):

    def test_shell(self):
        out, err = sabersql.Utilities._shell("echo hi")
        self.assertEqual("hi\n", out)
        self.assertEqual("", err)

        out, err = sabersql.Utilities._shell(">&2 echo hi")
        self.assertEqual("", out)
        self.assertEqual("hi\n", err)

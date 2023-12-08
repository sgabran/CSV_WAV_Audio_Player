# This class allows to stop and resume updating the console

from io import StringIO
import sys


class NullIO(StringIO):
    def write(self, txt):
       pass

    @staticmethod
    def stop_io():
        sys.stdout = NullIO()

    @staticmethod
    def resume_io():
        sys.stdout = sys.__stdout__

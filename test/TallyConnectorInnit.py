from pythonnet import load
load("coreclr")

import clr
import sys

path = r"./Python_Tally/lib"
sys.path.append(path)

clr.AddReference("TallyConnector")

from TallyConnector.Services import TallyService
tally = TallyService()


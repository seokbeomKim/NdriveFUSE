#!/usr/bin/env python

import os
import sys
import base64
sys.path.append(os.path.join(os.path.dirname(__file__), "modules"))
import confgen
        
if __name__ == '__main__':
    confGen = confgen.ConfGenerator()
    confGen.generateFile()

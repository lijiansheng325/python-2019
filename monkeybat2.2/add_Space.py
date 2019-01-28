# -*- coding: utf8 -*-
## remark: python version 2-7-12
import os
import sys
import re

fd = open(filename)
content= fd.readlines()
fd.close()
result = re.sub(r"(?<=\w)(?=(?:\w\w\w)+$)", " ", content)
print result

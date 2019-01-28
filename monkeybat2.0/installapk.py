#!/usr/bin/env python 
# 
# Copyright (c) 2012 The Chromium Authors. All rights reserved. 
# Use of this source code is governed by a BSD-style license that can be 
# found in the LICENSE file. 

import os
import sys
import time
import datetime


doc = "d:\apk\"
apkInstall = "adb install "

apk = os.listdir(r'doc')

for i in apk:
	apkPath = os.path.join(doc, i)
	os.sytem(apkInstall, apkPath)
	

	

 
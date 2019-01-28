@echo off 

adb -s 2e6404f009ce0001 shell /system/bin/screencap -p /sdcard/screenshot.png
adb -s 2e6404f009ce0001 pull /sdcard/screenshot.png .\test\screenshot
cd /d  .\test\screenshot
set a=%Date:~0,4%%Date:~5,2%%Date:~8,2%_
set b=%TIME:~0,2%
if %TIME:~0,2% leq 9 (set b=0%TIME:~1,1%)else set b=%TIME:~0,2%
set c=%TIME:~3,2%%TIME:~6,2%
mv screenshot.png screenshot%a%%b%%c%.png
echo on
dir /b 
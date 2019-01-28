adb push .\l\WhiteBlack.txt /data/local/tmp/

adb shell monkey --throttle 1000 -s 14041 --pct-anyevent 0 --pct-trackball 0 --pct-nav 0 --pct-majornav 2 --pct-appswitch 2 --ignore-timeouts --ignore-crashes --ignore-security-exceptions  --pkg-whitelist-file /data/local/tmp/WhiteBlack.txt -v -v 1000 > monkeylog.log

adb push .\l\WhiteBlack.txt /data/local/tmp/

adb shell monkey --throttle 500 -s 1000 --pct-anyevent 0 --pct-trackball 0 --pct-nav 0 --pct-majornav 2 --pct-appswitch 2 --ignore-timeouts --ignore-crashes --ignore-security-exceptions  --pkg-blacklist-file /data/local/tmp/WhiteBlack.txt -v -v  576000 > monkeylog.log
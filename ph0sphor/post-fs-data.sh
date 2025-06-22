#!/system/bin/sh
rm -fv /data/adb/modules/ph0sphor/log.txt
cp -v -a "/system_ext/overlay/." "/data/adb/modules/ph0sphor/system_ext/overlay" >> /data/adb/modules/ph0sphor/log.txt &&
mount -v -o bind "/data/adb/modules/ph0sphor/system_ext/overlay" "/system_ext/overlay" >> /data/adb/modules/ph0sphor/log.txt &&
echo Done >> /data/adb/modules/ph0sphor/log.txt
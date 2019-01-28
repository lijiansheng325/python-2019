rem adb reboot bootloader

fastboot -i 0x1ebf flash  boot boot.img

fastboot -i 0x1ebf flash cache cache.img

fastboot -i 0x1ebf flash system system.img

fastboot -i 0x1ebf flash userdata userdata.img 

fastboot -i 0x1ebf flash recovery recovery.img

fastboot -i 0x1ebf reboot



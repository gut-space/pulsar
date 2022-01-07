# Various SDR performance tests

## Raspberry Pi

Tests conducted on Raspberry Pi 4 B with two storage options:

- SD card: SanDisk SANDISK Ultra microSDXC 64GB 120MB/s (C10, U1, A1, exact model: SDSQUA4-064G-GN6MA).
- External SSD disk: Samsung T5 500GB, with claimed rate of 540MB/s

```
cat /proc/cpuinfo

...

processor	: 3
model name	: ARMv7 Processor rev 3 (v7l)
BogoMIPS	: 108.00
Features	: half thumb fastmult vfp edsp neon vfpv3 tls vfpv4 idiva idivt vfpd32 lpae evtstrm crc32 
CPU implementer	: 0x41
CPU architecture: 7
CPU variant	: 0x0
CPU part	: 0xd08
CPU revision	: 3

Hardware	: BCM2711
Revision	: c03111
Serial		: 1000000033692ec6
Model		: Raspberry Pi 4 Model B Rev 1.1
```

### 1. AirSpy 10MSPS on Samsung SSD

```
pi@raspberrypi:/media/pi/Samsung_T5 $ airspy_rx -r as_10M.raw -f 635 -a 10000000 -t 2 -v 14 -m 15 -l 14 -n 600000000
Device Serial Number: 0xA74068C830933C93
Stop with Ctrl-C
Streaming at 9.999 MSPS
Streaming at 9.859 MSPS
Streaming at 8.536 MSPS
Streaming at 7.462 MSPS
Streaming at 6.613 MSPS
Streaming at 6.889 MSPS
Streaming at 6.115 MSPS
Streaming at 6.115 MSPS
Streaming at 5.350 MSPS
Streaming at 5.350 MSPS
Streaming at 6.708 MSPS
Streaming at 7.355 MSPS
Streaming at 6.610 MSPS
Streaming at 6.610 MSPS
Streaming at 5.646 MSPS
Streaming at 6.985 MSPS
Streaming at 6.614 MSPS
Streaming at 6.415 MSPS
Streaming at 5.628 MSPS
Streaming at 5.628 MSPS
Streaming at 4.920 MSPS
Streaming at 6.774 MSPS
Streaming at 6.097 MSPS
Streaming at 6.097 MSPS
Streaming at 5.180 MSPS
Streaming at 4.758 MSPS
Streaming at 7.037 MSPS
Streaming at 6.318 MSPS
Streaming at 6.318 MSPS
Streaming at 6.318 MSPS
Streaming at 5.274 MSPS
Streaming at 7.695 MSPS
Streaming at 6.752 MSPS
Streaming at 7.433 MSPS
Streaming at 7.433 MSPS
Streaming at 7.433 MSPS
Streaming at 7.659 MSPS
Streaming at 8.115 MSPS
Streaming at 7.593 MSPS
Streaming at 7.593 MSPS
Streaming at 6.375 MSPS
Streaming at 6.375 MSPS
Streaming at 7.174 MSPS
Streaming at 6.996 MSPS
Streaming at 6.359 MSPS
Streaming at 6.359 MSPS
Streaming at 6.359 MSPS
Streaming at 7.048 MSPS
```

### 1. AirSpy 6MSPS on Samsung SSD

```
pi@raspberrypi:/media/pi/Samsung_T5 $ airspy_rx -r as_6M.raw -f 635 -a 6000000 -t 2 -v 14 -m 15 -l 14 -n 600000000
Device Serial Number: 0xA74068C830933C93
Stop with Ctrl-C
Streaming at 6.003 MSPS
Streaming at 6.002 MSPS
Streaming at 6.000 MSPS
Streaming at 5.385 MSPS
Streaming at 4.945 MSPS
Streaming at 4.377 MSPS
Streaming at 4.377 MSPS
Streaming at 3.860 MSPS
Streaming at 4.626 MSPS
Streaming at 4.905 MSPS
Streaming at 4.472 MSPS
Streaming at 4.472 MSPS
Streaming at 4.018 MSPS
Streaming at 3.554 MSPS
Streaming at 4.043 MSPS
Streaming at 4.748 MSPS
Streaming at 4.372 MSPS
Streaming at 4.372 MSPS
Streaming at 3.960 MSPS
Streaming at 3.607 MSPS
Streaming at 4.555 MSPS
Streaming at 4.820 MSPS
Streaming at 4.861 MSPS
Streaming at 4.385 MSPS
Streaming at 4.385 MSPS
Streaming at 3.953 MSPS
Streaming at 3.742 MSPS
Streaming at 4.609 MSPS
Streaming at 4.862 MSPS
Streaming at 4.862 MSPS
Streaming at 4.767 MSPS
Streaming at 4.591 MSPS
Streaming at 4.669 MSPS
Streaming at 4.270 MSPS
Streaming at 3.844 MSPS
Streaming at 4.251 MSPS
Streaming at 3.825 MSPS
Streaming at 4.066 MSPS
Streaming at 4.760 MSPS
```


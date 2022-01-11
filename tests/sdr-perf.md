# Various SDR performance tests

## Raspberry Pi

Tests conducted on Raspberry Pi 4 B with two storage options:

- SD card1: SanDisk Ultra microSDXC 64GB 120MB/s read speed (C10, U1, A1, exact model: SDSQUA4-064G-GN6MA).
- SD card2: SanDisk Extreme A2 (160MB/s read speed, 60MB/s write speed according to producer).
- External SSD disk: Samsung T5 500GB, with claimed rate of 540MB/s
- SDR used: AirSpy Mini

Each test was designed to last 60 seconds, with the appropriate number of samples chosen to correspond to the sampling rate. Tests were run in the console, using airspy_rx version 1.0.6.

The SSD disk was completely empty. The SSD card had the Raspberry Pi system on it with some software. 12 out of 64GB was used.

All commands were issued as root, to ensure maximum priority.

I was not able to overclock my SD host. Despite adding ``dtparam=sd_overclock=100` to `/boot/config.txt`, it still used the default 50MHz.
```
# cat /sys/kernel/debug/mmc0/ios
clock:		50000000 Hz
actual clock:	50000000 Hz
vdd:		21 (3.3 ~ 3.4 V)
bus mode:	2 (push-pull)
chip select:	0 (don't care)
power mode:	2 (on)
bus width:	2 (4 bits)
timing spec:	7 (sd uhs DDR50)
signal voltage:	1 (1.80 V)
driver type:	0 (driver type B)
```


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

Practical max. performance was measured with `dd` command that wrote 1GB of zeros.

SD Card1:
```
# dd if=/dev/zero of=/home/pi/zero.raw count=2000000
2000000+0 records in
2000000+0 records out
1024000000 bytes (1.0 GB, 977 MiB) copied, 48.7694 s, 21.0 MB/s
```

SD Card2:
```
# dd if=/dev/zero of=/home/pi/zero.raw count=2000000
2000000+0 records in
2000000+0 records out
1024000000 bytes (1.0 GB, 977 MiB) copied, 18.0299 s, 56.8 MB/s
```

However, after couple reboots, writing and deleting files, it went down to:

```
# dd if=/dev/zero of=/home/pi/zero.raw count=2000000
2000000+0 records in
2000000+0 records out
1024000000 bytes (1.0 GB, 977 MiB) copied, 31.8347 s, 32.2 MB/s
```

SSD disk:
```
# dd if=/dev/zero of=/media/pi/Samsung_T5/zero.raw count=2000000
2000000+0 records in
2000000+0 records out
1024000000 bytes (1.0 GB, 977 MiB) copied, 37.6617 s, 27.2 MB/s
```

### 1. AirSpy 3MSPS on SD Card1

```
# airspy_rx -r as_3M.raw -f 635 -a 3000000 -t 2 -v 14 -m 15 -l 14 -n 180000000
Device Serial Number: 0xA74068C830933C93
Stop with Ctrl-C
Streaming at 3.000 MSPS
Streaming at 3.002 MSPS
Streaming at 3.001 MSPS
Streaming at 3.001 MSPS
Streaming at 3.001 MSPS
Streaming at 2.817 MSPS
Streaming at 2.817 MSPS
Streaming at 2.854 MSPS
Streaming at 2.883 MSPS
Streaming at 2.906 MSPS
Streaming at 2.925 MSPS
Streaming at 2.940 MSPS
Streaming at 2.952 MSPS
Streaming at 2.962 MSPS
Streaming at 2.969 MSPS
Streaming at 2.975 MSPS
Streaming at 2.980 MSPS
Streaming at 2.984 MSPS
Streaming at 2.984 MSPS
Streaming at 2.987 MSPS
Streaming at 2.990 MSPS
Streaming at 2.992 MSPS
Streaming at 2.993 MSPS
Streaming at 2.995 MSPS
Streaming at 2.996 MSPS
Streaming at 2.997 MSPS
Streaming at 2.997 MSPS
Streaming at 2.999 MSPS
Streaming at 2.998 MSPS
Streaming at 2.998 MSPS
Streaming at 2.883 MSPS
Streaming at 2.907 MSPS
Streaming at 2.924 MSPS
Streaming at 2.941 MSPS
Streaming at 2.941 MSPS
Streaming at 2.625 MSPS
Streaming at 2.625 MSPS
Streaming at 2.699 MSPS
Streaming at 2.759 MSPS
Streaming at 2.737 MSPS
Streaming at 2.881 MSPS
Streaming at 2.905 MSPS
Streaming at 2.924 MSPS
Streaming at 2.939 MSPS
Streaming at 2.939 MSPS
Streaming at 2.939 MSPS
Streaming at 2.568 MSPS
Streaming at 2.684 MSPS
Streaming at 2.747 MSPS
Streaming at 2.798 MSPS
Streaming at 2.838 MSPS
Streaming at 2.838 MSPS
Streaming at 2.872 MSPS
Streaming at 2.896 MSPS
Streaming at 2.917 MSPS
Streaming at 2.935 MSPS
Streaming at 2.947 MSPS
Streaming at 2.957 MSPS
Streaming at 2.966 MSPS
Streaming at 2.835 MSPS
Streaming at 2.835 MSPS
Streaming at 2.868 MSPS
Streaming at 2.893 MSPS
Streaming at 2.914 MSPS
Streaming at 2.914 MSPS

User cancel, exiting...
Total time: 64.9837 s
Average speed 2.9048 MSPS IQ
done
```

### 2. AirSpy 6MSPS on SD Card1

```
root@raspberrypi:/home/pi# airspy_rx -r as_6M.raw -f 635 -a 6000000 -t 2 -v 14 -m 15 -l 14 -n 360000000
Device Serial Number: 0xA74068C830933C93
Stop with Ctrl-C
Streaming at 6.020 MSPS
Streaming at 6.013 MSPS
Streaming at 6.008 MSPS
Streaming at 6.006 MSPS
Streaming at 6.000 MSPS
Streaming at 5.558 MSPS
Streaming at 5.723 MSPS
Streaming at 5.823 MSPS
Streaming at 5.859 MSPS
Streaming at 5.910 MSPS
Streaming at 5.910 MSPS
Streaming at 5.445 MSPS
Streaming at 5.641 MSPS
Streaming at 5.774 MSPS
Streaming at 5.856 MSPS
Streaming at 5.351 MSPS
Streaming at 5.586 MSPS
Streaming at 5.669 MSPS
Streaming at 5.789 MSPS
Streaming at 5.861 MSPS
Streaming at 5.893 MSPS
Streaming at 5.137 MSPS
Streaming at 5.447 MSPS
Streaming at 5.646 MSPS
Streaming at 5.717 MSPS
Streaming at 5.717 MSPS
Streaming at 5.361 MSPS
Streaming at 5.591 MSPS
Streaming at 5.738 MSPS
Streaming at 5.833 MSPS
Streaming at 5.833 MSPS
Streaming at 4.985 MSPS
Streaming at 5.351 MSPS
Streaming at 5.481 MSPS
Streaming at 5.669 MSPS
Streaming at 5.669 MSPS
Streaming at 4.826 MSPS
Streaming at 5.255 MSPS
Streaming at 5.404 MSPS
Streaming at 5.618 MSPS
Streaming at 5.618 MSPS
Streaming at 4.783 MSPS
Streaming at 5.277 MSPS
Streaming at 5.422 MSPS
Streaming at 5.630 MSPS
Streaming at 5.630 MSPS
Streaming at 4.805 MSPS
Streaming at 5.333 MSPS
Streaming at 5.574 MSPS
Streaming at 5.659 MSPS
Streaming at 5.659 MSPS
Streaming at 5.659 MSPS
Streaming at 5.191 MSPS
Streaming at 5.482 MSPS
Streaming at 5.586 MSPS
Streaming at 5.669 MSPS
Streaming at 5.669 MSPS
Streaming at 4.804 MSPS
Streaming at 5.235 MSPS
Streaming at 5.506 MSPS
Streaming at 5.506 MSPS
Streaming at 5.506 MSPS
Streaming at 4.624 MSPS
Streaming at 5.134 MSPS
Streaming at 5.446 MSPS
Streaming at 5.645 MSPS
Streaming at 5.716 MSPS
Streaming at 5.818 MSPS
Streaming at 5.884 MSPS
Streaming at 5.925 MSPS
Streaming at 5.925 MSPS
Streaming at 5.130 MSPS
Streaming at 5.444 MSPS
Streaming at 5.644 MSPS
Streaming at 5.772 MSPS
Streaming at 5.215 MSPS
Streaming at 5.640 MSPS
Streaming at 5.771 MSPS
Streaming at 5.771 MSPS

User cancel, exiting...
Total time: 78.9924 s
Average speed 5.5353 MSPS IQ
done
```

### 3. AirSpy 10MSPS on SD card1

```
/home/pi# airspy_rx -r as_10M.raw -f 635 -a 10000000 -t 2 -v 14 -m 15 -l 14 -n 600000000
Device Serial Number: 0xA74068C830933C93
Stop with Ctrl-C
Streaming at 10.019 MSPS
Streaming at 9.992 MSPS
Streaming at 9.937 MSPS
Streaming at 8.831 MSPS
Streaming at 7.526 MSPS
Streaming at 7.526 MSPS
Streaming at 7.526 MSPS
Streaming at 6.231 MSPS
Streaming at 8.079 MSPS
Streaming at 8.998 MSPS
Streaming at 8.365 MSPS
Streaming at 8.095 MSPS
Streaming at 8.095 MSPS
Streaming at 8.095 MSPS
Streaming at 6.684 MSPS
Streaming at 6.684 MSPS
Streaming at 7.371 MSPS
Streaming at 8.635 MSPS
Streaming at 9.298 MSPS
Streaming at 8.276 MSPS
Streaming at 8.276 MSPS
Streaming at 8.276 MSPS
Streaming at 8.276 MSPS
Streaming at 7.957 MSPS
Streaming at 8.935 MSPS
Streaming at 8.935 MSPS
Streaming at 8.935 MSPS
Streaming at 8.086 MSPS
Streaming at 9.194 MSPS
Streaming at 9.570 MSPS
Streaming at 9.570 MSPS
Streaming at 8.488 MSPS
Streaming at 9.019 MSPS
Streaming at 9.019 MSPS
Streaming at 8.926 MSPS
Streaming at 8.926 MSPS
Streaming at 8.038 MSPS
Streaming at 8.977 MSPS
Streaming at 8.617 MSPS
Streaming at 7.527 MSPS
Streaming at 7.527 MSPS
Streaming at 6.313 MSPS
Streaming at 8.287 MSPS
Streaming at 8.682 MSPS
Streaming at 8.365 MSPS
Streaming at 8.365 MSPS
Streaming at 8.365 MSPS
Streaming at 8.088 MSPS
Streaming at 8.783 MSPS
Streaming at 8.391 MSPS
Streaming at 8.391 MSPS
Streaming at 8.391 MSPS
Streaming at 7.289 MSPS
Streaming at 8.594 MSPS
Streaming at 8.468 MSPS
Streaming at 8.468 MSPS
Streaming at 8.468 MSPS
Streaming at 7.864 MSPS
Streaming at 8.079 MSPS
Streaming at 8.710 MSPS
Streaming at 8.710 MSPS
Streaming at 8.710 MSPS
Streaming at 7.780 MSPS
Streaming at 8.845 MSPS
Streaming at 8.806 MSPS
Streaming at 8.806 MSPS
Streaming at 7.998 MSPS
Streaming at 8.957 MSPS
Streaming at 8.897 MSPS
Streaming at 8.570 MSPS
Streaming at 8.570 MSPS
Streaming at 8.570 MSPS
Streaming at 8.570 MSPS
Streaming at 7.613 MSPS
Streaming at 8.760 MSPS
Streaming at 9.347 MSPS
Streaming at 9.441 MSPS
Streaming at 9.441 MSPS
Streaming at 8.268 MSPS
Streaming at 8.393 MSPS
Streaming at 9.122 MSPS
Streaming at 9.122 MSPS
Streaming at 9.122 MSPS
Streaming at 8.035 MSPS
Streaming at 8.729 MSPS
Streaming at 7.438 MSPS
Streaming at 7.438 MSPS
Streaming at 7.438 MSPS
Streaming at 6.181 MSPS
Streaming at 8.187 MSPS
Streaming at 9.053 MSPS
Streaming at 9.053 MSPS
Streaming at 8.706 MSPS
Streaming at 7.624 MSPS
Streaming at 8.766 MSPS
Streaming at 8.664 MSPS
Streaming at 8.664 MSPS
Streaming at 8.664 MSPS
Streaming at 8.664 MSPS
Streaming at 7.108 MSPS
Streaming at 8.502 MSPS
Streaming at 8.593 MSPS
Streaming at 9.262 MSPS
Streaming at 8.882 MSPS
Streaming at 8.703 MSPS
Streaming at 8.400 MSPS
Streaming at 8.400 MSPS
Streaming at 8.400 MSPS
Streaming at 8.400 MSPS
Streaming at 8.009 MSPS
Streaming at 8.982 MSPS
Streaming at 8.982 MSPS
Streaming at 8.982 MSPS
Streaming at 8.545 MSPS
Streaming at 9.237 MSPS
Streaming at 9.382 MSPS

User cancel, exiting...
Total time: 116.0110 s
Average speed 8.3668 MSPS IQ
done
```

### 4. AirSpy 3MSPS on Samsung SSD

```
# airspy_rx -r as_3M.raw -f 635 -a 3000000 -t 2 -v 14 -m 15 -l 14 -n 180000000
Device Serial Number: 0xA74068C830933C93
Stop with Ctrl-C
Streaming at 3.000 MSPS
Streaming at 3.002 MSPS
Streaming at 3.001 MSPS
Streaming at 3.001 MSPS
Streaming at 3.001 MSPS
Streaming at 3.002 MSPS
Streaming at 3.002 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.001 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 2.999 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.001 MSPS
Streaming at 3.000 MSPS
Streaming at 3.001 MSPS
Streaming at 2.999 MSPS
Streaming at 3.000 MSPS
Streaming at 3.001 MSPS
Streaming at 2.999 MSPS
Streaming at 2.999 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.001 MSPS
Streaming at 3.000 MSPS
Streaming at 2.999 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.001 MSPS
Streaming at 3.000 MSPS
Streaming at 3.001 MSPS
Streaming at 3.001 MSPS
Streaming at 2.999 MSPS
Streaming at 3.001 MSPS
Streaming at 2.999 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS

User cancel, exiting...
Total time: 60.9824 s
Average speed 3.0002 MSPS IQ
done
```

### 5. AirSpy 6MSPS on Samsung SSD

```
root@raspberrypi:/media/pi/Samsung_T5# airspy_rx -r as_6M.raw -f 635 -a 6000000 -t 2 -v 14 -m 15 -l 14 -n 360000000
Device Serial Number: 0xA74068C830933C93
Stop with Ctrl-C
Streaming at 6.003 MSPS
Streaming at 6.003 MSPS
Streaming at 5.865 MSPS
Streaming at 5.724 MSPS
Streaming at 5.512 MSPS
Streaming at 5.382 MSPS
Streaming at 5.333 MSPS
Streaming at 5.268 MSPS
Streaming at 5.251 MSPS
Streaming at 5.224 MSPS
Streaming at 5.213 MSPS
Streaming at 5.200 MSPS
Streaming at 5.181 MSPS
Streaming at 5.176 MSPS
Streaming at 5.172 MSPS
Streaming at 5.168 MSPS
Streaming at 5.160 MSPS
Streaming at 5.160 MSPS
Streaming at 5.151 MSPS
Streaming at 5.152 MSPS
Streaming at 5.156 MSPS
Streaming at 5.157 MSPS
Streaming at 5.157 MSPS
Streaming at 5.157 MSPS
Streaming at 5.160 MSPS
Streaming at 5.158 MSPS
Streaming at 5.159 MSPS
Streaming at 5.165 MSPS
Streaming at 5.165 MSPS
Streaming at 5.164 MSPS
Streaming at 5.156 MSPS
Streaming at 5.155 MSPS
Streaming at 5.152 MSPS
Streaming at 5.157 MSPS
Streaming at 5.160 MSPS
Streaming at 5.161 MSPS
Streaming at 5.162 MSPS
Streaming at 5.162 MSPS
Streaming at 5.163 MSPS
Streaming at 5.169 MSPS
Streaming at 5.164 MSPS
Streaming at 5.157 MSPS
Streaming at 5.160 MSPS
Streaming at 5.156 MSPS
Streaming at 5.149 MSPS
Streaming at 5.151 MSPS
Streaming at 5.150 MSPS
Streaming at 5.152 MSPS
Streaming at 5.154 MSPS
Streaming at 5.152 MSPS
Streaming at 5.150 MSPS
Streaming at 5.147 MSPS
Streaming at 5.141 MSPS
Streaming at 5.145 MSPS
Streaming at 5.145 MSPS
Streaming at 5.149 MSPS
Streaming at 5.154 MSPS
Streaming at 5.150 MSPS
Streaming at 5.156 MSPS
Streaming at 5.159 MSPS
Streaming at 5.161 MSPS
Streaming at 5.162 MSPS
Streaming at 5.167 MSPS
Streaming at 5.151 MSPS
Streaming at 5.149 MSPS
Streaming at 5.149 MSPS
Streaming at 5.150 MSPS
Streaming at 5.147 MSPS
Streaming at 5.146 MSPS
Streaming at 5.146 MSPS

User cancel, exiting...
Total time: 69.9960 s
Average speed 5.2189 MSPS IQ
done
```


### 6. AirSpy 10MSPS on Samsung SSD

```
# airspy_rx -r as_10M.raw -f 635 -a 10000000 -t 2 -v 14 -m 15 -l 14 -n 600000000
Device Serial Number: 0xA74068C830933C93
Stop with Ctrl-C
Streaming at 10.016 MSPS
Streaming at 9.078 MSPS
Streaming at 8.297 MSPS
Streaming at 7.159 MSPS
Streaming at 6.761 MSPS
Streaming at 6.185 MSPS
Streaming at 5.984 MSPS
Streaming at 5.693 MSPS
Streaming at 5.504 MSPS
Streaming at 5.434 MSPS
Streaming at 5.338 MSPS
Streaming at 5.300 MSPS
Streaming at 5.252 MSPS
Streaming at 5.223 MSPS
Streaming at 5.219 MSPS
Streaming at 5.203 MSPS
Streaming at 5.205 MSPS
Streaming at 5.201 MSPS
Streaming at 5.196 MSPS
Streaming at 5.183 MSPS
Streaming at 5.180 MSPS
Streaming at 5.177 MSPS
Streaming at 5.170 MSPS
Streaming at 5.161 MSPS
Streaming at 5.153 MSPS
Streaming at 5.172 MSPS
Streaming at 5.168 MSPS
Streaming at 5.168 MSPS
Streaming at 5.171 MSPS
Streaming at 5.170 MSPS
Streaming at 5.169 MSPS
Streaming at 5.168 MSPS
Streaming at 5.170 MSPS
Streaming at 5.161 MSPS
Streaming at 5.161 MSPS
Streaming at 5.161 MSPS
Streaming at 5.157 MSPS
Streaming at 5.158 MSPS
Streaming at 5.161 MSPS
Streaming at 5.152 MSPS
Streaming at 5.155 MSPS
Streaming at 5.159 MSPS
Streaming at 5.163 MSPS
Streaming at 5.160 MSPS
Streaming at 5.166 MSPS
Streaming at 5.167 MSPS
Streaming at 5.164 MSPS
Streaming at 5.167 MSPS
Streaming at 5.167 MSPS
Streaming at 5.164 MSPS
Streaming at 5.149 MSPS
Streaming at 5.155 MSPS
Streaming at 5.146 MSPS
Streaming at 5.139 MSPS
Streaming at 5.141 MSPS
Streaming at 5.144 MSPS
Streaming at 5.139 MSPS
Streaming at 5.137 MSPS
Streaming at 5.139 MSPS
Streaming at 5.139 MSPS
Streaming at 5.148 MSPS
Streaming at 5.152 MSPS
Streaming at 5.143 MSPS
Streaming at 5.154 MSPS
Streaming at 5.162 MSPS
Streaming at 5.163 MSPS
Streaming at 5.169 MSPS
Streaming at 5.168 MSPS
Streaming at 5.165 MSPS
Streaming at 5.157 MSPS
Streaming at 5.160 MSPS
Streaming at 5.154 MSPS
Streaming at 5.157 MSPS
Streaming at 5.153 MSPS
Streaming at 5.144 MSPS
Streaming at 5.148 MSPS
Streaming at 5.143 MSPS
Streaming at 5.141 MSPS
Streaming at 5.144 MSPS
Streaming at 5.144 MSPS
Streaming at 5.146 MSPS
Streaming at 5.144 MSPS
Streaming at 5.148 MSPS
Streaming at 5.140 MSPS
Streaming at 5.146 MSPS
Streaming at 5.150 MSPS
Streaming at 5.149 MSPS
Streaming at 5.152 MSPS
Streaming at 5.145 MSPS
Streaming at 5.142 MSPS
Streaming at 5.145 MSPS
Streaming at 5.076 MSPS
Streaming at 5.096 MSPS
Streaming at 5.098 MSPS
Streaming at 5.120 MSPS
Streaming at 5.126 MSPS
Streaming at 5.124 MSPS
Streaming at 5.126 MSPS
Streaming at 5.127 MSPS
Streaming at 5.135 MSPS
Streaming at 5.098 MSPS
Streaming at 5.109 MSPS
Streaming at 5.114 MSPS
Streaming at 5.036 MSPS
Streaming at 4.951 MSPS
Streaming at 5.039 MSPS
Streaming at 5.040 MSPS
Streaming at 5.075 MSPS
Streaming at 5.101 MSPS
Streaming at 5.104 MSPS
Streaming at 5.070 MSPS
Streaming at 5.066 MSPS
Streaming at 5.063 MSPS
Streaming at 5.061 MSPS
Streaming at 4.999 MSPS
Streaming at 4.977 MSPS

User cancel, exiting...
Total time: 116.0130 s
Average speed 5.3539 MSPS IQ
done
```

### 7. AirSpy 10MSPS on SD card2

The test was done on disconnected antenna, but I don't think it matters.

```
# airspy_rx -r as_10M.raw -f 635 -a 10000000 -t 2 -v 14 -m 15 -l 14 -n 600000000
Device Serial Number: 0xA74068C830933C93
Stop with Ctrl-C
Streaming at 10.016 MSPS
Streaming at 10.010 MSPS
Streaming at 10.035 MSPS
Streaming at 10.026 MSPS
Streaming at 10.008 MSPS
Streaming at 8.657 MSPS
Streaming at 9.419 MSPS
Streaming at 9.717 MSPS
Streaming at 9.878 MSPS
Streaming at 9.937 MSPS
Streaming at 8.664 MSPS
Streaming at 9.355 MSPS
Streaming at 9.676 MSPS
Streaming at 9.847 MSPS
Streaming at 9.921 MSPS
Streaming at 9.937 MSPS
Streaming at 9.093 MSPS
Streaming at 9.553 MSPS
Streaming at 9.817 MSPS
Streaming at 9.906 MSPS
Streaming at 8.640 MSPS
Streaming at 9.291 MSPS
Streaming at 9.665 MSPS
Streaming at 9.807 MSPS
Streaming at 9.923 MSPS
Streaming at 9.310 MSPS
Streaming at 9.647 MSPS
Streaming at 9.819 MSPS
Streaming at 9.907 MSPS
Streaming at 9.967 MSPS
Streaming at 9.227 MSPS
Streaming at 9.607 MSPS
Streaming at 9.740 MSPS
Streaming at 9.907 MSPS
Streaming at 9.981 MSPS
Streaming at 8.772 MSPS
Streaming at 9.320 MSPS
Streaming at 9.701 MSPS
Streaming at 9.861 MSPS
Streaming at 9.929 MSPS
Streaming at 8.809 MSPS
Streaming at 9.389 MSPS
Streaming at 9.638 MSPS
Streaming at 9.849 MSPS
Streaming at 9.941 MSPS
Streaming at 9.185 MSPS
Streaming at 9.583 MSPS
Streaming at 9.786 MSPS
Streaming at 9.833 MSPS
Streaming at 9.953 MSPS
Streaming at 8.576 MSPS
Streaming at 9.292 MSPS
Streaming at 9.638 MSPS
Streaming at 9.815 MSPS
Streaming at 9.832 MSPS
Streaming at 8.671 MSPS
Streaming at 9.488 MSPS
Streaming at 9.753 MSPS
Streaming at 9.874 MSPS
Streaming at 9.936 MSPS
Streaming at 8.604 MSPS
Streaming at 9.355 MSPS
Streaming at 9.674 MSPS
Streaming at 9.833 MSPS
Streaming at 9.914 MSPS
Streaming at 9.018 MSPS
Streaming at 9.408 MSPS
Streaming at 9.628 MSPS

User cancel, exiting...
Total time: 67.9956 s
Average speed 9.5926 MSPS IQ
done
```

### 8. AirSpy 6MSPS on SD card2

```
# airspy_rx -r as_6M.raw -f 635 -a 6000000 -t 2 -v 14 -m 15 -l 14 -n 360000000
Device Serial Number: 0xA74068C830933C93
Stop with Ctrl-C
Streaming at 6.011 MSPS
Streaming at 6.003 MSPS
Streaming at 6.005 MSPS
Streaming at 6.004 MSPS
Streaming at 5.997 MSPS
Streaming at 5.667 MSPS
Streaming at 5.791 MSPS
Streaming at 5.860 MSPS
Streaming at 5.912 MSPS
Streaming at 5.934 MSPS
Streaming at 5.958 MSPS
Streaming at 5.973 MSPS
Streaming at 5.984 MSPS
Streaming at 5.989 MSPS
Streaming at 5.967 MSPS
Streaming at 6.001 MSPS
Streaming at 6.001 MSPS
Streaming at 6.000 MSPS
Streaming at 6.000 MSPS
Streaming at 6.000 MSPS
Streaming at 5.579 MSPS
Streaming at 5.731 MSPS
Streaming at 5.828 MSPS
Streaming at 5.891 MSPS
Streaming at 5.913 MSPS
Streaming at 5.295 MSPS
Streaming at 5.686 MSPS
Streaming at 5.800 MSPS
Streaming at 5.867 MSPS
Streaming at 5.896 MSPS
Streaming at 5.896 MSPS
Streaming at 5.448 MSPS
Streaming at 5.647 MSPS
Streaming at 5.774 MSPS
Streaming at 5.856 MSPS
Streaming at 5.856 MSPS
Streaming at 5.079 MSPS
Streaming at 5.410 MSPS
Streaming at 5.623 MSPS
Streaming at 5.759 MSPS
Streaming at 5.759 MSPS
Streaming at 4.999 MSPS
Streaming at 5.360 MSPS
Streaming at 5.586 MSPS
Streaming at 5.739 MSPS
Streaming at 5.739 MSPS
Streaming at 4.975 MSPS
Streaming at 5.345 MSPS
Streaming at 5.545 MSPS
Streaming at 5.736 MSPS
Streaming at 5.736 MSPS
Streaming at 4.957 MSPS
Streaming at 5.333 MSPS
Streaming at 5.573 MSPS
Streaming at 5.727 MSPS
Streaming at 5.727 MSPS
Streaming at 4.929 MSPS
Streaming at 5.315 MSPS
Streaming at 5.561 MSPS
Streaming at 5.649 MSPS
Streaming at 5.782 MSPS
Streaming at 5.863 MSPS
Streaming at 5.913 MSPS
Streaming at 5.940 MSPS
Streaming at 5.965 MSPS
Streaming at 5.617 MSPS
Streaming at 5.756 MSPS
Streaming at 5.839 MSPS
Streaming at 5.839 MSPS

User cancel, exiting...
Total time: 69.0022 s
Average speed 5.7156 MSPS IQ
done
```

### 8. AirSpy 3MSPS on SD card2

```
# airspy_rx -r as_3M.raw -f 635 -a 3000000 -t 2 -v 14 -m 15 -l 14 -n 180000000
Device Serial Number: 0xA74068C830933C93
Stop with Ctrl-C
Streaming at 3.000 MSPS
Streaming at 2.990 MSPS
Streaming at 3.002 MSPS
Streaming at 3.001 MSPS
Streaming at 3.001 MSPS
Streaming at 3.001 MSPS
Streaming at 2.742 MSPS
Streaming at 2.792 MSPS
Streaming at 2.834 MSPS
Streaming at 2.867 MSPS
Streaming at 2.894 MSPS
Streaming at 2.915 MSPS
Streaming at 2.932 MSPS
Streaming at 2.945 MSPS
Streaming at 2.945 MSPS
Streaming at 2.787 MSPS
Streaming at 2.923 MSPS
Streaming at 2.938 MSPS
Streaming at 2.950 MSPS
Streaming at 2.960 MSPS
Streaming at 2.915 MSPS
Streaming at 2.930 MSPS
Streaming at 2.930 MSPS
Streaming at 2.945 MSPS
Streaming at 2.956 MSPS
Streaming at 2.965 MSPS
Streaming at 2.972 MSPS
Streaming at 2.977 MSPS
Streaming at 2.981 MSPS
Streaming at 2.986 MSPS
Streaming at 2.990 MSPS
Streaming at 2.992 MSPS
Streaming at 2.994 MSPS
Streaming at 2.993 MSPS
Streaming at 2.993 MSPS
Streaming at 2.995 MSPS
Streaming at 2.996 MSPS
Streaming at 2.997 MSPS
Streaming at 2.999 MSPS
Streaming at 2.998 MSPS
Streaming at 2.998 MSPS
Streaming at 2.998 MSPS
Streaming at 3.000 MSPS
Streaming at 3.000 MSPS
Streaming at 2.999 MSPS
Streaming at 2.999 MSPS
Streaming at 2.999 MSPS
Streaming at 3.000 MSPS
Streaming at 2.999 MSPS
Streaming at 2.997 MSPS
Streaming at 2.990 MSPS
Streaming at 2.990 MSPS
Streaming at 2.992 MSPS
Streaming at 2.994 MSPS
Streaming at 2.997 MSPS
Streaming at 2.997 MSPS
Streaming at 2.797 MSPS
Streaming at 2.836 MSPS
Streaming at 2.869 MSPS
Streaming at 2.895 MSPS
Streaming at 2.918 MSPS
Streaming at 2.918 MSPS

User cancel, exiting...
Total time: 62.0110 s
Average speed 2.9504 MSPS IQ
done
```



## Useful links for further study

- Great raspi SD cards benchmark: http://www.pidramble.com/wiki/benchmarks/microsd-cards#4-model-b
- raspi SD host overclocking: https://forums.raspberrypi.com/viewtopic.php?p=930812
- raspi SD host overclocking report (claims to increase performance from 21 to 42MB/sec): https://forums.raspberrypi.com/viewtopic.php?p=911543
- Slow SSD 3.0 devices and how to fix this (my setup does not seem to be affected by this issue): https://forums.raspberrypi.com/viewtopic.php?f=28&t=245931



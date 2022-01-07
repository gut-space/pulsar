# Various SDR performance tests

## Raspberry Pi

Tests conducted on Raspberry Pi 4 B with two storage options:

- SD card: SanDisk SANDISK Ultra microSDXC 64GB 120MB/s (C10, U1, A1, exact model: SDSQUA4-064G-GN6MA).
- External SSD disk: Samsung T5 500GB, with claimed rate of 540MB/s
- SDR used: AirSpy Mini

Each test was designed to last 60 seconds, with the appropriate number of samples chosen to correspond to the sampling rate. Tests were run in the console, using airspy_rx version 1.0.6.

The SSD disk was completely empty. The SSD card had the Raspberry Pi system on it with some software. 12 out of 64GB was used.

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

### 1. AirSpy 3MSPS on SD Card

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

### 2. AirSpy 6MSPS on SD Card

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

## 3. AirSpy 10MSPS on SD card

```

```

### 4. AirSpy 3MSPS on Samsung SSD

### 5. AirSpy 6MSPS on Samsung SSD

### 6. AirSpy 10MSPS on Samsung SSD

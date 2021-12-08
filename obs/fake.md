This is not a real observation. It's a generated `.fil` file that was created using `fake` tool from `sigproc`. It was created using the following command:

`fake -period 714 -nbits 16 -nchans 16 -tobs 30 -fch1 463.1875 -foff 0.375 > fake.fil`

Parameters mean period 714ms, samples are 16 bits, there are 16 channels, simulated observation was 30s, the first channel was 463.18175, each channel width is 0.375MHz. The parameters were chosen so to get something as close to [2021-10-24](obs/2021-10-24.md) observation as possible.

## `.fil` file

Inspecting the file:

```
$readfile fake.fil 
Assuming the data is a SIGPROC filterbank file.


1: From the SIGPROC filterbank file 'fake.fil':
                  Telescope = Parkes
                Source Name = P: 714.000000000000 ms, DM: 715.662
                    Backend = Unknown
            Obs Date String = 1995-10-10T00:00:00
             MJD start time = 50000.00000000000000
                   RA J2000 = 00:00:00.0000
             RA J2000 (deg) = 0                
                  Dec J2000 = 00:00:00.0000
            Dec J2000 (deg) = 0                
                  Tracking? = True
              Azimuth (deg) = 1.976263e-323
           Zenith Ang (deg) = 6.931535e-310
            Number of polns = 2 (summed)
           Sample time (us) = 80               
         Central freq (MHz) = 460.375          
          Low channel (MHz) = 457.5625         
         High channel (MHz) = 463.1875         
        Channel width (MHz) = 0.375            
         Number of channels = 16
      Total Bandwidth (MHz) = 6                
                       Beam = 1 of 1
            Beam FWHM (deg) = 0.700
         Spectra per subint = 2400
           Spectra per file = 375296
      Time per subint (sec) = 0.192
        Time per file (sec) = 30.02368
            bits per sample = 16
          bytes per spectra = 32
        samples per spectra = 16
           bytes per subint = 76800
         samples per subint = 38400
                zero offset = 0                
           Invert the band? = False
       bytes in file header = 245
```

## Searching for interference

After some experiments (-time 10, -time 1, -time 3, -time 10 -noclip) I found that -time 3 works best.

Bad attempt:

```
$ rfifind -time 10 -o fake10 fake.fil 


               Pulsar Data RFI Finder
                 by Scott M. Ransom

Assuming the data are SIGPROC filterbank format...
Reading SIGPROC filterbank data from 1 file:
  'fake.fil'

    Number of files = 1
       Num of polns = 2 (summed)
  Center freq (MHz) = 460.375
    Num of channels = 16
    Sample time (s) = 8e-05         
     Spectra/subint = 2400
   Total points (N) = 375296
     Total time (s) = 30.02368      
     Clipping sigma = 6.000
   Invert the band? = False
          Byteswap? = False
     Remove zeroDM? = False

File  Start Spec   Samples     Padding        Start MJD
----  ----------  ----------  ----------  --------------------
1              0      375296           0  50000.00000000000000

Analyzing data sections of length 124800 points (9.984 sec).
  Prime factors are:  2 2 2 2 2 2 2 3 5 5 13 

Writing mask data  to 'fake10_rfifind.mask'.
Writing  RFI data  to 'fake10_rfifind.rfi'.
Writing statistics to 'fake10_rfifind.stats'.

Massaging the data ...

Amount Complete = 100%
There are 99 RFI instances.


Total number of intervals in the data:  64

  Number of padded intervals:       16  (25.000%)
  Number of  good  intervals:        0  ( 0.000%)
  Number of  bad   intervals:       48  (75.000%)

  Ten most significant birdies:
#  Sigma     Period(ms)      Freq(Hz)       Number 
----------------------------------------------------
1  9.87      118.857         8.41346        248     
2  9.82      119.569         8.36338        238     
3  8.78      178.286         5.60897        233     
4  8.41      179.892         5.55889        201     
5  8.05      356.571         2.80449        242     
6  7.50      59.606          16.7768        114     
7  7.48      89.5426         11.1679        155     
8  7.41      47.8849         20.8834        3       
9  7.40      363.055         2.75441        203     
10 7.38      59.4286         16.8269        117     

  Ten most numerous birdies:
#  Number    Period(ms)      Freq(Hz)       Sigma 
----------------------------------------------------
1  248       118.857         8.41346        9.87    
2  242       356.571         2.80449        8.05    
3  238       119.569         8.36338        9.82    
4  233       178.286         5.60897        8.78    
5  203       363.055         2.75441        7.40    
6  201       179.892         5.55889        8.41    
7  200       237.714         4.20673        6.90    
8  179       89.1429         11.2179        7.11    
9  160       118.154         8.46354        7.19    
10 155       89.5426         11.1679        7.48    

Done.
```

Good attempt:
```
$ rfifind -time 3 -o rfifind_time3 fake.fil 


               Pulsar Data RFI Finder
                 by Scott M. Ransom

Assuming the data are SIGPROC filterbank format...
Reading SIGPROC filterbank data from 1 file:
  'fake.fil'

    Number of files = 1
       Num of polns = 2 (summed)
  Center freq (MHz) = 460.375
    Num of channels = 16
    Sample time (s) = 8e-05         
     Spectra/subint = 2400
   Total points (N) = 375296
     Total time (s) = 30.02368      
     Clipping sigma = 6.000
   Invert the band? = False
          Byteswap? = False
     Remove zeroDM? = False

File  Start Spec   Samples     Padding        Start MJD
----  ----------  ----------  ----------  --------------------
1              0      375296           0  50000.00000000000000

Analyzing data sections of length 38400 points (3.072 sec).
  Prime factors are:  2 2 2 2 2 2 2 2 2 3 5 5 

Writing mask data  to 'rfifind_time3_rfifind.mask'.
Writing  RFI data  to 'rfifind_time3_rfifind.rfi'.
Writing statistics to 'rfifind_time3_rfifind.stats'.

Massaging the data ...

Amount Complete = 100%
There are 27 RFI instances.


Total number of intervals in the data:  160

  Number of padded intervals:       16  (10.000%)
  Number of  good  intervals:      143  (89.375%)
  Number of  bad   intervals:        1  ( 0.625%)

  Ten most significant birdies:
#  Sigma     Period(ms)      Freq(Hz)       Number 
----------------------------------------------------
1  5.95      61.44           16.276         1       
2  5.84      60.8317         16.4388        2       
3  5.70      62.0606         16.1133        1       
4  5.65      186.182         5.37109        1       
5  5.47      62.6939         15.9505        1       
6  5.21      87.7714         11.3932        1       
7  4.94      90.3529         11.0677        7       
8  4.69      59.6505         16.7643        18      
9  4.69      175.543         5.69661        1       
10 4.65      118.154         8.46354        20      

  Ten most numerous birdies:
#  Number    Period(ms)      Freq(Hz)       Sigma 
----------------------------------------------------
1  20        118.154         8.46354        4.65    
2  18        59.6505         16.7643        4.69    
3  8         180.706         5.53385        4.57    
4  8         120.471         8.30078        4.35    
5  7         90.3529         11.0677        4.94    
6  6         60.2353         16.6016        4.45    
7  6         59.0769         16.9271        4.41    
8  5         91.7015         10.9049        4.52    
9  4         236.308         4.23177        4.59    
10 3         102.4           9.76562        4.37    

Done.
```

I'm particularly pleased with the good intervals being 89%. This is what the rfifind generated in the .ps file. .ps files can be viewed with gv tool.

![fake-rfifind](https://user-images.githubusercontent.com/663576/145277398-52bf64e7-55d3-4a96-93e9-21100b50796a.png)

## Looking for low-level RFI

`prepdata -nobary -o rfifind_time3_rfifind_zerodm -dm 0.0 -mask rfifind_time3_rfifind.mask fake.fil`

This step generated `rfifind_time3_rfifind_zerodm.dat` file. It can be explored using `exploredat rfifind_time3_rfifind_zerodm.dat`.

![fake-exploredat](https://user-images.githubusercontent.com/663576/145277966-80052882-1ba7-4096-8061-aae514448d3f.png)

`realfft rfifind_time3_rfifind_zerodm.dat` then processed the data through another FFT. The resulting file (`rfifind_time3_rfifind_zerodm.fft`) can be viewed with explorefft. To view anything useful, I had to change the Y scale a bit (hit + couple times).

![fake-explore-fft](https://user-images.githubusercontent.com/663576/145278726-13128d2d-2c51-451c-bb9b-a88cfb652060.png)

## Searching



```
$ accelsearch -numharm 4 -zmax 0 rfifind_time3_rfifind_zerodm.dat 


    Fourier-Domain Acceleration and Jerk Search Routine
                    by Scott M. Ransom

Analyzing P: 714.000000000000 ms, DM: 715.662 data from 'rfifind_time3_rfifind_zerodm.dat'.

Reading and FFTing the time series...done.
Removing red-noise...done.

Normalizing powers using median-blocks (default).

Full f-fdot plane would need 0.00 GB: using in-memory accelsearch.

Searching with up to 4 harmonics summed:
  f = 1.0 to 6250.0 Hz
  r = 30.0 to 191999.0 Fourier bins
  z = 0.0 to 0.0 Fourier bins drifted

Generating correlation kernels:
  Harm  1/1 :     1 kernels,    0 < z < 0    (2048 pt FFTs)
Total RAM used by correlation kernels:  0.000 GB
Done generating kernels.

Starting the search.

Amount of search complete = 100%

Done searching.  Now optimizing each candidate.

Removed 9 likely harmonically related candidates.
Amount of optimization complete = 100%
width < len (14) in center_string(outstring, ' 0.3(2.2)x10^1', width=12)


Searched the following approx numbers of independent points:
  1 harmonic:      191969
  2 harmonics:      95984
  4 harmonics:      47992

Timing summary:
    CPU time: 0.040 sec (User: 0.040 sec, System: 0.000 sec)
  Total time: 0.050 sec

Final candidates in binary format are in 'rfifind_time3_rfifind_zerodm_ACCEL_0.cand'.
Final Candidates in a text format are in 'rfifind_time3_rfifind_zerodm_ACCEL_0'.
```

Those two files (rfifind_time3_rfifind_zerodm_ACCEL_0 and rfifind_time3_rfifind_zerodm_ACCEL_0.cand) are super useful.

Here's content of the rfifind_time3_rfifind_zerodm_ACCEL_0 file:

```
             Summed  Coherent  Num        Period          Frequency         FFT 'r'        Freq Deriv       FFT 'z'         Accel...........................
Cand  Sigma  Power    Power    Harm        (ms)             (Hz)             (bin)           (Hz/s)         (bins)         (m/s^2)             Notes........
------------------------------------------------------------------------------------------------------------------------------------------------------------
1     20.77  245.12   93.63     4         714(2)           1.400(4)        43.00(13)        0.0000(5)       0.00(50)    0.0(1.1)x10^5.........................
2     4.23   23.53    18.53     1        23.028(9)         43.42(2)       1334.00(50)        0.000(2)       0.0(2.0)    0.0(1.5)x10^4     H 30 of Cand 1
3     2.73   17.93    10.85     1      0.1691378(5)       5912.34(2)     181627.00(50)       0.000(2)       0.0(2.0)    0.0(1.1)x10^2.........................
4     2.29   23.03     5.70     4       1.126647(5)       887.590(4)      27266.75(13)      0.0000(5)       0.00(50)    0.0(1.8)x10^2.........................


                        Power /          Raw           FFT 'r'          Pred 'r'       FFT 'z'     Pred 'z'      Phase       Centroid     Purity........................
Cand   Harm  Sigma      Loc Pow         Power           (bin)             (bin)         (bins)      (bins)       (rad)        (0-1)      <p> = 1           Notes........
------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 1     1     21.83      242(22)          202          43.010(25)          43.00        0.09(20)      0.00       1.727(45)    0.487(13)   0.982(21)........................
       2     0.00       0.27(73)        0.343          86.02(36)          86.00        0.2(1.3)      0.00       0.2(1.4)     0.12(39)    2.09(29).........................
       3     8.14      36.2(8.5)        45.9          129.029(63)        129.00        0.28(48)      0.00       2.13(12)     0.421(34)   1.026(51)........................
       4     0.63       1.3(1.6)        1.66          172.04(33)         172.00        0.4(2.5)      0.00       5.77(61)     0.39(18)    1.03(27).........................
 2     1     5.63      18.5(6.1)        27.2         1333.790(90)        1334.00      -0.53(70)      0.00       0.42(16)     0.480(47)   1.002(73)........................
 3     1     4.11      10.9(4.7)        19.3         181627.13(13)      181627.00     -1.7(1.2)      0.00       1.16(21)     0.506(62)   0.89(11).........................
 4     1     1.63       3.0(2.4)        2.52         27265.75(80)       27266.75      0.3(2.2)x10    0.00       3.90(41)     0.69(12)    0.28(64).........................
       2     3.28       7.6(3.9)        6.57         54531.50(13)       54533.50       6.75(91)      0.00       5.37(26)     0.544(74)   1.10(10).........................
       3     1.11       2.0(2.0)         2.8         81797.26(26)       81800.25       10.1(1.9)     0.00       1.80(50)     0.60(14)    1.06(21).........................
       4     1.76       3.2(2.5)        2.72         109063.01(30)      109067.00      13.5(3.2)     0.00       5.01(39)     0.47(11)    0.73(24).........................


 Data file name without suffix          =  rfifind_time3_rfifind_zerodm
 Telescope used                         =  Parkes
 Instrument used                        =  Unknown
 Object being observed                  =  P: 714.000000000000 ms, DM: 715.662
 J2000 Right Ascension (hh:mm:ss.ssss)  =  00:00:00.0000
 J2000 Declination     (dd:mm:ss.ssss)  =  00:00:00.0000
 Data observed by                       =  unset
 Epoch of observation (MJD)             =  50000.000000000000000
 Barycentered?           (1 yes, 0 no)  =  0
 Number of bins in the time series      =  384000.....
 Width of each time series bin (sec)    =  8e-05
 Any breaks in the data? (1 yes, 0 no)  =  1
 On/Off bin pair #  1                   =  0          , 374399.....
 On/Off bin pair #  2                   =  383999     , 383999.....
 Type of observation (EM band)          =  Radio
 Beam diameter (arcsec)                 =  2518
 Dispersion measure (cm-3 pc)           =  0
 Central freq of low channel (MHz)      =  457.5625
 Total bandwidth (MHz)                  =  6
 Number of channels                     =  16
 Channel bandwidth (MHz)                =  0.375
 Data analyzed by                       =  thomson
 Any additional notes:
    Project ID unset, Date: 1995-10-10T00:00:00.
    2 polns were summed.  Samples have 16 bits.
```

The most important lines are 1 and 2:

```
             Summed  Coherent  Num        Period          Frequency         FFT 'r'        Freq Deriv       FFT 'z'         Accel...........................
Cand  Sigma  Power    Power    Harm        (ms)             (Hz)             (bin)           (Hz/s)         (bins)         (m/s^2)             Notes........
------------------------------------------------------------------------------------------------------------------------------------------------------------
1     20.77  245.12   93.63     4         714(2)           1.400(4)        43.00(13)        0.0000(5)       0.00(50)    0.0(1.1)x10^5.........................
```

The prepdata found out that there is a signal with 714ms, which is exactly what was using during generation of this fake.fil

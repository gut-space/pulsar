This is not a real observation. It's a generated `.fil` file that was created using `fake` tool from `sigproc`. It was created using the following command:

`fake -period 714 -nbits 16 -nchans 16 -tobs 30 -fch1 463.1875 -foff 0.375 > fake.fil`

Parameters mean period 714ms, samplea are 16 bits, there are 16 channels, simulated observation was 30s, the first channel was 463.18175, each channel width is .375MHz.
The parameters were chosen so to get something as close to [2021-10-24](obs/2021-10-24.md) observation as possible.

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

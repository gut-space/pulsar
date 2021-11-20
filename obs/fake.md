This is not a real observation. It's a generated `.fil` file that was created using `fake` tool from `sigproc`. It was created using the following command:

`fake -period 714 -nbits 16 -nchans 16 -tobs 30 -fch1 463.1875 -foff 0.375 > fake.fil`

Parameters mean period 714ms, samplea are 16 bits, there are 16 channels, simulated observation was 30s, the first channel was 463.18175, each channel width is .375MHz.
The parameters were chosen so to get something as close to [2021-10-24](obs/2021-10-24.md) observation as possible.

# sigproc-4.3 compilation on modern systems

This description is accurate as of 2021-10-29. This will work on Ubuntu Linux for sure. You may try other distros or even MacOS or Windows if you feel adventurous.
 
Tested on Ubuntu 20.04 and 21.04.

1. Download sigproc-4.3 from http://sigproc.sourceforge.net/
2. Extract it: `tar zxvf sigproc-4.3.tar.gz`
4. `export OSTYPE=linux`
5. ./configure
6. Fix error in makefile. Edit makefile line 452 should look like this:

```export:``` (no space before semicolon)

7. Fix compilation error in Fortran. edit dosearch.f and remove apostrophe from line 265. After edits, the file should look like the following:

   ```write(llog,*) 'DBs slow-but-simple harmonic summing routine'```
   
8. Add the following to the makefile.linux:

```
FFLAGS=-c -ffixed-line-length-132 -fallow-argument-mismatch

%.o: %.f
		$(F77) $(FFLAGS) -o $@ $<
```

Explanation: by default Fortran77 requires the lines in source code to be no longer than 72 chars. This rule is broken in many places in the sigproc code.
The lines above add extra compilation flag that says lines up to 132 chars are ok. Also fixes problems with mismatching parameters.

9. Edit makefile.linux (this is only needed on Ubuntu 21.04 or later)

```CCC = gcc-9 -O2```

Explanation: the sigproc code is poorly written and defines the same variables multiple times. See https://github.com/SixByNine/sigproc/issues/7 for details. As a workaround, we can compile it with gcc 9. The standard version in Ubuntu 21.04 (gcc 10) no longer turns a blind eye on this and fails compilation.

10. Compile: `make`

# psrcat installation

1. Extract the sources: `tar zxvf psrcat-upstream-1.59.tar.gz`

2. edit file makeit and replace `gcc` with `gcc-9` in two places.

3. Run `./makeit`

4. Export `PSRCAT_FILE` variable to point to the location of psrcat.db (included in the sources), e.g.

    ```export PSRCAT_FILE=/home/thomson/radio/psrcat-upstream-1.59/psrcat.db```

# sigproc-4.3

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
FLFLAGS=-ffixed-line-length-132

%.o: %.f
		$(F77) $(FLFLAGS) -o $@ $<
```

Explanation: by default Fortran77 requires the lines in source code to be no longer than 72 chars. This rule is broken in many places in the sigproc code.
The lines above add extra compilation flag that says lines up to 132 chars are ok.

8. Compile: `make`


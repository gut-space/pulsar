# Installation instructions for GNU Radio filterbank on Ubuntu 21.04

First, you need to enable [recent GNU Radio](https://wiki.gnuradio.org/index.php/UbuntuInstall):

```
sudo add-apt-repository ppa:gnuradio/gnuradio-releases
sudo apt-get update
sudo apt-get install gnuradio
```

Second, you need to get the pulsar_filterbank code:

```git clone git@github.com:ccera-astro/pulsar_filterbank.git```

Why trying to compile, the first initial errors are easy enough:

```
$make
grcc -d . pulsar_filterbank_uhd.grc
usage: grcc [-h] [-o DIR] [-u] [-r] GRC_FILE [GRC_FILE ...]
grcc: error: unrecognized arguments: -d
```

**Solution**: Edit makefile, lines 35 and 38 and remove `-d .`.

After this change, the grcc (GNU Radio companion compiler) at least tries to do the compilation.

This time, it's complaining about old style (python 2.x) print calling:
```
ERROR:gnuradio.grc.core.FlowGraph:Failed to evaluate expression in module fb_helper
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/gnuradio/grc/core/FlowGraph.py", line 248, in renew_namespace
    exec(expr, module.__dict__)
  File "<string>", line 473
    print "No rx_time tag, start time will be approximate."
          ^
SyntaxError: Missing parentheses in call to 'print'. Did you mean print("No rx_time tag, start time will be approximate.")?
```

**Solution**: Edit fb_helper.py around line 473: add parentheses, so it look like this `print("No rx_time tag, start time will be approximate.")`. Do the same for grc_parser.py around line 65 (`print(line)`).

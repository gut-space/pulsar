# psrcat installation

1. Extract the sources: `tar zxvf psrcat-upstream-1.59.tar.gz`

2. edit file makeit and replace `gcc` with `gcc-9` in two places.

3. Run `./makeit`

4. Export `PSRCAT_FILE` variable to point to the location of psrcat.db (included in the sources), e.g.

    ```export PSRCAT_FILE=/home/thomson/radio/psrcat-upstream-1.59/psrcat.db```

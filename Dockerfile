#
# FITS2DB -- Docker container for the FITS2DB task
#
# To Build:     % docker build -t fits2db .
#
# To Run       
#       # Process a file in the current user directory:
#       % docker run fits2db --sql=postgres --create test.fits | psql
#
#       # Mount data from a path for processing:
#       % docker run -v /<path>/:/data fits2db --sql=postgres \
#                       -C /data/test.fits | psql

FROM alpine
RUN apk add --no-cache build-base
RUN apk add --no-cache curl-dev
RUN apk add --no-cache cfitsio-dev

WORKDIR /app
COPY . /app
RUN gcc -DLinux -I/usr/include/cfitsio -o fits2db fits2db.c -lcfitsio
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib
ENTRYPOINT ["/app/fits2db"] 
CMD [""]

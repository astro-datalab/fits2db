#
# FITS2DB -- Docker container for the FITS2DB task
#
# To Build:     % docker build -t fits2db .
# To Run       
#       % docker run fits2db --sql=postgres --create test.fits | psql
#       % docker run -v /<path>/:/data fits2db --sql=postgres \
#                       -C /data/test.fits | psql

FROM alpine
RUN apk add --no-cache bash
RUN apk add --no-cache build-base
RUN apk add --no-cache curl-dev
RUN apk add --no-cache cfitsio
RUN apk add --no-cache cfitsio-dev
RUN apk add --no-cache cfitsio-static

WORKDIR /app
COPY . /app
RUN gcc -DLinux -I/usr/include/cfitsio -o fits2db fits2db.c -lcfitsio
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib
ENTRYPOINT ["/app/fits2db"] 
CMD [""]

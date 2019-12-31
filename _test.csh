#!/bin/csh -f

set P = "psql tapdb datalab"


# CSV conversions
echo "=================="
echo "CSV TESTS"
echo "=================="
./fits2db --create --drop --csv -t foobar test.fits
./fits2db --create --drop --csv -t foobar test.fits | $P
$P -c "select * from foobar"
echo "=================="
./fits2db --create --drop --csv -t foobar --sid=serid test.fits
./fits2db --create --drop --csv -t foobar --sid=serid test.fits | $P
$P -c "select * from foobar"
echo "=================="
./fits2db --create --drop --csv -t foobar --sid=serid --rid=ranid test.fits
./fits2db --create --drop --csv -t foobar --sid=serid --rid=ranid test.fits | $P
$P -c "select * from foobar"

echo "=================="
echo "=================="


# Binary conversions
echo "=================="
echo "BINARY TESTS"
echo "=================="
./fits2db --create --drop --csv -t foobar -B test.fits | $P
$P -c "select * from foobar"
echo "=================="
./fits2db --create --drop --csv -t foobar -B --sid=serid test.fits | $P
$P -c "select * from foobar"
echo "=================="
./fits2db --create --drop --csv -t foobar -B --sid=serid --rid=ranid test.fits | $P
$P -c "select * from foobar"


# Clean up
psql tapdb datalab -c "drop table if exists foobar"


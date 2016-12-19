#!/bin/sh

all()
{
	cd src
	python setup.py build_ext --inplace
	cd -
}

clean()
{
	rm -f src/*.c
	rm -f src/*.so
	rm -rf build
}

### main logic ###
case "$1" in
  all)
        all
        ;;
  clean)
        clean
        ;;
  rebuild)
        clean
        all
        ;;
  *)
        echo $"Usage: $0 {all|clean|rebuild}"
        exit 1
esac

PYMOD_INC ?= $(shell python-config --includes)
PYSITE_PACKAGES ?= $(shell python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")


all:   _pwrusb.so
	echo "Make all successfully made _pwrusb.so"
	

_PwrUsbCmd.cpp:  PwrUsbCmd.cpp
	sed -e 's/".\/libpowerusb.dylib"/"libpowerusb.dylib"/g' PwrUsbCmd.cpp > _PwrUsbCmd.cpp

Mac.zip:
	curl -O http://www.pwrusb.com/downloads/Mac.zip

libpowerusb.dylib:  Mac.zip
	unzip -oq Mac.zip
	mv "`find Mac -name libpowerusb.dylib | head -1`" .

PwrUsbCmd.cpp:  Mac.zip
	unzip -oq Mac.zip
	mv "`find Mac -name PwrUsbCmd.cpp | head -1`" .

PwrUSBImp.h:  Mac.zip
	unzip -oq Mac.zip
	mv "`find Mac -name PwrUSBImp.h | head -1`" .

_pwrusb.so:  PwrUsbCmd_interface.cpp  PwrUsbCmd_interface.i  _PwrUsbCmd.cpp  libpowerusb.dylib  PwrUSBImp.h
	swig -c++ -python -o PwrUsbCmd_interface_wrap.cpp PwrUsbCmd_interface.i
	g++ -fPIC -Wall -g -c -framework IOKit -framework CoreFoundation PwrUsbCmd_interface.cpp
	g++ -fPIC -Wall -g -c -framework IOKit -framework CoreFoundation PwrUsbCmd_interface_wrap.cpp -I$(PYMOD_INC)
	ld -bundle -flat_namespace -macosx_version_min 10.7 -undefined suppress -lusb-1.0 -L./ -lpowerusb -o _pwrusb.so PwrUsbCmd_interface.o PwrUsbCmd_interface_wrap.o
	install_name_tool -change libpowerusb.dylib $(PYSITE_PACKAGES)/libpowerusb.dylib _pwrusb.so


clean:
	rm -f _PwrUsbCmd.cpp
	rm -f *.o
	rm -f *.so
	rm -f *.pyc
	rm -f PwrUsbCmd_interface_wrap.cpp
	rm -f pwrusb.py
	rm -rf Mac
	rm -f libpowerusb.dylib
	rm -f PwrUsbCmd.cpp
	rm -f PwrUSBImp.h
	rm -f Mac.zip

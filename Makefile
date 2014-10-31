PYMOD_INC ?= $(shell python-config --includes)

_PwrUsbCmd.cpp:  PwrUsbCmd.cpp
	sed -e 's/".\/libpowerusb.dylib"/"~\/Library\/Application\ Support\/pwruHenry Roe <henryroe@mac.com>sb\/libpowerusb.dylib"/g' PwrUsbCmd.cpp > _PwrUsbCmd.cpp


_pwrusb.so:  PwrUsbCmd_interface.cpp  PwrUsbCmd_interface.i  _PwrUsbCmd.cpp
	swig -c++ -python -o PwrUsbCmd_interface_wrap.cpp PwrUsbCmd_interface.i
	g++ -fPIC -Wall -g -c -framework IOKit -framework CoreFoundation PwrUsbCmd_interface.cpp
	g++ -fPIC -Wall -g -c -framework IOKit -framework CoreFoundation PwrUsbCmd_interface_wrap.cpp -I$(PYMOD_INC)
	ld -bundle -flat_namespace -macosx_version_min 10.7 -undefined suppress -lusb-1.0 -L./ -lpowerusb -o _pwrusb.so PwrUsbCmd_interface.o PwrUsbCmd_interface_wrap.o
#	install_name_tool -change libpowerusb.dylib ~/Library/Application\ Support/pwrusb/libpowerusb.dylib _pwrusb.so


clean:
	rm -f _PwrUsbCmd.cpp
	rm -f *.o
	rm -f *.so
	rm -f *.pyc
	rm -f PwrUsbCmd_interface_wrap.cpp
	rm -f pwrusb.py
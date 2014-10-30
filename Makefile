

_PwrUsbCmd.cpp:  PwrUsbCmd.cpp
	sed -e 's/".\/libpowerusb.dylib"/"~\/Library\/Application\ Support\/pwrusb\/libpowerusb.dylib"/g' PwrUsbCmd.cpp > _PwrUsbCmd.cpp

~/Library/Application\ Support/pwrusb:
	mkdir -p ~/Library/Application\ Support/pwrusb

_pwrusb.so:  PwrUsbCmd_interface.cpp  PwrUsbCmd_interface.i  _PwrUsbCmd.cpp  ~/Library/Application\ Support/pwrusb
	swig -c++ -python -o PwrUsbCmd_interface_wrap.cpp PwrUsbCmd_interface.i
	g++ -fPIC -Wall -g -c -framework IOKit -framework CoreFoundation PwrUsbCmd_interface.cpp
	g++ -fPIC -Wall -g -c -framework IOKit -framework CoreFoundation PwrUsbCmd_interface_wrap.cpp -I/Library/Frameworks/Python.framework/Versions/7.3/include/python2.7
	ld -bundle -flat_namespace -macosx_version_min 10.7 -undefined suppress -lusb -L./ -lpowerusb -o _pwrusb.so PwrUsbCmd_interface.o PwrUsbCmd_interface_wrap.o
	install_name_tool -change libpowerusb.dylib /usr/local/lib/libpowerusb.dylib _pwrusb.so
	rm -f _PwrUsbCmd.cpp

clean:
	rm -f *.o
	rm -f *.so
	rm -f *.pyc
	rm -f PwrUsbCmd_interface_wrap.cpp
	rm -f pwrusb.py
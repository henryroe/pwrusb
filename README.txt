
# pwrusb

A python wrapper for controlling pwrusb.com power strip outlets.

## Installation notes

For copyright reasons several files are not included in this distribution.  They can be downloaded from the Mac software distribution from the [pwrusb website](http://www.pwrusb.com/downloads.html).  These files are:
    
    PwrUSBImp.h
    PwrUsbCmd.cpp
    libpowerusb.dylib

A version of libusb-1.0 will need to be installed as well.  One straightforward way to get this is via [homebrew](http://brew.sh/) with:

    brew install libusb

## Usage

Example usage:

    import pwrusb
    bank = 0
    for outlet in [1, 2, 3]:
        print "outlet {} is {}".format(outlet, pwrusb.get_single_outlet_state(bank, outlet))
    pwrusb.set_single_outlet_state(bank, 2, True)
    for outlet in [1, 2, 3]:
        print "outlet {} is {}".format(outlet, pwrusb.get_single_outlet_state(bank, outlet))
    for outlet in [1, 2, 3]:
        pwrusb.set_single_outlet_state(bank, outlet, False)



# pwrusb

A python wrapper for controlling pwrusb.com power strip outlets.

## Installation notes

To avoid copyright issues, several files are not included in this distribution.  Makefile will attempt to download and install these files automatically.  Or, they can be downloaded from the Mac software distribution from the [pwrusb website](http://www.pwrusb.com/downloads.html).  These files are:
    
    PwrUSBImp.h
    PwrUsbCmd.cpp
    libpowerusb.dylib

A version of libusb-1.0 will need to be installed.  One straightforward way to get this is via [homebrew](http://brew.sh/) with:

    brew install libusb
    
TODO: determine if above should be libusb or libusb-compat
    
The `swig` package also needs to be installed in your python distribution for pwrusb to work. One straightforward way to get this is via [homebrew](http://brew.sh/) with:

    brew install swig
    
## Typical Installation

From PyPI:

    pip install pwrusb

## Usage

Example usage:

    import pwrusb
    print("State of all outlets: {}".format(pwrusb.get_all_outlet_states()))
    # turn ON all outlets
    pwrusb.set_all_outlet_states(True)
    print("State of all outlets: {}".format(pwrusb.get_all_outlet_states()))
    # turn ON outlets 1 and 3
    pwrusb.set_all_outlet_states([True, False, True])
    print("State of all outlets: {}".format(pwrusb.get_all_outlet_states()))
    # turn OFF all outlets
    pwrusb.set_all_outlet_states(False)
    print("State of all outlets: {}".format(pwrusb.get_all_outlet_states()))
    # turn ON outlet #3, not changing outlets 1 or 2
    pwrusb.set_outlet_state(3, True)
    # read state of only outlet #3
    pwrusb.get_outlet_state(3)
    
## Additional Usage Notes

Lighted power switch on pwrusb.com strips controls power to outlets, but does not power on/off the USB controller within the strip.  When the physical switch is off, strip should report a low (but not zero) current draw and will report what state the outlets will be when the physical switch is flipped back on, i.e. can report True even when no power is coming out of an outlet.

# History

- Originally written by hroe in 2014-January.
- Repackaged for upload to github and pypi in 2014-October.
- Lots of small updates to project layout etc, including update to Python 3.5 compatibility in 2016-March.
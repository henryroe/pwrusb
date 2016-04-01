import pwrusb_swig_interface as __pwrusb

__version__ = __pwrusb.version()

class pwrusbError(Exception):
    pass

# hot-plugging/unplugging the pwrusb strips is unreliable without restarting this python package, 
# so check number of strips attached once at the beginning
n_banks = __pwrusb.get_number_of_strips_attached() 

def get_single_outlet_state(outlet, bank=0):
    """
    Get state of single outlet on a pwrusb.com power strip.
    If only one strip attached via usb, then default bank=0 is correct.
    
    outlet = 1,2, or 3
    
    (If multiple strips attached, then use bank= to access the different
    strips, but the behavior and repeatability of multiple pwrusb.com 
    strips has not been thoroughly tested.)
    """
    if outlet not in [1,2,3]:
        raise pwrusbError(("Unrecognized outlet number {0} " + 
                           "(outlet should be one of 1,2,3)").format(outlet))
    if bank > (n_banks - 1):
        raise pwrusbError(("Request bank number {0} is greater than the available " + 
                           "number of banks ({1}) (count from zero)").format(bank, n_banks))
    state = __pwrusb.get_single_outlet_state(bank, outlet)
    if state == 0:
        return False
    if state == 1:
        return True
    raise pwrusbError(("Unrecognized response {0} from pwrusb for (bank,outlet)=" +
                      "({1},{2})").format(state, bank, outlet))
                      

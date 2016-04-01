import pwrusb_swig_interface as __pwrusb

__version__ = __pwrusb.version()

class pwrusbError(Exception):
    pass

# hot-plugging/unplugging the pwrusb strips is unreliable without restarting this python package, 
# so check number of strips attached once at the beginning
n_banks = __pwrusb.get_number_of_strips_attached() 

def _validate_outlet_and_bank(outlet, bank):
    if n_banks < 1:
        raise pwrusbError("no pwrusb.com strips detected on USB")
    if outlet not in [1,2,3]:
        raise pwrusbError(("Unrecognized outlet number {0} " + 
                           "(outlet should be one of 1,2,3)").format(outlet))
    if bank > (n_banks - 1):
        raise pwrusbError(("Request bank number {0} is greater than the available " + 
                           "number of banks ({1}) counting from zero").format(bank, n_banks))

def get_outlet_state(outlet, bank=0):
    """
    Get state of single outlet on a pwrusb.com power strip.
    If only one strip attached via usb, then default bank=0 is correct.
    
    outlet = 1, 2, or 3
    
    return is True/False (on/off)
    
    (If multiple strips attached, then use bank= to access the different
    strips, but the behavior and repeatability of multiple pwrusb.com 
    strips has not been thoroughly tested.)
    """
    _validate_outlet_and_bank(outlet, bank)
    state = __pwrusb.get_single_outlet_state(bank, outlet)
    if state == 0:
        return False
    if state == 1:
        return True
    raise pwrusbError(("Unrecognized response {0} from pwrusb for (bank,outlet)=" +
                      "({1},{2})").format(state, bank, outlet))

def get_all_outlet_states(bank=0):
    """
    Get state of all outlets on a pwrusb.com power strip
    If only one strip attached via usb, then default bank=0 is correct.
        
    return is list of len=3 of True/False (on/off), e.g.:   [True, False, False]
    where outlets 1-3 are listed in order
    
    (If multiple strips attached, then use bank= to access the different
    strips, but the behavior and repeatability of multiple pwrusb.com 
    strips has not been thoroughly tested.)
    """
    _validate_outlet_and_bank(1, bank)
    states = []
    for outlet in [1, 2, 3]:
        state = __pwrusb.get_single_outlet_state(bank, outlet)
        if state == 0:
            states.append(False)
        elif state == 1:
            states.append(True)
        else:
            raise pwrusbError(("Unrecognized response {0} from pwrusb for (bank,outlet)=" +
                              "({1},{2})").format(state, bank, outlet))    
    return states

def set_outlet_state(outlet, state, bank=0):
    """
    Turn on/off outlet on a pwrusb.com power strip
    If only one strip attached via usb, then default bank=0 is correct.

    outlet = 1, 2, or 3
    state = True/False (on/off)
    
    (If multiple strips attached, then use bank= to access the different
    strips, but the behavior and repeatability of multiple pwrusb.com 
    strips has not been thoroughly tested.)
    """
    _validate_outlet_and_bank(outlet, bank)
    __pwrusb.set_single_outlet_state(bank, outlet, state)

def set_all_outlet_states(states, bank=0):
    """
    Turn on/off all outlets on a pwrusb.com power strip
    If only one strip attached via usb, then default bank=0 is correct.

    states = True -> turn all outlets on
             False -> turn all outlets off
             [True, False, True] -> turn some outlets on & some off

    (If multiple strips attached, then use bank= to access the different
    strips, but the behavior and repeatability of multiple pwrusb.com 
    strips has not been thoroughly tested.)
    """
    if states is True:
        states = [True]*3
    if states is False:
        states = [False]*3
    if len(states) != 3:
        raise pwrusbError("states must be True, False, or iterable of len=3, e.g. [True, False, True]")
    states = [True if a else False for a in states]
    for i,cur_state in enumerate(states):
        set_outlet_state(i+1, cur_state, bank=bank)

def get_total_current_milliamps(bank=0):
    """
    Read the total current (milliamps) being drawn on a pwrusb.com power strip.
    Note that will not be 0 even when all outlets are off as the strip itself draws a 
    small amount of current.
    
    There is no way to read the individual outlet current draw.
    """
    return __pwrusb.get_total_current_milliamps(bank)
    
    
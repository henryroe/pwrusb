// #include <stdio.h>
#include "_PwrUSBCmd.cpp"

// The purpose of this file is to provide a few functions for SWIG wrapping to Python while leaving the
// `PwrUSBCmd.cpp` file unchanged.  (the path to the dylib has to be changed in the make process
// and at that point we renamed the file to _PwrUSBCmd.cpp)

extern const char* version()
{
    return "ABC-version-XYZ";
}

extern int get_number_of_strips_attached()
{
    int i, MaxUnits, connected;
    int ioStates[7];
	char firmware[32];

	memset(ioStates, 0, sizeof(int)*7);					// triggger state of 3 outputs and 4 inputs
    strcpy(firmware, "");
    loadSharedLibrary();
    if ((MaxUnits=(*InitPowerUSB_Address)(&i, firmware)) > 0)		// Initialize the PowerUSB
        connected = (*CheckStatusPowerUSB_Address)();
    return MaxUnits;
}

extern int get_total_current_milliamps(int bank)
{
    int r1, current, i, MaxUnits, connected;
    int ioStates[7];
	char firmware[32];

	memset(ioStates, 0, sizeof(int)*7);					// triggger state of 3 outputs and 4 inputs
    strcpy(firmware, "");
    loadSharedLibrary();
    if ((MaxUnits=(*InitPowerUSB_Address)(&i, firmware)) > 0)		// Initialize the PowerUSB
        connected = (*CheckStatusPowerUSB_Address)();
    // TODO: sometime when I have multiple pwrusb strips attached, test `bank`
    (*SetCurrentPowerUSB_Address)(bank);
    r1 = (*ReadCurrentPowerUSB_Address)(&current);						// Present current consumption reading in milli amps
    return current;
}

extern void get_outlet_states(int bank, int *outlet1, int *outlet2, int *outlet3)
{
	int connected=0;
    int in1, in2, in3, i, MaxUnits;
    int ioStates[7];
	char firmware[32];

	memset(ioStates, 0, sizeof(int)*7);					// triggger state of 3 outputs and 4 inputs
    strcpy(firmware, "");
    loadSharedLibrary();
    
    if ((MaxUnits=(*InitPowerUSB_Address)(&i, firmware)) > 0)		// Initialize the PowerUSB
        connected = (*CheckStatusPowerUSB_Address)();
    // TODO: sometime when I have multiple pwrusb strips attached, test `bank`
    (*SetCurrentPowerUSB_Address)(bank);

    (*ReadPortStatePowerUSB_Address)(&in1, &in2, &in3);
    *outlet1 = in1;
    *outlet2 = in2;
    *outlet3 = in3;
    return;
}


extern void set_outlet_states(int bank, int outlet1, int outlet2, int outlet3)
{
	int connected=0;
    int i, MaxUnits;
    int ioStates[7];
	char firmware[32];

	memset(ioStates, 0, sizeof(int)*7);					// triggger state of 3 outputs and 4 inputs
    strcpy(firmware, "");
    loadSharedLibrary();
    
    if ((MaxUnits=(*InitPowerUSB_Address)(&i, firmware)) > 0)		// Initialize the PowerUSB
        connected = (*CheckStatusPowerUSB_Address)();
    // TODO: sometime when I have multiple pwrusb strips attached, test `bank`
    (*SetCurrentPowerUSB_Address)(bank);
    (*SetPortPowerUSB_Address)(outlet1, outlet2, outlet3);
    return;
}


extern int get_single_outlet_state(int bank, int outlet_number)
{
    int outlet1, outlet2, outlet3;
    get_outlet_states(bank, &outlet1, &outlet2, &outlet3);
    if (outlet_number == 1){return outlet1;}
    else if (outlet_number == 2){return outlet2;}
    else if (outlet_number == 3){return outlet3;}
    else{return -1;}
}


extern void set_single_outlet_state(int bank, int outlet_number, int state)
{
    int outlet1, outlet2, outlet3, state_checked;
    if (state)
        state_checked = 1;
    else
        state_checked = 0;
    get_outlet_states(bank, &outlet1, &outlet2, &outlet3);
    if (outlet_number == 1){outlet1 = state_checked;}
    else if (outlet_number == 2){outlet2 = state_checked;}
    else if (outlet_number == 3){outlet3 = state_checked;}
    set_outlet_states(bank, outlet1, outlet2, outlet3);
    return;
}

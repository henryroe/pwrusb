%module pwrusb
%include "typemaps.i"
%{
extern void get_outlet_states(int bank, int *OUTPUT, int *OUTPUT, int *OUTPUT);
extern void set_outlet_states(int bank, int OUTPUT, int OUTPUT, int OUTPUT);
extern int get_single_outlet_state(int bank, int outlet_number);
extern void set_single_outlet_state(int bank, int outlet_number, int state);
extern char* version();
%}

extern void get_outlet_states(int bank, int *OUTPUT, int *OUTPUT, int *OUTPUT);
extern void set_outlet_states(int bank, int OUTPUT, int OUTPUT, int OUTPUT);
extern int get_single_outlet_state(int bank, int outlet_number);
extern void set_single_outlet_state(int bank, int outlet_number, int state);
extern char* version();

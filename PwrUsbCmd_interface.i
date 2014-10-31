%module pwrusb
%include "typemaps.i"
%{
extern int get_single_outlet_state(int bank, int outlet_number);
extern void set_single_outlet_state(int bank, int outlet_number, int state);
extern char* version();
%}

extern int get_single_outlet_state(int bank, int outlet_number);
extern void set_single_outlet_state(int bank, int outlet_number, int state);
extern char* version();

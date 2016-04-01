%module pwrusb_swig_interface
%include "typemaps.i"
%{
extern char* version();
extern int get_number_of_strips_attached();
extern int get_single_outlet_state(int bank, int outlet_number);
extern void set_single_outlet_state(int bank, int outlet_number, int state);
extern int get_total_current_milliamps(int bank);
%}

extern char* version();
extern int get_number_of_strips_attached();
extern int get_single_outlet_state(int bank, int outlet_number);
extern void set_single_outlet_state(int bank, int outlet_number, int state);
extern int get_total_current_milliamps(int bank);

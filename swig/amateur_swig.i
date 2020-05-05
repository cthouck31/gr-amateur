/* -*- c++ -*- */

#define AMATEUR_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "amateur_swig_doc.i"

%{
#include "amateur/Tagged_Nrzi_Encoder.h"
#include "amateur/Saturated_Counter.h"
#include "amateur/Burst_Stager.h"
#include "amateur/Burst_Injector.h"
#include "amateur/Tagged_Stream_Add_Length_Tag.h"
#include "amateur/Burst_Afsk_Modulator.h"
%}


%include "amateur/Tagged_Nrzi_Encoder.h"
GR_SWIG_BLOCK_MAGIC2(amateur, Tagged_Nrzi_Encoder);

%include "amateur/Saturated_Counter.h"
GR_SWIG_BLOCK_MAGIC2(amateur, Saturated_Counter);
%include "amateur/Burst_Stager.h"
GR_SWIG_BLOCK_MAGIC2(amateur, Burst_Stager);
%include "amateur/Burst_Injector.h"
GR_SWIG_BLOCK_MAGIC2(amateur, Burst_Injector);

%include "amateur/Tagged_Stream_Add_Length_Tag.h"
GR_SWIG_BLOCK_MAGIC2(amateur, Tagged_Stream_Add_Length_Tag);

%include "amateur/Burst_Afsk_Modulator.h"
GR_SWIG_BLOCK_MAGIC2(amateur, Burst_Afsk_Modulator);



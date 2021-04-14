#include <hls_stream.h>
#include <ap_axi_sdata.h>
#include<ap_fixed.h>

// typedef ap_axiu<8,1,1,1> intS;

// stripped down ap_axiu for use with video
typedef struct ap_axiu_for_video {
	ap_uint<8>      data;
	ap_uint<1>       user;
	ap_uint<1>       last;
} video;

typedef hls::stream<video> AXI_STREAM;

#define MAX_HEIGHT 2000
#define MAX_WIDTH 2000

// ===== ENTRY POINT =====
void red_shift(AXI_STREAM &in_buffer,
		AXI_STREAM &out_buffer,
		short rows,
		short cols
		) {
#pragma HLS INTERFACE ap_ctrl_none port=return
#pragma HLS INTERFACE axis register both port=in_buffer
#pragma HLS INTERFACE axis register both port=out_buffer
#pragma HLS INTERFACE s_axilite register port=rows
#pragma HLS INTERFACE s_axilite register port=cols

	// loop through every rgb pixel data point in the buffer
//	loopydeeloop: for(int ii = 0; ii < (rows * cols * 3); ii++) {
		int ii = 0;
		while (1) {
			video dataIn = in_buffer.read();
			video dataOut = dataIn;

			// if data index % 3 ==  0 we are on a red data point
			if (ii % 3 == 0){
				dataOut.data = 255;
			} else {
				dataOut.data = dataIn.data;
			}
			out_buffer.write(dataOut);
			if (dataIn.last) {
				break;
			}
			ii++;
		}
//	} // loopdeeloop

}



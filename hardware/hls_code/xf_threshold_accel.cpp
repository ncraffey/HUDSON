/*
 * Copyright 2019 Xilinx, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


#include "xf_threshold_config.h"
#include "ap_int.h"
#include "imgproc/xf_duplicateimage.hpp"


// struct added by John Craffey for HUDSON project
// stripped down ap_axiu for use with video
struct axis_t {
	ap_uint<INPUT_PTR_WIDTH>      data;
	ap_uint<1>     				  last;
};
/////

// AXI stream mat convert functions sourced from https://discuss.pynq.io/t/vitis-vision-core-fails-on-pynq-v2-5-1/1822/16
void axis2xfMat (axis_t *src,
		 xf::cv::Mat<XF_8UC1, HEIGHT, WIDTH, NPIX>& img,
		 int rows,
		 int cols) {

		int idx = 0;

		for (int i = 0; i < rows; i++) {
			for (int j = 0; j < cols; j++) {
				// clang-format off
	    		#pragma HLS loop_flatten off
	    		#pragma HLS pipeline II=1
				// clang-format on
		        img.write(idx++, src->data);
				src++;
			}
		}

}

void xfMat2axis (xf::cv::Mat<XF_8UC1, HEIGHT, WIDTH, NPIX>& img,
		 axis_t *dst,
		 int rows,
		 int cols) {

		int idx = 0;

		for (int i = 0; i < rows; i++) {
			for (int j = 0; j < cols; j++) {
				// clang-format off
	    		#pragma HLS loop_flatten off
	    		#pragma HLS pipeline II=1
				// clang-format on
				ap_uint<1> tmp = 0;
				if ((i==rows-1) && (j== cols-1)) {
					tmp = 1;
				}
				dst->last = tmp;
				dst->data = img.read(idx++);
				dst++;
			}
		}
}

// take in a Mat image and calculate the location of the X,Y coordinates of a body
void findBody(xf::cv::Mat<XF_8UC1, HEIGHT, WIDTH, NPIX>& img,
				int rows,
				int cols,
				ap_uint<12>& xx,
				ap_uint<12>& yy) {

	xx = 400;
	yy = 400;
	int idx = 0;

			for (int i = 0; i < rows; i++) {
				for (int j = 0; j < cols; j++) {
					// clang-format off
		    		#pragma HLS loop_flatten off
		    		#pragma HLS pipeline II=1
					// clang-format on
					img.read(idx++);
				}
			}

	return;
}

// top function based from https://github.com/Xilinx/Vitis_Libraries/blob/master/vision/L1/examples/threshold/xf_threshold_accel.cpp
// ===== EntryPoint =====
void threshold_accel(axis_t* srcPtr,
					 axis_t* dstPtr,
                     unsigned char thresh,
                     unsigned char maxval,
                     int rows,
                     int cols,
					 ap_uint<12>& xOut,
					 ap_uint<12>& yOut) {
// clang-format off
	// taken from redshift
#pragma HLS INTERFACE ap_ctrl_none port=return
#pragma HLS INTERFACE axis register both port=srcPtr
#pragma HLS INTERFACE axis register both port=dstPtr

#pragma HLS INTERFACE s_axilite register port=thresh
#pragma HLS INTERFACE s_axilite register port=maxval
#pragma HLS INTERFACE s_axilite register port=rows
#pragma HLS INTERFACE s_axilite register port=cols
#pragma HLS INTERFACE s_axilite register port=xOut
#pragma HLS INTERFACE s_axilite register port=yOut
// clang-format on

    const int pROWS = HEIGHT;
    const int pCOLS = WIDTH;
    const int pNPC1 = NPIX;

    xf::cv::Mat<XF_8UC1, HEIGHT, WIDTH, NPIX> in_mat(rows, cols);
    xf::cv::Mat<XF_8UC1, HEIGHT, WIDTH, NPIX> out_of_thresh_mat(rows, cols);
    xf::cv::Mat<XF_8UC1, HEIGHT, WIDTH, NPIX> in_findbody_mat(rows, cols);
    xf::cv::Mat<XF_8UC1, HEIGHT, WIDTH, NPIX> out_mat(rows, cols);

// clang-format off
    #pragma HLS DATAFLOW
// clang-format on

    // read in the axi stream
    axis2xfMat(srcPtr,in_mat, rows, cols);
    // threshold the image
    xf::cv::Threshold<THRESH_TYPE, XF_8UC1, HEIGHT, WIDTH, NPIX>(in_mat, out_of_thresh_mat, thresh, maxval);

    // copy processed image so we dont lose it
    xf::cv::duplicateMat<XF_8UC1, HEIGHT, WIDTH, NPIX>(out_of_thresh_mat,  out_mat, in_findbody_mat);
    // find coordinates for rectangle
    findBody(in_findbody_mat, rows, cols, xOut, yOut);
    // write the processed image from out_mat to axi stream output
    xfMat2axis(out_mat, dstPtr, rows, cols);

}

`include "/home/lorenzo/Git/CodiceTesiMagistrale/correlations/libs/primitives.v"
`include "/home/lorenzo/Git/CodiceTesiMagistrale/correlations/libs/sky130_fd_sc_hd.v"

`timescale 1ns / 1fs

module module_2_gates (
    VGND,
    VPWR,
    in,
    y);
 input VGND;
 input VPWR;
 input [3:0] in;
 output y;

 wire _01_;
 wire _02_;

    sky130_fd_sc_hd__nand2_1 _nand_ (.A(in[0]),
        .B(in[1]),
        .VGND(VGND),
        .VNB(VGND),
        .VPB(VPWR),
        .VPWR(VPWR),
        .Y(_01_));

    sky130_fd_sc_hd__xor2_1 _xor_(.A(in[2]),
        .B(in[3]),
        .VGND(VGND),
        .VNB(VGND),
        .VPB(VPWR),
        .VPWR(VPWR),
        .X(_02_));

    sky130_fd_sc_hd__xnor2_1 _xnor_(.A(_01_),
        .B(_02_),
        .VGND(VGND),
        .VNB(VGND),
        .VPB(VPWR),
        .VPWR(VPWR),
        .Y(y));

endmodule

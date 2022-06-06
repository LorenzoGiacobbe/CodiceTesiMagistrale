`include "/home/lorenzo/gadget_simulation/libs/primitives.v"
`include "/home/lorenzo/gadget_simulation/libs/sky130_fd_sc_hd.v"

`timescale 1ns / 1fs

module module_2_gates (
    VGND,
    VPWR,
    a,
    b,
    r1,
    r2,
    y);
 input VGND;
 input VPWR;
 input a;
 input b;
 input r1;
 input r2; 
 output y;

 wire _delA_;
 wire _delB_;
 wire _delR1_;
 wire _delR2_;
 wire _01_;
 wire _02_;

    assign _delA_  = a;
    assign _delB_  = b;
    assign _delR1_ = r1;
    assign _delR2_ = r2;

    sky130_fd_sc_hd__nand2_1 _nand_ (.A(_delA_),
        .B(_delB_),
        .VGND(VGND),
        .VNB(VGND),
        .VPB(VPWR),
        .VPWR(VPWR),
        .Y(_01_));

    sky130_fd_sc_hd__xor2_1 _xor_(.A(_delR1_),
        .B(_delR2_),
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

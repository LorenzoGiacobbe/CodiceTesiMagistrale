`include "/home/lorenzo/gadget_simulation/libs/primitives.v"
`include "/home/lorenzo/gadget_simulation/libs/sky130_fd_sc_hd.v"

`timescale 1ns / 1fs

module module_3_gates (
    VGND,
    VPWR,
    a,
    b,
    r1,
    r2,
    q,
    y);
 input VGND;
 input VPWR;
 input a;
 input b;
 input r1;
 input r2; 
 input q;
 output y;

 wire _delA_;
 wire _delB_;
 wire _delR1_;
 wire _delR2_;
 wire _delQ_;
 wire _01_;
 wire _02_;

    assign #0.02 _delA_  = a;
    assign #0.53 _delB_  = b;
    assign #0.32 _delR1_ = r1;
    assign #0.04 _delR2_ = r2;
    assign #0.10 _delQ_ = q;

    sky130_fd_sc_hd__nand2_1 _nand_ (.A(_delA_),
        .B(_delB_),
        .VGND(VGND),
        .VNB(VGND),
        .VPB(VPWR),
        .VPWR(VPWR),
        .Y(_01_));

    sky130_fd_sc_hd__xnor2_1 _xnorR_(.A(_delR1_),
        .B(_delR2_),
        .VGND(VGND),
        .VNB(VGND),
        .VPB(VPWR),
        .VPWR(VPWR),
        .Y(_02_));

    sky130_fd_sc_hd__xnor2_1 _xnorQ_(.A(_01_),
        .B(_delQ_),
        .VGND(VGND),
        .VNB(VGND),
        .VPB(VPWR),
        .VPWR(VPWR),
        .Y(_03_));

    sky130_fd_sc_hd__xnor2_1 _xnor_(.A(_02_),
        .B(_03_),
        .VGND(VGND),
        .VNB(VGND),
        .VPB(VPWR),
        .VPWR(VPWR),
        .Y(y));

endmodule

`timescale 1ns/1ps
// toll_controller.v
// Interprets UART data into control actions for gate, alert, and EV discount

module toll_controller(
    input wire clk,
    input wire reset,
    input wire [2:0] uart_data,
    output reg gate_open,
    output reg tailgate_alert,
    output reg ev_discount
);

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            gate_open      <= 0;
            tailgate_alert <= 0;
            ev_discount    <= 0;
        end
        else begin
            // [2]=vehicle_detected, [1]=tailgate, [0]=ev_detected
            gate_open      <= uart_data[2];
            tailgate_alert <= uart_data[1];
            ev_discount    <= uart_data[0];
        end
    end
endmodule


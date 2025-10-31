`timescale 1ns/1ps
// testbench.v
// Automatically runs until uart_rx_sim finishes reading all lines

module testbench;
    reg clk = 0;
    reg reset = 1;
    wire [2:0] uart_data;
    wire gate_open, tailgate_alert, ev_discount;

    // Completion flag from UART simulator
    wire uart_done;

    // Instantiate UART simulator
    uart_rx_sim uart_sim(
        .clk(clk),
        .reset(reset),
        .uart_data(uart_data),
        .done(uart_done)
    );

    // Instantiate Toll Controller
    toll_controller toll_ctrl(
        .clk(clk),
        .reset(reset),
        .uart_data(uart_data),
        .gate_open(gate_open),
        .tailgate_alert(tailgate_alert),
        .ev_discount(ev_discount)
    );

    // Clock generation
    always #5 clk = ~clk;

    initial begin
        $display("Simulation start...");
        #10 reset = 0;
        wait(uart_done);  // waits until file reading is done
        $display("? All UART frames processed ? simulation complete at time %0t", $time);
        #100 $finish;
    end
endmodule


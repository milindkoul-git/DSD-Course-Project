`timescale 1ns/1ps
// uart_rx_sim.v ? Reads 3-bit UART data from text file line-by-line

module uart_rx_sim(
    input wire clk,
    input wire reset,
    output reg [2:0] uart_data,
    output reg done
);
    integer file;
    reg [2:0] temp;

    initial begin
        uart_data = 3'b000;
        done = 0;
        #20;  // wait a bit after reset

        file = $fopen("uart_sim.txt", "r");
        if (file == 0) begin
            $display("? Error: Could not open uart_sim.txt");
            $finish;
        end

        $display("UART SIM: Starting transmission from uart_sim.txt");

        while (!$feof(file)) begin
            $fscanf(file, "%b\n", temp);
            uart_data = temp;
            $display("UART SIM: Time=%0t | Sent=%b", $time, uart_data);
            #100; // wait 100ns before next frame
        end

        $fclose(file);
        done = 1;
        $display("UART SIM: ? Finished sending all frames at time %0t", $time);
    end
endmodule


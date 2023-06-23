--**
--* ecc_decode.vhd - error correcrion code decoder
--*
--* Copyright (c) 2023 Caspar Trittibach
--* Author: Caspar Trittibach <ctrittibach@gmail.com>
--*
--**

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

use IEEE.NUMERIC_STD.ALL;
use IEEE.math_real.all;

entity ecc_decode is
    GENERIC(
        C_ODD_PARITY : std_logic := '1';
        C_DATA_WIDTH : natural range 32 to 64 := 33;
        C_NR_PARITY  : natural range 6 to 7 := 6
           );
    PORT(
        clk   : in std_logic;
        rst   : in std_logic;
        in_valid : in std_logic;
        in_ready : out std_logic;
        in_data  : in std_logic_vector(C_DATA_WIDTH+C_NR_PARITY downto 0);

        out_valid : out std_logic;
        out_ready : in std_logic;
        out_data  : out std_logic_vector(C_DATA_WIDTH-1 downto 0);
        out_is_err : out std_logic
    );
end ecc_decode;

architecture behavioral of ecc_decode is
    constant ECC_DATA_WIDTH : natural := C_DATA_WIDTH + C_NR_PARITY + 1;

    signal parity_bit : std_logic_vector(C_NR_PARITY - 1 downto 0);
    signal ecc_data : std_logic_vector(ECC_DATA_WIDTH - 1 downto 0);
    signal extended_parity : std_logic;
    signal reduced_data : std_logic_vector(C_DATA_WIDTH - 1 downto 0);
    signal corrected_data : std_logic_vector(ECC_DATA_WIDTH - 2 downto 0);

    signal rdy : std_logic;
    signal result_err : std_logic;

begin

    --check if enough parity bits are present--
    --assert 2**C_NR_PARITY >= C_DATA_WIDTH + C_NR_PARITY + 2
    --    report "Generics do not satisfy hamming theorem" severity failure;

    parity_gen: for n in 1 to C_NR_PARITY generate
        rth_parity_inst_n : entity work.rth_parity
            generic map(
                C_DATA_WIDTH => (ECC_DATA_WIDTH-1),
                C_ODD_PARITY => C_ODD_PARITY,
                C_RTH   => n
            )
            port map(
                data => in_data(ECC_DATA_WIDTH-2 downto 0),
                parity => parity_bit(n-1)
            );
    end generate;

    parity_proc : process(in_data)
        variable var_parity : std_logic;
    begin
        var_parity := not(C_ODD_PARITY);
        for n in 0 to ECC_DATA_WIDTH-1 loop
            var_parity := var_parity xor in_data(n);
        end loop;
        extended_parity <= var_parity;
    end process;

    ff_stage_proc : process(clk)
    begin
        if rising_edge(clk) then
            if rst = '1' then
                out_valid <= '0';
                out_data <= (others => '0');
            else
                if rdy = '1' then
                    out_valid <= in_valid;
                    out_data <= reduced_data;
                end if;
            end if;
        end if;
    end process;

    bit_reduction_proc : process(all)
        variable var_data_bit : integer;
    begin
        var_data_bit := 0;
        for n in 1 to ECC_DATA_WIDTH-1 loop
            if n = 2**var_data_bit then
                var_data_bit := var_data_bit + 1;
            else
                reduced_data(n-var_data_bit-1) <= corrected_data(n-1);
            end if;
        end loop;
    end process;

    correction_stage_gen : for n in 1 to ECC_DATA_WIDTH-1 generate
        corrected_data(n-1) <= not(in_data(n-1))
                               when TO_INTEGER(unsigned(parity_bit)) = n
                               else in_data(n-1);
    end generate;

    rdy <= not(out_valid) or out_ready;
    in_ready <= rdy;
    result_err <= '0' when unsigned(parity_bit) = 0 else '1';
    out_is_err <= result_err and not(extended_parity);

end behavioral;

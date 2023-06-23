--**
--* ecc_encode.vhd- error correcrion code encoder
--*
--* Copyright (c) 2023 Caspar Trittibach
--* Author: Caspar Trittibach <ctrittibach@gmail.com>
--*
--**

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

use IEEE.NUMERIC_STD.ALL;
use IEEE.math_real.all;

entity ecc_encode is
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
        in_data  : in std_logic_vector(C_DATA_WIDTH-1 downto 0);

        out_valid : out std_logic;
        out_ready : in std_logic;
        out_data  : out std_logic_vector(C_DATA_WIDTH+C_NR_PARITY downto 0)
    );
end ecc_encode;

architecture behavioral of ecc_encode is
    constant ECC_DATA_WIDTH : natural := C_DATA_WIDTH + C_NR_PARITY + 1;

    signal parity_bit : std_logic_vector(C_NR_PARITY - 1 downto 0);
    signal extended_parity : std_logic;
    signal ecc_data : std_logic_vector(ECC_DATA_WIDTH - 1 downto 0);

    signal extended_data : std_logic_vector(ECC_DATA_WIDTH - 1 downto 0);
    signal inserted_data : std_logic_vector(ECC_DATA_WIDTH - 1 downto 0);
    signal valid_d : std_logic_vector(1 downto 0);

    signal rdy : std_logic;
begin

    --check if enough parity bits are present--
    --assert 2**C_NR_PARITY >= C_DATA_WIDTH+C_NR_PARITY+2
    --    report "Generics do not satisfy hamming distance" severity failure;

    parity_gen: for n in 1 to C_NR_PARITY generate
        rth_parity_inst_n : entity work.rth_parity
            generic map(
                C_DATA_WIDTH => (ECC_DATA_WIDTH-1),
                C_ODD_PARITY => C_ODD_PARITY,
                C_RTH   => n
            )
            port map(
                data => extended_data(ECC_DATA_WIDTH-2 downto 0),
                parity => parity_bit(n-1)
            );
    end generate;

    parity_proc : process(ecc_data)
        variable var_parity : std_logic;
    begin
        var_parity := not(C_ODD_PARITY);
        for n in 0 to ECC_DATA_WIDTH-2 loop
            var_parity := var_parity xor ecc_data(n);
        end loop;
        extended_parity <= var_parity;
    end process;

    ff_proc : process(clk)
    begin
        if rising_edge(clk) then
            if rst = '1' then
                ecc_data <= (others =>'0');
                out_data <= (others =>'0');
                valid_d <= (others =>'0');
            else
                if rdy = '1' then
                    ecc_data <= inserted_data;
                    out_data(ECC_DATA_WIDTH - 2 downto 0) <= ecc_data(ECC_DATA_WIDTH - 2 downto 0);
                    out_data(out_data'high) <= extended_parity;
                    valid_d(0) <= in_valid;
                    valid_d(1) <= valid_d(0);
                end if;
            end if;
        end if;
    end process;

    data_extending_proc : process(in_data)
        variable var_bit_cnt : integer;
    begin
        var_bit_cnt := 0;
        for n in 1 to ECC_DATA_WIDTH-1 loop
            if n = 2**var_bit_cnt then
                var_bit_cnt := var_bit_cnt + 1;
                extended_data(n-1) <= '0';
            else
                extended_data(n-1) <= in_data(n-var_bit_cnt-1);
            end if;
        end loop;
        extended_data(ECC_DATA_WIDTH-1) <= '0';
    end process;

    parity_insertion_proc : process(all)
        variable var_bit_cnt : integer;
    begin
        var_bit_cnt := 0;
        for n in 1 to ECC_DATA_WIDTH-1 loop
            if n = 2**var_bit_cnt then
                inserted_data(n-1) <= parity_bit(var_bit_cnt);
                var_bit_cnt := var_bit_cnt + 1;
            else
                inserted_data(n-1) <= extended_data(n-1);
            end if;
        end loop;
        inserted_data(ECC_DATA_WIDTH-1) <= '0';
    end process;

    rdy <= not(out_valid) or out_ready;
    in_ready <= rdy;
    out_valid <= valid_d(1);

end behavioral;

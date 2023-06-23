--**
--* debounce.vhd - debouncing core for IO signals
--*
--* Copyright (c) 2021 Caspar Trittibach
--* Author: Caspar Trittibach <ctrittibach@gmail.com>
--*
--**

library IEEE;
use ieee.std_logic_1164.all;

use ieee.numeric_std.all;
use ieee.math_real.all;

entity debounce is
    generic(
        NR_OF_SIGNAL    : integer := 1;
        DEBOUNCE_TIME   : integer := 100
    );
    port(
        clk     : in std_logic;
        rst     : in std_logic;
        sig_in  : in std_logic_vector(NR_OF_SIGNAL - 1 downto 0);
        sig_out : out std_logic_vector(NR_OF_SIGNAL -1 downto 0)
    );
end debounce;

architecture behavioral of debounce is

    -- TODO: Fix float rounding problem
    constant C_CNT_SIZE : natural := integer(ceil(log2(real(DEBOUNCE_TIME))));
    type u_deb_cnt_type is array (NR_OF_SIGNAL -1 downto 0) of unsigned(C_CNT_SIZE-1 downto 0);

    signal debounce_cnt         : u_deb_cnt_type ;
    signal sig_in_d1            : std_logic_vector(NR_OF_SIGNAL - 1 downto 0);
    signal sig_in_d2            : std_logic_vector(NR_OF_SIGNAL - 1 downto 0);
    signal sig_debounce         : std_logic_vector(NR_OF_SIGNAL - 1 downto 0);

begin
    debounce_gen: for n in NR_OF_SIGNAL -1 downto 0 generate
        debounce_proc: process(clk)
        begin
            if rising_edge(clk) then
                if rst = '1' then
                    sig_in_d1(n) <= '0';
                    sig_in_d2(n) <= '0';
                    sig_debounce(n) <= '0';
                    debounce_cnt(n) <= to_unsigned(DEBOUNCE_TIME,C_CNT_SIZE);
                else
                    sig_in_d1(n) <= sig_in(n);
                    sig_in_d2(n) <= sig_in_d1(n);
                    if sig_in_d1(n) /= sig_in_d2(n) then
                        debounce_cnt(n) <= to_unsigned(DEBOUNCE_TIME,C_CNT_SIZE);
                    elsif debounce_cnt(n) > 0 then
                        debounce_cnt(n) <= debounce_cnt(n) - 1;
                    else
                        debounce_cnt(n) <= debounce_cnt(n);
                    end if;
                    if debounce_cnt(n) = 0 then
                       sig_debounce(n) <= sig_in_d2(n);
                    else
                        sig_debounce(n) <= sig_debounce(n);
                    end if;
                end if;
            end if;
        end process;
    end generate;
    sig_out <= sig_debounce;
end behavioral;

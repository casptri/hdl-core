-- **
-- * debounce.vhd - debouncing core for IO signals
-- *
-- * Copyright (c) 2021 Caspar Trittibach
-- * Author: Caspar Trittibach <ctrittibach@gmail.com>
-- *
-- **

library ieee;
  use ieee.std_logic_1164.all;
  use ieee.numeric_std.all;
  use ieee.math_real.all;

entity debounce is
  generic (
    nr_of_signal  : integer := 1;
    debounce_time : integer := 100
  );
  port (
    clk     : in    std_logic;
    rst     : in    std_logic;
    sig_in  : in    std_logic_vector(nr_of_signal - 1 downto 0);
    sig_out : out   std_logic_vector(nr_of_signal - 1 downto 0)
  );
end entity debounce;

architecture behavioral of debounce is

  -- TODO: Fix float rounding problem
  constant c_cnt_size : natural := integer(ceil(log2(real(debounce_time))));

  type u_deb_cnt_type is array (nr_of_signal - 1 downto 0) of unsigned(c_cnt_size - 1 downto 0);

  signal debounce_cnt : u_deb_cnt_type;
  signal sig_in_d1    : std_logic_vector(nr_of_signal - 1 downto 0);
  signal sig_in_d2    : std_logic_vector(nr_of_signal - 1 downto 0);
  signal sig_debounce : std_logic_vector(nr_of_signal - 1 downto 0);

begin

  debounce_gen : for n in nr_of_signal - 1 downto 0 generate

    debounce_proc : process (clk) is
    begin

      if rising_edge(clk) then
        if (rst = '1') then
          sig_in_d1(n)    <= '0';
          sig_in_d2(n)    <= '0';
          sig_debounce(n) <= '0';
          debounce_cnt(n) <= to_unsigned(debounce_time, c_cnt_size);
        else
          sig_in_d1(n) <= sig_in(n);
          sig_in_d2(n) <= sig_in_d1(n);
          if (sig_in_d1(n) /= sig_in_d2(n)) then
            debounce_cnt(n) <= to_unsigned(debounce_time, c_cnt_size);
          elsif (debounce_cnt(n) > 0) then
            debounce_cnt(n) <= debounce_cnt(n) - 1;
          else
            debounce_cnt(n) <= debounce_cnt(n);
          end if;
          if (debounce_cnt(n) = 0) then
            sig_debounce(n) <= sig_in_d2(n);
          else
            sig_debounce(n) <= sig_debounce(n);
          end if;
        end if;
      end if;

    end process debounce_proc;

  end generate debounce_gen;

  sig_out <= sig_debounce;

end architecture behavioral;

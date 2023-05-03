/**
 * rth_parity.vhd - Calculate R'th parrity bit of a vector
 *
 * Copyright (c) 2023 Caspar Trittibach
 * Author: Caspar Trittibach <ctrittibach@gmail.com>
 *
 */

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

use IEEE.NUMERIC_STD.ALL;
use IEEE.math_real.all;

entity rth_parity is
    GENERIC(
            C_DATA_WIDTH : natural range 1 to 256 := 39;
            C_ODD_PARITY : std_logic := '1';
            C_RTH   : natural range 1 to 8 := 3
           );
    PORT(
            data : in std_logic_vector(C_DATA_WIDTH-1 downto 0);
            parity : out std_logic
    );
end rth_parity;

architecture behavioral of rth_parity is
    -- TODO: Fix float rounding problem
    constant C_INDEX_WIDTH : natural := integer(ceil(log2(real(C_DATA_WIDTH))));
begin
    process(data)
        variable var_parity : std_logic ;
        variable var_index : std_logic_vector(C_INDEX_WIDTH-1 downto 0);
    begin
        var_parity := C_ODD_PARITY;
        for n in 1 to C_DATA_WIDTH loop
            var_index := std_logic_vector(to_unsigned(n,C_INDEX_WIDTH));
            if var_index(C_RTH-1) = '1' then
                var_parity :=  var_parity xor data(n-1);
            end if;
        end loop;
        parity <= var_parity;
    end process;

end behavioral;

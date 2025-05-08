-- **
-- * skid_buffer.vhd - skid buffer with axi stream interface
-- *
-- * Copyright (c) 2025 Caspar Trittibach
-- * Author: Caspar Trittibach <ctrittibach@gmail.com>
-- *
-- **

library ieee;
  use ieee.std_logic_1164.all;
  use ieee.numeric_std.all;

entity skid_buffer is
  generic (
    data_width : integer := 8
  );
  port (
    clk : in    std_logic;
    rst : in    std_logic;
    -- AXI-Stream slave (input)
    s_tdata  : in    std_logic_vector(data_width - 1 downto 0);
    s_tready : out   std_logic;
    s_tvalid : in    std_logic;
    -- AXI-Stream master (output)
    m_tdata  : out   std_logic_vector(data_width - 1 downto 0);
    m_tready : in    std_logic;
    m_tvalid : out   std_logic
  );
end entity skid_buffer;

architecture behavioral of skid_buffer is

  signal in_reg      : std_logic_vector(data_width - 1 downto 0);
  signal in_mux_data : std_logic_vector(data_width - 1 downto 0);

  signal intern_ready : std_logic;
  signal intern_valid : std_logic;

begin

  in_reg_proc : process (clk) is
  begin

    if rising_edge(clk) then
      if (rst = '1') then
        in_reg   <= (others => '0');
        m_tdata  <= (others => '0');
        m_tvalid <= '0';
        s_tready <= '1';
      else
        if (s_tready = '1') then
          in_reg <= s_tdata;
        end if;
        if (intern_ready = '1') then
          m_tdata <= in_mux_data;
        end if;
        if (intern_ready = '1') then
          m_tvalid <= intern_valid;
        end if;
        if (intern_valid = '1') then
          s_tready <= intern_ready;
        end if;
      end if;
    end if;

  end process in_reg_proc;

  in_mux_data  <= in_reg when s_tready = '0' else
                  s_tdata;
  intern_valid <= s_tvalid or not(s_tready);
  intern_ready <= m_tready or not(m_tvalid);

end architecture behavioral;

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity simple_adder is
    port (
            a : in  std_logic_vector(7 downto 0);
            b : in  std_logic_vector(7 downto 0);
            c : out std_logic_vector(7 downto 0)
        );
end simple_adder;

architecture Behavioral of simple_adder is
begin
    c <= std_logic_vector(unsigned(a) + unsigned(b));
end Behavioral;

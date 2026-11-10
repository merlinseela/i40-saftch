library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity sobel_patch_core is
    Port (
        aclk          : in  STD_LOGIC;
        aresetn       : in  STD_LOGIC;

        s_axis_tdata  : in  STD_LOGIC_VECTOR(7 downto 0);
        s_axis_tvalid : in  STD_LOGIC;
        s_axis_tready : out STD_LOGIC;
        s_axis_tlast  : in  STD_LOGIC;

        m_axis_tdata  : out STD_LOGIC_VECTOR(7 downto 0);
        m_axis_tvalid : out STD_LOGIC;
        m_axis_tready : in  STD_LOGIC;
        m_axis_tlast  : out STD_LOGIC
    );
end sobel_patch_core;

architecture Behavioral of sobel_patch_core is
    type state_type is (READ_PATCH, CALC_OUTPUT);
    signal state : state_type := READ_PATCH;

    signal byte_cnt : integer range 0 to 8 := 0;
    signal gx_sum   : signed(11 downto 0) := (others => '0');
    signal gy_sum   : signed(11 downto 0) := (others => '0');
    signal last_reg : STD_LOGIC := '0';

begin
    s_axis_tready <= '1' when (state = READ_PATCH) else '0';

    process(aclk)
        variable p_val      : signed(11 downto 0);
        variable abs_gx     : signed(11 downto 0);
        variable abs_gy     : signed(11 downto 0);
        variable total_grad : signed(12 downto 0);
    begin
        if rising_edge(aclk) then
            if aresetn = '0' then
                state         <= READ_PATCH;
                byte_cnt      <= 0;
                gx_sum        <= (others => '0');
                gy_sum        <= (others => '0');
                m_axis_tvalid <= '0';
                m_axis_tlast  <= '0';
                m_axis_tdata  <= (others => '0');
                last_reg      <= '0';
            else
                case state is
                    when READ_PATCH =>
                        m_axis_tvalid <= '0'; 

                        if s_axis_tvalid = '1' then
                            p_val := signed("0000" & s_axis_tdata);

                            case byte_cnt is
                                when 0 => gx_sum <= -p_val;           gy_sum <= p_val;
                                when 1 => gx_sum <= gx_sum;           gy_sum <= gy_sum + shift_left(p_val, 1);
                                when 2 => gx_sum <= gx_sum + p_val;   gy_sum <= gy_sum + p_val;
                                when 3 => gx_sum <= gx_sum - shift_left(p_val, 1); gy_sum <= gy_sum;
                                when 4 => gx_sum <= gx_sum;           gy_sum <= gy_sum; -- Center pixel (weight 0)
                                when 5 => gx_sum <= gx_sum + shift_left(p_val, 1); gy_sum <= gy_sum;
                                when 6 => gx_sum <= gx_sum - p_val;   gy_sum <= gy_sum - p_val;
                                when 7 => gx_sum <= gx_sum;           gy_sum <= gy_sum - shift_left(p_val, 1);
                                when 8 => gx_sum <= gx_sum + p_val;   gy_sum <= gy_sum - p_val;
                            end case;

                            if byte_cnt = 8 then
                                last_reg <= s_axis_tlast;
                                state    <= CALC_OUTPUT;
                                byte_cnt <= 0; 
                            else
                                byte_cnt <= byte_cnt + 1;
                            end if;
                        end if;

                    when CALC_OUTPUT =>
                        if gx_sum < 0 then abs_gx := -gx_sum; else abs_gx := gx_sum; end if;
                        if gy_sum < 0 then abs_gy := -gy_sum; else abs_gy := gy_sum; end if;

                        total_grad := ('0' & abs_gx) + ('0' & abs_gy);

                        if total_grad > 255 then
                            m_axis_tdata <= "11111111";
                        else
                            m_axis_tdata <= std_logic_vector(total_grad(7 downto 0));
                        end if;

                        m_axis_tvalid <= '1';
                        m_axis_tlast  <= last_reg;

                        if m_axis_tready = '1' then
                            state <= READ_PATCH;
                        end if;
                end case;
            end if;
        end if;
    end process;
end Behavioral;
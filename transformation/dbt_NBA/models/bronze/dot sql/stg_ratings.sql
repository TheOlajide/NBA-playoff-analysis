SELECT
 Rk AS rank,
 Team AS team,
 Conf AS conference,
 Div AS division,
 W   AS wins,
 L   AS losses,
 W_L_perc AS win_loss_percentage,
 MOV AS margin_of_victory,
 ORtg AS offensive_rating,
 DRtg AS defensive_rating,
 NRtg AS net_rating,
 MOV_A AS moving_average,
 Ortg_A AS adjusted_offensive_rating,
 DRtg_A AS adjusted_defensive_rating,
 NRtg_A AS adjusted_net_rating,
 Year AS year
FROM
 {{source ('NBA_Project', 'ratings')}}
 
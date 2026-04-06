SELECT
 W AS wins,
 L AS losses,
 W_L_perc AS win_loss_percentage,
 GB AS games_behind,
 PS_G AS points_scored_per_game,
 PA_G AS points_allowed_per_game,
 SRS AS simple_rating_system,
 YEAR AS year
FROM
 {{source ('NBA_Project', 'teams_conf_standings')}}
# AFLPredictor-v1
This program aims to predict the outcome of each match of an AFL season. By using data from the previous 3 seasons, teams will be applied a score for each match which will be compared against their opponents score to determine a winner. 

Additionally, a set of ransomised variables will be applied to each score to alter the final result of a match. Without this feature, an upset would never due  to the team with the higher base score always winning.

# Data Used In Comparison

<p>A team's score for a match will have 4 variables applied with different weightings depending on how important that variable is. These variables are:

* Skill; A team will be given a score from 0 to 10 (not-inclusive) depending on their team's raw ability. This figure largely follows season predictions from AFL media organisations. Eg. for season 2025, the Brisbane Lions will be given a score of 9 and the Richmond Tigers will be given a score of 1.
* Stadium Peformance; A team's win/rate at a given venue over the previous 3 seasons. This variable is applied a multiplier of 1.2x for the home team and 0.8x for the away team
* VS Record; A team's win rate against specific opponents over the previous 3 seasons. This variable is applied a multiplier of 1x
* Win Rate; A taem's overall win/rate over the previous 3 seasons. This variable is applied a multiplier of 0.2x

Other variables that could be considered are:

* Time between matches; A shorter break of 5-6 days could apply a negative multiplier of 0.9x whilst a longer break could apply a multiplier of 1.1x
* Form; A tally of previous results could be kept that increments a team's skill value if they are on a predicted win streak. This could provide unique outcomes throughout the season if poor peforming teams go on an early win-streak and boost their skill rating. In it's current form, poor peforming teams will rarely climb higher than 13th position.</p>

# Example Output

<h3>-=-Round 24-=-</h3>

<h6>GWS Giants  VS  St Kilda  @  ENGIE Stadium  WINNER:  St Kilda || PRE-RANDOMISATION:  8.461 - 4.288 || POST-RANDOMISATION:  5.246 - 9.954</h6>
<h6>North Melbourne  VS  Adelaide Crows  @  Marvel Stadium  WINNER:  Adelaide Crows || PRE-RANDOMISATION:  3.383 - 7.153 || POST-RANDOMISATION:  4.628 - 6.947</h6>
<h6>Western Bulldogs  VS  Fremantle  @  Marvel Stadium  WINNER:  Fremantle || PRE-RANDOMISATION:  6.491 - 8.978 || POST-RANDOMISATION:  3.017 - 3.954</h6>
<h6>Collingwood  VS  Melbourne  @  MCG  WINNER:  Collingwood || PRE-RANDOMISATION:  8.853 - 5.683 || POST-RANDOMISATION:  7.61 - 6.362</h6>
<h6>Richmond  VS  Geelong Cats  @  MCG  WINNER:  Geelong Cats || PRE-RANDOMISATION:  1.771 - 9.358 || POST-RANDOMISATION:  1.468 - 10.418</h6>
<h6>Essendon  VS  Carlton  @  MCG  WINNER:  Carlton || PRE-RANDOMISATION:  4.76 - 7.361 || POST-RANDOMISATION:  0.467 - 6.895</h6>
<h6>Brisbane Lions  VS  Hawthorn  @  Gabba  WINNER:  Hawthorn || PRE-RANDOMISATION:  10.165 - 9.096 || POST-RANDOMISATION:  8.773 - 12.997</h6>
<h6>Port Adelaide  VS  Gold Coast Suns  @  Adelaide Oval  WINNER:  Gold Coast Suns || PRE-RANDOMISATION:  7.55 - 5.42 || POST-RANDOMISATION:  2.831 - 5.706</h6>
<h6>West Coast Eagles  VS  Sydney Swans  @  Optus Stadium  WINNER:  Sydney Swans || PRE-RANDOMISATION:  3.233 - 9.934 || POST-RANDOMISATION:  3.373 - 8.691</h6>

<h6>Round Upsets:  3</h6>

<h3>Post-Round Ladder</h3>

<h6>Brisbane Lions 18 5</h6>
<h6>Carlton 17 6</h6>
<h6>Sydney Swans 17 6</h6>
<h6>Collingwood 16 7</h6>
<h6>Fremantle 15 8</h6>
<h6>Geelong Cats 15 8</h6>
<h6>Hawthorn 15 8</h6>
<h6>Adelaide Crows 13 10</h6>
<h6>Western Bulldogs 13 10</h6>
<h6>GWS Giants 12 11</h6>
<h6>Gold Coast Suns 10 13</h6>
<h6>Port Adelaide 10 13</h6>
<h6>Essendon 9 14</h6>
<h6>Melbourne 9 14</h6>
<h6>North Melbourne 7 16</h6>
<h6>St Kilda 6 17</h6>
<h6>West Coast Eagles 3 20</h6>
<h6>Richmond 2 21</h6>

*Ladder still to be formatted

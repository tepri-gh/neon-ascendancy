# Garrison spike runbook

This is a development experiment, not a gameplay feature. Save first. The lead
installs the scripts and tweak with `tools/deploy.sh` and the CET panel with
`tools/deploy-probe.sh`, with the game closed. Start the game normally; open
CET's overlay and the Neon Ascendancy Garrison Spike window.

Outside the H10 lobby, stand in open space and press **Q1 Spawn** once. Wait
15 seconds for both requests. Press **Q2 PowerLevel** and wait one second.
Press **Q5 Name**, scan the first spawned unit and record whether its scanner
shows `NA Spike Boss (Lieutenant)`. Press **Q3 AI** and watch the three-point
patrol, then the fight (up to 60 seconds after the patrol ends). Workspot is
reported UNKNOWN because no reference was selected. Attitudes are logged as
numeric EAIAttitude values. Avoid repeating a test before it finishes.

At the working H10 lobby lift, stand by the door, press **Q4 Lift capture**,
and read the logged lift, active floor and floor count. Set **Call cab to
floor** to the floor you stand on (the panel defaults it to the active floor)
and **Ride to floor** to another one (default active + 1), then press **Lift
board & ride**. The spike spawns four units 2 m behind you, calls the cab and
waits (up to 30 s) until it has stopped at your floor, sends the units into
the cab, logs how many are inside after 8 s (`boarded=`), rides to the target
floor, waits until the cab stops there, and logs each unit's height change.
PASS needs three of the four to have moved more than 2.5 m. A `cab not at
floor` FAIL means the floor index is wrong for this lift or the cab never
answered. The four lift units are tracked separately from Q1's units. Allow
about a minute for the result.

Press **Cleanup** after all checks. The count is despawn requests, not proof
that the entities disappeared. Inspect them in game. Do not start another test
until the previous one finishes; cleanup does not cancel scheduled callbacks.

Lines beginning `GarrisonSpike: Q<n>` use PASS for a measured condition, FAIL
for a measured failure or missing spawn completion, and UNKNOWN for observations
or unavailable evidence. Q5 is always UNKNOWN until visually checked. The last
10 lines appear in the panel and are appended to `spike.log` in the
`NeonAscendancySpike` CET mod folder. Send that file and the scanner
observation back to the lead. The native plugin log also receives the lines.

# Owner decisions pending

Calls only the owner can make, collected from the venue research waves. Things
to *look at* in game live on the tour checklists instead (see
`docs/venue-playbook.md` section 7). Research agents list new calls in their
proposal's `owner_decisions`; the lead agent adds them here after each wave.

Answer inline (a word is enough) and the lead agent applies it, then deletes
the item. Items marked **(after tour)** only matter if the tour shows the
problem.

## 1. Named people who are missing or could move

The venue layer can only re-use vanilla's own spawn data. These characters have
none outside their quest scenes, so placing them is a cast-layer job
(`data/clean-slate/cast_and_hubs.json`).

1. **Susie Q at Lizzie's Bar.** Lizzie's owner exists only inside q105's quest
   prefab (scene triggers and props). Add her through the cast layer, or leave
   the bar without its boss?
2. **Rachel Casich at Fourth Wall Studios.** The studio's owner only spawns
   with her quest crew. Add her alone, or leave her out?
3. **Zuleikha at Gloria's house.** She lives there per the wiki but has no
   spawn entry. Add her?
4. **Adam Ibrahimovic and Larry Fanghorn** (`sts_cct_dtn_03`). The venue's
   owners exist only as gig characters. Add them?
5. **Anthony Harris's farm** (`sq021_farm`). The "meatman" is a braindance
   actor, so the farm is unattended. Fine, or add a caretaker?
6. **XBD studio owner** (`q105_braindance_studio`). No named scavenger boss
   exists; the elite tacticians stand in. Fine, or design a named owner?
7. **Sasquatch at Pacifica Mall.** Her `hall_chat` phase would suit a relaxed
   mall boss, but vanilla never spawns it, so the checker blocks it. Allow it?
8. **Brigitte.** Both the Chapel of the Black Madonna and the elders' lair
   could own her, and neither has a non-quest spot. Which one, or neither?
9. **Mr. Hands.** The cast layer seats him at his fixer spot; Heavy Hearts
   also has a `#ws_mr_hands_default` in his suite. Move him to the club?
10. **Claire.** Stays at the Afterlife bar (vendor) and Marianne's garage is
    left to its mechanic. Keep it that way?
11. **Bill and Charles at Dodger's precinct** (`sts_ep1_10`). The gig's
    premise is that Dodger already holds them. Leave them out (current), or
    show the blackmail operation permanently (kneeling/hiding)?
12. **Anderson at Haven Clinic** (`sts_ep1_01`). He is present but not an
    interactive ripperdoc; his vendor spawn set belongs to the Dogtown vendor
    layer. Make him a working ripperdoc?
13. **Lizzy Wizzy at the No-Tell Motel** (`q005_notell_motel`). The proposal
    puts her at her room window (`mq019_01_at_window`). Keep her there, or
    leave the room empty?

## 2. How full or busy a venue should be

14. **Dark Matter lounge.** Vanilla has no crowd outside the Us Cracks
    premiere, so the lounge is empty with a doorman downstairs. Keep it a
    quiet private-event lounge, or re-use the relaxed party guests as
    regulars?
15. **Rosebud.** Six Animals plus two warehouse posts, no civilian crowd.
    Fewer guards, or add a public crowd? **(after tour)**
16. **Ghost Town.** Seven Wraith guard posts for a town "only occasionally"
    visited. Keep all seven, or just the bar/fuel-station pair?
    **(after tour)**
17. **Chapel of the Black Madonna.** Vanilla fills it 08:00-18:00; ours is
    full all day. Add a time gate later?
18. **Odell's annex at Haven Clinic.** It reads as a second clinic across
    the road. Keep it, or drop it (Odell then absent)?
19. **Kabuki street maze.** The district phase also switches on the
    nervous-looking street crowd (junkies, street men/women). Accept it, or
    have the clean slate deactivate specific entries? **(after tour)**
20. **Silver Pixel Cloud drive-in.** Empty and shut by design. Give it a
    scav holding crew (the design's rule for neutral nodes)?
21. **Hotel ambush site** (`q305_netwatch_ambush`). 6th Street is the venue's
    own population but their base is Santo Domingo. Keep 6th Street, or
    prefer local scavs?
22. **SoCal border crossing.** Both Border Patrol and Militech crews are
    kept. Trim to one if it looks doubled? **(after tour)**

## 3. Access and privacy

23. **Peralez apartment.** The door policy lets V walk into the Peralezes'
    home while they are in it (design section 10: everything accessible).
    Keep, or exclude their front hallway door like Judy's flat?
24. **Judy's flat.** Stays locked until the companion/apartment pass.
    Confirm.
25. **Night City Prison visitor entrance.** Vanilla opens it only through the
    intercom dialogue. If it has an NCPD authorization module the policy
    leaves it locked. Allow a policy exception? **(after tour)**
26. **Nighthawks bar shutters.** Vanilla force-closes all seven window
    shutters even in ambient play; the policy never force-opens. Add a venue
    action that opens them?

## 4. Hostile on sight?

Vanilla sets neutral attitudes inside phases we do not run, so some groups may
default hostile. Each is: keep neutral (needs an attitude action) or reduce to
the non-combat people. **(after tour)**

27. Militech at the q114 tunnel site.
28. Arasaka Estate gate sentries and patrols (neutral curtilage or restricted?).
29. Animals at the paint factory gym (`sts_pac_wwd_05`).
30. q103 mine turrets (live and hostile from the tunnel?) and Nash as a
    possible boss with a health bar.

## 5. Tooling scope

31. **Parked cars** (`q000_underground_parking_lot`). The garage's 22 cars
    are quest vehicle spawners; venues cannot activate spawners yet. Extend
    the builder, or accept an empty garage?
32. **Diner crowd** (`sq012_diner`). Only 28 of 33 entries run, because the
    community's overall posture rates alert. Add a per-entry override so all
    33 can run?
33. **Dogtown-wide switch.** Several Dogtown venues re-activate communities
    the vanilla layer may also run. Keep per-venue activations, or one
    Dogtown-wide switch?
34. **Container-zone yard** (`q302_way_to_blackbox`). Should the later batch
    venue `container_zone` own the yard's garrison instead of this venue?
35. **Cerberus on display at Cynosure.** The bunker's standby robot is the
    one unkillable unit; leave it out (current) or show it?
36. **Arasaka tower lift seal.** Allow `ForceUnseal` for the sealed lift door
    if `ForceUnlock` does not clear it? **(after tour)**
37. **Tenth worker at the Arasaka Industrial Park lookout.** Its only phase
    is nervous/alert. Add it after a visual check?
38. **Farmhouse power** (`sq004_abandoned_farmhouse`). Keep the abandoned,
    unpowered look, or a lit, lived-in landmark?

## 6. Wave 11

39. **Arasaka safe house** (`q112_safe_house`). Vanilla's only people are
    the raid and Hanako/Takemura hiding from it, so it is an empty, intact
    ruin (gate and passage open). Keep it as a venue, or drop it? Give it a
    later purpose (scav squat, player safehouse, stash)? Allow loading the
    raid-dressed quest prefab if the shell turns out bare?
40. **Love Shack** (`sq030_love_shack`). Lights on (proposed) or dark and
    derelict? Should Judy ever rest here? Scenery only, or a later
    safehouse / dive-job site?
41. **Eva Cole's yacht** (`sts_cct_dtn_05`). A running party (proposed) or a
    quiet moored yacht with crew and security? Keep the doll guests? Add
    Eva Cole as a new cast entry?
42. **C-Team office** (`sts_std_rcr_01`). Rogue's fixer car outside as
    dressing? All ten guards (proposed) or only gate and patrol? Vic Vega
    as the owner on the floor (proposed)?
43. **7th Hell** (`sts_cct_dtn_02_metal_club`). Keep the 500-eddie cover
    charge as a mod gate, or free entry (current)? Place Jack Mausser (no
    vanilla spawn data)? Full nightclub (proposed) or low-key bar?
44. **Delamain HQ** (`sq025_delamain_garage`). Keep the eight-person
    complaint queue (staged for the cab crisis), or a quiet lobby with the
    cleaner?
45. **Brainporium** (`mq303_shanks_store`). Tool as a calm regular
    (proposed), absent, or locked in the basement cell (the job's premise)?
46. **Red Peaks bus stop** (`sq017_ambush`, excluded). Mod-authored content
    later (nomad pull-off, checkpoint, stall)?
47. **The Hammer, 2077** (`q101_backalley`, excluded). Should the planned
    new Hammer include this back alley and rooftop? Should Totentanz get a
    back-of-house? Where do Nancy, Denny and Henry belong (unplaced now)?
48. **Dry Creek protein farm and Yucca** (`q000_protein_farm`,
    `q000_roadhouse_town`). The farm sits about 1.2 km south of the border,
    outside free roam. Should the border fix let V drive into the SoCal
    prologue area, or do these stay scenery? Farm empty (proposed) or
    Jackie's Badlands camp? Who holds Yucca (Scav, Aldecaldos supply stop,
    NCPD)? Keep Sheriff Jones? Make the food cart and garage real vendors
    later?
49. **Chram Denya Jinja shrine** (`sts_wbr_jpn_03`). Seven Tyger guards
    (proposed) or just the stair pair? Restore the interior's device set
    (doors, shutters, honden terminal as fittings), or courtyard only?
50. **High Peak VDB meeting ground** (`mq304_vdb_meeting`). Jago standing
    there permanently (proposed)? A standing Voodoo Boys site, or neutral
    construction they borrow?
51. **Municipal landfill** (`q101_landfill`). Empty dump with a toggle-only
    entry (proposed), or no entry? A scavenging or waste node in the org
    game later?
52. **Rancho Coronado coffee cart** (`sq017_emptystreet`). One silent
    barista (proposed), an empty corner, or later a working coffee vendor?
53. **Jackie's garage** (`sq018_jackies_storage`). Add Jackie there through
    the cast layer, or keep him for the companion design? Open to V like any
    venue, or shut like Judy's flat? Keep his ARCH parked inside (proposed)?
54. **Laguna Bend drowned town** (`sq030_underwater_house`). Leave it an
    unreachable landmark, or add a dive or boat route? Should Judy's dive
    gear exist as ordinary equipment?
55. **Revere Courier depot** (`sts_wat_nid_02`). Keep the courier van the
    gig steals (proposed)? Open for business (proposed) or a shut-up Tyger
    Claw front? Tyger Claws neutral here, or hostile on sight?
56. **Wellsprings pump station beach** (`q111_pumpstation`). A permanent
    beach rave (proposed) or just the homeless crowd? Invented staff or
    security for the unmanned facility later?
57. **Longshore Stacks courtyard** (`sts_ep1_03_gunfight`). A plain chapel
    yard (proposed) or a permanent memorial for Jason Foreman? Briana Dolson
    as the Stacks' resident representative?

## 7. Wave 12

58. **Lift access (cross-venue).** The door policy never touches lifts
    (playbook rule 13), so a floor that needs authorisation stays shut. It
    matters at Dark Matter, the Peralez penthouse and the Gutierrez
    penthouse. Extend the policy to authorise lift floors at venues, or
    keep lifts vanilla?
59. **Panam's freight bay** (`q103_meeting_point_panam`). Empty bay
    (proposed) or stage Panam and her car there? Leave the yard to the
    ambient crowd (proposed) or invent workers?
60. **Megabuilding H6, floor 19** (`sts_std_arr_11`). A live 6th Street den
    (proposed) or a sealed floor? Include the three-ganger reinforcement
    wave? Lucius as the resident techie (proposed) or a generic netrunner?
    Door policy (current) or a placed door code? Computers powered
    (proposed) or the gig's sabotaged look?
61. **Boat Drinks beach** (`sq028_beach`, excluded). Is the *Seamurai*
    intact and part of the Gold Beach Marina yacht venue? Ambient people on
    the beach later?
62. **Columbarium** (`q204_columbarium`, nothing to restore). Arasaka
    security, funeral staff or a vendor (all recommended no)? Re-activate
    the crowd if the tour finds it empty?
63. **Jacked and Coke** (`sts_hey_rey_08`). Karubo as the owner
    (proposed)? All nine staff and regulars, or five? Padre's driver and
    the reinforcement car stay out (proposed)?
64. **Motel Kabuki** (`sts_wat_kab_08`). Keep the bouncer vanilla never
    activates? Anna Hamill absent (proposed) or placed? The full 34 people,
    or fewer civilians?
65. **Bennett alley** (`mq304_bennett_meeting`). The driver and Thrax as an
    everyday wait (proposed) or an empty alley? Show the clutter
    (proposed) or vanilla's bare lane? A mod meeting or dead-drop site
    later?
66. **Tranquil Terrace** (`q304_songbird_meeting`). Songbird here at all
    (proposed no)? Both gangs stay (proposed)? Keep the airdrop camp
    populated permanently, even though vanilla despawns it?
67. **Luxor High Wellness Spa** (`sts_ep1_12`). Milko and Alan Noël stay
    (proposed)? All 22 androids plus the heavy, or fewer? Ayo Zarin's wing
    stays with the `we_ep1_05` venue (proposed)? Accept the courier, drone
    and broken android that come with the whole garrison (proposed)?
68. **Night Corp tour trail** (`mq061`, excluded). Revive the Pacifica
    hazmat camp or the Med Center medics (both recommended no)? Author a
    Night Corp investor tour later?
69. **Coastview relay tower** (`q110_surroundings`). A six-man Voodoo Boys
    watch (proposed), the initial pair, or only ambient people? Kids stay
    with the Arroyo venue, or a Coastview kid crowd?
70. **Poppy Farm** (`sq021_farm_wrong`). A Wraith garrison (proposed) or
    abandoned? All ten, or fewer? Smuggled-goods content later?
71. **Gutierrez penthouse** (`sts_wbr_hil_01`). Owners absent (no vanilla
    data) or add them? Alarm, turrets and gates armed or calmed? The
    penthouse floor open to all, or resident-only (see 58)?
72. **Hillpark campfire and plaza** (`mq304_ce_1`, `hip_mq304_ce`, nothing
    to restore). Kurt's four soldiers as a standalone patrol, or his car
    parked there (both recommended no)? A standing Barghest post on the
    plaza? Force the plaza's security area safe if it reacts?
73. **Cali Express** (`q004_braindance_store`). Its vendor was gated on
    `q004_done`; the lead agent added `hey_gle_foodshop_01_default_on` to
    the vendor facts so it trades normally. Keep it a normal shop with the
    robbery as backstory (recommended)?
74. **Bullard & Sequoia site** (`mq059_freedom`). Staffed (proposed) or
    empty? Working look (proposed) or bare? Yorinobu's Mordred parked there
    (recommended no)? Accept the restricted-area security, or ask for an
    exception? Two 6th Street gangers at the dam corner?
75. **Clement St. house** (`sts_bls_ina_09`, nothing to restore). Empty
    derelict (recommended) or a scav squat? Basement sealed (recommended)
    or opened?
76. **Psychiatric center** (`sts_std_rcr_02`). Jasmine Dixon sedated in
    cell 7 (proposed) or left out? All ten orderlies or the seven core
    guards? Vanilla security areas (the restricted wing turns hostile) or
    a calmer setup? Trim the ten patients and staff?
77. **Old WNS station** (`sts_wat_nid_12`). The lead agent added Max Jones
    in his default chair (vanilla's own activation). Keep him there
    (recommended)? Keep the trapped door, turret, cameras and mines as
    atmosphere if inert? If the front door is locked, a door-action
    exception, or the roof ladder as the only way in?

## 8. Wave 13

78. **Hostile garrisons (cross-venue, replaces asking venue by venue).**
    Vanilla often makes a venue's guards neutral only inside a quest phase
    we do not run, so they may attack on sight: Cytech, C-Team, the casino,
    Rosebud, the paint factory, Militech's tunnel site, Arasaka Estate,
    Lina's scavs and the Maelstrom warehouse among them. Build a small
    attitude layer that sets venue garrisons neutral until provoked (faction
    hostility stays a sim decision), or trim each hostile venue to its
    non-combat people? **(after tour)**
79. **Leah Gladen** (`sts_wbr_jpn_12`, `sts_wbr_jpn_12b`). Alive in our
    timeline, but vanilla only has her corpse. Hand-author her alive in her
    Japantown flat (recommended), or leave the flat empty?
80. **Japantown Apartments** (`sts_wbr_jpn_12`). The gig's bespoke guard as
    building security (recommended no)? Keep the service worker
    (recommended yes)? The hidden stash shutter openable as vanilla
    (recommended)?
81. **Wired Head** (`sts_wbr_jpn_12b`). All ten Claws (recommended) or
    fewer? Add the two reinforcement gunmen (recommended no)?
82. **Eisenhower St. block** (`sts_wat_kab_05`). Keep the joytoy and BD
    civilians, or Scavengers only? Basement reachable or sealed? A standing
    Scavenger crew, or let the territory layer own the den?
83. **Kabuki rooftop slums** (`sts_wat_kab_101`). Scavs and residents
    (recommended), or one group? Were the residents already driven out?
    Hand-place Jae-Hyun (no vanilla data)?
84. **Lina's home** (`mq303_linas_mansion`). Add Lina (vanilla never places
    her there, so it needs a hand-made placement) or leave the flat to her
    crew? All five scavs, a light guard, or none? Schedule variant 0
    (proposed) or 1? Keep the parked Archer Hella?
85. **City Center back alley** (`q306_meeting_spot`). The one sleeper
    (proposed) or an empty alley? Songbird's spy van never here
    (recommended), or her fixed spot?
86. **The Hammer, 2077, continued** (`q108_back_alley`, excluded). Reuse this
    alley too (recommended)? Any trace of the 2013 abduction (recommended
    no)? Where does Lyle Thompson belong in 2077?
87. **Soulkiller room** (`q101_soulkiller_room`, excluded). Keep it excluded
    (recommended), or repurpose it as a present-day Arasaka Soulkiller lab?
    Saburo's 2077 home is the tower's executive level, not this set.
88. **Cytech factory** (`sts_std_arr_10`). Ten guards (recommended), fewer if
    hostile (see 78)? A working plant (recommended)? Rihanna Kumar absent
    (recommended)?
89. **Tyger Claws casino** (`sts_wbr_hil_07`). Free entry (recommended) or a
    mod toll at the culvert (like 7th Hell's cover charge)? Keep the bar
    vendor here (recommended)? Post-heist guards off (recommended)? Vortex
    out (recommended) or a living netrunner stand-in?
90. **Maelstrom warehouse** (`mq032_maelstrom_warehouse`). A live Maelstrom
    stash (proposed) or empty? Both monks out, or a non-quest cameo? Fenrir
    left as world loot, or removed? Maelstrom hostile or neutral (see 78)?
91. **Kenmore Diner** (`sts_std_arr_12_diner`). Vanilla's thin crowd
    (proposed) or extra staff? Scenery, or a mod food vendor later (vanilla
    has no vendor node)?
92. **Landfill road** (`q101_landfill_road`, nothing to restore). Chase-only
    road lights off (recommended) or on permanently? Convoy or ambush
    content later?
93. **Cynosure Site D** (`mq305_wanted_lab`). A dormant, sealed site
    (proposed) or a re-occupied Militech post (needs new cast)? Leave its
    turrets, mines and cameras live? Can the squat lift reach the lab (see
    58)? Replay Evan McRay's video logs?
94. **Boxing ring by Montezuma's Throne** (`mq306_boxing_ring`). A live bout
    with a full crowd (recommended) or an empty ring? Add Aaron Waines by
    hand (vanilla never places him there)? Angie and her two Animals stay
    out (recommended)?
95. **Memorial Park NCART station** (`sts_cct_cpz_01`). The security wing
    enterable with a trespass warning (recommended)? Activate the two unused
    corpo passengers (recommended yes)? Does the concourse belong to this
    venue or to the metro venue?
96. **El Pinche Pollo** (`sts_hey_gle_04`). The office inert (proposed) or
    staged with the gig's evidence? Generic boss and bouncer, or name them
    Mauricio Salinas and Ernesto Muñoz? A neutral hangout downstairs only,
    or a hostile restricted upstairs (see 78)?
97. **BuryGer** (`mq022_ezekiel`). Robbers out (recommended)? King's
    Clampdown briefing booth out (recommended)? The quest's own barman
    (recommended)?
98. **Farida's clinic** (`q303_macs_clinic`). The lead agent added Farida at
    work (her only vanilla phase is `faceplate_meeting`). Keep her? Should
    she sell cyberware (needs the vendor layer)? Kurt's AV over Dogtown off
    (default) or forced on? A research pass for Anderson's Monument Ave
    ripperdoc point of interest?
99. **Yucca radio tower** (`q000_radio_tower`, nothing to restore).
    Unmanned (proposed) or a maintenance presence? Restore the quest prefab
    and Willie's car? Pin q000's air-traffic vista?

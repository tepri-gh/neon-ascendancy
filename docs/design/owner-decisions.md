# Owner decisions pending


> **2026-11-27:** Items #59–182 have been resolved automatically against [`venue-node-policy.md`](venue-node-policy.md) and the finalized classification in [`venue-classification.md`](venue-classification.md) (all 11 undecideds settled by the owner).
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

   A: Add her.

2. **Rachel Casich at Fourth Wall Studios.** The studio's owner only spawns
   with her quest crew. Add her alone, or leave her out?

   A: Add her and the crew.

3. **Zuleikha at Gloria's house.** She lives there per the wiki but has no
   spawn entry. Add her?

   A: Don't add her, popular player home mod uses the location.

4. **Adam Ibrahimovic and Larry Fanghorn** (`sts_cct_dtn_03`). The venue's
   owners exist only as gig characters. Add them?

   A: Add them.

5. **Anthony Harris's farm** (`sq021_farm`). The "meatman" is a braindance
   actor, so the farm is unattended. Fine, or add a caretaker?

  A: No meatman

6. **XBD studio owner** (`q105_braindance_studio`). No named scavenger boss
   exists; the elite tacticians stand in. Fine, or design a named owner?

A: The problem is we're going to be using these kinds of locations and swapping
affiliation + spawns based on node capture, so we need to dynamically generate
an owner (also if the player ever kills a boss/owner anywhere, they need to be
dynamically replaced.)

7. **Sasquatch at Pacifica Mall.** Her `hall_chat` phase would suit a relaxed
   mall boss, but vanilla never spawns it, so the checker blocks it. Allow it?

A: Allow it, make sure she isn't at the gym.

8. **Brigitte.** Both the Chapel of the Black Madonna and the elders' lair
   could own her, and neither has a non-quest spot. Which one, or neither?

A: Elder's Lair

9. **Mr. Hands.** The cast layer seats him at his fixer spot; Heavy Hearts
   also has a `#ws_mr_hands_default` in his suite. Move him to the club?

A: Keep him in the suite.

10. **Claire.** Stays at the Afterlife bar (vendor) and Marianne's garage is
    left to its mechanic. Keep it that way?

A: Yes

11. **Bill and Charles at Dodger's precinct** (`sts_ep1_10`). The gig's
    premise is that Dodger already holds them. Leave them out (current), or
    show the blackmail operation permanently (kneeling/hiding)?

A: Leave them out.

12. **Anderson at Haven Clinic** (`sts_ep1_01`). He is present but not an
    interactive ripperdoc; his vendor spawn set belongs to the Dogtown vendor
    layer. Make him a working ripperdoc?

A: Working ripperdoc. I forget if we still allow shops/ripperdoc areas to be
safe zones, but if not we need some way to prevent actor death, either that or a
system that allows vendors to die and be replaced, either way deferred mechanic.

13. **Lizzy Wizzy at the No-Tell Motel** (`q005_notell_motel`). The proposal
    puts her at her room window (`mq019_01_at_window`). Keep her there, or
    leave the room empty?

A: Would rather have her at the venue at the end of the quest? Forget which one.

## 2. How full or busy a venue should be

14. **Dark Matter lounge.** Vanilla has no crowd outside the Us Cracks
    premiere, so the lounge is empty with a doorman downstairs. Keep it a
    quiet private-event lounge, or re-use the relaxed party guests as
    regulars?

A: Relaxed party guests.

15. **Rosebud.** Six Animals plus two warehouse posts, no civilian crowd.
    Fewer guards, or add a public crowd? **(after tour)**

A: Public crowd.

16. **Ghost Town.** Seven Wraith guard posts for a town "only occasionally"
    visited. Keep all seven, or just the bar/fuel-station pair?
    **(after tour)**

A: All seven.

17. **Chapel of the Black Madonna.** Vanilla fills it 08:00-18:00; ours is
    full all day. Add a time gate later?

A: Time gate it later.

18. **Odell's annex at Haven Clinic.** It reads as a second clinic across
    the road. Keep it, or drop it (Odell then absent)?

A: Keep it.

19. **Kabuki street maze.** The district phase also switches on the
    nervous-looking street crowd (junkies, street men/women). Accept it, or
    have the clean slate deactivate specific entries? **(after tour)**

A: Accept it.

20. **Silver Pixel Cloud drive-in.** Empty and shut by design. Give it a
    scav holding crew (the design's rule for neutral nodes)?

A: Open it, no holding crew.

21. **Hotel ambush site** (`q305_netwatch_ambush`). 6th Street is the venue's
    own population but their base is Santo Domingo. Keep 6th Street, or
    prefer local scavs?

A: Keep 6th street. The city is going to be a mess early on, and clearing out
neighbouring nodes taken by other gangs in their local areas is the "creeping"
phase.

22. **SoCal border crossing.** Both Border Patrol and Militech crews are
    kept. Trim to one if it looks doubled? **(after tour)**


A: Whatever vanilla uses. If not just border patrol.

## 3. Access and privacy

23. **Peralez apartment.** The door policy lets V walk into the Peralezes'
    home while they are in it (design section 10: everything accessible).
    Keep, or exclude their front hallway door like Judy's flat?

A: Keep.

24. **Judy's flat.** Stays locked until the companion/apartment pass.
    Confirm.

A: There's too many issues like this, just have it open.

25. **Night City Prison visitor entrance.** Vanilla opens it only through the
    intercom dialogue. If it has an NCPD authorization module the policy
    leaves it locked. Allow a policy exception? **(after tour)**

A: Get rid of the policy. We can't have areas like this gated.

26. **Nighthawks bar shutters.** Vanilla force-closes all seven window
    shutters even in ambient play; the policy never force-opens. Add a venue
    action that opens them?


A: Sure that's fine.

## 4. Hostile on sight?

Vanilla sets neutral attitudes inside phases we do not run, so some groups may
default hostile. Each is: keep neutral (needs an attitude action) or reduce to
the non-combat people. **(after tour)**

27. Militech at the q114 tunnel site.
28. Arasaka Estate gate sentries and patrols (neutral curtilage or restricted?).
29. Animals at the paint factory gym (`sts_pac_wwd_05`).
30. q103 mine turrets (live and hostile from the tunnel?) and Nash as a
    possible boss with a health bar.


A: Keep neutral. Attitude needs to be based specifically on V's affiliation so
all spawns should be neutral. We can work out later what should be considered
hostile areas when she has neutral relations with a gang/corp. I want to be able
to check off two things for venues during a tour:

1. Use as node yes or no
2. Node type (we can work out node types and their properties for design in a discussion while subagents run)

## 5. Tooling scope

31. **Parked cars** (`q000_underground_parking_lot`). The garage's 22 cars
    are quest vehicle spawners; venues cannot activate spawners yet. Extend
    the builder, or accept an empty garage?

A: Extend the builder. You do this yourself (or you can spawn GPT 6.2 Sol on medium to do it), don't use a subagent.

32. **Diner crowd** (`sq012_diner`). Only 28 of 33 entries run, because the
    community's overall posture rates alert. Add a per-entry override so all
    33 can run?

A: 28 of 33 is fine.

33. **Dogtown-wide switch.** Several Dogtown venues re-activate communities
    the vanilla layer may also run. Keep per-venue activations, or one
    Dogtown-wide switch?

A: Per-venue I think? Probably best to keep it granular, interested in your
thoughts though.

34. **Container-zone yard** (`q302_way_to_blackbox`). Should the later batch
    venue `container_zone` own the yard's garrison instead of this venue?

A: I need a tour stop on this to decide.

35. **Cerberus on display at Cynosure.** The bunker's standby robot is the
    one unkillable unit; leave it out (current) or show it?

A: Cynosure bunker should be sealed off/inaccessible, leave it out. Too many
lore implications.

36. **Arasaka tower lift seal.** Allow `ForceUnseal` for the sealed lift door
    if `ForceUnlock` does not clear it? **(after tour)**

A: Yes.

37. **Tenth worker at the Arasaka Industrial Park lookout.** Its only phase
    is nervous/alert. Add it after a visual check?

A: No.

38. **Farmhouse power** (`sq004_abandoned_farmhouse`). Keep the abandoned,
    unpowered look, or a lit, lived-in landmark?

A: Keep it lit.

## 6. Wave 11

39. **Arasaka safe house** (`q112_safe_house`). Vanilla's only people are
    the raid and Hanako/Takemura hiding from it, so it is an empty, intact
    ruin (gate and passage open). Keep it as a venue, or drop it? Give it a
    later purpose (scav squat, player safehouse, stash)? Allow loading the
    raid-dressed quest prefab if the shell turns out bare?

A: Later purpose, need tour stop to decide if worth keeping as a venue.

40. **Love Shack** (`sq030_love_shack`). Lights on (proposed) or dark and
    derelict? Should Judy ever rest here? Scenery only, or a later
    safehouse / dive-job site?

A: Lights on. Rule going forward is lights always on.

41. **Eva Cole's yacht** (`sts_cct_dtn_05`). A running party (proposed) or a
    quiet moored yacht with crew and security? Keep the doll guests? Add
    Eva Cole as a new cast entry?

A: Quiet moored yacht with crew and security. We need an owner here though, this is a
good venue for dynamic freelancer missions.

42. **C-Team office** (`sts_std_rcr_01`). Rogue's fixer car outside as
    dressing? All ten guards (proposed) or only gate and patrol? Vic Vega
    as the owner on the floor (proposed)?

A: Should be fine. Go ahead with this and then I'll tour it.

43. **7th Hell** (`sts_cct_dtn_02_metal_club`). Keep the 500-eddie cover
    charge as a mod gate, or free entry (current)? Place Jack Mausser (no
    vanilla spawn data)? Full nightclub (proposed) or low-key bar?

A: Free entry, place jack, full nightclub.

44. **Delamain HQ** (`sq025_delamain_garage`). Keep the eight-person
    complaint queue (staged for the cab crisis), or a quiet lobby with the
    cleaner?

A: Quiet lobby and we drop this as a potential node. Delamain remains a fully
neutral contractor for gangs to use in a later Delamain system.

45. **Brainporium** (`mq303_shanks_store`). Tool as a calm regular
    (proposed), absent, or locked in the basement cell (the job's premise)?

Calm regular and then drop this as a possible node/venue we use.

46. **Red Peaks bus stop** (`sq017_ambush`, excluded). Mod-authored content
    later (nomad pull-off, checkpoint, stall)?

A: Mod authored content later. Will need tour to decide.

47. **The Hammer, 2077** (`q101_backalley`, excluded). Should the planned
    new Hammer include this back alley and rooftop? Should Totentanz get a
    back-of-house? Where do Nancy, Denny and Henry belong (unplaced now)?

A: Seems fine to include the alley and roof, Totentanz can have a back of house.
Nancy, Denny and Henry can probably be excluded from spawns? You can help decide
this.

48. **Dry Creek protein farm and Yucca** (`q000_protein_farm`,
    `q000_roadhouse_town`). The farm sits about 1.2 km south of the border,
    outside free roam. Should the border fix let V drive into the SoCal
    prologue area, or do these stay scenery? Farm empty (proposed) or
    Jackie's Badlands camp? Who holds Yucca (Scav, Aldecaldos supply stop,
    NCPD)? Keep Sheriff Jones? Make the food cart and garage real vendors
    later?

A: NCPD can hold Yucca, keep the Sheriff. Garage might be used for a vehicle
customization system later (thinking something like NFS Underground 2, simple
engine/transmission etc improvement system).

49. **Chram Denya Jinja shrine** (`sts_wbr_jpn_03`). Seven Tyger guards
    (proposed) or just the stair pair? Restore the interior's device set
    (doors, shutters, honden terminal as fittings), or courtyard only?

A: Restore interior and the seven guards are fine.

50. **High Peak VDB meeting ground** (`mq304_vdb_meeting`). Jago standing
    there permanently (proposed)? A standing Voodoo Boys site, or neutral
    construction they borrow?

A: I need to tour this to decide. Make sure there's a new "decisions" doc after
this.

51. **Municipal landfill** (`q101_landfill`). Empty dump with a toggle-only
    entry (proposed), or no entry? A scavenging or waste node in the org
    game later?

Empty dump toggle only.

52. **Rancho Coronado coffee cart** (`sq017_emptystreet`). One silent
    barista (proposed), an empty corner, or later a working coffee vendor?

Empty corner drop this from our venues.

53. **Jackie's garage** (`sq018_jackies_storage`). Add Jackie there through
    the cast layer, or keep him for the companion design? Open to V like any
    venue, or shut like Judy's flat? Keep his ARCH parked inside (proposed)?

A: Sure have Jackie there, we will need a system later that removes these spawns
if they're with V though.

54. **Laguna Bend drowned town** (`sq030_underwater_house`). Leave it an
    unreachable landmark, or add a dive or boat route? Should Judy's dive
    gear exist as ordinary equipment?

A: Leave it as unreachable.

55. **Revere Courier depot** (`sts_wat_nid_02`). Keep the courier van the
    gig steals (proposed)? Open for business (proposed) or a shut-up Tyger
    Claw front? Tyger Claws neutral here, or hostile on sight?

A: Proposals are both good, Tyger Claw neutral, again, affiliation and
replacement system, could be a node.

56. **Wellsprings pump station beach** (`q111_pumpstation`). A permanent
    beach rave (proposed) or just the homeless crowd? Invented staff or
    security for the unmanned facility later?

A: Rave should only happen at night. Security for the facility? I need a tour
stop to decide. Facility is possible node.

57. **Longshore Stacks courtyard** (`sts_ep1_03_gunfight`). A plain chapel
    yard (proposed) or a permanent memorial for Jason Foreman? Briana Dolson
    as the Stacks' resident representative?


A: Proposal is fine.

## 7. Wave 12

58. **Lift access (cross-venue).** The door policy never touches lifts
    (playbook rule 13), so a floor that needs authorisation stays shut. It
    matters at Dark Matter, the Peralez penthouse and the Gutierrez
    penthouse. Extend the policy to authorise lift floors at venues, or
    keep lifts vanilla?

A: Why are we not touching lifts? Lifts should be touched, areas can't be
inaccessible unless they have strict lore implications and we cannot otherwise
modify them to remove those implications (Like the NUSA crash site or the
Cynosure bunker)

59. **Panam's freight bay** (`q103_meeting_point_panam`). Empty bay
    (proposed) or stage Panam and her car there? Leave the yard to the
    ambient crowd (proposed) or invent workers?
   **Auto-resolved (2026-11-27):** Drop from nodes (nothing to restore / open-world ambient only); keep civilian ambient life and vendors where applicable, no gang garrison or gig cast.
60. **Megabuilding H6, floor 19** (`sts_std_arr_11`). A live 6th Street den
    (proposed) or a sealed floor? Include the three-ganger reinforcement
    wave? Lucius as the resident techie (proposed) or a generic netrunner?
    Door policy (current) or a placed door code? Computers powered
    (proposed) or the gig's sabotaged look?
   **Auto-resolved (2026-11-27):** Keep a live neutral garrison and generic tech staff, omit Lucius and reinforcements, make doors usable and computers powered. (`loc_sts_std_arr_11` -> `node`, `sixth_street` `large` `military`)
61. **Boat Drinks beach** (`sq028_beach`, excluded). Is the *Seamurai*
    intact and part of the Gold Beach Marina yacht venue? Ambient people on
    the beach later?
   **Auto-resolved (2026-11-27):** Keep excluded per lore-cleanliness rule (memory/ending/crash/out-of-bounds set); no static venue restoration.
62. **Columbarium** (`q204_columbarium`, nothing to restore). Arasaka
    security, funeral staff or a vendor (all recommended no)? Re-activate
    the crowd if the tour finds it empty?
   **Auto-resolved (2026-11-27):** Drop from nodes (nothing to restore / open-world ambient only); keep civilian ambient life and vendors where applicable, no gang garrison or gig cast.
63. **Jacked and Coke** (`sts_hey_rey_08`). Karubo as the owner
    (proposed)? All nine staff and regulars, or five? Padre's driver and
    the reinforcement car stay out (proposed)?
   **Auto-resolved (2026-11-27):** Remove one-off target Karubo, retain the bartender and suitable regulars, and leave Padre’s driver and reinforcement car out. (`loc_sts_hey_rey_08` -> `civilian_venue`)
64. **Motel Kabuki** (`sts_wat_kab_08`). Keep the bouncer vanilla never
    activates? Anna Hamill absent (proposed) or placed? The full 34 people,
    or fewer civilians?
   **Auto-resolved (2026-11-27):** Keep the bouncer and full ordinary market crowd, omit Anna Hamill, and retain a neutral-until-provoked Tyger garrison. (`loc_sts_wat_kab_08_cop_hotel` -> `node`, `tyger_claws` `medium` `economy`)
65. **Bennett alley** (`mq304_bennett_meeting`). The driver and Thrax as an
    everyday wait (proposed) or an empty alley? Show the clutter
    (proposed) or vanilla's bare lane? A mod meeting or dead-drop site
    later?
   **Auto-resolved (2026-11-27):** Leave the alley empty of the quest driver and car, retain ordinary clutter, and defer any future dead-drop use. (`loc_mq304_bennett_meeting` -> `excluded`)
66. **Tranquil Terrace** (`q304_songbird_meeting`). Songbird here at all
    (proposed no)? Both gangs stay (proposed)? Keep the airdrop camp
    populated permanently, even though vanilla despawns it?
   **Auto-resolved (2026-11-27):** Keep the civilian park population, omit Songbird and both gang crews, and remove the airdrop encounter. (`loc_q304_songbird_meeting` -> `civilian_venue`)
67. **Luxor High Wellness Spa** (`sts_ep1_12`). Milko and Alan Noël stay
    (proposed)? All 22 androids plus the heavy, or fewer? Ayo Zarin's wing
    stays with the `we_ep1_05` venue (proposed)? Accept the courier, drone
    and broken android that come with the whole garrison (proposed)?
   **Auto-resolved (2026-11-27):** Replace Milko and Alan with a generated lieutenant and ordinary staff, retain proportionate neutral security and functioning androids, and leave Ayo’s wing with its separate venue. (`loc_sts_ep1_12` -> `node`, `voodoo_boys` `large` `espionage`)
68. **Night Corp tour trail** (`mq061`, excluded). Revive the Pacifica
    hazmat camp or the Med Center medics (both recommended no)? Author a
    Night Corp investor tour later?
   **Auto-resolved (2026-11-27):** Keep excluded per lore-cleanliness rule (memory/ending/crash/out-of-bounds set); no static venue restoration.
69. **Coastview relay tower** (`q110_surroundings`). A six-man Voodoo Boys
    watch (proposed), the initial pair, or only ambient people? Kids stay
    with the Arroyo venue, or a Coastview kid crowd?
   **Auto-resolved (2026-11-27):** Keep the six calm Voodoo Boys and existing ambient people, add a generated lieutenant, and do not transplant an unrelated child crowd. (`loc_q110_surroundings` -> `node`, `voodoo_boys` `small` `espionage`)
70. **Poppy Farm** (`sq021_farm_wrong`). A Wraith garrison (proposed) or
    abandoned? All ten, or fewer? Smuggled-goods content later?
   **Auto-resolved (2026-11-27):** Keep the ten Wraiths as neutral-until-provoked security and treat the site as a working smuggling asset; defer detailed goods content. (`loc_sq021_farm_wrong` -> `node`, `wraiths` `medium` `economy`)
71. **Gutierrez penthouse** (`sts_wbr_hil_01`). Owners absent (no vanilla
    data) or add them? Alarm, turrets and gates armed or calmed? The
    penthouse floor open to all, or resident-only (see 58)?
   **Auto-resolved (2026-11-27):** Owner call (U6): Charter Hill luxury penthouse node owned initially by NCPD. (`loc_sts_wbr_hil_01` -> `node`, `ncpd` `medium` `economy`)
72. **Hillpark campfire and plaza** (`mq304_ce_1`, `hip_mq304_ce`, nothing
    to restore). Kurt's four soldiers as a standalone patrol, or his car
    parked there (both recommended no)? A standing Barghest post on the
    plaza? Force the plaza's security area safe if it reacts?
   **Auto-resolved (2026-11-27):** Drop from nodes (nothing to restore / open-world ambient only); keep civilian ambient life and vendors where applicable, no gang garrison or gig cast.
73. **Cali Express** (`q004_braindance_store`). Its vendor was gated on
    `q004_done`; the lead agent added `hey_gle_foodshop_01_default_on` to
    the vendor facts so it trades normally. Keep it a normal shop with the
    robbery as backstory (recommended)?
   **Auto-resolved (2026-11-27):** Keep the vendor and normal lighting, with the robbery cast and tutorial staging absent. (`loc_q004_braindance_store` -> `civilian_venue`)
74. **Bullard & Sequoia site** (`mq059_freedom`). Staffed (proposed) or
    empty? Working look (proposed) or bare? Yorinobu's Mordred parked there
    (recommended no)? Accept the restricted-area security, or ask for an
    exception? Two 6th Street gangers at the dam corner?
   **Auto-resolved (2026-11-27):** Keep the working staffed site and ordinary parked sedans, omit Mordred and dam gangers, and make security neutral until provoked. (`loc_mq059_freedom` -> `node`, `arasaka` `medium` `tech`)
75. **Clement St. house** (`sts_bls_ina_09`, nothing to restore). Empty
    derelict (recommended) or a scav squat? Basement sealed (recommended)
    or opened?
   **Auto-resolved (2026-11-27):** Drop from nodes (nothing to restore / open-world ambient only); keep civilian ambient life and vendors where applicable, no gang garrison or gig cast.
76. **Psychiatric center** (`sts_std_rcr_02`). Jasmine Dixon sedated in
    cell 7 (proposed) or left out? All ten orderlies or the seven core
    guards? Vanilla security areas (the restricted wing turns hostile) or
    a calmer setup? Trim the ten patients and staff?
   **Auto-resolved (2026-11-27):** Remove Dixon and rescue staging, retain ordinary patients and staff, and use at least five neutral-until-provoked security staff. (`loc_sts_std_rcr_02` -> `node`, `ncpd` `medium` `tech`)
77. **Old WNS station** (`sts_wat_nid_12`). The lead agent added Max Jones
    in his default chair (vanilla's own activation). Keep him there
    (recommended)? Keep the trapped door, turret, cameras and mines as
    atmosphere if inert? If the front door is locked, a door-action
    exception, or the roof ladder as the only way in?
   **Auto-resolved (2026-11-27):** Remove Max Jones and quest mines and traps, make the front door usable, and install neutral security and a generated lieutenant. (`loc_sts_wat_nid_12` -> `node`, `scavs` `medium` `espionage`)

## 8. Wave 13

78. **Hostile garrisons (cross-venue, replaces asking venue by venue).**
    Vanilla often makes a venue's guards neutral only inside a quest phase
    we do not run, so they may attack on sight: Cytech, C-Team, the casino,
    Rosebud, the paint factory, Militech's tunnel site, Arasaka Estate,
    Lina's scavs and the Maelstrom warehouse among them. Build a small
    attitude layer that sets venue garrisons neutral until provoked (faction
    hostility stays a sim decision), or trim each hostile venue to its
    non-combat people? **(after tour)**
   **Auto-resolved (2026-11-27):** Set all node garrisons neutral until provoked, with faction standing and affiliation determining hostility. (`loc_rosebud` -> `node`, `animals` `medium` `economy`)
79. **Leah Gladen** (`sts_wbr_jpn_12`, `sts_wbr_jpn_12b`). Alive in our
    timeline, but vanilla only has her corpse. Hand-author her alive in her
    Japantown flat (recommended), or leave the flat empty?
   **Auto-resolved (2026-11-27):** Do not hand-author Leah; remove her side-job remains from static placements. (`loc_sts_wbr_jpn_12b` -> `node`, `tyger_claws` `medium` `economy`)
80. **Japantown Apartments** (`sts_wbr_jpn_12`). The gig's bespoke guard as
    building security (recommended no)? Keep the service worker
    (recommended yes)? The hidden stash shutter openable as vanilla
    (recommended)?
   **Auto-resolved (2026-11-27):** Keep the service worker, replace the bespoke gig guard with normal neutral security, and make the stash shutter usable. (`loc_sts_wbr_jpn_12` -> `civilian_venue`)
81. **Wired Head** (`sts_wbr_jpn_12b`). All ten Claws (recommended) or
    fewer? Add the two reinforcement gunmen (recommended no)?
   **Auto-resolved (2026-11-27):** Keep the ten ordinary Claws neutral until provoked, omit reinforcements, and add a generated lieutenant. (`loc_sts_wbr_jpn_12b` -> `node`, `tyger_claws` `medium` `economy`)
82. **Eisenhower St. block** (`sts_wat_kab_05`). Keep the joytoy and BD
    civilians, or Scavengers only? Basement reachable or sealed? A standing
    Scavenger crew, or let the territory layer own the den?
   **Auto-resolved (2026-11-27):** Keep a neutral territory-owned scav garrison and ordinary clinic staff, omit gig-specific BD occupants, and make the basement accessible. (`loc_sts_wat_kab_05_client_signal` -> `node`, `scavs` `small` `tech`)
83. **Kabuki rooftop slums** (`sts_wat_kab_101`). Scavs and residents
    (recommended), or one group? Were the residents already driven out?
    Hand-place Jae-Hyun (no vanilla data)?
   **Auto-resolved (2026-11-27):** Keep the ordinary rooftop residents, strip the Scav combat crew, and do not hand-place Jae-Hyun. (`loc_sts_wat_kab_101_slums` -> `civilian_venue`)
84. **Lina's home** (`mq303_linas_mansion`). Add Lina (vanilla never places
    her there, so it needs a hand-made placement) or leave the flat to her
    crew? All five scavs, a light guard, or none? Schedule variant 0
    (proposed) or 1? Keep the parked Archer Hella?
   **Auto-resolved (2026-11-27):** Remove Lina and the acting crew from static cast; retain the ordinary parked car and use a calm ambient state. (`loc_mq303_linas_mansion` -> `civilian_venue`)
85. **City Center back alley** (`q306_meeting_spot`). The one sleeper
    (proposed) or an empty alley? Songbird's spy van never here
    (recommended), or her fixed spot?
   **Auto-resolved (2026-11-27):** Keep the ordinary sleeper and omit Songbird, the spy van and quest meeting props. (`loc_q306_meeting_spot` -> `excluded`)
86. **The Hammer, 2077, continued** (`q108_back_alley`, excluded). Reuse this
    alley too (recommended)? Any trace of the 2013 abduction (recommended
    no)? Where does Lyle Thompson belong in 2077?
   **Auto-resolved (2026-11-27):** Keep excluded per lore-cleanliness rule (memory/ending/crash/out-of-bounds set); no static venue restoration.
87. **Soulkiller room** (`q101_soulkiller_room`, excluded). Keep it excluded
    (recommended), or repurpose it as a present-day Arasaka Soulkiller lab?
    Saburo's 2077 home is the tower's executive level, not this set.
   **Auto-resolved (2026-11-27):** Keep excluded per lore-cleanliness rule (memory/ending/crash/out-of-bounds set); no static venue restoration.
88. **Cytech factory** (`sts_std_arr_10`). Ten guards (recommended), fewer if
    hostile (see 78)? A working plant (recommended)? Rihanna Kumar absent
    (recommended)?
   **Auto-resolved (2026-11-27):** Run the plant with workers and ten neutral-until-provoked guards; leave Rihanna and the gig objective out. (`loc_sts_std_arr_10` -> `node`, `scavs` `large` `tech`)
89. **Tyger Claws casino** (`sts_wbr_hil_07`). Free entry (recommended) or a
    mod toll at the culvert (like 7th Hell's cover charge)? Keep the bar
    vendor here (recommended)? Post-heist guards off (recommended)? Vortex
    out (recommended) or a living netrunner stand-in?
   **Auto-resolved (2026-11-27):** Allow free entry, retain the bar vendor and ordinary patrons, omit Vortex and post-heist guards, and use generic neutral security and staff. (`loc_sts_wbr_hil_07` -> `node`, `tyger_claws` `medium` `economy`)
90. **Maelstrom warehouse** (`mq032_maelstrom_warehouse`). A live Maelstrom
    stash (proposed) or empty? Both monks out, or a non-quest cameo? Fenrir
    left as world loot, or removed? Maelstrom hostile or neutral (see 78)?
   **Auto-resolved (2026-11-27):** Keep the stash and neutral Maelstrom guards; remove both monks and quest-specific Fenrir loot. (`loc_mq032_maelstrom_warehouse` -> `node`, `maelstrom` `medium` `economy`)
91. **Kenmore Diner** (`sts_std_arr_12_diner`). Vanilla's thin crowd
    (proposed) or extra staff? Scenery, or a mod food vendor later (vanilla
    has no vendor node)?
   **Auto-resolved (2026-11-27):** Keep the vanilla staff and customers as scenery and defer any new food-vendor implementation. (`loc_sts_std_arr_12_diner` -> `civilian_venue`)
92. **Landfill road** (`q101_landfill_road`, nothing to restore). Chase-only
    road lights off (recommended) or on permanently? Convoy or ambush
    content later?
   **Auto-resolved (2026-11-27):** Keep normal lighting on, omit chase-only staging and leave convoy or ambush content off. (`loc_q101_landfill` -> `civilian_venue`)
93. **Cynosure Site D** (`mq305_wanted_lab`). A dormant, sealed site
    (proposed) or a re-occupied Militech post (needs new cast)? Leave its
    turrets, mines and cameras live? Can the squat lift reach the lab (see
    58)? Replay Evan McRay's video logs?
   **Auto-resolved (2026-11-27):** Keep the lab sealed and unoccupied; remove quest hazards and recordings rather than reoccupying it. (`loc_mq305_wanted_lab` -> `excluded`)
94. **Boxing ring by Montezuma's Throne** (`mq306_boxing_ring`). A live bout
    with a full crowd (recommended) or an empty ring? Add Aaron Waines by
    hand (vanilla never places him there)? Angie and her two Animals stay
    out (recommended)?
   **Auto-resolved (2026-11-27):** Keep a generic bout, referee and civilian crowd; omit Aaron, Angie and her Animals. (`loc_mq306_boxing_ring` -> `civilian_venue`)
95. **Memorial Park NCART station** (`sts_cct_cpz_01`). The security wing
    enterable with a trespass warning (recommended)? Activate the two unused
    corpo passengers (recommended yes)? Does the concourse belong to this
    venue or to the metro venue?
   **Auto-resolved (2026-11-27):** Keep the concourse and annex accessible with calm staff and the two commuters, coordinating the shared concourse with the metro venue. (`loc_sts_cct_cpz_01` -> `node`, `ncpd` `medium` `tech`)
96. **El Pinche Pollo** (`sts_hey_gle_04`). The office inert (proposed) or
    staged with the gig's evidence? Generic boss and bouncer, or name them
    Mauricio Salinas and Ernesto Muñoz? A neutral hangout downstairs only,
    or a hostile restricted upstairs (see 78)?
   **Auto-resolved (2026-11-27):** Keep the office ordinary and inert, use generated faction staff and lieutenant, and make the garrison neutral until provoked throughout. (`loc_sts_hey_gle_04` -> `node`, `valentinos` `medium` `economy`)
97. **BuryGer** (`mq022_ezekiel`). Robbers out (recommended)? King's
    Clampdown briefing booth out (recommended)? The quest's own barman
    (recommended)?
   **Auto-resolved (2026-11-27):** Keep the ordinary barman and patrons; omit robbers and King’s briefing booth. (`loc_mq022_ezekiel` -> `civilian_venue`)
98. **Farida's clinic** (`q303_macs_clinic`). The lead agent added Farida at
    work (her only vanilla phase is `faceplate_meeting`). Keep her? Should
    she sell cyberware (needs the vendor layer)? Kurt's AV over Dogtown off
    (default) or forced on? A research pass for Anderson's Monument Ave
    ripperdoc point of interest?
   **Auto-resolved (2026-11-27):** Keep Farida as the ordinary cyberware vendor, leave Kurt’s AV off, and defer any separate Monument Avenue research. (`loc_q303_macs_clinic` -> `civilian_venue`)
99. **Yucca radio tower** (`q000_radio_tower`, nothing to restore).
    Unmanned (proposed) or a maintenance presence? Restore the quest prefab
    and Willie's car? Pin q000's air-traffic vista?
   **Auto-resolved (2026-11-27):** Drop from nodes (nothing to restore / open-world ambient only); keep civilian ambient life and vendors where applicable, no gang garrison or gig cast.

## 9. Wave 14

100. **Mayor Rhyne** (`sq012_city_hall_conference_room`). His assassination
     is recent 2077 lore. In a "before anything happened" timeline, is
     Rhyne alive (then he needs a cast placement) or dead as in the
     backstory (agent's recommendation)? Holt left out (recommended)? City
     Hall's conference room empty but accessible (recommended), or a
     mod-built City Hall presence?
   **Auto-resolved (2026-11-27):** Resolved by 3-way City Politics design (2026-11-27): incumbent Mayor (pro-corp/anti-gang) sits in the politics sim roster with immediate dynamic replacement + 1-week election on assassination; City Hall stays accessible.
101. **Q104 hill** (`q104_hill`, excluded). Keep excluded with the crash
     site (recommended), or invent an original Badlands lookout?
   **Auto-resolved (2026-11-27):** Keep excluded per lore-cleanliness rule (memory/ending/crash/out-of-bounds set); no static venue restoration.
102. **Arasaka Memorial courtyard** (`cct_cpz_commemorative_park`, nothing
     to restore). Nix only at the Afterlife (recommended)? Rely on the
     open-world crowd (recommended), or add visitors and security later?
   **Auto-resolved (2026-11-27):** Drop from nodes (nothing to restore / open-world ambient only); keep civilian ambient life and vendors where applicable, no gang garrison or gig cast.
103. **Laguna Bend school** (`sq021_school`, excluded). If a school venue is
     wanted, use a real 2077 school such as Rancho Coronado Public High?
     Bring this set back only as a mod-authored braindance (deferred)?
   **Auto-resolved (2026-11-27):** Keep excluded per lore-cleanliness rule (memory/ending/crash/out-of-bounds set); no static venue restoration.
104. **Aaron's flat, Northside** (`sts_wat_nid_07b`). Aaron at home
     (proposed) or saved for a later NCPD storyline? Door open to anyone
     (recommended) or sealed until a mission? The flat's valuables as
     ordinary belongings?
   **Auto-resolved (2026-11-27):** Leave Aaron out as a one-off side-job character, allow ordinary access to the flat, and retain its ordinary belongings. (`loc_sts_wat_nid_07` -> `node`, `maelstrom` `medium` `economy`)
105. **Container Zone 3 court** (`mq304_ce_3`, nothing to restore). The
     five succession bodyguards out (recommended) or a standing presence?
     A mod encounter there later?
   **Auto-resolved (2026-11-27):** Drop from nodes (nothing to restore / open-world ambient only); keep civilian ambient life and vendors where applicable, no gang garrison or gig cast.
106. **Road outside the Kenmore Diner** (`sts_std_arr_12_carchase`, nothing
     to restore). Ambient traffic only (recommended), or the chase's
     stopped cars as static dressing? Convoy or ambush use later?
   **Auto-resolved (2026-11-27):** Drop from nodes (nothing to restore / open-world ambient only); keep civilian ambient life and vendors where applicable, no gang garrison or gig cast.
107. **Reconciliation Park** (`sq006_park_meeting`, nothing to restore). Mr.
     Blue Eyes absent (recommended) or a balcony watcher? The Peralezes
     absent (recommended)? The vanilla crowd and Valentinos (recommended),
     or a mod-built crowd?
   **Auto-resolved (2026-11-27):** Drop from nodes (nothing to restore / open-world ambient only); keep civilian ambient life and vendors where applicable, no gang garrison or gig cast.
108. **Dream Gig bar** (`mq306_bar`, nothing to restore). Leave the ambient
     crowd (recommended; the job's eight would sit on top of it)? Force
     Aaron's corpse variant off as insurance? Aaron stays out?
   **Auto-resolved (2026-11-27):** Drop from nodes (nothing to restore / open-world ambient only); keep civilian ambient life and vendors where applicable, no gang garrison or gig cast.
109. **Los Osos motel** (`sts_ep1_03`). The Scav den (proposed) or empty?
     Rinder out (recommended)? The Yasha heavy out (recommended), leaving
     the top floor dark? Keep both parked cars?
   **Auto-resolved (2026-11-27):** Keep the calm Scav den and ambient parked cars, omit Rinder and the quest heavy, and provide ordinary lighting and a generated boss. (`loc_sts_ep1_03` -> `node`, `scavs` `medium` `tech`)
110. **Benko St bus depot** (`sts_hey_spr_01`). José Luis as the resident
     lieutenant (proposed)? Ten Valentinos and a Thrax, or add the static
     enemy detail? Valentinos hostile or neutral (see 78)? Leave the
     quest's bus and car fleet out (proposed)?
   **Auto-resolved (2026-11-27):** Use a generated Valentino lieutenant and the existing ten neutral guards and ordinary Thrax; omit José Luis and quest fleet. (`loc_sts_hey_spr_01` -> `node`, `valentinos` `medium` `military`)
111. **Dewdrop Inn** (`sts_std_arr_01`). Keep the 6th Street lab crew as
     permanent ambience (recommended) or civilians only (see 78)? Booker
     Updike out (recommended), or his corpse shown?
   **Auto-resolved (2026-11-27):** Keep the 6th Street lab crew as neutral-until-provoked node personnel and omit Booker Updike and his corpse. (`loc_sts_std_arr_01` -> `node`, `sixth_street` `medium` `economy`)
112. **Longshore Stacks container yard** (`mq304_ce_2`). A scav squat
     (proposed), a Barghest guard pair, or both (likely a firefight)? Drop
     the camp if the combat zone already spawns encounters there?
   **Auto-resolved (2026-11-27):** Owner call (U11): overlaps Stacks Container Yard (loc_q301_crashsite_way_up); drop. (`loc_mq304_ce_2` -> `excluded`)
113. **Horrigan home** (`sts_std_rcr_05`). Who lives there: empty
     (proposed), a hand-built Juliet, or a relaxed Rose? The murder props
     (corpse, blood, shard cases) are baked world nodes with no hide
     variant; remove them with a cleanup pass? Keep the roof window open as
     a no-skill entrance?
   **Auto-resolved (2026-11-27):** Remove the murder dressing and side-job cast, retain ordinary access including the window, and leave population to ambient systems. (`loc_sts_std_rcr_05` -> `civilian_venue`)
114. **H10 garage** (`q001_garage`, nothing to restore). Jackie and V's
     Quadra stay out (recommended)? No invented garage crowd unless the tour
     finds it empty?
   **Auto-resolved (2026-11-27):** Drop from nodes (nothing to restore / open-world ambient only); keep civilian ambient life and vendors where applicable, no gang garrison or gig cast.
115. **Capitán Caliente, Eden Plaza** (`q302_goodnight_charlies`).
     Abandoned with one squatter (proposed), or reopened with mod staff?
     Display name "Capitán Caliente" or "Goodnight Charlie's"? Ronald
     Malone absent for now? Leave the mines and phone shelf vanilla, or a
     device-action exception?
   **Auto-resolved (2026-11-27):** Reopen as Capitán Caliente with ordinary staff and a neutral garrison, omit Malone and quest staging, and make the entrance usable. (`loc_q302_goodnight_charlies` -> `civilian_venue`)
116. **Zen master** (`mq014_zen`, excluded). Keep the vision set excluded,
     or save it for a meditation activity? Place the Zen master as an
     ambient monk in Reconciliation Park (unplaced now)? Research the se5
     cliff separately?
   **Auto-resolved (2026-11-27):** Keep excluded per lore-cleanliness rule (memory/ending/crash/out-of-bounds set); no static venue restoration.
117. **Sq006 truck-ambush corner** (`sq006_truck_ambush_spot`, nothing to
     restore). An ordinary empty corner (recommended; the living-world layer
     owns its Maelstrom spawn anchors) or a standing Maelstrom presence (use
     the relaxed reinforcement crew, not the window shooters)? If the tour
     finds the road blocks up, allow a road-block device exception?
   **Auto-resolved (2026-11-27):** Drop from nodes (nothing to restore / open-world ambient only); keep civilian ambient life and vendors where applicable, no gang garrison or gig cast.
118. **Container-yard lanes, Dogtown** (`conz_mq304_ce`). The 15-person
     lane crowd as street life (proposed), or drop it as wake staging?
     Rebuild the scav-versus-Barghest fight as a random encounter
     (recommended no)? Leave the two restricted security areas vanilla
     unless the tour shows a trespass warning?
   **Auto-resolved (2026-11-27):** Keep the fifteen calm locals, omit the staged fight, and leave security areas subject to normal access policy. (`loc_conz_mq304_ce` -> `civilian_venue`)
119. **Vista del Rey diner and clinic** (`q111_killers_apartment`, nothing to
     restore). Leave the upstairs clinic as the ripper's empty flat until
     `hvdr_03` is researched, or add `ripperdoc/start` there? Name it for
     the diner and clinic rather than the cut quest's "killer's apartment"?
   **Auto-resolved (2026-11-27):** Drop from nodes (nothing to restore / open-world ambient only); keep civilian ambient life and vendors where applicable, no gang garrison or gig cast.

## 10. Wave 15

120. **La Catrina funeral home** (`sts_hey_rey_06`). Ambient crowd only
     (recommended) or a permanent wake? An empty morgue (recommended) or
     two Valentino morticians? Staffed around the clock (recommended) or
     time-gated?
   **Auto-resolved (2026-11-27):** Keep regular reception and visitors, add normal mortuary staff and a neutral garrison, and operate without a staged permanent wake or time gate. (`loc_sts_hey_rey_06` -> `node`, `valentinos` `large` `economy`)
121. **Sunshine Motel, Militech outpost** (`sts_bla_ina_04`). Restore the
     fight's reinforcement staging (recommended no)? Keep the radar van and
     Emperor parked (recommended yes)? Leave the always-loaded restricted
     area live for now (see 78)? Confirm it reads as an occupied Militech
     base, not a derelict motel?
   **Auto-resolved (2026-11-27):** Keep the radar van, Emperor and calm base crew, omit reinforcement waves, and make garrison attitude neutral until provoked. (`loc_sts_bla_ina_04` -> `node`, `militech` `medium` `military`)
122. **8ug8ear's building** (`sts_hey_rey_09`). 8ug8ear present in normal
     play (recommended)? Wakako's driver and van out (recommended)? The
     Tyger Claw raid crew out (recommended) or reused as building security?
   **Auto-resolved (2026-11-27):** Keep ordinary residents, remove 8ug8ear and the raid crew, and omit the extraction driver and van. (`loc_sts_hey_rey_09` -> `civilian_venue`)
123. **Union Railroad Station, Wraith outpost** (`sts_bls_ina_03`). All 14
     guards, or about 8 (guards and snipers first)? The two-Wraith
     reinforcement car as a standing picket (recommended no)? Add the
     five-Wraith ambient crowd if the yard reads thin?
   **Auto-resolved (2026-11-27):** Keep the routine garrison, omit the reinforcement car and add calm ambient Wraiths only if useful. (`loc_sts_bls_ina_03` -> `node`, `wraiths` `medium` `espionage`)
124. **Gustavo's building, Petrel St.** (`sts_hey_rey_01`). Marta out, or an
     alive or coma pose? The apartment crew at six or two? Keep the lower
     alley trio? Gustavo ambient, or saved for missions? Lift floor access
     (see 58).
   **Auto-resolved (2026-11-27):** Remove Gustavo, Marta and the apartment and alley gang crews, retain ordinary neighbours, and allow usable lift floors. (`loc_sts_hey_rey_01` -> `civilian_venue`)
125. **Kendachi plant lot** (`sts_std_arr_05_parking`). Ted Fox out
     (proposed)? Keep or drop the quest's transport? Vanilla restricted-area
     behaviour, or a freely walkable lot? Activate the six parked-car
     spawners if the yard reads empty (same gap as 31)?
   **Auto-resolved (2026-11-27):** Omit Ted and the quest transport, keep ordinary parked cars as needed, and make the security detail neutral until provoked. (`loc_sts_std_arr_05_parking` -> `civilian_venue`)
126. **Lobos St tower, Gaston Slayton** (`sts_hey_gle_03`). How much private
     security (reduced recommended)? Keep the parked Zetatech AV? Add Gaston
     through a new cast entry? Restore his guitar, shrine and collection as
     dressing? Floor 17 lift access (see 58).
   **Auto-resolved (2026-11-27):** Owner call (U5): luxury apartment tower node owned initially by NCPD. (`loc_sts_hey_gle_03` -> `node`, `ncpd` `medium` `economy`)
127. **Monokatana workshop, Raymond St.** (`sts_wbr_jpn_02`). Drop the gig's
     torturer (proposed) or seat him? Drop the hostage? A hostile-looking
     hideout or a calm staff (see 78)? All 13 or a trimmed ground crew?
   **Auto-resolved (2026-11-27):** Drop the hostage and torturer, retain the working crew and sufficient neutral guards, and add a generated lieutenant. (`loc_sts_wbr_jpn_02_monoblade_workshop` -> `node`, `tyger_claws` `medium` `tech`)
128. **Acorn Towers lot** (`sts_wbr_hil_06`). Keep the full 12-ganger,
     11-car crew, or trim it? Dan out, or at his meeting spot? Leave the
     bar vendor to the casino venue? Security hidden (proposed) or shown?
   **Auto-resolved (2026-11-27):** Keep a calm crew of at least five and ordinary cars, remove Dan and the gig boss, leave the vendor with the casino, and use routine security. (`loc_sts_wbr_hil_06` -> `node`, `sixth_street` `medium` `economy`)
129. **Tirempire Auto Shop** (`sts_std_arr_12_gas_station`). The gig's
     friendly workshop crew and eight cars as everyday staff (proposed;
     vanilla switches them off in open play), or a quiet shop? Kirk and Big
     Joe out? Trim the cars?
   **Auto-resolved (2026-11-27):** Keep the mechanics, assistants and ordinary customer cars, remove Kirk and Big Joe, and add neutral security and a generated boss. (`loc_sts_std_arr_12_gas_station` -> `node`, `scavs` `medium` `economy`)
130. **Kabuki basement ripperdoc lab** (`sts_wat_kab_02`). A live Maelstrom
     den (proposed) or empty? Ripperdoc Lucy out until a proper spot is
     authored? Maelstrom hostile or neutral (see 78)? Crime-scene gore off
     (recommended)? Add the crew's parked Thrax?
   **Auto-resolved (2026-11-27):** Keep a calm Maelstrom crew with a generated lieutenant, remove the hostage and gore, and retain the parked Thrax if ambient. (`loc_sts_wat_kab_02_ripperdoc_lab` -> `node`, `maelstrom` `small` `tech`)
131. **Mallagra St. house** (`sts_std_rcr_03`). Flavio and his 6th Street
     crew (recommended), Flavio alone, or none? The five party guests later
     (no calm phase exists)? The escape car in the garage (recommended no)?
   **Auto-resolved (2026-11-27):** Retain the neutral 6th Street garrison with a generated lieutenant; omit Flavio, terrified guests, escape car and massacre staging. (`loc_sts_std_rcr_03` -> `civilian_venue`)
132. **Kabuki docks container yard** (`sts_wat_kab_102`). A plain working
     dock (proposed), or also the gig's nine elite guards and five workers
     (recommended no)? GPS trackers and restricted-area markers off
     (recommended)? Name it "Kabuki Docks Container Yard" or "Kabuki Cargo
     Yard"?
   **Auto-resolved (2026-11-27):** Use the name Kabuki Docks Container Yard, keep ordinary workers and truck, add a neutral garrison and lieutenant, and omit tracker and quest markers. (`loc_sts_wat_kab_102_cargo` -> `node`, `scavs` `medium` `economy`)
133. **Rovinj St. glitter kitchen** (`sts_wat_lch_06`). The full Tyger crew
     and cars (proposed), cooks only, or empty? Keep the junkie? Hostile or
     neutral (see 78)? The plain street-entrance door is outside the door
     scope; force it if it is shut?
   **Auto-resolved (2026-11-27):** Keep generic cooks, neutral Tyger security, ordinary parked cars and the ambient junkie; remove named gig cast and make the entrance usable. (`loc_sts_wat_lch_06_neon_basement` -> `node`, `tyger_claws` `medium` `tech`)
134. **2071 minefield** (`sts_bls_ina_07`, nothing to restore). Guarded by
     nobody (recommended), the gig's three drones, or a new smuggler camp?
     A mod mission site later? A territory node despite restoring nothing?
   **Auto-resolved (2026-11-27):** Drop from nodes (nothing to restore / open-world ambient only); keep civilian ambient life and vendors where applicable, no gang garrison or gig cast.
135. **Highway 101 Wraith camp** (`sts_bls_ina_08`). Trevor's death as
     backstory (proposed) or his car and body? Accept the 1.48 km anchor,
     or allow a camp-side trigger for venues with no device? Day-only
     vanilla phases, or add a night arrangement? Nine Wraiths, or more cars
     and guards? Scenery or an occupiable Wraith node?
   **Auto-resolved (2026-11-27):** Keep the Wraith garage camp as a node with neutral security and day/night coverage, omit Trevor and his car, and use a reliable camp-side trigger if needed. (`loc_sts_bls_ina_08` -> `node`, `wraiths` `medium` `economy`)
136. **Data Inc., Wellsprings** (`sts_hey_spr_06`). Rebeca Price as the live
     manager (proposed) or a clerk-only shop? Keep the three calm Animals as
     staff? Keep the Valentino complaining customer? If the front door is
     locked (its auth module counts as an in-world way), force-unlock it, or
     accept the back routes?
   **Auto-resolved (2026-11-27):** Owner call (U2): keep Data Inc. as small Animals economy node. (`loc_sts_hey_spr_06` -> `node`, `animals` `small` `economy`)
137. **Wang's Clinic** (`sts_wat_kab_06`, nothing to restore). The lead
     agent set `kana_yakin_default_on` so the kept vendor layer staffs Roger
     Wang (as for Cali Express). Wang as a named cast entry (recommended
     no)? Any Animals presence (recommended no)? The world-streamed final
     loot and security markers?
   **Auto-resolved (2026-11-27):** Drop from nodes (nothing to restore / open-world ambient only); keep civilian ambient life and vendors where applicable, no gang garrison or gig cast.
138. **H11 server room** (`sts_wat_lch_01`). Allow a venue to power the H11
     lift if it is not callable (see 58)? All five crew including Tatsuya
     Takei and Yuri Shaku (recommended)? The slacker look, or everyone in
     default? Disable the restricted area, or a hostile hideout (see 78)?
   **Auto-resolved (2026-11-27):** Owner call (U3): keep H11 Server Room as small Tyger Claws espionage node. (`loc_sts_wat_lch_01_server_room` -> `node`, `tyger_claws` `small` `espionage`)
139. **Valentinos auto shop, Russell St.** (`sts_hey_spr_03`). The full
     11-person crew (proposed), trimmed, or empty? A neutral shop, or a
     restricted hostile site (see 78)? The quest SUV on the lift off
     (proposed)? Park the nomad truck as ambient?
   **Auto-resolved (2026-11-27):** Keep the calm eleven-person crew with a generated boss, remove the quest SUV, and retain the nomad truck if it is ambient. (`loc_sts_hey_spr_03` -> `node`, `valentinos` `medium` `economy`)

## 11. Wave 16 (final research wave)

140. **Warbler Lake waste facility** (`sts_bls_ina_11`). Keep or drop the
     broken sparring bot? All five guards and two cars, or fewer? Open the
     two office interiors, or keep them shut?
   **Auto-resolved (2026-11-27):** Keep the five neutral guards and ordinary cars, open usable offices, and omit the broken quest sparring bot. (`loc_sts_bls_ina_11` -> `node`, `scavs` `medium` `economy`)
141. **Redwood St. car workshop** (`sts_wbr_jpn_01_tygerclaw_garage`). Sergei
     as garage keeper (recommended) or an empty lock-up? Guard-free rather
     than borrowing the restaurant's Claw squad? Car-forbidden area on
     (recommended)? Park Sergei's Colby there?
   **Auto-resolved (2026-11-27):** Remove one-off gig character Sergei, add a generated Tyger garrison and lieutenant, allow normal vehicle access, and omit his quest-associated car. (`loc_sts_wbr_jpn_01_tygerclaw_garage` -> `civilian_venue`)
142. **6th Street garage, Hargreaves St.** (`sts_std_arr_06`). A live den
     (proposed) or empty? Karl Ginsky out (recommended)? Hostility (see 78)?
     Clear the blood (proposed) or keep vanilla's decals? Leave the
     `before_DLC` variants at their defaults?
   **Auto-resolved (2026-11-27):** Keep the calm gang den with a generated boss, omit Karl and quest blood, and leave unrelated vanilla variants at their defaults. (`loc_sts_std_arr_06` -> `node`, `sixth_street` `medium` `economy`)
143. **Northside XBD studio** (`sts_wat_nid_04`). Nine posted guards only
     (recommended), or also the three-car reinforcement wave? Tuners at
     work (recommended)? Studio open (recommended) or sealed?
   **Auto-resolved (2026-11-27):** Keep nine calm posted guards and normal studio staff with a generated boss, omit the named gig tuners and reinforcement wave, and open the studio. (`loc_sts_wat_nid_04_netrunner_hideout` -> `node`, `maelstrom` `medium` `espionage`)
144. **Columbus St. block** (`sts_wat_kab_03`). Corporal William Hare as the
     block's armed squatter (proposed) or an empty flat? Stolen meds out
     (recommended)? Leave the tech door hackable (recommended)?
   **Auto-resolved (2026-11-27):** Leave the flat free of Hare and stolen meds and make the door usable. (`loc_sts_wat_kab_03_stolen_meds` -> `civilian_venue`)
145. **Megabuilding H6** (`loc_megabuilding_h6`, nothing to restore). Lobby
     left to the ambient crowd and vendors (recommended)? Keep the 6th
     Street hideout venue as the only owner of floor 19 (recommended)? Lift
     to floor 19: see 58.
   **Auto-resolved (2026-11-27):** Drop from nodes (nothing to restore / open-world ambient only); keep civilian ambient life and vendors where applicable, no gang garrison or gig cast.
146. **Maelstrom chop shop, Offshore St** (`sts_wat_nid_06`; the lead agent
     renamed it from "Wicked Tires", which is the Glen garage, 149). All
     ten, or the five inside only? Hostile or neutral (see 78)? Park
     stripped cars there later?
   **Auto-resolved (2026-11-27):** Keep both five-person crews neutral, provide a lieutenant and retain ordinary stripped cars as shop dressing. (`loc_sts_wat_nid_06` -> `node`, `maelstrom` `medium` `economy`)
147. **HeavenMed, Daniels St.** (`sts_wat_nid_05`). Whole community
     (recommended) or nine entries? Keep the two crew cars (recommended)?
     Vanilla security and hostility (recommended) or a neutral reception?
     Othmar Brasi as he is (recommended)?
   **Auto-resolved (2026-11-27):** Keep ordinary clinic staff and cars, replace Othmar with a generated lieutenant, and make the security neutral until provoked. (`loc_sts_wat_nid_05` -> `node`, `maelstrom` `medium` `tech`)
148. **Japantown netrunner parking lot** (`sts_wbr_jpn_09`). Keep the
     netrunner, Walt Ozark and the truck (proposed) or an empty lot? The
     Militech ambush teams out (proposed)? A netrunner-hire hook later?
   **Auto-resolved (2026-11-27):** Leave the staging lot empty, omit the netrunner, Walt, truck and ambush, and defer any hire hook. (`loc_sts_wbr_jpn_09_netrunner_parking_lot` -> `excluded`)
149. **Wicked Tires, the Glen** (`sts_hey_gle_06`). The full eight-person
     crew (proposed) or a trimmed day crew? Keep the baked security areas,
     or neutralise them (see 78)? Jake Estevez out (recommended)? No quest
     Colby on the lift (recommended)? Is the generic crew enough without
     Joaquín Davis as a named owner?
   **Auto-resolved (2026-11-27):** Keep the full working crew with neutral security, omit Jake and the quest Colby, and use a generated lieutenant instead of a side-job owner. (`loc_sts_hey_gle_06` -> `node`, `sixth_street` `medium` `economy`)
150. **Megabuilding H1 lift workshop** (`sts_hey_gle_05`). El Gallo as H1's
     lift technician (proposed) or an empty room? His syn-coke routine or a
     cleaner stance? The gig's homeless squatter out (recommended)? All
     three lift stops are live; two may lead to unbuilt space (tour).
   **Auto-resolved (2026-11-27):** Remove El Gallo and the gig squatter, use ordinary staff if available, and enable only built, vanilla-usable lift stops. (`loc_sts_hey_gle_05` -> `civilian_venue`)
151. **Tyger Claws diner, Japantown** (`sts_wbr_jpn_01_tygerclaw_restaurant`).
     The four vanilla Claws only (proposed) or an added civilian layer?
     Neutral until provoked or a hostile den (see 78)? Its display name?
   **Auto-resolved (2026-11-27):** Keep the Japantown diner as civilian space with ordinary patrons or staff, and strip the four Claws and delivery staging. (`loc_sts_wbr_jpn_01_tygerclaw_restaurant` -> `civilian_venue`)
152. **Dakota's Inland Avenue garage** (`sts_bls_ina_07_workshop`, nothing
     to restore). No entry (proposed) or a redundant safety-net activation?
     Let `gate_02` stay shut? Keep the antenna mechanic? A low-priority
     territory node or scenery?
   **Auto-resolved (2026-11-27):** Drop from nodes (nothing to restore / open-world ambient only); keep civilian ambient life and vendors where applicable, no gang garrison or gig cast.
153. **Tucker Albach's condo** (`sts_hey_gle_01`). Tucker in her office
     (proposed) or saved for a mod mission? The eight-person Militech detail
     or fewer for a private home? The construction truck later (needs
     spawner support, as 31)?
   **Auto-resolved (2026-11-27):** Remove Tucker from static cast, retain an appropriately neutral security detail and ordinary renovation staff, and add the truck only as ambient scenery. (`loc_sts_hey_gle_01` -> `node`, `militech` `medium` `economy`)
154. **Deravaja Dojo** (`sts_wat_lch_03`). Keep it a Tyger Claws venue?
     Roh Chi-Won and Ricky out (proposed)? Add the wiki's instructor,
     Timothee LeBeau, later? Keep the yard worker?
   **Auto-resolved (2026-11-27):** Keep the Tyger dojo and yard worker, remove the gig cast, and supply five neutral guards and a generated lieutenant. (`loc_sts_wat_lch_03_dojo` -> `node`, `tyger_claws` `medium` `military`)
155. **Maelstrom warehouse, Industrial & Eisenhower** (`sts_wat_nid_07`).
     Keep the six-person crew (proposed)? Hostile or neutral (see 78)? The
     intact pre-gig look (proposed) or the opened one? Roof hatch shut or
     open? Reuse the gated homeless crowd as street population?
   **Auto-resolved (2026-11-27):** Keep the six Maelstrom neutral until provoked, use the intact pre-gig look with a usable roof hatch, and retain the homeless as ambient civilians. (`loc_sts_wat_nid_07` -> `node`, `maelstrom` `medium` `economy`)
156. **Kendachi factory, El Camino Rd** (`sts_std_arr_03`). The full
     13-person security detail or trimmed? Keep or neutralise the
     restricted-area controllers (see 78)? Yard cars later (20 quest
     spawners, as 31)? Matheus Stove absent, or an invented director?
   **Auto-resolved (2026-11-27):** Keep proportionate security neutral until provoked, omit quest-spawned cars and Matheus, and install a generated Scav lieutenant. (`loc_sts_std_arr_03` -> `node`, `scavs` `large` `economy`)
157. **Dicky Twister, Vista del Rey** (`sts_hey_rey_02`). Place Señor
     Ladrillo (no vanilla data here)? Eight Valentinos or three? Lena
     Dominguez as the crew chief (proposed)? Keep the service worker?
     Approve the name?
   **Auto-resolved (2026-11-27):** Use a generated Valentino lieutenant and at least five neutral guards, retain the service worker and established club name, and do not add Señor Ladrillo or Lena as static cast. (`loc_sts_hey_rey_02` -> `node`, `valentinos` `medium` `economy`)
158. **Biotechnica Hotel, Downtown** (`sts_cct_dtn_04`). Koch as the floor
     19 resident (proposed) or an empty floor? Full in-house security or a
     lean lobby detail? An open bar (proposed)? Floor 19 lift access (see
     58).
   **Auto-resolved (2026-11-27):** Remove Koch as a one-off gig target, keep the full neutral security detail and open bar, and make the usable nineteenth-floor lift accessible. (`loc_sts_cct_dtn_04` -> `node`, `biotechnica` `medium` `economy`)
159. **6th Street freight compound, Oak St.** (`sts_std_rcr_04`). Hostile
     yard or walkable (see 78)? Keep the four workers? The west building as
     part of this venue or its own stop? Keep the propaganda server farm
     running in this timeline?
   **Auto-resolved (2026-11-27):** Keep the four workers and propaganda servers, include the west building in the compound, and make the garrison neutral until provoked. (`loc_sts_std_rcr_04` -> `node`, `sixth_street` `medium` `espionage`)
160. **Autowerks, Longshore North** (`sts_wat_nid_01`). Hal Cantos out
     (recommended)? Anna Nox absent, or later as a non-psycho manager
     (recommended absent)? Vanilla's three workers (recommended)?
   **Auto-resolved (2026-11-27):** Omit Hal Cantos and Anna Nox, keep the three ordinary workers, and add the required neutral garrison and generated lieutenant. (`loc_sts_wat_nid_01` -> `node`, `the_mox` `medium` `economy`)
161. **Wollesen St motel, Arroyo** (`sts_std_arr_12_motel`). Pedro at his
     desk (proposed) or an empty room? Let the door policy open his room, or
     keep it private? Re-issue the courtyard crowd as a guaranteed spawn?
   **Auto-resolved (2026-11-27):** Omit Pedro, keep ordinary courtyard residents, and make usable room doors accessible. (`loc_sts_std_arr_12_motel` -> `node`, `scavs` `medium` `economy`)
162. **Big Pete's garage, Sage Gulch Road** (`sts_bls_ina_02`). A calm
     seven-man Wraith garrison (proposed) or the whole community with its two
     shooting gunmen? Big Pete at the terminal (proposed) or waiting? A
     hostile restricted compound or a neutral fuel stop (see 78)? Accept
     the missing roof turret, or extend venue support for world nodes?
     Day-only phases (empty at night), or a mod night crew?
   **Auto-resolved (2026-11-27):** Keep a calm seven-person Wraith garrison with a generated boss and night coverage, omit Big Pete and shooting staging, and use normal access without adding a missing turret. (`loc_sts_bls_ina_02` -> `node`, `wraiths` `medium` `economy`)

## 12. From the first tour leg (2026-11-26)

Decided by the owner on the tour (recorded, already applied):

163. **Space Force One crash area** (`q302_way_to_blackbox`). Ignore it and
     leave it sealed: the crash damage only makes sense in Phantom Liberty's
     story. Excluded in `data/venues/triage_overrides.json`.
164. **The Cynosure bunker** (`q305_bunker`). Scrapped for now (too many lore
     implications), kept as a *maybe, much later* area. Deferred. The owner
     sees it, Blackwall residue and all, as a possible unique player base;
     that needs a discussion.
165a. **The Spidertank arena** (`q302_spidertank_arena`, the Founding Our
     Future Expo). Stripped (2026-11-27): the game hung loading it during
     the sweep, and its entry was the only thing loading q302's boss-fight
     prefab. Excluded; the hall stays sealed and empty.
165. **Goodnight Charlie's and the Dogtown basketball court.** Toured again
     on the second leg (night at the court; the mine at Charlie's entrance).

Open, for a later discussion:

166. **Konpeki Plaza** (`q004_q005_arasaka_hotel`). A large job: lockdown
     gates and "code red" panels to remove, Yorinobu's suite not fully
     loaded, no reception staff, only one lift option. The owner sees it as
     a good dynamic mission spot with civilians and guards. Scope it as its
     own task?
   **Auto-resolved (2026-11-27):** Scope a dedicated restoration task to remove lockdown dressing, restore staff and guards, and make usable access and available lift floors work. (`loc_q004_q005_arasaka_hotel` -> `node`, `arasaka` `large` `economy`)
167. **Pacifica mall gym** (`q110_pacifica_mall`). The owner suggests
     Sasquatch there. She is an Animals boss; this is a cast-layer job.
   **Auto-resolved (2026-11-27):** Place Sasquatch here as the Animals’ flagship lieutenant; generate the boss at Tripple Extreme. (`loc_q110_pacifica_mall` -> `node`, `animals` `large` `military`)
168. **North Oak marina** (`sts_cct_dtn_05_luxury_yacht`). A prominent port
     business (marine bar sign) that needs guards. Its own node or part of
     the yacht venue?
   **Auto-resolved (2026-11-27):** Treat the marina and yacht as one economy node, with security covering both. (`loc_sts_cct_dtn_05_luxury_yacht` -> `node`, `militech` `medium` `economy`)
169. **Gas station, Badlands** (`q104_gas_station`). The owner rates it a
     good business node; its garage doors should work like normal garage
     doors (the fix pass handles the doors).
   **Auto-resolved (2026-11-27):** Keep the station operating and make garage doors usable; remove mines and other quest dressing while retaining or replacing shutters as needed. (`loc_q104_gas_station` -> `node`, `kang_tao` `small` `economy`)

From the leg 1 fix pass (agent reports in
`~/.cache/neon-ascendancy/extracts/venues/research/fixes/`):

170. **Hidden NUSA room, Nighthawks** (`q303_nighthawks_bar`). Its secret
     door stays shut on purpose (the briefing boards belong to the removed
     plot). Open it up, or keep it hidden?
   **Auto-resolved (2026-11-27):** Keep the secret room accessible while removing the NUSA plot boards and other quest dressing. (`loc_q303_nighthawks_bar` -> `civilian_venue`)
171. **SoCal border office double door.** It is usable now. If it reads as
     staff-only on the second tour, should it stay shut?
   **Auto-resolved (2026-11-27):** Keep the usable double door accessible under the general access policy. (`loc_q000_border_crossing` -> `node`, `militech` `medium` `military`)
172. **Pump station police scene** (`q111_pumpstation`). Removed as you
     flagged it. Bring the cordon and bodies back as lived-in flavour
     instead? (The 13 hustle mines on the beach path stay off either way.)
   **Auto-resolved (2026-11-27):** Keep the cordon, bodies and mines off; retain the ordinary beach crowd. (`loc_q111_pumpstation` -> `node`, `ncpd` `large` `tech`)
173. **Goodnight Charlie's mines.** Disarmed. Lore has the security system
     still live; keep them as visible, disarmable traps instead?
   **Auto-resolved (2026-11-27):** Remove or disable the quest mines rather than keeping live traps. (`loc_q302_goodnight_charlies` -> `civilian_venue`)
174. **Squat lighting** (`q302_squat`). The warm day lamps are on now. Keep
     the blue lights and glowsticks vanilla leaves on?
   **Auto-resolved (2026-11-27):** Keep normal lighting on, including the blue lights and glowsticks where they are ambient. (`loc_q302_squat` -> `civilian_venue`)
175. **North Oak yacht deck devices.** The party layout also brings a few
     toolboxes and safes with its deck lights. Fine?
   **Auto-resolved (2026-11-27):** Keep ordinary toolboxes and safes with the party lighting, excluding gig-specific loot. (`loc_sts_cct_dtn_05_luxury_yacht` -> `node`, `militech` `medium` `economy`)
176. **Gas station shutters.** They belong to the q104 quest prefab, which
     also brings the quest's garage and mine dressing. Leave them out?
   **Auto-resolved (2026-11-27):** Keep the station operating and make garage doors usable; remove mines and other quest dressing while retaining or replacing shutters as needed. (`loc_q104_gas_station` -> `node`, `kang_tao` `small` `economy`)

From the sweep fix pass (agent reports in the fixes folder's `sweep/`):

177. **Barry's flat, H10** (`megabuilding_a`). The door policy unlocks it,
     so you can walk in; vanilla keeps it shut until his quest, and the
     entry has Barry refusing to answer. Keep it open or lock it?
   **Auto-resolved (2026-11-27):** Make Barry’s door usable and leave the one-off quest resident out. (`loc_megabuilding_a` -> `civilian_venue`)
178. **Bree's flat, Wellsprings** (`mq305_wanted`). Disabled and locked;
     nothing is placed inside. Keep it shut or open it?
   **Auto-resolved (2026-11-27):** Open usable entrances and lift floors while leaving Bree and her quest dressing absent. (`loc_mq305_wanted` -> `civilian_venue`)
179. **Ghost Town.** The fuel station and bar doors open now, but the town
     stays dark (its fusebox was powered by a skipped q103 phase). Power
     the whole town instead?
   **Auto-resolved (2026-11-27):** Power the town and keep the fuel station and bar accessible with neutral Wraith security. (`loc_q103_ghost_town` -> `node`, `wraiths` `small` `economy`)
180. **Arasaka Tower, floor 33.** Jenkins's office, its vestibule and the
     AV hangar open now. The meeting room (the restored trio sits behind
     its two doors) and 19 back rooms stay locked as in vanilla. Open the
     meeting room, or more of the floor? First check the tower lift
     reaches floor 33 at all.
   **Auto-resolved (2026-11-27):** Open the meeting room and usable floor-33 doors, verify lift access, and leave vanilla-unusable lift floors closed. (`loc_arasaka_tower` -> `node`, `arasaka` `large` `espionage`)
181. **Delamain garage upstairs** (`sq025_delamain_garage`). The workshop
     and control room are sealed; vanilla opens them only for the finale.
     Walkable in normal business?
   **Auto-resolved (2026-11-27):** Make the workshop and control-room doors usable where the floors are normally accessible, while preserving Delamain as a neutral service hub. (`loc_sq025_delamain_garage` -> `neutral_hub`)
182. **Abandoned motel rooms** (`sts_wat_nid_03_abandoned_motel`). Two
     first-floor rooms are empty because the gig's props are not loaded.
     Furnish one or two, or leave them derelict?
   **Auto-resolved (2026-11-27):** Leave the rooms derelict unless ordinary furnishings are needed for a functioning motel; remove gig props and make usable doors accessible. (`loc_sts_wat_nid_03_abandoned_motel` -> `node`, `scavs` `medium` `economy`)

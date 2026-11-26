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

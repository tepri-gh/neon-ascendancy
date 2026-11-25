# Known bugs

Open issues found during playtesting, to resolve later. Remove an entry once
its fix is verified in-game.

## Open

### Viktor's cyberware menu starts in tutorial mode on first open

- **Found:** 2026-11-24, clean-slate *Start Ascendancy* run (`2f55cff`).
- **Repro:** New clean-slate run → go to Viktor's clinic → open his ripperdoc
  (cyberware) menu for the first time.
- **Observed:** The menu runs the vanilla ripperdoc tutorial flow, so only the
  3 tutorial cyberware slots are available.
- **Workaround:** Follow the tutorial arrows and confirm; the full menu is then
  available.
- **Expected:** The full ripperdoc menu opens directly, with no tutorial.
- **Suspected cause (unverified):** The vanilla ripperdoc tutorial is normally
  completed during the prologue, which clean-slate skips, so its
  completion/tutorial state is never set.

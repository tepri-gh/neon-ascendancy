module NeonAscendancy.Core

// Push a short HUD onscreen toast using the vanilla UI_Notifications blackboard.
public func NeonAscendancy_ShowHudNotice(game: GameInstance, text: String) -> Void {
  if !GameInstance.IsValid(game) || Equals(text, "") {
    return;
  }
  let bb = GameInstance
    .GetBlackboardSystem(game)
    .Get(GetAllBlackboardDefs().UI_Notifications);
  if !IsDefined(bb) {
    return;
  }
  let msg: SimpleScreenMessage;
  msg.isShown = true;
  msg.duration = 5.0;
  msg.message = text;
  msg.type = SimpleMessageType.Neutral;
  bb
    .SetVariant(GetAllBlackboardDefs().UI_Notifications.OnscreenMessage, ToVariant(msg), true);
}

// Drain queued C++-formatted notices and display the newest one on HUD.
public func NeonAscendancy_DrainHudNotices(game: GameInstance) -> Void {
  let latest = "";
  let next = NcPopHudNotice();
  while NotEquals(next, "") {
    latest = next;
    next = NcPopHudNotice();
  }
  if NotEquals(latest, "") {
    NeonAscendancy_ShowHudNotice(game, latest);
  }
}


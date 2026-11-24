module NeonAscendancy.Sandbox

public enum NeonAscendancy_WorldEra {
  Unknown = 0,
  Prologue = 1,
  Act1PreHeist = 2,
  Interlude = 3,
  Act2 = 4,
  Endgame = 5,
  PostStory = 6,
  PLStandalone = 7,
}

public struct NeonAscendancy_EraFacts {
  let ep1Standalone: Int32;
  let q000Done: Int32;
  let q001Active: Int32;
  let q001Done: Int32;
  let q005Active: Int32;
  let q005Done: Int32;
  let q101Done: Int32;
  let q101EnableSideContent: Int32;
  let q115PointOfNoReturn: Int32;
  let q116Done: Int32;
  let q201Done: Int32;
  let q202Done: Int32;
  let q203Done: Int32;
  let q204Done: Int32;
  let watsonPrologLock: Int32;
  let watsonPrologUnlock: Int32;
}

// Pure world-era classifier over the canonical fact spine (always uses > 0, never == 1).
public func NeonAscendancy_ClassifyWorldEra(facts: NeonAscendancy_EraFacts) -> NeonAscendancy_WorldEra {
  if facts.ep1Standalone > 0 {
    return NeonAscendancy_WorldEra.PLStandalone;
  }
  if facts.q201Done
    > 0
    || facts.q202Done > 0
    || facts.q203Done > 0
    || facts.q204Done > 0 {
    return NeonAscendancy_WorldEra.PostStory;
  }
  if facts.q115PointOfNoReturn > 0 || facts.q116Done > 0 {
    return NeonAscendancy_WorldEra.Endgame;
  }
  if facts.q005Done > 0 {
    if facts.q101Done
      > 0
      || facts.q101EnableSideContent > 0
      || facts.watsonPrologLock == 0 {
      return NeonAscendancy_WorldEra.Act2;
    }
    return NeonAscendancy_WorldEra.Interlude;
  }
  if facts.watsonPrologUnlock > 0 {
    return NeonAscendancy_WorldEra.Interlude;
  }
  if facts.q001Done > 0 {
    return NeonAscendancy_WorldEra.Act1PreHeist;
  }
  if facts.q005Active > 0 || facts.q001Active > 0 || facts.q000Done > 0 {
    return NeonAscendancy_WorldEra.Prologue;
  }
  return NeonAscendancy_WorldEra.Unknown;
}

public func NeonAscendancy_ReadEraFacts(qs: QuestsSystem) -> NeonAscendancy_EraFacts {
  return NeonAscendancy_EraFacts(
    qs.GetFact(n"ep1_standalone"),
    qs.GetFact(n"q000_done"),
    qs.GetFact(n"q001_active"),
    qs.GetFact(n"q001_done"),
    qs.GetFact(n"q005_active"),
    qs.GetFact(n"q005_done"),
    qs.GetFact(n"q101_done"),
    qs.GetFact(n"q101_enable_side_content"),
    qs.GetFact(n"q115_point_of_no_return"),
    qs.GetFact(n"q116_done"),
    qs.GetFact(n"q201_done"),
    qs.GetFact(n"q202_done"),
    qs.GetFact(n"q203_done"),
    qs.GetFact(n"q204_done"),
    qs.GetFact(n"watson_prolog_lock"),
    qs.GetFact(n"watson_prolog_unlock")
  );
}


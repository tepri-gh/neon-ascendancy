module NeonAscendancy.Sandbox

// Pack the 16 canonical QuestsSystem facts (> 0 presence) into a single Uint32
// bitmask matching native/lib/sim/era.cpp::UnpackEraFactsMask (single source of truth).
public func NeonAscendancy_ReadEraFactsMask(qs: QuestsSystem) -> Uint32 {
  let bits = 0u;
  if qs.GetFact(n"ep1_standalone") > 0 {
    bits += 1u;
  }
  if qs.GetFact(n"q000_done") > 0 {
    bits += 2u;
  }
  if qs.GetFact(n"q001_active") > 0 {
    bits += 4u;
  }
  if qs.GetFact(n"q001_done") > 0 {
    bits += 8u;
  }
  if qs.GetFact(n"q005_active") > 0 {
    bits += 16u;
  }
  if qs.GetFact(n"q005_done") > 0 {
    bits += 32u;
  }
  if qs.GetFact(n"q101_done") > 0 {
    bits += 64u;
  }
  if qs.GetFact(n"q101_enable_side_content") > 0 {
    bits += 128u;
  }
  if qs.GetFact(n"q115_point_of_no_return") > 0 {
    bits += 256u;
  }
  if qs.GetFact(n"q116_done") > 0 {
    bits += 512u;
  }
  if qs.GetFact(n"q201_done") > 0 {
    bits += 1024u;
  }
  if qs.GetFact(n"q202_done") > 0 {
    bits += 2048u;
  }
  if qs.GetFact(n"q203_done") > 0 {
    bits += 4096u;
  }
  if qs.GetFact(n"q204_done") > 0 {
    bits += 8192u;
  }
  if qs.GetFact(n"watson_prolog_lock") > 0 {
    bits += 16384u;
  }
  if qs.GetFact(n"watson_prolog_unlock") > 0 {
    bits += 32768u;
  }
  return bits;
}


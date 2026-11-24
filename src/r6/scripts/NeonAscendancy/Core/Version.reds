module NeonAscendancy.Core

// Keep in sync with repository root VERSION and docs/versioning.md.
public func NeonAscendancy_ModVersion() -> String {
  return "0.0.0-dev";
}

// Monotonic persisted schema version (see docs/versioning.md).
public func NeonAscendancy_SchemaVersion() -> Int32 {
  return 1;
}


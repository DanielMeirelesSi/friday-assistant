import assert from "node:assert/strict";
import test from "node:test";
import { getPollIntervalMs } from "../src/poller.js";

test("uses the configured polling interval", () => {
  assert.equal(getPollIntervalMs(), 20_000);
});

# SPDX-FileCopyrightText: (C) 2026 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Showcase scene metadata — names and roles only; no hardcoded UUIDs.

UUIDs are resolved at install time by setup.sh and written to
config/resolved-uuids.json (mounted at /app/config/resolved-uuids.json
inside the container).  This file never contains UUIDs — it defines the
scene by human-readable names so it remains valid across reinstalls.
"""

import json
import os
from functools import lru_cache
from pathlib import Path

SCENE_NAME = "Showcase"

# ── Regions ────────────────────────────────────────────────────────────────────
# Regions where horizontal posture is expected (suppresses fall alert)
FURNITURE_REGIONS = {"Couch"}
# Seated people near a couch edge can be tracked just outside its polygon
FURNITURE_MARGIN_M = 1.0

# Object categories that should not move on their own. When one of these is
# moving, the narrator infers it is attached to the nearest non-inert actor.
INERT_CATEGORIES = {"luggage"}

# ── Sensors ────────────────────────────────────────────────────────────────────
# sensor_id → human label
SENSOR_NAMES = {
  "badge-001":      "BadgeReader",
  "faceid-001":     "FaceID",
  "showcase_light": "LightSensor",
}

# Sensor coverage centre points (world metres) for proximity notes in narrator
SENSOR_CENTERS = {
  "badge-001":  [14.25, 5.77],
  "faceid-001": [14.08, 6.38],
}

# ── Tripwires ──────────────────────────────────────────────────────────────────
# Checkpoint: badge/face readers are between Entry and Checkpoint.
#   inbound (+1) crossings should have credentials.
# Entry: outer entrance before the readers.
#   inbound (+1) crossings are not expected to have credentials.
CHECKPOINT_TRIPWIRE = "Checkpoint"
ENTRY_TRIPWIRE      = "Entry"

# ── Cameras ───────────────────────────────────────────────────────────────────
CAMERA_NAMES = {f"cam-{i}": f"cam-{i}" for i in range(1, 8)}

# ── Runtime UUID resolution ───────────────────────────────────────────────────
# setup.sh writes config/resolved-uuids.json after scene import.
# Format: {"scene_id": "...", "regions": {"Name": "uuid"}, "tripwires": {...}}
# The file is volume-mounted into the container at /app/config/.
_uuid_file = Path(__file__).parent.parent / "config" / "resolved-uuids.json"
_uuids: dict = {}
if _uuid_file.exists():
  try:
    _uuids = json.loads(_uuid_file.read_text())
  except Exception:
    pass

# SCENE_ID: env var (from docker-compose / .env) takes priority, then JSON file
SCENE_ID = os.environ.get("SCENE_ID") or _uuids.get("scene_id", "")

# Build UUID → name lookups from the name → UUID source in the JSON file
_regions_by_name:   dict = _uuids.get("regions", {})    # name → uuid
_tripwires_by_name: dict = _uuids.get("tripwires", {})  # name → uuid

REGION_NAMES   = {uid: name for name, uid in _regions_by_name.items()}    # uuid → name
TRIPWIRE_NAMES = {uid: name for name, uid in _tripwires_by_name.items()}  # uuid → name


@lru_cache(maxsize=1)
def _furniture_boxes() -> tuple:
  """Bounding boxes (min_x, max_x, min_y, max_y) of furniture regions in the scene file."""
  scene_file = Path(__file__).parent.parent / "config" / "scenes" / f"{SCENE_NAME}.json"
  try:
    regions = json.loads(scene_file.read_text()).get("regions", [])
  except (OSError, ValueError):
    return ()
  boxes = []
  for r in regions:
    if r.get("name") in FURNITURE_REGIONS and r.get("points"):
      xs, ys = zip(*r["points"])
      boxes.append((min(xs), max(xs), min(ys), max(ys)))
  return tuple(boxes)


def near_furniture(x: float, y: float) -> bool:
  """True if (x, y) is within FURNITURE_MARGIN_M of a furniture region's bounding box."""
  m = FURNITURE_MARGIN_M
  return any(x0 - m <= x <= x1 + m and y0 - m <= y <= y1 + m for x0, x1, y0, y1 in _furniture_boxes())


def region_name(uid: str) -> str:
  """Return human name for a region UUID, or the raw uid if unknown."""
  return REGION_NAMES.get(uid, uid)


def sensor_name(uid: str) -> str:
  return SENSOR_NAMES.get(uid, uid)


def tripwire_name(uid: str) -> str:
  return TRIPWIRE_NAMES.get(uid, uid)

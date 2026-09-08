# leaderboard.py
import json
import os
from typing import List, Dict, Optional, Tuple

LEADERBOARD_PATH = "leaderboard.json"

def _ensure_store() -> Dict:
    os.makedirs(os.path.dirname(LEADERBOARD_PATH), exist_ok=True)
    if not os.path.exists(LEADERBOARD_PATH):
        data = {"tracks": {}}
        with open(LEADERBOARD_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return data
    with open(LEADERBOARD_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # reset if corrupted
            data = {"tracks": {}}
            with open(LEADERBOARD_PATH, "w", encoding="utf-8") as wf:
                json.dump(data, wf, indent=2)
            return data

def _save_store(data: Dict) -> None:
    with open(LEADERBOARD_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def _track_key(track_id: Optional[str], track_name: Optional[str]) -> str:
    # Prefer a stable id; fall back to name.
    if track_id is not None:
        return str(track_id)
    if track_name is not None:
        return str(track_name)
    return "unknown_track"

def record_player_best_lap(track_id: Optional[str], track_name: Optional[str],
                           username: str, lap_time_sec: float) -> None:
    """
    Save/update the user's fastest lap for a track.
    Schema:
    {
      "tracks": {
        "<track_key>": {
          "name": "<display name>",
          "entries": [
            {"user": "Muhammad", "best_lap": 12.34},
            ...
          ]
        }
      }
    }
    """
    if lap_time_sec is None:
        return
    store = _ensure_store()
    key = _track_key(track_id, track_name)
    track = store["tracks"].setdefault(key, {"name": track_name or key, "entries": []})

    # Update if user exists, else append
    updated = False
    for entry in track["entries"]:
        if entry.get("user") == username:
            if lap_time_sec < entry.get("best_lap", 1e12):
                entry["best_lap"] = round(float(lap_time_sec), 3)
            updated = True
            break
    if not updated:
        track["entries"].append({"user": username, "best_lap": round(float(lap_time_sec), 3)})

    # Keep only top N (e.g., 20) per track, sorted ascending
    track["entries"].sort(key=lambda e: e.get("best_lap", 1e12))
    track["entries"] = track["entries"][:20]
    _save_store(store)

def get_top_fastest(track_id: Optional[str], track_name: Optional[str], limit: int = 7) -> List[Dict]:
    store = _ensure_store()
    key = _track_key(track_id, track_name)
    track = store["tracks"].get(key)
    if not track:
        return []
    entries = sorted(track.get("entries", []), key=lambda e: e.get("best_lap", 1e12))
    return entries[:max(0, limit)]


# Put this beside the functions above, or import its parts where you render UI
import pygame

def draw_leaderboard_panel(win: pygame.Surface,
                           panel_rect: pygame.Rect,
                           track_id: Optional[str],
                           track_name: Optional[str],
                           font: pygame.font.Font,
                           highlight_username: Optional[str] = None,
                           limit: int = 5) -> None:
    # Header
    header = font.render("Leaderboard — Fastest Laps", True, (200, 230, 255))
    win.blit(header, (panel_rect.x + 14, panel_rect.y + 10))

    entries = get_top_fastest(track_id, track_name, limit=limit)

    # No data case
    if not entries:
        empty = font.render("No laps recorded yet.", True, (180, 180, 190))
        win.blit(empty, (panel_rect.x + 14, panel_rect.y + 40))
        return

    # List entries
    y = panel_rect.y + 40
    line_h = max(24, font.get_height() + 2)
    rank_color = (160, 200, 255)
    user_color = (220, 220, 230)
    time_color = (200, 255, 200)

    for i, e in enumerate(entries, start=1):
        user = str(e.get("user", "Unknown"))
        best = e.get("best_lap")
        if best is None:
            continue

        is_you = (highlight_username is not None and user.lower() == highlight_username.lower())
        bg_highlight = (40, 60, 80) if is_you else None
        if bg_highlight:
            pygame.draw.rect(win, bg_highlight,
                             pygame.Rect(panel_rect.x + 8, y - 2, panel_rect.w - 16, line_h),
                             border_radius=6)

        rank_s = font.render(f"{i}.", True, rank_color)
        user_s = font.render(user, True, user_color if not is_you else (255, 255, 180))
        time_s = font.render(f"{best:.2f}s", True, time_color)

        # Column layout
        x_rank = panel_rect.x + 14
        x_user = panel_rect.x + 44
        x_time = panel_rect.right - time_s.get_width() - 14

        win.blit(rank_s, (x_rank, y))
        win.blit(user_s, (x_user, y))
        win.blit(time_s, (x_time, y))

        y += line_h
        if y > panel_rect.bottom - line_h:
            break
        
record_player_best_lap(track_name="Classic 1", username="test", lap_time_sec= 1.2)
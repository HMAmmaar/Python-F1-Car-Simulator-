import json
import os
from typing import Dict, List, Optional, Union
import pygame

# Global data structure
laptime_data = {
    "tracks": {}
}

# File to persist data
DATA_FILE = "laptimes.json"

def load_laptime_data() -> None:
    """Load laptime data from JSON file"""
    global laptime_data
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                laptime_data = json.load(f)
        except (json.JSONDecodeError, IOError):
            # If file is corrupted or empty, start with empty data
            laptime_data = {"tracks": {}}
    else:
        laptime_data = {"tracks": {}}

def save_laptime_data() -> None:
    """Save laptime data to JSON file"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(laptime_data, f, indent=2)
    except IOError as e:
        print(f"Error saving laptime data: {e}")

def update_best_lap(track_name: str, user: str, time: float) -> bool:
    """
    Update the best lap time for a user on a specific track.
    Only updates if the new time is better (smaller) than the current best.
    
    Args:
        track_name: Name of the track
        user: Username
        time: New lap time (in seconds)
        
    Returns:
        bool: True if the lap time was updated, False otherwise
    """
    # Ensure the track exists
    if track_name not in laptime_data["tracks"]:
        laptime_data["tracks"][track_name] = {
            "name": track_name,
            "entries": []
        }
    
    track = laptime_data["tracks"][track_name]
    entries = track["entries"]
    
    # Find existing entry for the user
    existing_entry = None
    existing_index = -1
    for i, entry in enumerate(entries):
        if entry["user"].lower() == user.lower():
            existing_entry = entry
            existing_index = i
            break
    
    if existing_entry:
        # Only update if new time is better (smaller)
        current_best = existing_entry["best_lap"]
        if time < current_best:
            existing_entry["best_lap"] = time
            
            # Sort entries by best_lap (ascending)
            entries.sort(key=lambda x: x["best_lap"])
            
            save_laptime_data()
            return True
        return False
    else:
        # Add new entry
        new_entry = {
            "user": user,
            "best_lap": time
        }
        entries.append(new_entry)
        
        # Sort entries by best_lap (ascending)
        entries.sort(key=lambda x: x["best_lap"])
        
        save_laptime_data()
        return True

def get_player_best_lap(track_name: str, user: str) -> Optional[float]:
    """
    Get a player's best lap time on a specific track.
    
    Args:
        track_name: Name of the track
        user: Username
        
    Returns:
        Optional[float]: Best lap time in seconds, or None if not found
    """
    track = laptime_data["tracks"].get(track_name)
    if not track:
        return None
    
    for entry in track["entries"]:
        if entry["user"].lower() == user.lower():
            return entry["best_lap"]
    
    return None

def get_track_entries(track_name: str) -> List[Dict]:
    """
    Get all entries for a specific track.
    
    Args:
        track_name: Name of the track
        
    Returns:
        List[Dict]: List of entry dictionaries
    """
    track = laptime_data["tracks"].get(track_name)
    if not track:
        return []
    
    return track["entries"]

def get_top_fastest(track_id: Optional[str] = None, 
                    track_name: Optional[str] = None, 
                    limit: int = 10) -> List[Dict]:
    """
    Get top fastest laps for a track.
    Can identify track by ID or name.
    
    Args:
        track_id: Optional track ID (if using numeric IDs)
        track_name: Optional track name
        limit: Number of top entries to return
        
    Returns:
        List[Dict]: List of entry dictionaries sorted by best_lap
    """
    # If track_name is provided, use it
    if track_name:
        target_track = track_name
    elif track_id:
        # If you have a mapping from IDs to names, implement it here
        # For now, assuming track_id is the same as track_name
        target_track = track_id
    else:
        return []
    
    track = laptime_data["tracks"].get(target_track)
    if not track:
        return []
    
    # Return top N entries (already sorted by update_best_lap)
    return track["entries"][:limit]

def get_player_rank(track_name: str, user: str) -> Optional[int]:
    """
    Get a player's rank on a specific track.
    
    Args:
        track_name: Name of the track
        user: Username
        
    Returns:
        Optional[int]: Rank (1-based), or None if not found
    """
    track = laptime_data["tracks"].get(track_name)
    if not track:
        return None
    
    for i, entry in enumerate(track["entries"], 1):
        if entry["user"].lower() == user.lower():
            return i
    
    return None

def draw_leaderboard_panel(win: pygame.Surface,
                           panel_rect: pygame.Rect,
                           track_id: Optional[str],
                           track_name: Optional[str],
                           font: pygame.font.Font,
                           highlight_username: Optional[str] = None,
                           limit: int = 5) -> None:
    """
    Draw a leaderboard panel with the fastest laps.
    
    Args:
        win: Pygame surface to draw on
        panel_rect: Rectangle defining the panel area
        track_id: Optional track ID
        track_name: Optional track name
        font: Pygame font to use
        highlight_username: Username to highlight (typically current player)
        limit: Number of entries to show
    """
    # Draw panel background
    pygame.draw.rect(win, (30, 40, 50), panel_rect, border_radius=8)
    pygame.draw.rect(win, (50, 70, 90), panel_rect, width=2, border_radius=8)
    
    # Header
    header = font.render("Leaderboard", True, (200, 230, 255))
    win.blit(header, (panel_rect.x + 14, panel_rect.y + 10))
    
    # Get track display name
    display_track = track_name or track_id or "Unknown Track"
    track_text = font.render(f"Track: {display_track}", True, (180, 200, 220))
    win.blit(track_text, (panel_rect.x + 14, panel_rect.y + 10 + header.get_height()))
    
    entries = get_top_fastest(track_id, track_name, limit=limit)
    
    # No data case
    if not entries:
        empty = font.render("No laps recorded yet.", True, (180, 180, 190))
        win.blit(empty, (panel_rect.x + 14, panel_rect.y + 60))
        return
    
    # List entries
    y = panel_rect.y + 70
    line_h = max(24, font.get_height() + 2)
    rank_color = (160, 200, 255)
    user_color = (220, 220, 230)
    time_color = (200, 255, 200)
    
    for i, e in enumerate(entries, start=1):
        user = str(e.get("user", "Unknown"))
        best = e.get("best_lap")
        if best is None:
            continue
        
        is_you = (highlight_username is not None and 
                  user.lower() == highlight_username.lower())
        
        # Highlight background for current player
        bg_highlight = (40, 60, 80) if is_you else None
        if bg_highlight:
            pygame.draw.rect(win, bg_highlight,
                           pygame.Rect(panel_rect.x + 8, y - 2, 
                                      panel_rect.w - 16, line_h),
                           border_radius=6)
        
        # Render text
        rank_s = font.render(f"{i}.", True, rank_color)
        user_s = font.render(user, True, user_color if not is_you else (255, 255, 180))
        time_s = font.render(f"{best:.3f}s", True, time_color)
        
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

# Example usage functions
def initialize_empty_tracks():
    """Initialize with empty tracks 1-9"""
    global laptime_data
    
    laptime_data["tracks"] = {}  # Clear any existing data
    
    for i in range(1, 10):
        track_name = f"Track {i}"
        laptime_data["tracks"][track_name] = {
            "name": track_name,
            "entries": []  # Empty, no lap times yet
        }
    
    # Save to file
    save_laptime_data()
    print(f"Initialized empty tracks: Track 1 to Track 9")

# Initialize on module import
# load_laptime_data()

# Example usage in your game:
# if __name__ == "__main__":
#     # Example of updating a lap time
#     updated = update_best_lap("Classic 1", "Author", 23.95)
#     if updated:
#         print("New best lap recorded!")
    
#     # Get player's best lap
#     best_time = get_player_best_lap("Classic 1", "Author")
#     print(f"Author's best lap on Classic 1: {best_time}")
    
#     # Get player's rank
#     rank = get_player_rank("Classic 1", "Author")
#     print(f"Author's rank on Classic 1: {rank}")
    
#     # Get top 5 fastest
#     top_5 = get_top_fastest(track_name="Classic 1", limit=5)
#     print("Top 5 fastest:")
#     for i, entry in enumerate(top_5, 1):
#         print(f"{i}. {entry['user']}: {entry['best_lap']:.3f}s")

# initialize_empty_tracks()
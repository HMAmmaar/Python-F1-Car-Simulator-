import pygame
from utils import scale_image

class Track:
    def __init__(self, name, track_index, track_image_path, track_border_path, 
                 track_border_mask_path, grass_image_path, finish_image_path, 
                 finish_pos, player_start_pos, comp_start_pos, path):
        self.name = name
        self.track_index = track_index
        self.track = self._load_scaled_image(track_image_path, 0.7)
        self.track_border = self._load_scaled_image(track_border_path, 0.7)
        self.track_border_mask = pygame.mask.from_surface(
            self._load_scaled_image(track_border_mask_path, 0.7)
        )
        self.grass = self._load_scaled_image(grass_image_path, 2)
        self.finish = self._load_scaled_image(finish_image_path, 0.75)
        self.finish_pos = finish_pos
        self.path = path
        self.player_start_pos = player_start_pos
        self.comp_start_pos = comp_start_pos
    
    def _load_scaled_image(self, path, scale_factor):
        """Helper method to load and scale images with error handling"""
        try:
            image = pygame.image.load(path)
            return scale_image(image, scale_factor)
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading image {path}: {e}")
            # Return a placeholder surface or raise exception
            return pygame.Surface((100, 100))

class TrackManager:
    def __init__(self):
        self.tracks = []
        self.current_track_index = 0
    
    def add_track(self, track):
        """Add a Track instance to the manager"""
        self.tracks.append(track)
    
    def next_track(self):
        """Move to the next track, cycling back to first if at end"""
        if self.tracks:
            self.current_track_index = (self.current_track_index + 1) % len(self.tracks)
        return self.get_current_track()
    
    def previous_track(self):
        """Move to the previous track, cycling to last if at beginning"""
        if self.tracks:
            self.current_track_index = (self.current_track_index - 1) % len(self.tracks)
        return self.get_current_track()
    
    def get_current_track(self):
        """Get the current track, returns None if no tracks"""
        if not self.tracks:
            return None
        return self.tracks[self.current_track_index]
    
    def reset(self):
        """Reset to first track"""
        self.current_track_index = 0
    
    @property
    def track_count(self):
        return len(self.tracks)
    
    def get_track_by_index(self, index):
        """Get track by specific index with bounds checking"""
        if 0 <= index < len(self.tracks):
            return self.tracks[index]
        return None




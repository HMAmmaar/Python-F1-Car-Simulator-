import pygame
from tracks import TrackManager, track_1, track_2, track_3, track_4, track_5, track_6, track_7, track_8, track_9, default_track
from utils import ORBITRON_FONT_INFO, blit_text_center, blit_title_center, scale_image, create_button, create_notification, ORBITRON_FONT, ORBITRON_FONT_TINY

track_manager = TrackManager()
track_manager.add_track(default_track)  # Default track

# Track selection state
selected_tracks = []  # List to track selection order

def create_track_preview(track, width=160, height=150, is_selected=False):
    """Create a track preview with selection border"""
    preview_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Draw grass background
    preview_surface.blit(scale_image(track.grass, 0.3), (0, 0))
    
    track_image = getattr(track, 'track', None)
    track_name = track.name
    
    if track_image:
        # Calculate scaling while maintaining aspect ratio
        img_width, img_height = track_image.get_size()
        aspect_ratio = img_width / img_height
        
        # Calculate dimensions to fit within preview (with some padding)
        padding = 8
        max_width = width - 2 * padding
        max_height = height - 2 * padding - 20  # Reserve space for name
        
        if max_width / max_height > aspect_ratio:
            scaled_height = max_height
            scaled_width = int(scaled_height * aspect_ratio)
        else:
            scaled_width = max_width
            scaled_height = int(scaled_width / aspect_ratio)
        
        # Scale the image
        scaled_image = pygame.transform.smoothscale(track_image, 
                                                   (scaled_width, scaled_height))
        
        # Center the scaled image on the preview surface
        image_x = (width - scaled_width) // 2
        image_y = (height - scaled_height - 20) // 2  # Account for name at bottom
        preview_surface.blit(scaled_image, (image_x, image_y))
    else:
        # If no track image, display placeholder text
        font = pygame.font.Font(None, 18)
        placeholder_text = font.render("No Preview", True, (150, 150, 150))
        text_x = (width - placeholder_text.get_width()) // 2
        text_y = (height - placeholder_text.get_height()) // 2
        preview_surface.blit(placeholder_text, (text_x, text_y))
    
    # Add selection number if track is in selection order
    if track in selected_tracks:
        # Draw number in top-left corner
        font = pygame.font.Font(None, 28)
        number = selected_tracks.index(track) + 1
        number_text = font.render(str(number), True, (255, 255, 255))
        
        # Create a colored circle background for the number
        circle_radius = 15
        circle_x, circle_y = circle_radius + 5, circle_radius + 5
        pygame.draw.circle(preview_surface, (0, 100, 200), 
                          (circle_x, circle_y), circle_radius)
        pygame.draw.circle(preview_surface, (255, 255, 255), 
                          (circle_x, circle_y), circle_radius, 2)
        
        # Draw the number centered in the circle
        number_rect = number_text.get_rect(center=(circle_x, circle_y))
        preview_surface.blit(number_text, number_rect)
    
    # Draw border - green if selected, gray otherwise
    border_color = (0, 200, 0) if is_selected else (100, 100, 100)
    border_width = 3 if is_selected else 2
    pygame.draw.rect(preview_surface, border_color, 
                    (0, 0, width, height), border_width)
    
    # Draw track name at bottom
    name_text = ORBITRON_FONT.render(track_name, True, (255, 255, 255))
    text_x = (width - name_text.get_width()) // 2
    text_y = height - name_text.get_height() - 5
    preview_surface.blit(name_text, (text_x, text_y))
    
    return preview_surface

def create_selection_order_display():
    """Create a display showing the current selection order"""
    if not selected_tracks:
        return None, (0, 0)  # Return None when no tracks selected
    
    # Calculate height based on number of rows needed
    items_per_row = 5  # How many tracks to show per row
    num_rows = (len(selected_tracks) - 1) // items_per_row + 1
    item_height = 40
    padding = 5
    total_height = num_rows * item_height + padding * 2
    total_width = 550  # Reduced width to fit 630 screen
    
    # Create a surface for the order display
    display_surface = pygame.Surface((total_width, total_height), pygame.SRCALPHA)
    
    # Semi-transparent background with green border
    pygame.draw.rect(display_surface, (30, 30, 30, 230), 
                    (0, 0, total_width, total_height), border_radius=8)
    pygame.draw.rect(display_surface, (0, 200, 0), 
                    (0, 0, total_width, total_height), 3, border_radius=8)
    
    # Display selected tracks with numbers
    x_offset = 10
    y_offset = 5
    
    for i, track in enumerate(selected_tracks):
        # Create mini preview for each selected track
        mini_preview = pygame.Surface((100, 30), pygame.SRCALPHA)  # Slightly smaller
        
        # Background for track item
        pygame.draw.rect(mini_preview, (50, 50, 50, 200), 
                        (0, 0, 100, 30), border_radius=4)
        pygame.draw.rect(mini_preview, (0, 180, 0), 
                        (0, 0, 100, 30), 1, border_radius=4)
        
        # Track name (truncated if too long)
        track_name = track.name[:10] + "..." if len(track.name) > 10 else track.name
        name_font = ORBITRON_FONT_TINY
        name_text = name_font.render(track_name, True, (255, 255, 255))
        mini_preview.blit(name_text, (25, 8))  # Offset for number badge
        
        # Number badge on left side
        num_font = pygame.font.Font(None, 20)
        num_text = num_font.render(str(i + 1), True, (255, 255, 255))
        
        # Draw number circle
        pygame.draw.circle(mini_preview, (0, 100, 200), (15, 15), 12)
        pygame.draw.circle(mini_preview, (255, 255, 255), (15, 15), 12, 1)
        
        # Draw number centered in circle
        num_rect = num_text.get_rect(center=(15, 15))
        mini_preview.blit(num_text, num_rect)
        
        # Position and draw - wrap to next row if needed
        if x_offset + 110 > total_width:  # Adjusted for smaller width
            x_offset = 10
            y_offset += 35
        
        display_surface.blit(mini_preview, (x_offset, y_offset))
        x_offset += 105  # Adjusted spacing
    
    # Position at bottom center, just above the bottom row of track previews
    # For 630x630 screen, bottom row is at y=440 with 150 height = extends to y=590
    # Put the selection display just above at y=580 - total_height
    screen_height = 630
    screen_width = 630
    pos_x = (screen_width - total_width) // 2
    pos_y = 610 - total_height  # Position it 50px from the bottom
    
    return display_surface, (pos_x, pos_y)

def track_selection_init():
    """Initialize track selection screen"""
    global win, selected_tracks
    win = pygame.display.get_surface()
    win.fill((20, 20, 20))
    pygame.display.set_caption("Track Selection Menu")
    
    # Clear selection when entering
    selected_tracks = []
    track_manager.clear_tracks()  # Assuming TrackManager has a clear method
    track_manager.add_track(default_track)

def track_selection_loop(event_list):
    """Main loop for track selection screen"""
    global win, track_manager, selected_tracks
    
    # Clear the window
    win.fill((20, 20, 20))
    
    # Draw title
    blit_title_center(pygame.display.get_surface(), "Select Your Track")
    
    # Track preview positions (grid layout) - adjusted for 630x630
    preview_positions = [
        (50, 90), (235, 90), (420, 90),   # Row 1
        (50, 255), (235, 255), (420, 255), # Row 2  
        (50, 420), (235, 420), (420, 420), # Row 3
    ]
    
    # Create and draw track previews FIRST (they go in the background)
    tracks = [track_1, track_2, track_3, track_4, track_5, 
              track_6, track_7, track_8, track_9]
    
    for i, (track, (x, y)) in enumerate(zip(tracks, preview_positions)):
        is_selected = track in selected_tracks
        preview = create_track_preview(track, is_selected=is_selected)
        win.blit(preview, (x, y))
    
    # Draw selection order display LAST (so it appears on top)
    # Only draw if there are selected tracks
    if selected_tracks:
        order_display, order_pos = create_selection_order_display()
        if order_display:
            win.blit(order_display, order_pos)
    else:
        # If no tracks selected, show instruction
        instruction_text = ORBITRON_FONT_INFO.render(
            "Selected tracks appear here.", True, (200, 200, 200))
        win.blit(instruction_text, 
                 (win.get_width() // 2 - instruction_text.get_width() // 2, 580))
    
    # Create Done button
    done_button_surface, done_button_rect = create_button("Done", 515, 45, (0, 180, 0))
    win.blit(done_button_surface, (done_button_rect.x, done_button_rect.y))
    
    # Create Clear All button
    clear_button_surface, clear_button_rect = create_button("Clear All", 475, 10, (180, 0, 0))
    win.blit(clear_button_surface, (clear_button_rect.x, clear_button_rect.y))

    back_button_surface, back_button_rect = create_button("Back", 10, 10, (0, 0, 180))
    win.blit(back_button_surface, (back_button_rect.x, back_button_rect.y))
    
    # Check for hover effects
    mouse_pos = pygame.mouse.get_pos()
    
    # Process events
    for event in event_list:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            # Check if Done button was clicked
            if done_button_rect.collidepoint(mouse_x, mouse_y):
                if not selected_tracks:
                    print("No tracks selected! Please select at least one track.")
                    create_notification(win, "Please select at least one track!", duration=1500)
                else:
                    # Update track manager with selected tracks
                    track_manager.clear_tracks()
                    for track in selected_tracks:
                        track_manager.add_track(track)
                    
                    print("Selected track(s):", [track.name for track in track_manager.tracks])
                    return "MAIN_GAME"
            
            # Check if Clear All button was clicked
            if clear_button_rect.collidepoint(mouse_x, mouse_y):
                if selected_tracks == []:
                    create_notification(win, "No tracks to be deselected")
                else:
                    selected_tracks = []
                    create_notification(win, "Tracks deselecting...")
        

            if back_button_rect.collidepoint(mouse_x, mouse_y):
                return "INTRO_MENU"
            
            # Check which track preview was clicked
            for track, (x, y) in zip(tracks, preview_positions):
                if x <= mouse_x <= x + 160 and y <= mouse_y <= y + 150:
                    # Toggle selection: remove if already selected, add to end if not
                    if track in selected_tracks:
                        selected_tracks.remove(track)
                    else:
                        selected_tracks.append(track)
                    break  # Only one track per click    
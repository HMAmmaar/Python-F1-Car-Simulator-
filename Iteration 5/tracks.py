import pygame
from utils import scale_image

class Track:
    def __init__(self, name, scale_factor,track_index, track_image_path, track_border_path, 
                 track_border_mask_path, grass_image_path, finish_scale, finish_image_path, 
                 finish_pos, player_start_pos, comp_start_pos, path):
        self.name = name
        self.track_index = track_index
        self.scale_factor = scale_factor
        self.track = self._load_scaled_image(track_image_path, self.scale_factor)
        self.track_border = self._load_scaled_image(track_border_path, self.scale_factor)
        self.track_border_mask = pygame.mask.from_surface(
            self._load_scaled_image(track_border_mask_path, self.scale_factor)
        )
        self.grass = self._load_scaled_image(grass_image_path, 3)
        self.finish_scale = finish_scale
        self.finish = self._load_scaled_image(finish_image_path, self.finish_scale)
        self.finish_mask = pygame.mask.from_surface(self.finish)
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
    
    def clear_tracks(self):
        self.tracks = []
        self.current_track_index = 0
    
    def remove_track(self, track):
        if track in self.tracks:
            self.tracks.remove(track)

    def next_track(self):
        if self.current_track_index >= len(self.tracks)-1:
            print("Gone through all tracks")
            return None
        else:
            self.current_track_index += 1
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


default_track = Track(
    name = "Track 1",
    track_index = 1,
    scale_factor = 0.7,
    track_image_path = "imgs/track-1/track.png",
    track_border_path = "imgs/track-1/track-border.png",
    track_border_mask_path = "imgs/track-1/track-1 border mask.png",
    grass_image_path = "imgs/grass.jpg",
    finish_scale = 0.75,
    finish_image_path = "imgs/finish.png",
    finish_pos = (100,135),
    player_start_pos = (117,160),
    comp_start_pos = (142,160),
    path = [(148, 87), (120, 69), (86, 60), (57, 71), (42, 118), (50, 356), (58, 370), (226, 558), (255, 569), (283, 563), (304, 544), (314, 513), (317, 475), (323, 426), (347, 388), (374, 372), (400, 375), (436, 391), (455, 430), (464, 500), (482, 558), (514, 573), (560, 570), (572, 538), (576, 510), (572, 332), (560, 297), (540, 288), (369, 282), (340, 284), (318, 271), (307, 241), (320, 212), (350, 196), (391, 196), (440, 197), (536, 203), (563, 186), (574, 149), (575, 91), (560, 70), (535, 62), (266, 62), (230, 69), (218, 88), (218, 268), (205, 302), (176, 313), (138, 308), (129, 268), (147, 86)]
)


track_1 = Track(
    name = "Track 1",
    track_index = 1,
    scale_factor = 0.7,
    track_image_path = "imgs/track-1/track.png",
    track_border_path = "imgs/track-1/track-border.png",
    track_border_mask_path = "imgs/track-1/track-1 border mask.png",
    grass_image_path = "imgs/grass.jpg",
    finish_scale = 0.75,
    finish_image_path = "imgs/finish.png",
    finish_pos = (100,135),
    player_start_pos = (117,160),
    comp_start_pos = (142,160),
    path = [(148, 87), (120, 69), (86, 60), (57, 71), (42, 118), (50, 356), (58, 370), (226, 558), (255, 569), (283, 563), (304, 544), (314, 513), (317, 475), (323, 426), (347, 388), (374, 372), (400, 375), (436, 391), (455, 430), (464, 500), (482, 558), (514, 573), (560, 570), (572, 538), (576, 510), (572, 332), (560, 297), (540, 288), (369, 282), (340, 284), (318, 271), (307, 241), (320, 212), (350, 196), (391, 196), (440, 197), (536, 203), (563, 186), (574, 149), (575, 91), (560, 70), (535, 62), (266, 62), (230, 69), (218, 88), (218, 268), (205, 302), (176, 313), (138, 308), (129, 268), (147, 86)]
)

track_2 = Track(
        name="Track 2", 
        track_index=2,
        scale_factor = 0.6,
        track_image_path="imgs/track-2/track-2.png",
        track_border_path="imgs/track-2/track-2 border.png",
        track_border_mask_path="imgs/track-2/track-2 border mask.png",
        grass_image_path="imgs/grass.jpg",
        finish_scale = 1,
        finish_image_path="imgs/finish.png",
        finish_pos=(620, 310),
        player_start_pos=(645, 350),
        comp_start_pos=(685, 350),
        path=[(656, 288), (631, 223), (582, 168), (524, 107), (448, 71), (378, 128), (399, 225), (344, 246), (281, 181), (268, 119), (218, 94), (178, 84), (135, 146), (137, 249), (142, 405), (153, 537), (241, 590), (396, 581), (437, 531), (386, 470), (305, 468), (264, 434), (279, 370), (506, 361), (560, 410), (544, 633), (489, 685), (241, 692), (172, 736), (154, 795), (197, 862), (470, 857), (650, 668), (670, 603), (656, 289)]
    )

track_3 = Track(
    name = "Track 3",
    track_index = 3,
    scale_factor = 0.6,
    track_image_path = "imgs/track-3/track.png",
    track_border_path = "imgs/track-3/track-border.png",
    track_border_mask_path = "imgs/track-3/track-3 border mask.png",
    grass_image_path = "imgs/grass.jpg",
    finish_scale = 1.2,
    finish_image_path = "imgs/finish.png",
    finish_pos = (680, 511),
    player_start_pos = (710, 531),
    comp_start_pos = (755, 531),
    path = [(728.0, 463.33333333333337), (692.6666666666667, 413.3333333333333), (656.0, 397.3333333333333), (599.3333333333334, 391.3333333333333), (325.6666666666667, 389.66666666666663), (261.6666666666667, 352.33333333333337), (256.3333333333333, 277.0), (316.3333333333333, 245.66666666666669), (671.6666666666667, 243.0), (726.6666666666667, 198.66666666666666), (727.3333333333333, 133.33333333333334), (672.0, 100.0), (342.0, 100.0), (201.33333333333331, 147.33333333333334), (120.66666666666667, 271.3333333333333), (110.0, 752.3333333333334), (122.0, 805.6666666666667), (156.66666666666666, 840.3333333333333), (280.0, 864.3333333333333), (356.6666666666667, 817.0), (344.6666666666667, 760.3333333333334), (269.3333333333333, 673.6666666666666), (240.66666666666666, 606.3333333333334), (304.0, 536.3333333333334), (483.66666666666663, 530.6666666666666), (535.0, 569.3333333333333), (555.6666666666666, 622.0), (559.3333333333333, 795.0), (619.3333333333333, 838.3333333333333), (684.6666666666667, 838.3333333333333), (732.6666666666667, 785.6666666666667),(728.0, 463.33333333333337)]
)

track_4 = Track(
        name="Track 4", 
        track_index=4,
        scale_factor = 0.6,
        track_image_path="imgs/track-4/track-4.png",
        track_border_path="imgs/track-4/track-4 border.png",
        track_border_mask_path="imgs/track-4/track-4 border mask.png",
        grass_image_path="imgs/grass.jpg",
        finish_scale = 1,
        finish_image_path="imgs/finish.png",
        finish_pos=(820, 511),
        player_start_pos=(850, 531),
        comp_start_pos=(885, 531),
        path=[(865.3333333333333, 238.0), (838.0, 194.0), (767.3333333333333, 188.0), (730.0, 226.0), (721.3333333333334, 364.0), (690.6666666666666, 412.6666666666667), (604.6666666666666, 420.6666666666667), (562.6666666666666, 377.3333333333333), (546.6666666666666, 246.0), (524.0, 176.0), (433.6666666666667, 187.33333333333334), (339.0, 380.66666666666663), (260.33333333333337, 414.66666666666663), (208.33333333333334, 344.0), (271.66666666666663, 216.0), (240.66666666666666, 133.33333333333334), (138.66666666666669, 116.66666666666667), (90.66666666666667, 174.0), (83.33333333333333, 488.33333333333337), (135.33333333333334, 561.6666666666667), (671.3333333333334, 574.3333333333334), (718.6666666666666, 623.6666666666666), (728.0, 780.3333333333333), (785.3333333333333, 851.6666666666667), (817.3333333333333, 849.0), (868.0, 788.3333333333333), (865.3333333333333, 238.33333333333334)]
    )

track_5 = Track(
    name = "Track 5",
    track_index = 5,
    scale_factor = 0.6,
    track_image_path = "imgs/track-5/track-5.png",
    track_border_path = "imgs/track-5/track-5 border.png",
    track_border_mask_path = "imgs/track-5/track-5 border mask.png",
    grass_image_path = "imgs/grass.jpg",
    finish_scale = 1.2,
    finish_image_path = "imgs/finish.png",
    finish_pos = (570,511),
    player_start_pos = (605, 531),
    comp_start_pos = (640, 531),
    path = [(634.0, 442.66666666666663), (634.6666666666667, 439.0), (661.3333333333333, 394.3333333333333), (721.3333333333334, 343.3333333333333), (845.3333333333333, 205.33333333333334), (838.0, 133.33333333333334), (796.0, 102.66666666666667), (739.3333333333334, 113.33333333333333), (672.6666666666666, 207.33333333333334), (637.3333333333334, 238.66666666666666), (580.6666666666666, 223.33333333333334), (562.6666666666666, 166.66666666666666), (523.3333333333334, 114.0), (471.33333333333337, 102.66666666666667), (183.33333333333334, 116.66666666666667), (120.66666666666667, 155.33333333333334), (105.33333333333333, 216.66666666666666), (144.0, 271.3333333333333), (480.66666666666663, 304.33333333333337), (520.6666666666666, 352.33333333333337), (494.0, 405.6666666666667), (296.33333333333337, 465.33333333333337), (266.33333333333337, 517.3333333333333), (277.66666666666663, 568.6666666666667), (503.33333333333337, 821.3333333333333), (565.3333333333334, 860.0), (654.0, 850.6666666666667), (690.0, 797.3333333333333), (631.6666666666667, 590.0), (635.6666666666667, 440.66666666666663)]
)

track_6 = Track(
        name="Track 6", 
        track_index=6,
        scale_factor = 0.6,
        track_image_path="imgs/track-6/track-6.png",
        track_border_path="imgs/track-6/track-6 border.png",
        track_border_mask_path="imgs/track-6/track-6 border mask.png",
        grass_image_path="imgs/grass.jpg",
        finish_scale = 1,
        finish_image_path="imgs/finish.png",
        finish_pos=(750, 511),
        player_start_pos=(800, 531),
        comp_start_pos=(825, 531),
        path=[(814.6666666666667, 227.0), (764.0, 201.66666666666666), (624.6666666666666, 199.0), (576.0, 249.66666666666666), (572.6666666666666, 309.6666666666667), (537.3333333333334, 361.6666666666667), (413.0, 360.33333333333337), (369.6666666666667, 319.66666666666663), (361.0, 166.33333333333334), (309.33333333333337, 123.33333333333333), (258.0, 151.33333333333334), (252.66666666666666, 324.6666666666667), (199.33333333333334, 375.3333333333333), (136.0, 418.6666666666667), (138.66666666666666, 781.3333333333333), (199.33333333333334, 844.0), (274.0, 832.6666666666667), (316.0, 765.3333333333334), (332.66666666666663, 525.0), (394.6666666666667, 476.33333333333337), (669.0, 474.33333333333337), (714.3333333333334, 521.6666666666667), (715.6666666666666, 617.0), (675.0, 662.3333333333333), (531.0, 669.6666666666666), (482.3333333333333, 731.0), (495.0, 800.3333333333333), (528.3333333333333, 827.6666666666667), (750.6666666666667, 829.6666666666667), (804.6666666666667, 787.6666666666667), (820.0, 735.0), (814.6666666666667, 227.0)]
)

track_7 = Track(
    name = "Track 7",
    track_index = 7,
    scale_factor = 0.6,
    track_image_path = "imgs/track-7/track-7.png",
    track_border_path = "imgs/track-7/track-7 border.png",
    track_border_mask_path = "imgs/track-7/track-7 border mask.png",
    grass_image_path = "imgs/grass.jpg",
    finish_scale = 1.2,
    finish_image_path = "imgs/finish.png",
    finish_pos = (790, 511),
    player_start_pos = (840, 531),
    comp_start_pos = (865, 531),
    path = [(860.0, 385.0), (811.3333333333333, 336.33333333333337), (566.6666666666666, 342.0), (513.3333333333333, 415.6666666666667), (474.0, 469.6666666666667), (424.0, 462.3333333333333), (402.66666666666663, 381.0), (354.66666666666663, 335.6666666666667), (265.0, 319.3333333333333), (203.66666666666669, 276.0), (120.33333333333333, 297.3333333333333), (109.33333333333333, 379.0), (155.33333333333334, 413.0), (232.0, 428.33333333333337), (262.6666666666667, 457.6666666666667), (256.6666666666667, 503.6666666666667), (213.33333333333334, 524.3333333333333), (141.33333333333334, 540.3333333333333), (98.0, 585.6666666666667), (101.33333333333333, 645.6666666666666), (151.33333333333334, 683.0), (223.33333333333334, 682.3333333333334), (526.6666666666667, 606.3333333333334), (591.3333333333333, 519.6666666666666), (650.0, 462.3333333333333), (725.3333333333334, 473.66666666666663), (759.3333333333333, 567.6666666666667), (787.3333333333333, 609.6666666666667), (834.6666666666667, 609.6666666666667), (863.3333333333333, 545.0),(860.0, 385.0)]
)

track_8 = Track(
        name="Track 8", 
        track_index=8,
        scale_factor = 0.6,
        track_image_path="imgs/track-8/track-8.png",
        track_border_path="imgs/track-8/track-8 border.png",
        track_border_mask_path="imgs/track-8/track-8 border mask.png",
        grass_image_path="imgs/grass.jpg",
        finish_scale = 1.2,
        finish_image_path="imgs/finish.png",
        finish_pos=(820, 461),
        player_start_pos=(860, 491),
        comp_start_pos=(885, 491),
        path=[(868.0, 435.33333333333337), (838.6666666666667, 406.33333333333337), (791.3333333333333, 384.3333333333333), (576.6666666666666, 379.33333333333337), (538.3333333333334, 363.66666666666663), (527.3333333333334, 350.33333333333337), (420.66666666666663, 235.66666666666666), (177.66666666666666, 202.66666666666666), (129.66666666666669, 218.66666666666666), (89.0, 263.3333333333333), (85.0, 310.0), (100.33333333333333, 344.6666666666667), (128.33333333333331, 375.3333333333333), (165.0, 387.3333333333333), (326.0, 381.0), (364.66666666666663, 390.33333333333337), (538.0, 559.6666666666667), (548.3333333333334, 615.3333333333333), (525.0, 646.0), (486.33333333333337, 658.0), (451.0, 650.0), (263.6666666666667, 637.6666666666667), (218.33333333333331, 619.3333333333333), (195.0, 582.0), (160.66666666666666, 542.0), (120.66666666666667, 541.3333333333334), (78.66666666666667, 568.0), (76.66666666666667, 605.3333333333333), (118.0, 715.6666666666666), (143.33333333333334, 745.0), (171.33333333333334, 762.3333333333333), (201.33333333333334, 760.0), (616.6666666666666, 760.0), (644.6666666666667, 743.3333333333334), (675.3333333333333, 704.6666666666666), (692.0, 646.6666666666666), (742.6666666666667, 614.0), (810.6666666666667, 593.0), (854.6666666666667, 559.6666666666666), (873.3333333333333, 517.0), (869.3333333333333, 440.0)]
)

track_9 = Track(
    name = "Track 9",
    track_index = 9,
    scale_factor = 0.6,
    track_image_path = "imgs/track-9/track-9.png",
    track_border_path = "imgs/track-9/track-9 border.png",
    track_border_mask_path = "imgs/track-9/track-9 border mask.png",
    grass_image_path = "imgs/grass.jpg",
    finish_scale = 0.75,
    finish_image_path = "imgs/finish.png",
    finish_pos = (590, 211),
    player_start_pos = (610, 240),
    comp_start_pos = (640, 240),
    path = [(625.6666666666666, 132.33333333333331), (585.0, 86.33333333333333), (377.3333333333333, 84.0), (328.66666666666663, 124.66666666666667), (324.0, 219.33333333333334), (365.3333333333333, 263.3333333333333), (482.6666666666667, 270.6666666666667), (524.0, 315.3333333333333), (487.3333333333333, 362.0), (365.3333333333333, 365.3333333333333), (324.0, 410.0), (324.0, 662.3333333333333), (336.6666666666667, 704.3333333333333), (411.66666666666663, 829.3333333333333), (410.66666666666663, 830.0), (428.0, 852.0), (465.3333333333333, 879.3333333333333), (585.0, 882.0), (624.3333333333333, 842.0), (625.6666666666667, 699.6666666666667), (584.3333333333333, 658.3333333333333), (481.0, 645.0), (426.3333333333333, 610.3333333333334), (427.6666666666667, 505.0), (463.0, 466.3333333333333), (582.0, 457.6666666666667), (632.3333333333334, 402.66666666666663), (629.3333333333334, 140.66666666666666)]
)
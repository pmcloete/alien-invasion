class Sounds:
    """
    A class to handle the loading and playing of sounds in the game
    """

    def __init__(self, ai):
        """
        Initialize the sound class
        """
        self.pygame = ai.pygame
        self.sound_played = True

        #  Title Screen Sounds
        self.theme_song = ai.os.path.join('assets','sounds','main_theme.wav')
        self.mouse_hover_sound = self.pygame.mixer.Sound(ai.os.path.join('assets','sounds','button_sound.wav'))
        self.play_pressed_sound = self.pygame.mixer.Sound(ai.os.path.join('assets','sounds','play_button.wav'))

        #  In-Game Sounds
        self.bullet_fired = self.pygame.mixer.Sound(ai.os.path.join('assets', 'sounds', 'bullet_sound.wav'))
        self.alien_hit = self.pygame.mixer.Sound(ai.os.path.join('assets','sounds','alien_hit.wav'))

    def play_sound(self, sound_to_play, volume = 0.8):
        """Play a sound as the mouse hovers over a button"""
        if self.sound_played:
            self.pygame.mixer.Sound.set_volume(sound_to_play,volume)
            #  Fade in for 40ms to remove clicking sound
            self.pygame.mixer.Sound.play(sound_to_play,0,0,40)
            self.sound_played = False

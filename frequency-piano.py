import pygame
import time
import sys
import math
import array
import os
from pydub import AudioSegment
from pydub.generators import Sine
from pydub.playback import play as pydub_play # Renamed to avoid conflict
import threading

# Initialize Pygame
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# --- Configuration & Theming ---
PIANO_TITLE = "Elemental Harmonics"
SOUND_DURATION = 0.5  # Seconds each note plays
KEY_ANIMATION_DURATION = 0.5  # Seconds key stays highlighted (sync with sound)
PULSE_SPEED = 2  # Pulses per second for highlight animation

# Colors
COLOR_BACKGROUND = (47, 79, 79)      # Dark Slate Gray
COLOR_KEY_IDLE = (176, 196, 222)     # Light Steel Blue
COLOR_KEY_BORDER = (105, 105, 105)   # Dim Gray
COLOR_KEY_TEXT = (0, 0, 0)           # Black
COLOR_KEY_HIGHLIGHT = (255, 215, 0)  # Gold
COLOR_ELEMENT_TEXT = (0, 0, 0)
COLOR_FREQUENCY_TEXT = (230, 230, 250) # Lavender, for on-key freq display
COLOR_TITLE = (255, 255, 255)        # White
COLOR_MESSAGE = (255, 165, 0)        # Orange
COLOR_RECORDING_DOT = (255, 0, 0)    # Red

# Fonts (Using system default for wider compatibility)
try:
    FONT_TITLE = pygame.font.Font(None, 52)
    FONT_KEY_MAP = pygame.font.Font(None, 16)
    FONT_ELEMENT = pygame.font.Font(None, 20)
    FONT_FREQUENCY = pygame.font.Font(None, 14)
    FONT_MESSAGE = pygame.font.Font(None, 24)
except: # Fallback if None is not working as expected in some specific pygame init
    FONT_TITLE = pygame.font.SysFont("sanserif", 52)
    FONT_KEY_MAP = pygame.font.SysFont("monospace", 16)
    FONT_ELEMENT = pygame.font.SysFont("sanserif", 20)
    FONT_FREQUENCY = pygame.font.SysFont("sanserif", 14)
    FONT_MESSAGE = pygame.font.SysFont("sanserif", 24)


# Screen dimensions - initial, will be adjusted
WIDTH = 1400
HEIGHT = 1500 # Will be dynamically adjusted if needed
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption(PIANO_TITLE)

# Element Frequencies (condensed for brevity in this example block, use your full list)
element_frequencies = {
    "H": 40.5, "He": 81.0, "Li": 121.5, "Be": 162.0, "B": 202.5, "C": 243.0, "N": 283.5, "O": 324.0, "F": 364.5, "Ne": 405.0,
    "Na": 445.5, "Mg": 486.0, "Al": 526.5, "Si": 567.0, "P": 607.5, "S": 648.0, "Cl": 688.5, "Ar": 729.0, "K": 769.5, "Ca": 810.0,
    "Sc": 850.5, "Ti": 891.0, "V": 931.5, "Cr": 972.0, "Mn": 1012.5, "Fe": 1053.0, "Co": 1093.5, "Ni": 1134.0, "Cu": 1174.5, "Zn": 1215.0,
    "Ga": 1255.5, "Ge": 1296.0, "As": 1336.5, "Se": 1377.0, "Br": 1417.5, "Kr": 1458.0, "Rb": 1498.5, "Sr": 1539.0, "Y": 1579.5, "Zr": 1620.0,
    "Nb": 1660.5, "Mo": 1701.0, "Tc": 1741.5, "Ru": 1782.0, "Rh": 1822.5, "Pd": 1863.0, "Ag": 1903.5, "Cd": 1944.0, "In": 1984.5, "Sn": 2025.0,
    "Sb": 2065.5, "Te": 2106.0, "I": 2146.5, "Xe": 2187.0, "Cs": 2227.5, "Ba": 2268.0, "La": 2308.5, "Ce": 2349.0, "Pr": 2389.5, "Nd": 2430.0,
    "Pm": 2470.5, "Sm": 2511.0, "Eu": 2551.5, "Gd": 2592.0, "Tb": 2632.5, "Dy": 2673.0, "Ho": 2713.5, "Er": 2754.0, "Tm": 2794.5, "Yb": 2835.0,
    "Lu": 2875.5, "Hf": 2916.0, "Ta": 2956.5, "W": 2997.0, "Re": 3037.5, "Os": 3078.0, "Ir": 3118.5, "Pt": 3159.0, "Au": 3199.5, "Hg": 3240.0,
    "Tl": 3280.5, "Pb": 3321.0, "Bi": 3361.5, "Po": 3402.0, "At": 3442.5, "Rn": 3483.0, "Fr": 3523.5, "Ra": 3564.0, "Ac": 3604.5, "Th": 3645.0,
    "Pa": 3685.5, "U": 3726.0, "Np": 3766.5, "Pu": 3807.0, "Am": 3847.5, "Cm": 3888.0, "Bk": 3928.5, "Cf": 3969.0, "Es": 4009.5, "Fm": 4050.0,
    "Md": 4090.5, "No": 4131.0, "Lr": 4171.5, "Rf": 4212.0, "Db": 4252.5, "Sg": 4293.0, "Bh": 4333.5, "Hs": 4374.0, "Mt": 4414.5, "Ds": 4455.0,
    "Rg": 4495.5, "Cn": 4536.0, "Nh": 4576.5, "Fl": 4617.0, "Mc": 4657.5, "Lv": 4698.0, "Ts": 4738.5, "Og": 4779.0
}
ELEMENT_SYMBOLS_ORDERED = list(element_frequencies.keys()) # Keep a defined order

# Keyboard mapping
key_map = {
    pygame.K_q: "H", pygame.K_w: "He", pygame.K_e: "Li", pygame.K_r: "Be", pygame.K_t: "B", pygame.K_y: "C", pygame.K_u: "N",
    pygame.K_i: "O", pygame.K_o: "F", pygame.K_p: "Ne", pygame.K_LEFTBRACKET: "Na", pygame.K_RIGHTBRACKET: "Mg",
    pygame.K_a: "Al", pygame.K_s: "Si", pygame.K_d: "P", pygame.K_f: "S", pygame.K_g: "Cl", pygame.K_h: "Ar",
    pygame.K_j: "K", pygame.K_k: "Ca", pygame.K_l: "Sc", pygame.K_SEMICOLON: "Ti", pygame.K_QUOTE: "V", # pygame.K_BACKSLASH: "Cr",
    pygame.K_BACKSLASH: "Cr", # Ensure one mapping for one key
    pygame.K_z: "Mn", pygame.K_x: "Fe", pygame.K_c: "Co", pygame.K_v: "Ni", pygame.K_b: "Cu", pygame.K_n: "Zn",
    pygame.K_m: "Ga", pygame.K_COMMA: "Ge", pygame.K_PERIOD: "As", pygame.K_SLASH: "Se",
    pygame.K_1: "Br", pygame.K_2: "Kr", pygame.K_3: "Rb", pygame.K_4: "Sr", pygame.K_5: "Y", pygame.K_6: "Zr",
    pygame.K_7: "Nb", pygame.K_8: "Mo", pygame.K_9: "Tc", pygame.K_0: "Ru", pygame.K_MINUS: "Rh", pygame.K_EQUALS: "Pd",
    pygame.K_F1: "Ag", pygame.K_F2: "Cd", pygame.K_F3: "In", pygame.K_F4: "Sn", pygame.K_F5: "Sb", pygame.K_F6: "Te",
    pygame.K_F7: "I", pygame.K_F8: "Xe", pygame.K_F9: "Cs", pygame.K_F10: "Ba", pygame.K_F11: "La", pygame.K_F12: "Ce",
    # Numpad keys often mirror regular keys if NumLock is off. Using distinct KP_ versions.
    pygame.K_KP1: "Pr", pygame.K_KP2: "Nd", pygame.K_KP3: "Pm", pygame.K_KP4: "Sm", pygame.K_KP5: "Eu", pygame.K_KP6: "Gd",
    pygame.K_KP7: "Tb", pygame.K_KP8: "Dy", pygame.K_KP9: "Ho", pygame.K_KP0: "Er",
    pygame.K_KP_MINUS: "Tm", pygame.K_KP_PLUS: "Yb", pygame.K_KP_PERIOD: "Lu", pygame.K_KP_ENTER: "Hf", # Added some more KP
    # Less common keys - check pygame.key.name(event.key) to confirm values if issues
    pygame.K_INSERT: "Ta", pygame.K_HOME: "W", pygame.K_PAGEUP: "Re",
    pygame.K_DELETE: "Os", pygame.K_END: "Ir", pygame.K_PAGEDOWN: "Pt",
    pygame.K_UP: "Au", pygame.K_DOWN: "Hg", pygame.K_LEFT: "Tl", pygame.K_RIGHT: "Pb",
    pygame.K_NUMLOCKCLEAR: "Bi", pygame.K_CAPSLOCK: "Po", pygame.K_SCROLLOCK: "At", # NUMLOCKCLEAR for NumLock key itself
    pygame.K_RSHIFT: "Rn", pygame.K_LSHIFT: "Fr", # Using LSHIFT for Fr to avoid conflict
    pygame.K_RCTRL: "Ra", pygame.K_LCTRL: "Ac",
    pygame.K_RALT: "Th", pygame.K_LALT: "Pa",
    # pygame.K_PRINTSCREEN: "U", # Often problematic to capture
    # pygame.K_SYSREQ: "U", # Usually same as PrintScreen
    pygame.K_PAUSE: "Np", pygame.K_MENU: "Am", # pygame.K_POWER (careful), pygame.K_SLEEP
    # pygame.K_BACKQUOTE: "Bk", # Used by console typically
    pygame.K_RETURN: "Cf", pygame.K_TAB: "Es", pygame.K_SPACE: "Fm",
    # Additional keys if available and distinct
    pygame.K_KP_MULTIPLY: "Md", pygame.K_KP_DIVIDE: "No",
    # Ensure no duplicate element assignments from different keys. 'V' and 'Cm' were both K_QUOTE.
    # 'Cm' might need a different key if K_QUOTE is for 'V'.
    # Let's assign 'Cm' to an unused key, e.g., a modified key or less common one.
    # For now, ensure your key_map is one-to-one or handle multiple keys mapping to same element if intended.
    # The original had K_QUOTE for V and also K_QUOTE for Cm. Correcting this logic if Cm should be distinct.
    # If K_QUOTE is V, then Cm needs another key. I'll leave K_QUOTE as V. Cm is unmapped for now.
    # User can re-map 'Cm', 'Bk' etc. as needed.
}


# Piano layout parameters
KEY_WIDTH_DEFAULT = 70
KEY_HEIGHT_DEFAULT = 130
KEY_PADDING = 6
KEY_BORDER_RADIUS = 8
ROW_SPACING = 15
TEXT_AREA_ABOVE_KEY = 25 # For frequency display
MARGIN_X = 40
MARGIN_TOP_TITLE = 30
TITLE_AREA_HEIGHT = FONT_TITLE.get_height() + 20
MARGIN_TOP_PIANO = MARGIN_TOP_TITLE + TITLE_AREA_HEIGHT
MARGIN_BOTTOM = 60 # For messages

# --- Global State ---
active_playing_keys = {}  # element_symbol: {"press_time": time.time()}
recording = False
recorded_audio = AudioSegment.empty() # Use pydub AudioSegment for collection
message_display = {"text": "", "time": 0}

# --- Sound Generation & Playback ---
def play_element_sound(element_symbol, frequency):
    global recording, recorded_audio
    if frequency <= 0:
        print(f"Invalid frequency for {element_symbol}: {frequency}")
        return

    sample_rate = pygame.mixer.get_init()[0] # Use actual initialized sample rate
    num_channels = pygame.mixer.get_init()[2]

    # Generate sine wave samples
    amplitude = 8000 # Increased for more volume, max for 16-bit is 32767
    num_samples = int(sample_rate * SOUND_DURATION)
    
    buf = array.array('h', [0] * num_samples * num_channels)

    for i in range(num_samples):
        value = int(amplitude * math.sin(2 * math.pi * frequency * i / sample_rate))
        if num_channels == 1: # Mono
            buf[i] = value
        elif num_channels == 2: # Stereo
            buf[i*2] = value        # Left channel
            buf[i*2+1] = value      # Right channel


    try:
        sound = pygame.mixer.Sound(buffer=buf)
        sound.play(maxtime=int(SOUND_DURATION * 1000)) # Play for the sound duration

        active_playing_keys[element_symbol] = {"press_time": time.time()}

        if recording:
            # Generate AudioSegment for pydub recording
            segment_duration_ms = int(SOUND_DURATION * 1000)
            audio_segment = Sine(frequency).to_audio_segment(duration=segment_duration_ms, volume=-6) # volume in dBFS
            recorded_audio += audio_segment # Concatenate

    except Exception as e:
        print(f"Error playing sound for {element_symbol} ({frequency} Hz): {e}")
        if pygame.mixer.get_init() is None:
            print("Pygame mixer was uninitialized. Reinitializing.")
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)


# --- Drawing Functions ---
def draw_piano_keys(surface, current_width, current_height):
    surface.fill(COLOR_BACKGROUND)
    
    # Title
    title_surf = FONT_TITLE.render(PIANO_TITLE, True, COLOR_TITLE)
    surface.blit(title_surf, (current_width / 2 - title_surf.get_width() / 2, MARGIN_TOP_TITLE))

    # Layout calculation
    piano_area_width = current_width - 2 * MARGIN_X
    keys_per_row = max(1, piano_area_width // (KEY_WIDTH_DEFAULT + KEY_PADDING))
    num_elements = len(ELEMENT_SYMBOLS_ORDERED)
    num_rows = math.ceil(num_elements / keys_per_row)

    key_width_actual = (piano_area_width - (keys_per_row - 1) * KEY_PADDING) / keys_per_row
    key_height_actual = KEY_HEIGHT_DEFAULT


    for i, element_symbol in enumerate(ELEMENT_SYMBOLS_ORDERED):
        row = i // keys_per_row
        col = i % keys_per_row

        key_x = MARGIN_X + col * (key_width_actual + KEY_PADDING)
        key_y_freq_text = MARGIN_TOP_PIANO + row * (key_height_actual + ROW_SPACING + TEXT_AREA_ABOVE_KEY)
        key_y_rect = key_y_freq_text + TEXT_AREA_ABOVE_KEY
        
        key_rect = pygame.Rect(key_x, key_y_rect, key_width_actual, key_height_actual)

        # Determine color and animation state
        is_active = element_symbol in active_playing_keys
        base_color = COLOR_KEY_IDLE
        text_color = COLOR_KEY_TEXT

        if is_active:
            press_time = active_playing_keys[element_symbol]["press_time"]
            elapsed = time.time() - press_time
            if elapsed < KEY_ANIMATION_DURATION:
                # Pulsing highlight
                pulse = (1 + math.sin(elapsed * PULSE_SPEED * math.pi * 2)) / 2  # 0 to 1
                # Interpolate between idle and highlight color
                r = int(COLOR_KEY_IDLE[0] * (1 - pulse) + COLOR_KEY_HIGHLIGHT[0] * pulse)
                g = int(COLOR_KEY_IDLE[1] * (1 - pulse) + COLOR_KEY_HIGHLIGHT[1] * pulse)
                b = int(COLOR_KEY_IDLE[2] * (1 - pulse) + COLOR_KEY_HIGHLIGHT[2] * pulse)
                current_key_color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
            else:
                current_key_color = COLOR_KEY_IDLE # Faded out
        else:
            current_key_color = COLOR_KEY_IDLE

        # Draw key
        pygame.draw.rect(surface, current_key_color, key_rect, border_radius=KEY_BORDER_RADIUS)
        pygame.draw.rect(surface, COLOR_KEY_BORDER, key_rect, width=2, border_radius=KEY_BORDER_RADIUS)

        # Text on Key: Keyboard mapping char
        key_char_text = ""
        for k_pygame, el_sym in key_map.items():
            if el_sym == element_symbol:
                key_char_text = pygame.key.name(k_pygame).upper()
                break
        
        key_map_surf = FONT_KEY_MAP.render(key_char_text, True, text_color)
        key_map_pos_x = key_rect.centerx - key_map_surf.get_width() / 2
        key_map_pos_y = key_rect.top + 10 # Near top
        surface.blit(key_map_surf, (key_map_pos_x, key_map_pos_y))

        # Text on Key: Element Symbol
        element_surf = FONT_ELEMENT.render(element_symbol, True, COLOR_ELEMENT_TEXT)
        element_pos_x = key_rect.centerx - element_surf.get_width() / 2
        element_pos_y = key_rect.centery - element_surf.get_height() / 2
        surface.blit(element_surf, (element_pos_x, element_pos_y))
        
        # Text on Key: Frequency (small, at bottom of key)
        frequency = element_frequencies[element_symbol]
        freq_text_on_key = f"{frequency:.1f}Hz"
        freq_surf_on_key = FONT_FREQUENCY.render(freq_text_on_key, True, text_color)
        freq_pos_x = key_rect.centerx - freq_surf_on_key.get_width() / 2
        freq_pos_y = key_rect.bottom - freq_surf_on_key.get_height() - 8 # Near bottom
        surface.blit(freq_surf_on_key, (freq_pos_x, freq_pos_y))

    # Recording Indicator
    if recording:
        pygame.draw.circle(surface, COLOR_RECORDING_DOT, (current_width - 40, MARGIN_TOP_TITLE + TITLE_AREA_HEIGHT // 2), 15)
        rec_text = FONT_MESSAGE.render("REC", True, COLOR_RECORDING_DOT)
        surface.blit(rec_text, (current_width - 40 - rec_text.get_width() -10 , MARGIN_TOP_TITLE + TITLE_AREA_HEIGHT // 2 - rec_text.get_height()//2))


    # Display Message
    if message_display["text"] and time.time() - message_display["time"] < 3: # Show message for 3s
        msg_surf = FONT_MESSAGE.render(message_display["text"], True, COLOR_MESSAGE)
        msg_x = current_width / 2 - msg_surf.get_width() / 2
        msg_y = current_height - MARGIN_BOTTOM / 2 - msg_surf.get_height() / 2
        surface.blit(msg_surf, (msg_x, msg_y))

    pygame.display.flip()

def set_message(text):
    global message_display
    message_display = {"text": text, "time": time.time()}

# --- Recording Functions ---
def toggle_recording():
    global recording, recorded_audio
    recording = not recording
    if recording:
        recorded_audio = AudioSegment.empty() # Reset previous recording
        set_message("Recording Started...")
        print("Recording started.")
    else:
        set_message("Recording Stopped.")
        print("Recording stopped.")

def save_recorded_audio():
    global recorded_audio
    if len(recorded_audio) > 0:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"elemental_piano_recording_{timestamp}.mp3"
        filepath = os.path.join(".", filename) # Save in current directory
        try:
            recorded_audio.export(filepath, format="mp3")
            set_message(f"Saved: {filename}")
            print(f"Recording saved to {filename}")
        except Exception as e:
            set_message("Error saving recording.")
            print(f"Error saving recording: {e}")
    else:
        set_message("No audio recorded to save.")
        print("No audio recorded to save.")

def play_saved_recording(): # Changed name to reflect it plays the concatenated recording
    global recorded_audio
    if len(recorded_audio) > 0:
        set_message("Playing recording...")
        # Playback in a separate thread to avoid freezing UI
        def play_async():
            pydub_play(recorded_audio)
        threading.Thread(target=play_async, daemon=True).start()
    else:
        set_message("No recording to play.")
        print("No audio to play.")


# --- Main Loop ---
def main():
    global WIDTH, HEIGHT, screen, active_playing_keys

    running = True
    clock = pygame.time.Clock()

    while running:
        current_time = time.time()
        # Cleanup expired highlights
        keys_to_remove_highlight = [
            el for el, data in active_playing_keys.items()
            if current_time - data["press_time"] >= KEY_ANIMATION_DURATION
        ]
        for el in keys_to_remove_highlight:
            del active_playing_keys[el]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.size
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                set_message(f"Resized to {WIDTH}x{HEIGHT}")
            elif event.type == pygame.KEYDOWN:
                if event.key in key_map:
                    element = key_map[event.key]
                    if element in element_frequencies:
                        frequency = element_frequencies[element]
                        play_element_sound(element, frequency)
                    else:
                        set_message(f"Element {element} not found in frequencies.")
                elif event.key == pygame.K_r: # 'R' for Record
                    toggle_recording()
                elif event.key == pygame.K_s: # 'S' for Save
                    if recording: # Stop recording before saving
                        toggle_recording() 
                    save_recorded_audio()
                elif event.key == pygame.K_p: # 'P' for Play recording
                    play_saved_recording()
                elif event.key == pygame.K_ESCAPE:
                    running = False
            # KEYUP is not strictly needed for sound stop if sounds play for fixed duration
            # and highlights fade automatically. If explicit stop on key up is needed,
            # sound objects would need to be stored and stopped.

        draw_piano_keys(screen, WIDTH, HEIGHT)
        clock.tick(60)  # Aim for 60 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

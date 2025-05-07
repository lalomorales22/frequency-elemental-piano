# Elemental Harmonics

A musical interactive application that translates the periodic table of elements into playable frequencies, creating a unique audio-visual experience.

![Screenshot 2025-05-06 at 6 43 20 PM](https://github.com/user-attachments/assets/ae40bc9d-bd20-4653-86a9-307bc2132ae4)


## 🌟 Overview

Elemental Harmonics transforms chemical elements into musical notes by mapping each element to a specific frequency. This creates a unique way to experience the periodic table through sound, allowing users to:

- Play individual element frequencies using keyboard inputs
- Record, save, and playback your elemental compositions
- Visualize the relationship between elements and their corresponding frequencies

The application represents a fascinating intersection of science, music, and interactive visualization, making it both educational and creative.

## ✨ Features

- **Element-to-Frequency Mapping**: All 118 elements of the periodic table mapped to corresponding frequencies
- **Interactive Keyboard Interface**: Visual piano-like interface with element symbols and frequencies
- **Real-time Sound Synthesis**: Pure sine wave generation at precise frequencies
- **Recording Capabilities**: Record your compositions and save them as MP3 files
- **Playback Function**: Play back your saved recordings
- **Visual Feedback**: Keys animate when played with a pulsing gold highlight
- **Resizable Interface**: Adjust the window size to fit your screen

## 🔧 Installation

### Prerequisites

- Python 3.7+
- Pygame
- PyDub

### Setup Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/lalomorales22/frequency-elemental-piano.git
   cd frequency-elemental-piano
   ```

2. Install required dependencies:
   ```bash
   pip install pygame pydub
   ```

3. Additional requirements:
   - For MP3 export functionality, you need FFmpeg installed on your system
     - **Windows**: Download from [FFmpeg.org](https://ffmpeg.org/download.html) and add to PATH
     - **macOS**: `brew install ffmpeg`
     - **Linux**: `sudo apt install ffmpeg`

## 🎹 How to Use

1. Launch the application:
   ```bash
   python frequency-piano.py
   ```

2. Play notes using your keyboard:
   - Each key on your keyboard is mapped to a specific element
   - Press keys to generate the corresponding element's frequency
   - The key mapping is shown at the top of each element key

3. Recording controls:
   - Press `R` to start/stop recording
   - Press `S` to save your recording (auto-saves in MP3 format)
   - Press `P` to play back your last recording

4. Additional controls:
   - `ESC` to exit the application
   - Resize the window as needed to see more keys at once

## 🔍 Element Frequency Mapping

The application maps each element to a frequency using a consistent pattern of increments:

- Starting with Hydrogen (H) at 40.5 Hz
- Each successive element increases by 40.5 Hz
- This creates a coherent scale of frequencies tied to the periodic table

## 🧪 Scientific Background

The element frequencies don't represent actual atomic properties like emission spectra, but rather provide a consistent system for musical exploration. The relationship between elements and sound creates an interesting way to experience chemistry through auditory patterns.

## 💻 Technical Details

- Built with Python and Pygame
- Uses sine wave generation for pure tones
- PyDub library handles audio recording and export
- Dynamic UI scaling based on window size
- Threading for non-blocking audio playback

## 🚀 Future Developments

- Ability to save and load custom keyboard mappings
- Option to use alternative frequency mappings (such as actual spectral frequencies)
- Chord and sequence programming features
- Visual spectrum analyzer

## 👨‍💻 About the Developer

Created by Lalo Morales, a software developer and data engineer based in San Diego. This project combines interests in programming, mathematics, and pattern recognition into an interactive audio-visual experience.

## 📄 License

This project is released under the MIT License. See the LICENSE file for details.

---

Feel free to contribute, report issues, or suggest improvements!

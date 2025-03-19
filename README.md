# Youtube-to-MP4-MP3-Downloader

Overview
YouTube Downloader is a Python-based desktop application with a graphical user interface (GUI) built using tkinter. It allows users to download videos or audio from YouTube by providing a URL and selecting the desired format (MP4 or MP3). The application uses yt-dlp for downloading content and FFmpeg for format conversion and merging. Key features include:

Video Title Retrieval: Automatically fetches the video title to name the output file.
Format Selection: Supports downloading videos as MP4 (up to 1080p with AAC audio) or audio as MP3.
Progress Tracking: Displays real-time download progress with a percentage bar and status updates.
Custom Output Folder: Allows users to choose where files are saved.
Cross-Platform: Works on both Windows and macOS with proper setup.
Error Handling: Provides feedback on download failures or missing dependencies.
The application is designed to be bundled into a standalone executable (e.g., using PyInstaller), but it can also be run directly from the source code with the required dependencies installed.

Prerequisites
To run this program, you need the following:

Python 3.6+: The programming language runtime.
FFmpeg: A multimedia framework for converting and merging media files.
yt-dlp: A YouTube downloading tool (fork of youtube-dl with additional features).
pip: Python package manager (typically bundled with Python).
The GUI relies on tkinter, which is included with standard Python installations, so no additional installation is required for it.

Installation Instructions
For Windows
1. Install Python
Download and install Python from python.org.
During installation, check the box to "Add Python to PATH".
Verify installation:
cmd

Collapse

Wrap

Copy
python --version
2. Install FFmpeg
Download the latest FFmpeg build from ffmpeg.org or use a pre-built binary from gyan.dev.
Extract the downloaded archive (e.g., ffmpeg-release-essentials.zip) to a folder, such as C:\ffmpeg.
Add FFmpeg to your system PATH:
Right-click "This PC" > "Properties" > "Advanced system settings" > "Environment Variables".
Under "System Variables," find Path, click "Edit," and add the path to the bin folder (e.g., C:\ffmpeg\bin).
Click "OK" to save.
Verify installation:
cmd

Collapse

Wrap

Copy
ffmpeg -version
3. Install yt-dlp
Open Command Prompt and install yt-dlp via pip:
cmd

Collapse

Wrap

Copy
pip install yt-dlp
Alternatively, download the executable from yt-dlp GitHub releases and place it in a folder (e.g., C:\yt-dlp).
If using the executable, add its folder to your system PATH (similar to FFmpeg).
Verify installation:
cmd

Collapse

Wrap

Copy
yt-dlp --version
4. Clone and Run the Repository
Install Git from git-scm.com if not already installed.
Clone the repository:
cmd

Collapse

Wrap

Copy
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
Ensure FFmpeg and yt-dlp are in the same directory as the script (e.g., rename to ffmpeg.exe and yt-dlp.exe) or accessible via PATH.
Run the program:
cmd

Collapse

Wrap

Copy
python youtube_downloader.py
For macOS
1. Install Python
Python is pre-installed on macOS, but it’s recommended to install a newer version via Homebrew:
Install Homebrew (if not installed):
bash

Collapse

Wrap

Copy
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
Install Python:
bash

Collapse

Wrap

Copy
brew install python
Verify installation:
bash

Collapse

Wrap

Copy
python3 --version
2. Install FFmpeg
Install FFmpeg using Homebrew:
bash

Collapse

Wrap

Copy
brew install ffmpeg
Verify installation:
bash

Collapse

Wrap

Copy
ffmpeg -version
3. Install yt-dlp
Install yt-dlp via pip:
bash

Collapse

Wrap

Copy
pip3 install yt-dlp
Alternatively, download the binary from yt-dlp GitHub releases, make it executable, and move it to a directory in your PATH:
bash

Collapse

Wrap

Copy
curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o yt-dlp
chmod +x yt-dlp
sudo mv yt-dlp /usr/local/bin/
Verify installation:
bash

Collapse

Wrap

Copy
yt-dlp --version
4. Clone and Run the Repository
Install Git (if not installed) via Homebrew:
bash

Collapse

Wrap

Copy
brew install git
Clone the repository:
bash

Collapse

Wrap

Copy
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
Ensure FFmpeg and yt-dlp are accessible (either in PATH or bundled as ffmpeg and yt-dlp in the script directory).
Run the program:
bash

Collapse

Wrap

Copy
python3 youtube_downloader.py
Usage
Launch the application by running the script as described above.
Enter a valid YouTube URL in the "YouTube URL" field.
Select the desired format (MP4 or MP3) from the dropdown menu.
Optionally, click "Choose Folder" to specify a custom download location (defaults to ~/Downloads).
Click "Download" to start the process.
Monitor the progress bar and status text for updates.
Once completed, the file will be saved in the specified folder with the video title as the filename.
Troubleshooting
FFmpeg or yt-dlp Not Found: Ensure both binaries are in the script directory or added to your system PATH. Check with ffmpeg -version and yt-dlp --version.
Download Fails: Verify the URL is valid and that your internet connection is stable. Check the status text for error details.
Permission Errors: On macOS, ensure the script and binaries have execute permissions (chmod +x <file>).
Building a Standalone Executable (Optional)
To distribute the app as a single executable file:

Install PyInstaller:
bash

Collapse

Wrap

Copy
pip install pyinstaller
Bundle the app, including FFmpeg and yt-dlp:
Windows:
cmd

Collapse

Wrap

Copy
pyinstaller --add-binary "ffmpeg.exe;." --add-binary "yt-dlp.exe;." -F youtube_downloader.py
macOS:
bash

Collapse

Wrap

Copy
pyinstaller --add-binary "ffmpeg:." --add-binary "yt-dlp:." -F youtube_downloader.py
Find the executable in the dist folder.

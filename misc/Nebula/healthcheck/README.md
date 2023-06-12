# Nebula by Ernikus
## Walkthrough

1. After obtaining the password, we gain access to the "nebula-melody.json" file. We use the **"file" command** and find out that `"7-zip archive data"` indicates that it is a .7Z file. We then extract the file and obtain another file named `nebula-melody.mp3`.

2. In short, the .MP3 file contains encoded data in an octal system, stored in the form of a musical scale. At the beginning, the entire scale is played (C4-C5), and then the data transmission begins. Each played sound lasts for 0.1 seconds. There is a pause (also lasting 0.1 seconds) between some of the sounds, which should also be noted. In summary, the entire file should be decoded into octal format text.

Sonic Visualizer with Melodic Range mode can be helpful.

You can use script [sound-converter.py](files/sound-converter.py) - example use `Python3 sound-converter.py file.mp3`

3. We do not need the information about the musical scale. We convert the entire decoded text from octal to decimal system. We interpret semicolon characters as newline characters.

`[CyberChief (from octal, replace(";", "\n"))]`

4. We convert the data from decimal system to binary and get rid of the spaces, leaving only the newline characters.

`[CyberChief (to binary, replace(" ", ""))]`

You can use script [picture-script.py](files/picture-script.py) - example use `Python3 picture-script.py file.txt -d`. You can also use the `-8` flag to convert data from decimal to binary.

5. Next, there is a string of characters in the binary format, which needs to be reconstructed as a graphic file where 0 represents white color, 1 represents black color. Additionally, we should rotate the obtained image to make the flag information clear to us.

6. The flag is located in the image
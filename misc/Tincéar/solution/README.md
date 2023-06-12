# Tincéar by Ernikus
## Walkthrough

1. Without major problems or complications, we unpack the .ZIP file - inside is a .GIF file.
2. The Exiftool tool provides interesting information:
"Comment: 1st Code: go to pastebin.com/ , it starts with 'J'; [more hidden] 2nd Code: go to youtube.com/watch?v= , 11 characters starting with 'F'"

The information obtained from this file should later be used on Pastebin and YouTube ("yt" in short). To establish the order - GIF and the code start with "J".

3. Analyzing the .GIF file - it has 8 rapidly changing image frames, each containing some information that needs to be decoded. Using various programs like Adobe Photoshop, export individual frame images as .PNG files (be careful with the order!).

### CODE 1: Frame Analysis:

- Frames 1 and 6 - these frames have data encoded with similar symbols, and additional information is also present - 322 and 2011. This refers to a date - 322 in 2011 (a non-leap year) corresponds to November 18th.

Link to date algorithm: https://www.dcode.fr/nth-day-year

What happened on November 18th, 2011?

Link to calendar page: https://bestofdate.com/2011-11-18

On that day, the game Minecraft was released, and it is related to this cipher.

The Standard Galactic Alphabet (officially known as this cipher) is an invented alphabet used in several video game universes, starting with Commander Keen, Quake 4, or Minecraft (where it is usually referred to as the "alphabet of enchantment" because it appears with the enchantment table).

Link to the cipher: https://www.dcode.fr/standard-galactic-alphabet"

    Frame 1 - 'J'
    Frame 6 - 'K'

- Frames 2, 4, and 7 - these frames have data encoded with similar symbols, using a different cipher, and the information is written in hexadecimal:
"46 55 53 20 52 4F 20 44 41 48 21" which translates to "FUS RO DAH!".

"FUS RO DAH!" is an old meme widely known from numerous popular compilations on YouTube and originates from the game "The Elder Scrolls V: Skyrim".

Link to the meme's history: https://knowyourmeme.com/memes/fus-ro-dah

In this game, there are several different ciphers, but in this case, we are interested in the "Dragon Language". It is a simple cipher, and the data can be easily deciphered.

Link to the Dragon Language cipher: https://elderscrolls.fandom.com/wiki/Dragon_Alphabet , https://www.dcode.fr/dovahzul-dragon-language

The symbol in Frame 7 is reversed.

    Frame 2 - 'R'
    Frame 4 - 'N'
    Frame 7 - 'F'

- Frame 3 - The background is not relevant here, and the number of digits doesn't matter.

`Frame 3 - '5'`

- Frame 5 - The lowercase letter 'z' is associated with a font and is meant to mislead, it doesn't have any significance.

`Frame 5 - 'Y'`
   
- Frame 8 - The background is not relevant here, and the number of characters doesn't matter. The inverted triangle (as an arrow) indicates that the letter should be lowercase.

`Frame 8 - 'z'`


Finally, code 1 is as follows:

    Frame 1 - 'J'
    Frame 2 - 'R'
    Frame 3 - '5'
    Frame 4 - 'N'
    Frame 5 - 'Y'
    Frame 6 - 'K'
    Frame 7 - 'F'
    Frame 8 - 'z'
        
    JR5NYKFz

We associate this information with the link to the note on Pastebin (https://pastebin.com/JR5NYKFz). The information is password-protected - code 2.

4. Barcode
### CODE 2: Barcode

As you may have noticed, in addition to the encrypted characters and distracting backgrounds on the image frames, fragments of a barcode were visible in the background. There are 4 fragments that need to be properly cut out and arranged in the correct order (frames 1 and 5 have the same barcode fragment, the same goes for 2 and 6, and so on). As for the order, there is no major complication - from 1 to 4.

We can cut out a thin fragment and later stretch it vertically (we won't lose any information).

The option of a black color layer with the "divide" option in Adobe Photoshop can be useful - it removes unevenness from our sample.

There is an image in the `healthcheck` folder in the file showing what needed to be done.

Then, the prepared barcode needs to be scanned.

Link to a barcode reader website: https://online-barcode-reader.inliteresearch.com

The barcode reveals the information: `FUy87tpfNe4`

This is the ID of a YouTube video: https://www.youtube.com/watch?v=FUy87tpfNe4

The link leads us to the video - "Icarus - Main Theme."

Specifically, it is the password for the Pastebin file: `Icarus`.

5. Pastebin - The first line contains a fake flag. The subsequent information and the YouTube link are unrelated to the solution; they are a distraction.

If there are white characters in a line but no other 'visible' characters, Pastebin in its default view displays only the newline character. To see the white characters, you need to view the 'RAW Data' - at the very bottom of the note.

The real flag is located between the phrases "that's all" and "for real" and is encrypted in whitespace characters.

Link to the whitespace decipher: https://www.dcode.fr/whitespace-language"

You get the right flag! :)

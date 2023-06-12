import argparse
from PIL import Image

def convert(filepath, combine_8):
    """
    Converts greyscale image pixels to binary numbers and saves the result to a text file.
    :param filepath: The path to the image file.
    :param combine_8: Combine every 8 bits into a single number from range 0-255.
    """

    # Open the image file
    image = Image.open(filepath).convert("L")

    # Get the image pixels as a 2D array
    pixels = image.load()

    # Create a new text file with the same name as the image file
    filename = filepath.split("/")[-1].split(".")[0]

    
    if combine_8:
        with open(filename + ".txt", "w") as f:
            # Iterate through the pixels and write the binary value to the text file
            for j in range(image.height):
                bit_line = ""
                for i in range(image.width):
                    if pixels[i, j] > 127:
                        bit_line += "0"
                    else:
                        bit_line += "1"
                    if (i+1) % 8 == 0:
                        decimal_value = int(bit_line, 2)
                        f.write(str(decimal_value) + " ")
                        bit_line = ""
                if bit_line:
                    decimal_value = int(bit_line.ljust(8, "0"), 2)
                    f.write(str(decimal_value) + " ")
                f.write("\n")
    else:
        with open(filename + ".txt", "w") as f:
            # Iterate through the pixels and write the binary value to the text file
            for j in range(image.height):
                for i in range(image.width):
                    if pixels[i, j] > 127:
                        f.write("0")
                    else:
                        f.write("1")
                f.write("\n")

    print("Image successfully converted to data and saved to text file.")

def reverse(filepath, combine_8):
    """
    Converts binary numbers to greyscale pixels and saves the result as an image.
    :param filepath: The path to the text file.
    :param combine_8: Combine every 8 bits into a single number from range 0-255.
    """
    # Open the text file
    filename = filepath.split("/")[-1].split(".")[0]
    with open(filepath, "r") as f:
        # Read the binary values from the text file
        data = f.read().split()
    
    if(combine_8):
        # Convert decimal numbers to binary and join them with spaces
        binary_data = []
        binary_str = ""
        
        for i, dec_str in enumerate(data):
            # Convert the decimal number to binary and add leading zeroes if necessary
            binary_str += format(int(dec_str), "08b")
            
            if (i+1) % 16 == 0:
                # Add a newline character every 16th binary number
                binary_data.append(binary_str)
                binary_str = ""
        
        # Add the last binary number
        if binary_str != "":
            binary_data.append(binary_str)
        
        data = binary_data
    
    # Remove the last empty string if there is one
    if data[-1] == "":
        data.pop()
    
    # print(data)
    
    # Create a new image with the same size as the original
    height = len(data)
    width = len(data[0])
    
    # if combine_8:
    #     width = width * 8
    #     height = height // 8
    
    image = Image.new("L", (width, height))
    
    # Get the image pixels as a 2D array
    pixels = image.load()
    
    # Iterate through the binary values and set the corresponding pixel value
    for j in range(height):
        for i in range(width):
            value = int(data[j][i])
                
            if value == 1:
                pixels[i, j] = 0
            else:
                pixels[i, j] = 255
    
    # Save the image with the same name as the text file
    image.save(filename + ".png")
    print("Data successfully converted to image and saved to png file.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert and reverse image to binary numbers.")
    parser.add_argument("-f", "--filepath", help="The path to the image or text file.", required=True)
    parser.add_argument("-d", "--reverse", help="To reverse binary numbers to image.", action="store_true")
    parser.add_argument("-8", "--combine_8", help="Combine every 8 bits into a single number from range 0-255.", action="store_true")
    args = parser.parse_args()

    if args.filepath:
        if args.reverse:
            reverse(args.filepath, args.combine_8)
        else:
            convert(args.filepath, args.combine_8)
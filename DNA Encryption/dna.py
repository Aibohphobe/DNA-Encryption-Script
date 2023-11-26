import os

# Function to convert plaintext string into ASCII binary string
def toBinary(input, input_type="plaintext"):
    binaryList = []
    if input_type == "plaintext":
        for char in input:
            binaryList.append(bin(ord(char))[2:].zfill(8))
    elif input_type =="nucleotides":
        nucleotide_mapping = {'A': '00','C': '01','G': '10','T': '11'}
        for char in input:
            binaryList.append(nucleotide_mapping[char])
    else:
        print("Missing or incorrect input type")
    return ''.join(binaryList)

# Function to convert ASCII binary string into plaintext string
def toPlaintext(binary):
    binaryInt = int(binary, 2)
    byte_number = binaryInt.bit_length() + 7 // 8
    binary_array = binaryInt.to_bytes(byte_number, "big")
    non_null_start = next(i for i, byte in enumerate(binary_array) if byte != 0)
    return binary_array[non_null_start:].decode().strip()

# Function to convert binary into nucleotides
def toNucleotides(binary):
    nucleotide_mapping = {'00': 'A','01': 'C','10': 'G','11': 'T'}
    nucleotides = [nucleotide_mapping[binary[i:i+2]] for i in range (0, len(binary), 2)]
    return ''.join(nucleotides)

# Function to encrypt a binary string with a key using XOR
def encrypt(binary, key, keyType):
    if keyType == "nucleotides":
        key = toBinary(key, input_type = "nucleotides")
    binaryKey = toBinary(key, input_type="plaintext")
    repeatedKey = (binaryKey * ((len(binary) // len(binaryKey)) + 1))[:len(binary)]
    return ''.join('1' if bit1 != bit2 else '0' for bit1, bit2 in zip(binary, repeatedKey))

# Function to decrypt an encrypted binary string with a key using XOR
def decrypt(binary, key, keyType):
    if keyType == "nucleotides":
        key = toBinary(key, input_type = "nucleotides")
    binaryKey = toBinary(key, input_type="plaintext")
    repeatedKey = (binaryKey * ((len(binary) // len(binaryKey)) + 1))[:len(binary)]
    return ''.join('1' if bit1 != bit2 else '0' for bit1, bit2 in zip(binary, repeatedKey))

# Function to acquire an encryption or decryption key based on the provided mode
def getKey(mode):
    response = None
    keyType = None
    while response not in {"A", "a", "B", "b"}:
        response = input("\nA. Plaintext\nB. Nucleotides\nSelect a key type by inputting the associated letter: ")
    if response == "A" or response == "a":
        nextResponse = None
        while nextResponse not in {"M", "m", "F", "f"}:
            nextResponse = input("Do you want to input a key manually (M) or read from a file (F)?: ")
            if nextResponse == "M" or nextResponse == "m":
                if mode == "encryption":
                    key = input("Enter a plaintext key for encryption: ")
                else:
                    key = input("Enter a plaintext key for decryption: ")
            else:
                while True:
                    filename = input("Enter the filename with the plaintext key to be utilized: ")
                    key = readFile(filename)
                    if key is None:
                        print("There is no text in this file or the file could not be found.")
                    else:
                        break
        keyType = "plaintext"
    else:
        nextResponse = None
        while nextResponse not in {"M", "m", "F", "f"}:
            nextResponse = input("Do you want to input a key manually (M) or read from a file (F)?: ")
            if nextResponse == "M" or nextResponse == "m":
                if mode == "encryption":
                    key = input("Enter a nucleotide key for encryption: ")
                else:
                    key = input("Enter a nucleotide key for decryption: ")
            else:
                while True:
                    filename = input("Enter the filename with the nucleotide key to be utilized: ")
                    key = readFile(filename)
                    if key is None:
                        print("There is no text in this file or the file could not be found.")
                    else:
                        break
        keyType = "nucleotides"
    return key, keyType

# Function to determine the input mode and fetch the plaintext message to be encrypted
def getInputMode():
    response = None
    while response not in {"M", "m", "F", "f"}:
        response = input("Do you want to input text manually (M) or read from a file (F)?: ")
        if response == "M" or response == "m":
            plaintextMessage = input("Enter a message to be encrypted: ")
        else:
            while True:
                filename = input("Enter the filename with the text to be encrypted: ")
                plaintextMessage = readFile(filename)
                if plaintextMessage is None:
                    print("There is no text in this file or the file could not be found.")
                else:
                    break
    return plaintextMessage

# Function to determine whether the user wants the decrypted output redirected to a file or simply in-line
def getOutputMode(content):
    response = None
    while response not in {"Y", "y", "N", "n"}:
        response = input("Do you want to save the decrypted output to a file instead of viewing it in-line? (Y/N): ")
        if response == "Y" or response == "y":
            outputFilename = input("Enter the filename to save the decrypted output: ")
            writeFile(outputFilename, content)
        else:
            print("The result of this decryption was: " + content)

# Function to read a file and return its content
def readFile(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    
# Function to write content to a file with a specified name
def writeFile(filename, content):
    with open(filename, 'w') as file:
        file.write(content)
    
# Function to trigger user inputs and relative display outputs
def main():
    print("========== ENCRYPTION PROCESS ==========")
    plaintextMessage = getInputMode()
    print("A key is needed for the encryption process")
    key, keyType = getKey("encryption")
    binaryMessage = toBinary(plaintextMessage, "plaintext")
    encryptedBinary = encrypt(binaryMessage, key, keyType)
    print("The result of this encryption is: " + encryptedBinary)
    nucleotides = toNucleotides(encryptedBinary)
    print("The encrypted binary in nucleotide encoding is: " + nucleotides)
    stop = input("Press Enter to continue")
    print("========== DECRYPTION PROCESS ==========")
    print("A key is needed for the decryption process")
    keyRequest, keyRequestType = getKey("decryption")
    backToBinary = toBinary(nucleotides, "nucleotides")
    decryptedBinary = decrypt(backToBinary, keyRequest, keyRequestType)
    backToPlaintext = toPlaintext(decryptedBinary)
    getOutputMode(backToPlaintext)
    stop = input("Press Enter to restart")
    os.system('cls' if os.name == 'nt' else 'clear')
    main()
main()

S_BOXES = {
    1: [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    2: [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    3: [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    4: [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    5: [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    6: [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    7: [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    8: [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
}

def get_sbox_output(xored_bits, j):
    """
    Calculate Sj(Bj) for a given j and 48-bit input

    Args:
    xored_bits (str): 48-bit string (Ki + E(Ri-1))
    j (int): S-box number (1-8)

    Returns:
    str: 4-bit output from the specified S-box
    """
    start_pos = (j - 1) * 6
    bj = xored_bits[start_pos:start_pos + 6]

    row = int(bj[0] + bj[5], 2)

    col = int(bj[1:5], 2)

    value = S_BOXES[j][row][col]

    result = format(value, '04b')

    print(f"\nCalculation steps for S{j}(B{j}):")
    print(f"Input 6 bits (B{j}): {bj}")
    print(f"Row bits: {bj[0]}{bj[5]} = {row}")
    print(f"Column bits: {bj[1:5]} = {col}")
    print(f"S-box output: {value} (decimal) = {result} (binary)")

    return result

def main():
    choice = input("Enter 1 for manual input, 2 for random generation: ")

    if choice == '1':
        xored_bits = input("Enter 48-bit string (Ki + E(Ri-1)): ")
        while len(xored_bits) != 48 or not all(bit in '01' for bit in xored_bits):
            print("Invalid input! Please enter exactly 48 bits (0s and 1s)")
            xored_bits = input("Enter 48-bit string: ")
    else:
        from random import choice
        xored_bits = ''.join(choice('01') for _ in range(48))
        print(f"Randomly generated 48-bit string: {xored_bits}")


    j = int(input("Enter S-box number (1-8): "))
    while j not in range(1, 9):
        print("Invalid S-box number! Please enter a number between 1 and 8")
        j = int(input("Enter S-box number (1-8): "))

    result = get_sbox_output(xored_bits, j)
    print(f"\nFinal result Sj(Bj): {result}")

if __name__ == "__main__":
    main()


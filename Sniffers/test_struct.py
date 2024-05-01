import struct

# Example binary data
binary_data = b'\x01\x02\x03\x04'

# Unpack the binary data into a tuple of integers
unpacked_data = struct.unpack('<BBBB', binary_data)

print(unpacked_data)  # Output: (1, 2, 3, 4)

# Ascii chars ordered by darkness
ascii_chars = '''$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|(1{[?-_+~<i!lI;:,"^`'. '''
length = -1 #len(ascii_chars)
ascii_arr = {}
# makes key:value pairs of darkness:character
for char in ascii_chars:
    length += 1
    ascii_arr[length]= char

ascii_arr

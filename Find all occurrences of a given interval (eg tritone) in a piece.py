# Find all occurrences of a given interval (eg tritone) in a piece
# Version 1.1
from music21 import *
# Choosing a piece / file type:
Piece = input("Score mxl or https: ")  # asks for the mxl file name or https: of the piece
# eg. bach/bwv99.6.mxl
# eg. https://kern.humdrum.org/cgi-bin/ksdata?l=osu/classical/bach/wtc-1&file=wtc1f01.krn&f=kern
# Alternatively, can input the name inline:
# Piece = "https://kern.humdrum.org/cgi-bin/ksdata?l=osu/classical/bach/wtc-1&file=wtc1f01.krn&f=kern"
# Piece = "bach/bwv99.6.mxl"

# Parsing the file:
# corpus files are included in music21, use the corpus.parse method
# use converter.parse method for https files (eg humdrum)

type_of_file = input("Is the file an in-built corpus (Y/N)?: ")
if type_of_file == "Y":
    s_original_key = corpus.parse(Piece) # s short for score
else:
    s_original_key = converter.parse(Piece)

# Find the original key signature and transpose if necessary
print("The piece is written in: %s" % s_original_key.analyze("key"))
sKey = input("Transpose to the key of: ") # eg C, D, A, B-, F#, d, e, f#, e minor (the "minor" at the end is optional)
number = input("How many semitones to transpose?: ") # eg if piece in A, then 3 or -9 will transpose to C an octave apart
s = s_original_key.transpose(int(number)) # note the conversion of a string to integer

sChords = s.chordify().recurse().getElementsByClass('Chord')
# List_sChords = list(sChords) # this converts the tuple to a list
displayPart = stream.Part(id='displayPart')

for i in range(len(sChords) - 1):
    if sChords[i].intervalVector[5] > 0: # if the number of 3Ts is not zero (ie the chord has a 3T)
        # interval vector = [m2/M7, M2/m7, m3/M6, M3/m6, P4/P5, 3T]; counts the number of occurrences eg [0,1,1,1,1,1]
        m = stream.Measure()
        m.append(sChords[i])
        m.append(sChords[i + 1])
        displayPart.append(m)

for c in displayPart.recurse().getElementsByClass('Chord'):
    rn = roman.romanNumeralFromChord(c, key.Key(sKey))
    c.addLyric(str(rn.figure))

## Optional title
# My_title = input("Title: ")
# metadata.Metadata.title = My_title

displayPart.show()
print("Number of matched chords: %s" % len(displayPart))
sChords.show()

#to change the lyrics to a nice rn font in MS, R click a rn, select all similar, "roman numeral analysis" style



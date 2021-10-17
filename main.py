import argparse, functools, operator, sys, string

#todo: support digraph analysis to improve algorithm confidence
#todo: add confidence score

#issues: confidence of frequency analysis can only be at best a function of the least
# of 

#hardcoded freq table done on the entire contents of the gutenberg-cd
DEFAULT_1_TABLE = {'p': 5716535, 'r': 19134462, 'o': 24352736,
     'j': 498307, 'e': 40404280, 'c': 8321846,
     't': 29321965, 'g': 6055786, 'u': 9079903,
     'n': 22148368, 'b': 4854054, 's': 20347424,
     'x': 595046, 'f': 7550824, 'h': 20050337,
     'a': 25649333, 'k': 2122323, 'i': 22183451,
     'l': 12609050, 'y': 5906023, 'd': 13684829,
     'm': 8254323, 'w': 6796171, 'v': 3191823,
     'z': 249785, 'q': 411784}

LETTERS = "abcdefghijklmnopqrstuvwxyz"
BANNED = (" ","") #letters not worth analysing

class WordChecker:
    """Class that accepts text and a wordlist to go along with it;
    can be used to check the percentage of a text that are words in
    that language.
    Params:
    wordlist_path: path to the wordlist
    """
    def __init__(self, wordlist_path):
        self.allowedwords = []
        with open(wordlist_path) as f:
            self.allowedwords = [line.strip("\n").lower() for line in f]
    
    def test_words(self, words):
        #produces % of words that are found in provided wordlist
        word_arr = words.lower().split()
        in_list_count = functools.reduce(operator.add,
                    [1 if word in self.allowedwords else 0
                    for word in word_arr],0)
        print([1 if word in self.allowedwords else 0
                    for word in word_arr])
        print(in_list_count)
        return in_list_count / len(word_arr)



class CorrespondenceTable:
    """
    Dict that provides a probabilities between
    ciphertext letters/digrams etc and plaintext letters. It is represented as
    a dict of dicts each dict containing a probability for letters.
    We can remove letters in the sub-dict with p < 0.01. To perform
    probability calculations, we treat the letters as random variables
    distributed in the same fashion as the letters in the corpus-
    generated table. (TODO this later; for now we shall simply treat them
    as normal variables with regard to their probability of being letters
    that are distant in frequency.)
    params:
    letters_permitted - string literal of letters that can be enciphered.
    defaults to english alphabet in lowercase. all other characters that
    when converted to lowercase (if that flag is on) are not part of the
    string will not be considered in frequency analyses and will remain
    unchanged between cipher and plaintext
    convert_lower - default true; if false upper and lowercase letters
    are analysed as distinct letters
    """
    def init(self,letters_permitted=LETTERS):
        self.letters_permitted = letters_permitted
        self.probabilities = {} #TODO add the dict-comp in a dict comp


def frequency_analysis(input_text,chunk_size=1,offset=1):
    #todo: perhaps give error if len(input_text) % offset is not 0
    # as this feature is only used when multiple letters represent a
    # letter. to find digrams one should keep the offset to one as to
    # find all possibilities
    # other potential feature: reject a letter if any banned letter appears
    # in it. it might not be useful in the case where the ciphertext has
    #spaces removed
    def nextchar(analysis, next_char):
        next_char = next_char.lower()
        if next_char not in BANNED:
            if next_char not in analysis:
                analysis[next_char] = 1
            else:
                analysis[next_char] += 1
        return analysis
    def createarray():
        nonlocal chunk_size
        nonlocal offset
        nonlocal input_text
        return [{}, *[chunk 
            if len(chunk:="".join(input_text[i:(i+chunk_size)])) == chunk_size
            else ""
            for i in range(0,len(input_text)-(chunk_size-1),offset)
            ]]
    x =  functools.reduce(nextchar,createarray())
    print(x)
    return functools.reduce(nextchar,createarray())


#todo: allow rolling one's own freq table with help of the analysis above
def frequency_table():
    return DEFAULT_1_TABLE

def decrypt(ciphertext, freq_table):
    enc_freqs = frequency_analysis(ciphertext)
    enc_freqs_sorted = sorted(enc_freqs.items(), key=operator.itemgetter(1))
    enc_freqs_sorted_list = list(enc_freqs_sorted)
    print(enc_freqs_sorted_list)
    freq_table_sorted = sorted(freq_table.items(), key=operator.itemgetter(1))
    #match up the frequencies to get a correspondence table
    correspondence = dict(zip([i[0] for i in enc_freqs_sorted],
                         [i[0] for i in freq_table_sorted]))
    return "".join([correspondence[letter]
            if letter not in BANNED else letter
            for letter in ciphertext])

def main(args):
    # take arg1 as the file to decrypt
    # todo arg2 as output file, arg3 as corpus to analyse
    parser = argparse.ArgumentParser(
            description="Decrypts a substitution-cipher encrypted text.")
    
    filetext = ""
    with open(args[1],'r') as f:
        filetext = f.read()
    #print(frequency_analysis(filetext,1,1))
    #print(frequency_analysis("suppers",3,1))
    print(decrypt(filetext, frequency_table()))


main(sys.argv)





import codecs
from collections import defaultdict
import sys

class Suggestor(object):
    def __init__(self):
        print("Initializing suggestor...")

        self.index = {}
        self.word = {}
        self.unigram_count = {}
        self.bigram_prob = defaultdict(dict)
        self.unique_words = 0
        self.total_words = 0
        self.bigram_pointers = [0, 1, 2]
        self.sorted_bigram = []
        if not self.read_model('guardian_model.txt'):
            print("lyckades ej läsa in modellen")
            sys.exit()

        self.sort_unigram()
        print("Suggestor initialized")

        
    def read_model(self, filename):
        try:
            with codecs.open(filename, 'r', 'utf-8') as f:
                self.unique_words, self.total_words = map(int, f.readline().strip().split(' '))

                # Read unigrams
                for _ in range(self.unique_words):
                    read_index, read_word, read_unicode_counter = f.readline().strip().split(' ')
                    self.index[read_word] = read_index
                    self.word[read_index] = read_word
                    self.unigram_count[read_word] = read_unicode_counter

                # Read bigrams
                while True:
                    line_list = f.readline().strip().split(' ')
                    if line_list[0] == "-1":
                        break
                    
                    index1, index2, log_probability = line_list[0], line_list[1], line_list[2]
                    if float(log_probability) != 0:
                        self.bigram_prob[index1][index2] = log_probability
    
                return True
        except IOError:
            print(f"Couldn't find bigram probabilities file {filename}")
            return False

    def sort_unigram(self):
        self.sorted_unigram = sorted(self.index.keys(), key=lambda x: int(self.unigram_count[x]), reverse=True)

    def sort_bigram(self, prev_index):
        prev_index = str(prev_index)
        if prev_index in self.bigram_prob:
            # Get items and sort based on probability, but only store indices
            items = self.bigram_prob[prev_index].items()
            self.sorted_bigram = [next_index for next_index, _ in sorted(items, key=lambda x: float(x[1]), reverse=True)]
            self.bigram_pointers = [0, 1, 2]  # Reset pointers after new sort
        else:
            self.sorted_bigram = []
            self.bigram_pointers = []


    def findUnigramPointers(self, currentWord):
        if not currentWord:
            self.unigram_pointers = [0, 1, 2][:len(self.sorted_unigram)]
            return
        
        new_pointers = []
        max_pointer = len(self.sorted_unigram) - 1
        search_start = 0
        
        for i in range(3):
            if i >= len(self.unigram_pointers):
                break
                    
            current_pointer = self.unigram_pointers[i]
            if current_pointer > max_pointer:
                continue
                    
            # Check if current pointer's word is still valid
            current_word = self.sorted_unigram[current_pointer]
            
            if current_word.startswith(currentWord):
                new_pointers.append(current_pointer)
                search_start = current_pointer + 1
                continue
            
            # Check remaining existing pointers
            found = False
            for next_p in self.unigram_pointers[i+1:]:
                if next_p > max_pointer:
                    continue
                next_word = self.sorted_unigram[next_p]
                if next_word.startswith(currentWord):
                    new_pointers.append(next_p)
                    search_start = next_p + 1
                    found = True
                    break
                        
            # Search forward if needed
            if not found:
                for j in range(search_start, len(self.sorted_unigram)):
                    next_word = self.sorted_unigram[j]
                    if next_word.startswith(currentWord):
                        new_pointers.append(j)
                        search_start = j + 1
                        break
                            
        self.unigram_pointers = new_pointers

    def findBigramPointers(self, currentWord):
        if not currentWord:
            self.bigram_pointers = [0, 1, 2][:len(self.sorted_bigram)]
            return
        
        new_pointers = []
        max_pointer = len(self.sorted_bigram) - 1
        search_start = 0
        
        for i in range(3):
            if i >= len(self.bigram_pointers):
                break
                
            current_pointer = self.bigram_pointers[i]
            if current_pointer > max_pointer:
                raise KeyError
                
            # Check if current pointer's word is still valid
            current_index = self.sorted_bigram[current_pointer]
            current_word = self.word[current_index]
            
            if current_word.startswith(currentWord):
                new_pointers.append(current_pointer)
                search_start = current_pointer + 1
                continue
            
            # Check remaining existing pointers
            found = False
            for next_p in self.bigram_pointers[i+1:]:
                if next_p > max_pointer:
                    continue
                next_index = self.sorted_bigram[next_p]
                next_word = self.word[next_index]
                if next_word.startswith(currentWord):
                    new_pointers.append(next_p)
                    search_start = next_p + 1
                    found = True
                    break
                    
            # Search forward if needed
            if not found:
                for j in range(search_start, len(self.sorted_bigram)):
                    next_index = self.sorted_bigram[j]
                    next_word = self.word[next_index]
                    if next_word.startswith(currentWord):
                        new_pointers.append(j)
                        search_start = j + 1
                        break
                        
        self.bigram_pointers = new_pointers
        
    def nextWord(self, prevWord, currentWord=""):
        seen_words = set()
        suggestions = []

        try:
            # Try bigram first
            if currentWord == "":
                self.sort_bigram(self.index[prevWord])
            self.findBigramPointers(currentWord)
            
            pointer_idx = 0
            while len(suggestions) < 3 and pointer_idx < len(self.bigram_pointers):
                pointer = self.bigram_pointers[pointer_idx]
                if pointer >= len(self.sorted_bigram):
                    pointer_idx += 1
                    continue
                    
                word_index = self.sorted_bigram[pointer]
                word = self.word[word_index]
                
                if word not in seen_words and word != "<s>":
                    if prevWord == "<s>":
                        suggestions.append(word.capitalize())
                    else:
                        suggestions.append(word)
                    seen_words.add(word)
                
                pointer_idx += 1
                
            if len(suggestions) == 3:
                return suggestions
            print(suggestions)
        except KeyError:
            pass  # Continue to unigram fallback
            
        # Unigram fallback
        print("\nFalling back to unigram:\n")
        self.unigram_pointers = [0, 1, 2]  # Reset pointers
        self.findUnigramPointers(currentWord)
        
        pointer_idx = 0
        while len(suggestions) < 3 and pointer_idx < len(self.unigram_pointers):
            pointer = self.unigram_pointers[pointer_idx]
            if pointer >= len(self.sorted_unigram):
                pointer_idx += 1
                continue
                
            word = self.sorted_unigram[pointer]
            
            if word != "<s>" and word not in seen_words:
                suggestions.append(word)
                seen_words.add(word)
            
            pointer_idx += 1
        
        return suggestions if suggestions else [currentWord, "", ""]
    
    def trainSuggestor(self):
        if not self.read_model('guardian_model.txt'):
            return 


def main():
    suggestor = Suggestor()
    if not suggestor.read_model('guardian_model.txt'):
        return

    try:
        prev_word = "<s>"
        start_index = suggestor.index[prev_word]
        suggestor.sort_bigram(start_index)
        current_word = ""
        
        while True:
            print(f"\nCurrent word: {current_word}")
            suggestions = suggestor.nextWord(prev_word, current_word)
            print("Suggestions:", " ".join(suggestions))
            
            char = input("Enter character (space=new word, q=quit): ")
            if char == 'q':
                break
            elif char == ' ':
                prev_word = current_word if current_word else prev_word
                current_word = ""
                try:
                    suggestor.sort_bigram(suggestor.index[prev_word])
                except KeyError:
                    print(f"Warning: '{prev_word}' not found in model")
                    suggestor.sorted_bigram = []
            else:
                current_word += char

    except KeyError as e:
        print(f"Error: {e}")
        return

if __name__ == "__main__":
    main()
from __future__ import unicode_literals
import codecs
import os

from Suggestor import Suggestor
from ModelBuilder import ModelBuilder
from Interface import SuggestionApp


def buildModel():
    output_file = 'guardian_model.txt'
    
    print("\n\n")
    # Only build model if file doesn't exist
    if not os.path.exists(output_file):
        print("Model doesn't exist")
        print(f"Building model: {output_file}")

        model_builder = ModelBuilder()
        model_builder.process_files('data/guardian_training.txt')
        stats = model_builder.stats()

        with codecs.open(output_file, 'w', 'utf-8' ) as f:
            for row in stats: f.write(row + '\n')
        
        print(f"Model built, stored in: {output_file}")
    else:
        print(f"Model {output_file} already exists")

def main():
    buildModel()

    suggestor = Suggestor()
    SuggestionApp(suggestor)

if __name__ == "__main__":
    main()
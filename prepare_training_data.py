import spacy
import os
from pymongo import MongoClient

def main():
    nlp = spacy.load("en", disable=['tagger', 'ner'])
    client = MongoClient()
    papers = client.predsynth.papers.find(no_cursor_timeout=True)
    
    for i, paper in enumerate(papers):
        doi = paper["doi"]
        safe_doi = ''.join(c for c in doi if c not in ["/", ".", "(", ")"])
        filename = f"training_data/{safe_doi}.txt"

        if os.path.isfile(filename):
            continue

        full_text = "\n".join([p["text"] for p in paper["paragraphs"]])

        with open(filename, "w") as f:
            for sent in nlp(full_text[:500000]).sents:
                f.write(f"{' '.join([t.text for t in sent])}\n")

if __name__ == "__main__":
    main()
        

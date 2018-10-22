import spacy
from pymongo import MongoClient

def main():
    nlp = spacy.load("en")
    client = MongoClient()
    papers = client.predsynth.papers.aggregate([{ "$sample": { "size": 100000 } }])
    
    for i, paper in enumerate(papers):
        full_text = "\n".join([p["text"] for p in paper["paragraphs"]])
        with open(f"training_data/{i}.txt", "w") as f:
            for sent in nlp(full_text[:500000]).sents:
                f.write(f"{' '.join([t.text for t in sent])}\n")

if __name__ == "__main__":
    main()
        

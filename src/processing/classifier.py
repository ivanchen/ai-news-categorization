from transformers import pipeline

class Classifier:
    def __init__(self):
        self.model = pipeline("zero-shot-classification", 
                            model="facebook/bart-large-mnli")
        self.categories = [
            "politics", "business", "technology", "entertainment",
            "sports", "health", "science", "education"
        ]
        
    def classify(self, text):
        """Perform classification on input text"""
        result = self.model(
            text,
            candidate_labels=self.categories,
            hypothesis_template="This text is about {}."
        )
        return {
            "labels": result["labels"],
            "scores": result["scores"]
        }

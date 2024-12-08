class CategorySelector:
    def select(self, classifications):
        """Select best category based on classification scores"""
        labels = classifications["labels"]
        scores = classifications["scores"]
        
        # Get the highest scoring category
        best_index = scores.index(max(scores))
        return {
            "category": labels[best_index],
            "confidence": scores[best_index]
        }

    def validate_confidence(self, score):
        """Validate confidence scores"""
        return score >= 0.5  # Minimum 50% confidence threshold

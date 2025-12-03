"""
Emotion analyzer using AI model with keyword fallback.
Analyzes text and returns one of 11 emotion types.
"""
import sys
from typing import Optional


class EmotionAnalyzer:
    """Analyzes text to determine emotional sentiment."""

    VALID_EMOTIONS = {
        "curious", "happy", "excited", "thoughtful", "concerned",
        "confused", "confident", "helpful", "analyzing", "creative", "neutral",
        "focused", "sad", "grumpy", "determined", "relaxed", "surprised"
    }

    def __init__(self, use_model: bool = True):
        """
        Initialize the emotion analyzer.

        Args:
            use_model: If True, attempt to load AI model. If False or loading fails,
                      use keyword-based analysis only.
        """
        self.model = None
        self.tokenizer = None
        self.use_model = use_model

        if use_model:
            try:
                print("Loading emotion classification model...", file=sys.stderr)
                from transformers import pipeline
                self.model = pipeline(
                    "text-classification",
                    model="j-hartmann/emotion-english-distilroberta-base",
                    top_k=1
                )
                print("✓ Model loaded successfully", file=sys.stderr)
            except Exception as e:
                print(f"✗ Failed to load model: {e}", file=sys.stderr)
                print("  Falling back to keyword-based analysis", file=sys.stderr)
                self.model = None

    def analyze(self, text: str) -> str:
        """
        Analyze text and return the detected emotion.

        Args:
            text: Text to analyze

        Returns:
            One of the 11 valid emotion names
        """
        if not text or not text.strip():
            return "neutral"

        text_lower = text.lower()

        # Priority 1: Context-based rules (ported from EmotionAgent.cs)
        # These take precedence because they capture intent better than sentiment

        # Curiosity and questions
        if "?" in text or any(word in text_lower for word in ["how", "why", "what", "when", "where"]):
            return "curious"

        # Creation and building
        if any(word in text_lower for word in ["create", "build", "make", "design", "implement"]):
            return "creative"

        # Analysis and research
        if any(word in text_lower for word in ["analyze", "find", "search", "look", "investigate", "explore"]):
            return "analyzing"

        # Focus and concentration
        if any(word in text_lower for word in ["focus", "concentrate", "working on", "debugging", "deep dive"]):
            return "focused"

        # Determination and commitment
        if any(word in text_lower for word in ["must", "will", "determined", "committed", "going to", "let's do"]):
            return "determined"

        # Relaxation and calm
        if any(word in text_lower for word in ["relax", "calm", "easy", "simple", "straightforward", "no problem"]):
            return "relaxed"

        # Help requests
        if any(word in text_lower for word in ["help", "please", "can you", "could you", "would you"]):
            return "helpful"

        # Priority 2: Use AI model if available
        if self.model:
            try:
                emotion = self._analyze_with_model(text)
                if emotion:
                    return emotion
            except Exception as e:
                print(f"✗ Model inference failed: {e}", file=sys.stderr)
                # Fall through to keyword analysis

        # Priority 3: Sentiment-based keyword matching
        return self._analyze_with_keywords(text_lower)

    def _analyze_with_model(self, text: str) -> Optional[str]:
        """
        Analyze text using the AI model.

        Args:
            text: Text to analyze

        Returns:
            Emotion name or None if analysis fails
        """
        if not self.model:
            return None

        # Get prediction from model
        result = self.model(text[:512])[0]  # Limit text length
        model_emotion = result[0]['label'].lower()

        # Map model emotions (6 basic) to our 17 emotions
        emotion_map = {
            "joy": "happy",
            "surprise": "surprised",
            "anger": "grumpy",
            "fear": "concerned",
            "sadness": "sad",
            "disgust": "confused",
            "neutral": "confident",  # Neutral statements often convey confidence
        }

        return emotion_map.get(model_emotion, "neutral")

    def _analyze_with_keywords(self, text_lower: str) -> str:
        """
        Analyze text using keyword matching (fallback method).
        Ported from EmotionAgent.cs lines 29-65.

        Args:
            text_lower: Lowercased text to analyze

        Returns:
            Emotion name
        """
        # Excitement and positivity
        if any(word in text_lower for word in ["awesome", "great", "amazing", "love", "excellent", "wonderful"]):
            return "excited"

        # Problems and concerns
        if any(word in text_lower for word in ["error", "bug", "broken", "issue", "problem", "fail", "crash"]):
            return "concerned"

        # Frustration and annoyance
        if any(word in text_lower for word in ["ugh", "annoying", "frustrated", "irritating", "damn", "argh"]):
            return "grumpy"

        # Sadness and disappointment
        if any(word in text_lower for word in ["sad", "disappointed", "unfortunate", "sorry", "regret", "bad news"]):
            return "sad"

        # Complex or uncertain
        if any(word in text_lower for word in ["maybe", "not sure", "confused", "unclear", "uncertain"]):
            return "thoughtful"

        # Happiness
        if any(word in text_lower for word in ["happy", "glad", "thanks", "thank you", "good"]):
            return "happy"

        # Default to confident
        return "confident"


if __name__ == "__main__":
    # Test the analyzer
    print("Testing Emotion Analyzer", file=sys.stderr)
    print("=" * 50, file=sys.stderr)

    analyzer = EmotionAnalyzer(use_model=True)

    test_cases = [
        ("How do I fix this bug?", "curious"),
        ("This is amazing!", "excited"),
        ("Error: system crashed", "concerned"),
        ("Create a new feature", "creative"),
        ("Let me analyze the code", "analyzing"),
        ("Can you help me?", "helpful"),
        ("I'm not sure about this", "thoughtful"),
        ("Everything works great!", "excited"),
        ("The API is broken", "concerned"),
        ("", "neutral"),
    ]

    print("", file=sys.stderr)
    correct = 0
    for text, expected in test_cases:
        result = analyzer.analyze(text)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{text[:40]}' → {result} (expected: {expected})", file=sys.stderr)
        if result == expected:
            correct += 1

    print("", file=sys.stderr)
    print(f"Accuracy: {correct}/{len(test_cases)} ({100*correct//len(test_cases)}%)", file=sys.stderr)

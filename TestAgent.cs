using System;

namespace EmotionDisplay
{
    // Example usage / test program
    public class TestAgent
    {
        public static void Main(string[] args)
        {
            Console.WriteLine("Emotion Agent Test");
            Console.WriteLine("==================");
            Console.WriteLine("Make sure the EmotionDisplay app is running first!");
            Console.WriteLine();
            Console.WriteLine("Enter requests to see emotions (or 'quit' to exit):");
            Console.WriteLine();

            while (true)
            {
                Console.Write("> ");
                string? input = Console.ReadLine();

                if (string.IsNullOrEmpty(input) || input.ToLower() == "quit")
                    break;

                // Analyze the request and determine emotion
                string emotion = EmotionAgent.AnalyzeRequest(input);
                Console.WriteLine($"  → Detected emotion: {emotion}");

                // Send to display
                EmotionAgent.SendEmotion(emotion);

                Console.WriteLine();
            }

            Console.WriteLine("Goodbye!");
        }
    }
}

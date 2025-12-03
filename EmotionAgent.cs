using System;
using System.IO;
using System.IO.Pipes;

namespace EmotionDisplay
{
    public class EmotionAgent
    {
        public static void SendEmotion(string emotion)
        {
            try
            {
                using (NamedPipeClientStream pipeClient = new NamedPipeClientStream(".", "EmotionDisplayPipe", PipeDirection.Out))
                {
                    pipeClient.Connect(1000);
                    using (StreamWriter writer = new StreamWriter(pipeClient))
                    {
                        writer.WriteLine(emotion);
                        writer.Flush();
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error sending emotion: {ex.Message}");
            }
        }

        public static string AnalyzeRequest(string request)
        {
            // Simple keyword-based sentiment analysis
            // This is where you'd integrate with an AI API in a real implementation
            request = request.ToLower();

            // Curiosity and questions
            if (request.Contains("?") || request.Contains("how") || request.Contains("why") || request.Contains("what"))
                return "curious";

            // Excitement and positivity
            if (request.Contains("awesome") || request.Contains("great") || request.Contains("amazing") || request.Contains("love"))
                return "excited";

            // Problems and concerns
            if (request.Contains("error") || request.Contains("bug") || request.Contains("broken") || request.Contains("issue"))
                return "concerned";

            // Creation and building
            if (request.Contains("create") || request.Contains("build") || request.Contains("make") || request.Contains("design"))
                return "creative";

            // Analysis and research
            if (request.Contains("analyze") || request.Contains("find") || request.Contains("search") || request.Contains("look"))
                return "analyzing";

            // Help requests
            if (request.Contains("help") || request.Contains("please") || request.Contains("can you"))
                return "helpful";

            // Complex or uncertain
            if (request.Contains("maybe") || request.Contains("not sure") || request.Contains("confused"))
                return "thoughtful";

            // Default
            return "confident";
        }
    }
}

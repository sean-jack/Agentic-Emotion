using System;
using System.IO;
using System.IO.Pipes;
using System.Threading.Tasks;
using System.Windows;

namespace EmotionDisplay
{
    public partial class MainWindow : Window
    {
        private NamedPipeServerStream? _pipeServer;

        public MainWindow()
        {
            InitializeComponent();
            StartPipeServer();
        }

        private async void StartPipeServer()
        {
            while (true)
            {
                try
                {
                    _pipeServer = new NamedPipeServerStream("EmotionDisplayPipe",
                        PipeDirection.In, 1, PipeTransmissionMode.Byte, PipeOptions.Asynchronous);

                    await _pipeServer.WaitForConnectionAsync();

                    using (StreamReader reader = new StreamReader(_pipeServer))
                    {
                        string? emotion = await reader.ReadLineAsync();
                        if (!string.IsNullOrEmpty(emotion))
                        {
                            Dispatcher.Invoke(() => UpdateEmotion(emotion));
                        }
                    }
                }
                catch (Exception)
                {
                    // Log error if needed
                    await Task.Delay(1000);
                }
                finally
                {
                    _pipeServer?.Dispose();
                }
            }
        }

        private void UpdateEmotion(string emotion)
        {
            var (emoji, label) = emotion.ToLower() switch
            {
                "curious" => ("🤔", "Curious"),
                "happy" => ("😊", "Happy"),
                "excited" => ("🤩", "Excited"),
                "thoughtful" => ("💭", "Thoughtful"),
                "concerned" => ("😟", "Concerned"),
                "confused" => ("😕", "Confused"),
                "confident" => ("😎", "Confident"),
                "helpful" => ("🤝", "Helpful"),
                "analyzing" => ("🔍", "Analyzing"),
                "creative" => ("✨", "Creative"),
                _ => ("😐", "Neutral")
            };

            EmotionDisplay.Text = emoji;
            EmotionLabel.Text = label;
        }

        protected override void OnClosed(EventArgs e)
        {
            _pipeServer?.Dispose();
            base.OnClosed(e);
        }
    }
}

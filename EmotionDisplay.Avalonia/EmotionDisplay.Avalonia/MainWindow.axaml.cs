using System;
using System.IO;
using System.IO.Pipes;
using System.Net.Sockets;
using System.Runtime.InteropServices;
using System.Threading.Tasks;
using Avalonia.Controls;
using Avalonia.Threading;

namespace EmotionDisplay.Avalonia;

public partial class MainWindow : Window
{
    private NamedPipeServerStream? _pipeServer;
    private Socket? _unixSocket;
    private const string PipeName = "EmotionDisplayPipe";
    private readonly string _socketPath = $"/tmp/{PipeName}";

    public MainWindow()
    {
        InitializeComponent();
        StartPipeServer();
    }

    private async void StartPipeServer()
    {
        if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
        {
            await StartWindowsPipeServer();
        }
        else
        {
            await StartUnixSocketServer();
        }
    }

    private async Task StartWindowsPipeServer()
    {
        while (true)
        {
            try
            {
                _pipeServer = new NamedPipeServerStream(PipeName,
                    PipeDirection.In, 1, PipeTransmissionMode.Byte, PipeOptions.Asynchronous);

                await _pipeServer.WaitForConnectionAsync();

                using (StreamReader reader = new StreamReader(_pipeServer))
                {
                    string? emotion = await reader.ReadLineAsync();
                    if (!string.IsNullOrEmpty(emotion))
                    {
                        await Dispatcher.UIThread.InvokeAsync(() => UpdateEmotion(emotion));
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

    private async Task StartUnixSocketServer()
    {
        // Remove existing socket file if it exists
        if (File.Exists(_socketPath))
        {
            File.Delete(_socketPath);
        }

        while (true)
        {
            try
            {
                _unixSocket = new Socket(AddressFamily.Unix, SocketType.Stream, ProtocolType.Unspecified);
                var endpoint = new UnixDomainSocketEndPoint(_socketPath);
                _unixSocket.Bind(endpoint);
                _unixSocket.Listen(1);

                // Accept connection
                Socket clientSocket = await _unixSocket.AcceptAsync();

                using (var stream = new NetworkStream(clientSocket, ownsSocket: true))
                using (var reader = new StreamReader(stream))
                {
                    string? emotion = await reader.ReadLineAsync();
                    if (!string.IsNullOrEmpty(emotion))
                    {
                        await Dispatcher.UIThread.InvokeAsync(() => UpdateEmotion(emotion));
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
                _unixSocket?.Dispose();
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
            "focused" => ("🎯", "Focused"),
            "sad" => ("😢", "Sad"),
            "grumpy" => ("😠", "Grumpy"),
            "determined" => ("💪", "Determined"),
            "relaxed" => ("😌", "Relaxed"),
            "surprised" => ("😲", "Surprised"),
            _ => ("😐", "Neutral")
        };

        if (EmotionDisplay != null)
            EmotionDisplay.Text = emoji;

        if (EmotionLabel != null)
            EmotionLabel.Text = label;
    }

    protected override void OnClosed(EventArgs e)
    {
        _pipeServer?.Dispose();
        _unixSocket?.Dispose();

        // Clean up Unix socket file
        if (!RuntimeInformation.IsOSPlatform(OSPlatform.Windows) && File.Exists(_socketPath))
        {
            try
            {
                File.Delete(_socketPath);
            }
            catch
            {
                // Ignore cleanup errors
            }
        }

        base.OnClosed(e);
    }
}
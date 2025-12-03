"""
Cross-platform named pipe client for communicating with the emotion display app.
Works on Windows, macOS, and Linux.
"""
import os
import sys
import platform


def send_emotion(emotion: str) -> bool:
    """
    Send an emotion to the display window via named pipe.

    Args:
        emotion: One of the 11 valid emotions (curious, happy, excited, thoughtful,
                concerned, confused, confident, helpful, analyzing, creative, neutral)

    Returns:
        True if emotion was sent successfully, False otherwise
    """
    pipe_name = os.getenv("EMOTION_PIPE_NAME", "EmotionDisplayPipe")

    # Platform-specific pipe path
    system = platform.system()
    if system == "Windows":
        pipe_path = f"\\\\.\\pipe\\{pipe_name}"
    else:  # macOS and Linux
        # Use /tmp for Unix domain sockets
        pipe_path = f"/tmp/{pipe_name}"

    try:
        if system == "Windows":
            return _send_emotion_windows(pipe_path, emotion)
        else:
            return _send_emotion_unix(pipe_path, emotion)
    except Exception as e:
        print(f"✗ Unexpected error sending emotion: {e}", file=sys.stderr)
        return False


def _send_emotion_windows(pipe_path: str, emotion: str) -> bool:
    """Send emotion using Windows named pipes."""
    try:
        import win32pipe
        import win32file
        import pywintypes

        # Connect to the named pipe
        handle = win32file.CreateFile(
            pipe_path,
            win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_EXISTING,
            0,
            None
        )

        # Send emotion followed by newline
        message = f"{emotion}\n".encode('utf-8')
        win32file.WriteFile(handle, message)
        win32file.CloseHandle(handle)

        print(f"✓ Sent emotion '{emotion}' to display", file=sys.stderr)
        return True

    except ImportError:
        print("✗ pywin32 not installed. Run: pip install pywin32", file=sys.stderr)
        return False
    except pywintypes.error as e:
        error_code = e.args[0]
        if error_code == 2:  # ERROR_FILE_NOT_FOUND
            print(f"✗ Display app not running (pipe not found)", file=sys.stderr)
        elif error_code == 231:  # ERROR_PIPE_BUSY
            print(f"✗ Display pipe busy, try again", file=sys.stderr)
        else:
            print(f"✗ Pipe error: {e}", file=sys.stderr)
        return False


def _send_emotion_unix(pipe_path: str, emotion: str) -> bool:
    """Send emotion using Unix domain sockets."""
    import socket

    try:
        # Connect to Unix domain socket
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(pipe_path)

        # Send emotion followed by newline
        message = f"{emotion}\n".encode('utf-8')
        sock.sendall(message)
        sock.close()

        print(f"✓ Sent emotion '{emotion}' to display", file=sys.stderr)
        return True

    except FileNotFoundError:
        print(f"✗ Display app not running (socket not found at {pipe_path})", file=sys.stderr)
        return False
    except ConnectionRefusedError:
        print(f"✗ Display app not accepting connections", file=sys.stderr)
        return False
    except Exception as e:
        print(f"✗ Socket error: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    # Test script
    import time

    print(f"Testing emotion display client on {platform.system()}...", file=sys.stderr)
    print("Make sure EmotionDisplay app is running!", file=sys.stderr)
    print("", file=sys.stderr)

    test_emotions = ["curious", "happy", "excited", "concerned", "creative"]

    for emotion in test_emotions:
        print(f"Sending: {emotion}", file=sys.stderr)
        success = send_emotion(emotion)
        if success:
            time.sleep(1)
        else:
            print(f"Failed to send {emotion}", file=sys.stderr)
            break

    print("Test complete!", file=sys.stderr)

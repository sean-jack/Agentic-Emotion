"""
Named pipe client for communicating with the .NET WPF emotion display app.
"""
import os
import sys
import win32pipe
import win32file
import pywintypes


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
    pipe_path = f"\\\\.\\pipe\\{pipe_name}"

    try:
        # Connect to the named pipe (1000ms timeout, matches .NET client)
        handle = win32file.CreateFile(
            pipe_path,
            win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_EXISTING,
            0,
            None
        )

        # Send emotion followed by newline (matches .NET protocol)
        message = f"{emotion}\n".encode('utf-8')
        win32file.WriteFile(handle, message)
        win32file.CloseHandle(handle)

        print(f"✓ Sent emotion '{emotion}' to display", file=sys.stderr)
        return True

    except pywintypes.error as e:
        error_code = e.args[0]
        if error_code == 2:  # ERROR_FILE_NOT_FOUND
            print(f"✗ Display app not running (pipe not found)", file=sys.stderr)
        elif error_code == 231:  # ERROR_PIPE_BUSY
            print(f"✗ Display pipe busy, try again", file=sys.stderr)
        else:
            print(f"✗ Pipe error: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"✗ Unexpected error sending emotion: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    # Test script
    import time

    print("Testing emotion display client...", file=sys.stderr)
    print("Make sure EmotionDisplay.exe is running!", file=sys.stderr)
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

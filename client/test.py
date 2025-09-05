import serial
import time


def test_serial():
    try:
        # Open serial connection
        ser = serial.Serial("COM7", 115200, timeout=1)
        print(f"Connected to COM7 at 115200 baud")
        print("Listening for data... (Press Ctrl+C to stop)")

        time.sleep(2)  # Wait for ESP32 to initialize

        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode("utf-8").strip()
                if data:
                    print(f"Received: {data}")
            else:
                print(".", end="", flush=True)  # Show we're still listening
                time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nStopped by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if "ser" in locals():
            ser.close()


if __name__ == "__main__":
    test_serial()

#!/usr/bin/env python3
"""
Test script to verify the ESP32 data parsing works correctly.
"""

import sys
import json
from serial_reader import SerialReader


def test_parser():
    """Test the ESP32 data parser with sample data."""

    # Sample data from your ESP32 test
    test_data = "Humidity: 51.00% | Temp: 29.40C/84.92F | Passengers: 96 | Distance: 22.29 cm | GPS: 6.927100, 79.861200 | Status: Comfortable temperature. Bus almost full, be cautious. Buzzer OFF."

    print("🧪 Testing ESP32 Data Parser")
    print("=" * 50)
    print(f"Original ESP32 data:")
    print(f"{test_data}")
    print()

    # Create a mock serial reader for testing
    class MockSerialReader(SerialReader):
        def __init__(self):
            # Don't initialize actual serial connection
            pass

    reader = MockSerialReader()

    # Test the parser
    try:
        parsed = reader.parse_esp32_format(test_data)

        if parsed:
            print("✅ Parsing successful!")
            print("📊 Parsed JSON data:")
            print(json.dumps(parsed, indent=2))
            print()

            # Verify all expected fields
            expected_fields = [
                "humidity",
                "temp_c",
                "temp_f",
                "passengers",
                "distance",
                "latitude",
                "longitude",
                "buzzer",
            ]

            missing_fields = [field for field in expected_fields if field not in parsed]

            if missing_fields:
                print(f"⚠️  Missing fields: {missing_fields}")
            else:
                print("✅ All expected fields present!")

            # Check GPS coordinates
            if "latitude" in parsed and "longitude" in parsed:
                lat, lng = parsed["latitude"], parsed["longitude"]
                print(f"🗺️  GPS Location: {lat}, {lng}")

                # Check if coordinates are in Sri Lanka region
                if 5.9 <= lat <= 9.9 and 79.5 <= lng <= 81.9:
                    print("✅ GPS coordinates appear to be in Sri Lanka")
                else:
                    print("ℹ️  GPS coordinates outside Sri Lanka region")

        else:
            print("❌ Parsing failed - no data extracted")

    except Exception as e:
        print(f"❌ Parser error: {e}")


if __name__ == "__main__":
    test_parser()

# Parse a .bin file using pymavlink and return a list of telemetry messages as Python dictionaries

from pymavlink import mavutil
import datetime
import json
import os

def parse_bin_file(file_path):
    """
    Parse a binary MAVLink log file and return a list of telemetry messages.
    
    Args:
        file_path (str): Path to the .bin file
        
    Returns:
        list: List of dictionaries containing parsed telemetry data
    """
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}

    try:
        mlog = mavutil.mavlink_connection(file_path)
    except Exception:
        try:
            mlog = mavutil.mavlink_connection(file_path, robust_parsing=True)
        except Exception as e:
            return {"error": f"Failed to open log file: {str(e)}"}

    messages = []

    try:
        while True:
            msg = mlog.recv_match()
            if msg is None:
                break

            print("Raw message type:", msg.get_type())  # DEBUG

            if msg.get_type() == 'BAD_DATA':
                continue

            data = msg.to_dict()

            if 'time_boot_ms' in data:
                try:
                    data['timestamp'] = datetime.datetime.fromtimestamp(
                        data['time_boot_ms'] / 1000.0).isoformat()
                except Exception:
                    pass

            data['message_type'] = msg.get_type()
            messages.append(data)
    except Exception as e:
        return {"error": f"Error parsing messages: {str(e)}"}

    return messages

def get_available_message_types(file_path):
    """
    Get a list of all available message types in the log file.
    
    Args:
        file_path (str): Path to the .bin file
        
    Returns:
        list: List of available message types
    """
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}

    try:
        mlog = mavutil.mavlink_connection(file_path)
    except Exception:
        try:
            mlog = mavutil.mavlink_connection(file_path, robust_parsing=True)
        except Exception as e:
            return {"error": f"Failed to open log file: {str(e)}"}

    message_types = set()

    try:
        while True:
            msg = mlog.recv_match()
            if msg is None:
                break

            if msg.get_type() != 'BAD_DATA':
                message_types.add(msg.get_type())
    except Exception as e:
        return {"error": f"Error parsing message types: {str(e)}"}

    return list(message_types)

def summarize_telemetry(messages):
    """
    Summarize the parsed telemetry data.

    Args:
        messages (list): List of parsed telemetry messages

    Returns:
        dict: Summary including total messages and average altitude if available
    """
    if isinstance(messages, dict) and "error" in messages:
        return messages

    summary = {
        "total_messages": len(messages),
        "message_types": {}
    }

    for msg in messages:
        msg_type = msg.get("message_type", "unknown")
        summary["message_types"][msg_type] = summary["message_types"].get(msg_type, 0) + 1

    altitude_msgs = [msg for msg in messages if "alt" in msg or "relative_alt" in msg]
    if altitude_msgs:
        total_alt = sum(msg.get("alt", msg.get("relative_alt", 0)) for msg in altitude_msgs)
        summary["average_altitude"] = total_alt / len(altitude_msgs)

    return summary

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"Parsing file: {file_path}")
        types = get_available_message_types(file_path)
        print(f"Available message types: {types}")
        messages = parse_bin_file(file_path)
        print(f"Parsed {len(messages)} messages")

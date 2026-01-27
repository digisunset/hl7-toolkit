import re

SEGMENT_PATTERN = re.compile(
    r"(MSH\|.*?)(?=(MSH\||$))",
    re.DOTALL
)

SEGMENTS = ("MSH|", "PID|", "ORC|", "OBR|", "OBX|", "NTE|")

def extract_hl7_blocks(text):
    messages = []

    # Find each HL7 message starting at MSH
    for match in SEGMENT_PATTERN.finditer(text):
        raw_msg = match.group(1)

        segments = []
        current = ""

        i = 0
        while i < len(raw_msg):
            if raw_msg[i:i+4] in SEGMENTS:
                if current:
                    segments.append(current)
                current = raw_msg[i:i+4]
                i += 4
            else:
                current += raw_msg[i]
                i += 1

        if current:
            segments.append(current)

        messages.append("\r".join(s.strip() for s in segments))

    return messages

from flask import Flask, request, render_template
import re

from pdf_reader import extract_text_from_pdf
from hl7_extract import extract_hl7_blocks
from hl7_parser import readable_oru

app = Flask(__name__)


def find_severities(text):
    markers = []
    for m in re.finditer(r"\((F|W)\).*", text):
        markers.append((m.start(), m.group(1), m.group(0)))
    return markers


def nearest_severity(msg_pos, markers):
    nearest = None
    for pos, sev, txt in markers:
        if pos < msg_pos:
            nearest = (sev, txt)
        else:
            break
    return nearest


def extract_obx_codes(error_text):
    return set(re.findall(r"OBX\s*3\.1:\s*(\d+)", error_text))


@app.route("/", methods=["GET", "POST"])
def index():
    output = ""

    if request.method == "POST":
        file = request.files.get("file")
        if file:
            text = extract_text_from_pdf(file)
            markers = find_severities(text)

            for m in re.finditer(r"MSH\|", text):
                msg_start = m.start()
                blocks = extract_hl7_blocks(text[msg_start:])
                if not blocks:
                    continue

                hl7 = blocks[0]
                sev_info = nearest_severity(msg_start, markers)

                ctx = {}
                if sev_info:
                    sev, txt = sev_info
                    ctx["severity"] = sev
                    ctx["message"] = txt
                    ctx["obx"] = extract_obx_codes(txt)

                output += readable_oru(hl7, ctx)

    return render_template("index.html", output=output)


if __name__ == "__main__":
    app.run(debug=False)

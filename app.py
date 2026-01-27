"""
HL7 Error Log Parser & HL7 Message Viewer

Version: 1.1
Author: HUBERMAR "THING2"
Email: marc.huber@med.usc.edu

License: MIT
Copyright (c) 2026 Marc Huber
"""


from flask import Flask, request, render_template
import re

from pdf_reader import extract_text_from_pdf
from hl7_extract import extract_hl7_blocks
from hl7_parser import readable_oru

app = Flask(__name__)


# -----------------------------
# Main Menu
# -----------------------------
@app.route("/")
def menu():
    return render_template("menu.html")


# -----------------------------
# Error Log HL7 Parser
# -----------------------------
@app.route("/error-log", methods=["GET", "POST"])
def error_log():
    output = ""

    if request.method == "POST":
        file = request.files.get("file")
        if file:
            text = extract_text_from_pdf(file)

            # Find (F)/(W) markers with position
            markers = []
            for m in re.finditer(r"\((F|W)\).*", text):
                markers.append((m.start(), m.group(1), m.group(0)))

            def nearest_marker(pos):
                found = None
                for p, sev, msg in markers:
                    if p < pos:
                        found = (sev, msg)
                    else:
                        break
                return found

            for msh in re.finditer(r"MSH\|", text):
                pos = msh.start()
                blocks = extract_hl7_blocks(text[pos:])
                if not blocks:
                    continue

                hl7 = blocks[0]
                ctx = {}

                marker = nearest_marker(pos)
                if marker:
                    sev, msg = marker
                    ctx["severity"] = sev
                    ctx["message"] = msg
                    if sev == "F":
                        ctx["obx"] = set(re.findall(r"OBX\s*3\.1:\s*(\d+)", msg))

                output += readable_oru(hl7, ctx)

    return render_template("index.html", output=output)


# -----------------------------
# Single HL7 Message Parser
# -----------------------------
@app.route("/single-message", methods=["GET", "POST"])
def single_message():
    output = ""
    raw = ""

    if request.method == "POST":
        raw = request.form.get("hl7", "")
        if raw.strip():

            # -----------------------------
            # 1. Extract HL7 block only
            # -----------------------------
            msh_match = re.search(r"MSH\|", raw)
            if not msh_match:
                output = "<div class='error'>No HL7 MSH segment found.</div>"
                return render_template(
                    "single_message.html",
                    output=output,
                    raw=raw
                )

            hl7_block = raw[msh_match.start():]

            # Stop at ESI LOG or end of text
            end_match = re.search(r"\nESI LOG", hl7_block)
            if end_match:
                hl7_block = hl7_block[:end_match.start()]

            # -----------------------------
            # 2. Normalize HL7 segments
            # -----------------------------
            segments = []
            for line in hl7_block.splitlines():
                line = line.strip()
                if not line:
                    continue
                if "|" in line:
                    segments.append(line)

            hl7 = "\r".join(segments)

            # -----------------------------
            # 3. Extract Error Text (if present)
            # -----------------------------
            ctx = {}
            err_match = re.search(r"Error Text\s+(.*)", raw)
            if err_match:
                error_text = err_match.group(1).strip()
                ctx["severity"] = "F"
                ctx["message"] = error_text
                ctx["obx"] = set(
                    re.findall(r"OBX\s*3\.1:\s*(\d+)", error_text)
                )

            # -----------------------------
            # 4. Render using same engine
            # -----------------------------
            output = readable_oru(hl7, ctx)

    return render_template(
        "single_message.html",
        output=output,
        raw=raw
    )




if __name__ == "__main__":
    app.run(debug=False)

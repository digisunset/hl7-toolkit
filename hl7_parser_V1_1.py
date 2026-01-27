from datetime import datetime


# -----------------------------
# Helpers
# -----------------------------
def format_hl7_ts(ts):
    try:
        return datetime.strptime(ts[:14], "%Y%m%d%H%M%S").strftime("%m-%d-%y %H:%M:%S")
    except Exception:
        return ts


def format_accession_human(acc):
    if not acc:
        return ""
    acc = acc.zfill(13)
    return f"{acc[0:3]}-{acc[3:5]}-{acc[5:8]}-{acc[8:]}"


def format_accession_ccl(acc):
    if not acc:
        return ""
    site = acc[0:3].zfill(5)
    year = "20" + acc[3:5]
    julian = acc[5:8]
    seq = acc[8:].zfill(6)
    return f"{site}{year}{julian}{seq}"


def extract_obr_code_and_name(seg, fs):
    fields = seg.split(fs)
    code = fields[4].strip() if len(fields) > 4 else ""
    name = ""

    # OBR-20 = LOINC~Order Name (Quest style)
    if len(fields) > 19 and "~" in fields[19]:
        name = fields[19].split("~", 1)[1].strip()

    return code, name


# -----------------------------
# Main renderer
# -----------------------------
def readable_oru(raw, ctx=None):
    if ctx is None:
        ctx = {}

    severity = ctx.get("severity")
    message_text = ctx.get("message", "")
    highlight_obx = ctx.get("obx", set())

    segments = raw.split("\r")
    msh = segments[0]
    fs = msh[3]

    def f(seg, idx):
        parts = seg.split(fs)
        return parts[idx] if idx < len(parts) else ""

    collapsed = "collapsed" if severity == "W" else ""

    lines = []

    # Card wrapper
    lines.append(f"<div class='card {collapsed}'>")

    # Header
    lines.append(
        "<div class='card-header'>"
        f"<b>MESSAGE:</b> Type: {f(msh,8)} | Timestamp: {format_hl7_ts(f(msh,6))}"
        "<button class='toggle' onclick='toggleCard(this)'>▾</button>"
        "</div>"
    )

    # Severity banner
    if severity == "F":
        lines.append(f"<div class='error'>ERROR: {message_text}</div>")
    elif severity == "W":
        lines.append(f"<div class='info'>ℹ️ {message_text}</div>")

    # Body
    lines.append("<div class='card-body'>")

    obr_groups = {}
    obr_order = []
    current_obr = None

    # -----------------------------
    # Parse HL7
    # -----------------------------
    for seg in segments:
        st = seg[:3]

        if st == "ORC":
            acc = f(seg, 2)
            acc_h = format_accession_human(acc)
            acc_c = format_accession_ccl(acc)

            lines.append(
                f"<div class='acc'>"
                f"ACCESSION: {acc_h} | "
                f"CCL ACCESSION: {acc_c} "
                f"<button onclick=\"copyText('{acc_c}')\">Copy</button>"
                f"</div>"
            )

        elif st == "OBR":
            code, name = extract_obr_code_and_name(seg, fs)
            current_obr = code
            obr_groups.setdefault(code, {"name": name, "obxs": []})
            if code not in obr_order:
                obr_order.append(code)

        elif st == "OBX" and current_obr:
            parts = seg.split(fs)[3].split("^")
            obr_groups[current_obr]["obxs"].append((parts[0], parts[1]))

    # -----------------------------
    # Render OBR / OBX
    # -----------------------------
    for code in obr_order:
        group = obr_groups[code]

        if group["name"]:
            display_name = group["name"]
        elif group["obxs"]:
            display_name = group["obxs"][0][1]
        else:
            display_name = "Unmatched order – no test name provided by source"

        # OBR line with copy button FIRST
        lines.append("<div class='order'>")
        lines.append(
            f"<div class='obr-line'>"
            f"<button onclick=\"copyText('{code}')\">Copy</button> "
            f"<b>{code} — {display_name}</b>"
            f"</div>"
        )

        # OBX lines with copy button FIRST
        for oc, on in group["obxs"]:
            hl = "highlight" if oc in highlight_obx else ""
            lines.append(
                f"<div class='obx {hl}'>"
                f"<button onclick=\"copyText('{oc}')\">Copy</button> "
                f"{oc} — {on}"
                f"</div>"
            )

        lines.append("</div>")

    lines.append("</div></div>")
    return "\n".join(lines)

# HL7 Tools

**HL7 Error Log Parser & HL7 Message Viewer**

Version: **1.1**  
Authored by: **THING2**  
Contact: **marc.huber@med.usc.edu**  
License: **MIT**

---

## Overview

HL7 Tools is an internal utility designed to help interface and integration analysts
quickly investigate HL7-related errors from ESI error logs and raw HL7 messages.

The tool focuses on **clarity, correctness, and investigation speed**, turning
raw HL7 and vendor error logs into structured, readable, and actionable output.

---

## Features

### Error Log HL7 Parser
- Upload ESI error log PDFs
- Automatically extracts HL7 messages
- Displays:
  - Accession and CCL accession
  - OBR and OBX segments (numbered)
  - Error and warning messages scoped to the correct HL7 message
- Highlights the specific OBX referenced in the error
- Handles unmatched / unsolicited orders gracefully
- Collapse/expand per message (warnings collapsed by default)
- Copy buttons for accession, OBR, and OBX codes

### Single HL7 Message Parser
- Paste raw HL7 or ESI log output
- Automatically extracts the HL7 payload
- Applies the same rendering and investigation logic as the error log parser
- Useful for ad-hoc troubleshooting, vendor tickets, and mapping validation

### Navigation
- Main menu landing page
- Clear navigation between tools
- Consistent UI and styling across pages

---

## Intended Audience

- Interface analysts
- Integration engineers
- Clinical systems support
- HL7 troubleshooting teams

---

## Design Principles

- Never guess missing data
- Prefer explicit source information over heuristics
- Keep parsing logic simple and transparent
- Optimize for real-world investigation workflows
- Separate parsing, context, and presentation logic

---

## License

This project is licensed under the **MIT License**.

Commercial licensing options may be available upon request.

See the `LICENSE` file for full details.

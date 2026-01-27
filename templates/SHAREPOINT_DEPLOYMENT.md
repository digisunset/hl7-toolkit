# SharePoint Deployment Checklist

This document outlines recommended steps for hosting HL7 Tools
on SharePoint or an internal web platform.

---

## Pre-Deployment

- [ ] Confirm version is tagged (v1.1)
- [ ] Confirm LICENSE file is present
- [ ] Confirm authorship and contact information is correct
- [ ] Validate that no PHI is stored or logged persistently
- [ ] Confirm tool is read-only (no writes to production systems)

---

## Hosting Considerations

- [ ] Decide hosting model:
  - SharePoint Embedded App
  - Internal IIS / reverse proxy
  - Containerized service behind SharePoint
- [ ] Ensure HTTPS is enforced
- [ ] Confirm access restrictions (internal users only)

---

## Security

- [ ] Disable file persistence (uploads processed in-memory only)
- [ ] No logging of uploaded HL7 or PDFs
- [ ] No external network calls (unless explicitly approved)
- [ ] Validate that pasted HL7 data is not stored server-side

---

## Configuration

- [ ] Set application title and version in UI footer
- [ ] Configure static assets (favicon, icons)
- [ ] Verify navigation links work behind SharePoint paths

---

## Validation

- [ ] Upload sample error log PDF
- [ ] Paste raw HL7 message
- [ ] Verify:
  - Accession display
  - OBR / OBX numbering
  - Error highlighting
  - Collapse/expand behavior
- [ ] Test with Quest and ARUP logs (if available)

---

## Post-Deployment

- [ ] Share usage instructions with interface team
- [ ] Collect feedback
- [ ] Log enhancement requests for v1.2+

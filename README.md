# PrivateText — Privacy-safe transcript redactor

A standalone desktop app that masks selected identifier patterns in pasted or local transcript files. It has no external dependencies, API, server, cloud account, database, or Atlas requirement.

## Run

```powershell
python main.py
```

## Features

- Pasting, opening, redacting, and saving text locally
- Optional masking rules for email, Indian phone numbers, card-like numbers, Aadhaar-like IDs, PAN-like IDs, IP addresses, URLs, and dates of birth
- Numbered placeholders such as `[EMAIL_1]`, preserving document structure
- Count of masked items by category

## Limits

This is an explainable regular-expression baseline, not a guarantee of complete de-identification. It will not reliably recognize every person name, address, organization, contextual identifier, or nonstandard format. Review the output before sharing it. The app does not save or transmit the original text; it only saves a file when you explicitly choose **Save redacted .txt**.

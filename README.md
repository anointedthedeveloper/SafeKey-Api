# SafeKey API

A cryptographically secure, customizable password generator API built with FastAPI and deployed on Vercel.

**Live API:** https://safe-key-api-at2w.vercel.app

---

## Endpoints

### `GET /api/generate`

Generate one or more secure passwords.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `length` | int | `12` | Password length (6–64) |
| `uppercase` | bool | `true` | Include uppercase letters |
| `lowercase` | bool | `true` | Include lowercase letters |
| `numbers` | bool | `true` | Include digits |
| `symbols` | bool | `true` | Include special characters |
| `exclude_similar` | bool | `false` | Exclude similar chars (`il1Lo0O`) |
| `count` | int | `1` | Number of passwords to generate (1–20) |

**Example Request**
```
GET /api/generate?length=16&symbols=true&count=3
```

**Example Response**
```json
{
  "status": "success",
  "passwords": [
    ">ND!.m'y>7%C2U8z",
    "6gi3p[A;l6Uz%=84",
    "#KxEesR;D0g(dF?N"
  ],
  "strength": "very strong",
  "entropy": 104.87
}
```

### `GET /`

Health check — confirms the API is running.

---

## Features

- Cryptographically secure using Python's `secrets` module
- Guarantees at least one character from each selected group
- Entropy-based strength meter (`weak` / `moderate` / `strong` / `very strong`)
- Rate limiting: 10 requests per minute per IP
- Input validation with clear error messages
- CORS enabled
- Swagger UI at `/docs`

---

## Project Structure

```
SafeKey-Api/
├── api/
│   └── index.py        # FastAPI app & routes
├── core/
│   └── generator.py    # Password generation + strength meter
├── utils/
│   └── validator.py    # Input validation
├── requirements.txt
└── vercel.json
```

---

## Run Locally

```bash
pip install -r requirements.txt
uvicorn api.index:app --reload
```

Visit `http://localhost:8000/docs` for the interactive Swagger UI.

---

## Deploy to Vercel

```bash
npm i -g vercel
vercel
```

---

## Tech Stack

- Python, FastAPI, slowapi
- Deployed on Vercel (`@vercel/python`)

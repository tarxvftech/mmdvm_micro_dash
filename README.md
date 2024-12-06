# mmdvm_micro_dash

A lightweight AGPLv3 dashboard for the MMDVM platform meant to be juuust
enough that you don't *need* SSH, while showing that claims about the
death of pi0w utility are grossly exaggerated.

Simple, as in KISS.

Lightweight, a Pi0w doesn't break a sweat.

Distributed as part of PorkAlpine.

Made with love by tarxvf.

## Tech

Backend: Python FastAPI, run by Uvicorn

Frontend: Svelte

File editing with snapshots.
Service management.
Log streaming.

I did say "simple".


## Installation

On PorkAlpine, you can `apk add mmdvm_micro_dash`.

## Configuration

## Security

## Development

NixOS: `nix-shell`

For frontend:
```
cd frontend
npm run dev
```
For backend:
```
cd backend
python -m venv env
source env/bin/activate
pip install -r requirements.txt
make
```
## Packaging

See the APKBUILD in the porkalpine / pim17 repo.

## License

AGPLv3
```

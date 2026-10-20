# site-aevia

The Aevia website (same al-folio theme as maxrommel.de). Pages are fragments in `src/pages/`; `python3 build.py`
wraps them with `src/layout.html` into `site/`. CI builds a Caddy image from `site/`; the Aevia platform deploys it
by digest (`catalog/services.yml`, service `aevia`).

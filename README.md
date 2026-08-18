# Secret Newsletter Podcast

Daily US-English product-discovery podcast for **The Secret Newsletter**, hosted by Maya and Daniel.

## Safety and editorial guarantees

- The only product source is the latest approved newsletter JSON.
- The source must contain exactly 10 complete products.
- Every product URL must be HTTPS and point to `OneFantasticShop.net`.
- The pipeline never reconstructs product URLs and never substitutes Amazon or eBay links.
- Missing or invalid source data stops generation instead of inventing content.
- The dialogue does not claim physical product testing.
- The subscription offer is fixed at: **30-day free trial, then $4.99/month, cancel anytime.**

## Architecture

1. GitHub Actions reads the permanent newsletter source configured in the repository variable `SECRET_NEWSLETTER_LATEST_URL`.
2. The source is validated and the current product rotation is selected.
3. Maya (`af_heart`) and Daniel (`am_michael`) are rendered with Kokoro in US English.
4. FFmpeg assembles a 128 kbps MP3.
5. GitHub Pages publishes `latest-podcast.mp3`, `latest.json`, and a mobile-friendly player page.

The scheduled job remains skipped until the permanent source variable exists. A manual run may provide a source URL override.

## Expected newsletter schema

```json
{
  "edition_id": "newsletter-2026-08-18",
  "edition_date": "2026-08-18T08:00:00Z",
  "updated_at": "2026-08-18T08:10:00Z",
  "title": "The Secret Newsletter",
  "products": [
    {
      "name": "Exact approved name",
      "price": "$00.00",
      "description": "Approved factual description",
      "why_it_made_the_list": "Approved editorial hook",
      "url": "https://onefantasticshop.net/exact-product-page",
      "image": "https://...",
      "category": "Optional category"
    }
  ]
}
```

The `products` array must contain exactly ten unique products.

## Local validation (optional for developers)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python -m src.run_pipeline --source path/to/latest.json --skip-audio
```

Production runs entirely on GitHub Actions; Franck's computer is not part of the production architecture.

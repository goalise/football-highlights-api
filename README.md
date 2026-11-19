# Football Highlights API

Official football (soccer) video highlights and goal clips as JSON: every clip comes with a thumbnail, a watch link, an embed URL, geo restriction data and the match it belongs to. One REST endpoint, filter by match, team, competition or date.

**[Start a 7-day free trial](https://goalise.com/checkout?product=basic&billing=monthly&utm_source=github&utm_medium=referral&utm_campaign=football-highlights-api)** · [Product page](https://goalise.com/football-highlights-api?utm_source=github&utm_medium=referral&utm_campaign=football-highlights-api) · [API reference](https://docs.goalise.com/v3/apireference/openapi#tag/highlights) · [Support](https://goalise.com/support)

| | |
| --- | --- |
| Endpoint | `GET https://api.goalise.com/api/v3/highlights` |
| Auth | `Authorization: Bearer YOUR_API_TOKEN` |
| Format | JSON, 120 clips per page, newest kick-off first |
| Price | Included in every [Goalise](https://goalise.com/?utm_source=github&utm_medium=referral&utm_campaign=football-highlights-api) plan, from $15/month. Highlights cost nothing extra |
| Trial | 7 days free on the Basic plan (card required, cancel anytime) |

## Quick start

1. Pick a plan at [goalise.com/checkout](https://goalise.com/checkout?product=basic&billing=monthly&utm_source=github&utm_medium=referral&utm_campaign=football-highlights-api). Basic starts with a 7-day free trial.
2. Copy your API token from the [dashboard](https://goalise.com/account).
3. Ask for the clips of one match:

```bash
curl -H "Authorization: Bearer YOUR_API_TOKEN" \
  "https://api.goalise.com/api/v3/highlights?match_id=466659"
```

## What a clip looks like

Every answer uses the same envelope: `status`, `pagination`, `errors`, `meta`, `response`. One item of `response`:

```json
{
  "id": 593001,
  "type": "VERIFIED",
  "category": "match-highlights",
  "title": "Maldini la Decide di Testa | CAGLIARI-LECCE | HIGHLIGHTS | SERIE A 2026/27",
  "description": null,
  "img_url": "https://i.ytimg.com/vi/7YVc_sZqfwg/hqdefault.jpg",
  "url": "https://www.youtube.com/watch?v=7YVc_sZqfwg",
  "embed_url": "https://www.youtube.com/embed/7YVc_sZqfwg",
  "channel": "Serie A",
  "source": "youtube",
  "match": {
    "id": 466659,
    "league":    { "id": 646, "name": "Serie A", "logo": "https://...", "type": "League" },
    "home_team": { "id": 404, "name": "Cagliari", "logo": "https://..." },
    "away_team": { "id": 668, "name": "Lecce",    "logo": "https://..." },
    "timestamp": 1788798600,
    "start_date": "2026-09-12 20:45:00",
    "timezone": "UTC",
    "status": { "long": "Match Finished", "short": "FT", "elapsed": 90 },
    "score": { "home": 1, "away": 0 }
  },
  "restriction": {
    "state": "Allowed countries restriction",
    "allowed_countries": ["IT"],
    "blocked_countries": [],
    "embeddable": true
  }
}
```

The `match` object already carries the competition, both teams with crests, the kick-off time, the status and the score, so a highlights screen is one request.

## Filters

At least one of `match_id`, `league_id` or `team_id` is required.

| Parameter | Example | What it does |
| --- | --- | --- |
| `match_id` | `466659` | Clips of one match |
| `league_id` | `646` | Clips of one competition |
| `team_id` | `404` | Clips of one team, home or away |
| `date_from`, `date_to` | `2026-09-12` | Kick-off on or after / on or before this day (`Y-m-d`) |
| `category` | `goal-clip` | Keep one kind of clip, see the list below |
| `type` | `VERIFIED` | `VERIFIED` (default), `UNVERIFIED` or `all` |
| `timezone` | `Europe/Madrid` | IANA zone for `start_date` and for the date filters. Default UTC |
| `page` | `2` | Page number, starting at 1 |

```bash
# Goal clips of one team, kick-off times in Madrid time
curl -H "Authorization: Bearer YOUR_API_TOKEN" \
  "https://api.goalise.com/api/v3/highlights?team_id=404&category=goal-clip&timezone=Europe/Madrid"

# Match highlights of one competition for one weekend
curl -H "Authorization: Bearer YOUR_API_TOKEN" \
  "https://api.goalise.com/api/v3/highlights?league_id=646&category=match-highlights&date_from=2026-09-12&date_to=2026-09-14"
```

## Clip categories

`match-highlights` · `goal-clip` · `pre-match-content` · `post-match-content` · `press-conference` · `behind-the-scenes` · `live-coverage` · `discussion-analysis` · `other`

Goal clips usually carry the scorer and the minute in `description`, for example `James Sands 45+1`.

## Verified clips and embedding

- `VERIFIED` clips are official uploads by the rights holder. They are the default and are the ones to embed.
- `UNVERIFIED` clips are third-party links without an embed URL. Ask for them with `type=UNVERIFIED` or `type=all`.
- Embed a clip only when `restriction.embeddable` is `true` and `embed_url` is present. Otherwise link to `url`.
- `restriction.allowed_countries` and `restriction.blocked_countries` are ISO alpha-2 lists exactly as the video provider reports them. Check them against your viewer's country before showing a player.

```html
<iframe src="https://www.youtube.com/embed/7YVc_sZqfwg"
        title="Cagliari - Lecce highlights" allowfullscreen loading="lazy"></iframe>
```

The API returns metadata and links. The video itself stays on the publisher's platform (YouTube in the example above), so you serve no video traffic.

## Code examples

Runnable scripts are in [`examples/`](examples): [Python](examples/python/highlights.py), [JavaScript](examples/javascript/highlights.mjs), [PHP](examples/php/highlights.php). They use only the standard library and read the token from the `GOALISE_TOKEN` environment variable.

```javascript
const url = new URL("https://api.goalise.com/api/v3/highlights");
url.searchParams.set("league_id", "646");
url.searchParams.set("category", "match-highlights");

const response = await fetch(url, {
  headers: { Authorization: `Bearer ${process.env.GOALISE_TOKEN}` },
});
const { response: clips } = await response.json();

for (const clip of clips) {
  const canEmbed = clip.restriction.embeddable === true && clip.embed_url;
  console.log(clip.title, canEmbed ? clip.embed_url : clip.url);
}
```

## What you can build

- A highlights section for a football news site or fan blog
- Goal clips next to live scores and match pages in a mobile app
- A "watch the highlights" block in match reports and newsletters
- Video for fantasy football, prediction and statistics products
- Telegram and Discord bots that post the highlights after full time

## Errors and limits

| HTTP | `errors[].code` | When |
| --- | --- | --- |
| 400 | `validation.required`, `validation.invalid` | No filter given, a date that is not `Y-m-d`, an unknown category, type or timezone |
| 401 | `auth.required`, `auth.invalid` | Token missing or rejected |
| 404 | `not_found` | `match_id`, `league_id` or `team_id` belongs to nothing |
| 429 | `rate_limit.exceeded` | Limit reached. Wait for the seconds in `Retry-After` |

A match that has no video yet answers `200` with an empty `response` array. Every answer carries `X-Rate-Limit-Limit`, `X-Rate-Limit-Remaining` and `X-Rate-Limit-Reset`, and `GET /quota` shows your usage without spending a request.

## Pricing

| Plan | Price | Requests per day |
| --- | --- | --- |
| Basic | $15/month, first 7 days free | 5,000 |
| Pro | $30/month | 50,000 |
| Premium | $50/month | 150,000 |

Every plan includes every endpoint and every competition: highlights, live scores, fixtures, standings, statistics, odds and news with one token. Annual billing is 30% cheaper. [See the plans](https://goalise.com/checkout?utm_source=github&utm_medium=referral&utm_campaign=football-highlights-api).

## FAQ

**Is there a free football highlights API?**
Goalise has no permanent free tier. The Basic plan starts with a 7-day free trial, then costs $15 per month. A card is required to start the trial and you can cancel at any time.

**Can I embed the videos on my website or in my app?**
Yes, when `restriction.embeddable` is `true` and the clip has an `embed_url`. For other clips, link to `url`. Respect the country lists in `restriction`.

**Which competitions have highlights?**
Video availability depends on the competition and its rights holder. Ask for a `league_id` to see what is there. The [coverage page](https://goalise.com/coverage?utm_source=github&utm_medium=referral&utm_campaign=football-highlights-api) lists every competition in the API.

**Does it return single goals or only full match highlights?**
Both. Use `category=goal-clip` for single goals and `category=match-highlights` for the full package.

**Do highlights cost extra?**
No. A highlights call counts as one request of your daily allowance, like any other endpoint.

**Do I need a separate token for scores and statistics?**
No. The same token works for all 46 endpoints of the Goalise Football API.

## Related

- [Football API](https://github.com/goalise/football-api): live scores, fixtures, standings, lineups, statistics, odds
- [Football News API](https://github.com/goalise/football-news-api): football news by league, team, category and date
- [Football MCP Server](https://goalise.com/football-mcp-server?utm_source=github&utm_medium=referral&utm_campaign=football-highlights-api): the same data for AI assistants
- [Full API documentation](https://docs.goalise.com/v3/get-started)

## License

The example code in this repository is released under the MIT License. Use of the API is subject to the [Goalise terms](https://goalise.com/terms).

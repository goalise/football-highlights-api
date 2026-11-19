// Match highlights of one competition, with the link to embed or to open.
//
// Usage:
//   export GOALISE_TOKEN=your_api_token
//   node highlights.mjs 646        # 646 = Serie A
//
// Needs Node.js 18+ and nothing else.

const leagueId = process.argv[2] ?? "646";

const url = new URL("https://api.goalise.com/api/v3/highlights");
url.searchParams.set("league_id", leagueId);
url.searchParams.set("category", "match-highlights");

const response = await fetch(url, {
  headers: {
    Authorization: `Bearer ${process.env.GOALISE_TOKEN ?? ""}`,
    Accept: "application/json",
  },
});
const data = await response.json();

if (data.status !== "success") {
  console.error("API error:", data.errors.map((error) => error.code).join(", "));
  process.exit(1);
}

for (const clip of data.response) {
  const home = clip.match?.home_team?.name ?? "?";
  const away = clip.match?.away_team?.name ?? "?";
  // Embed only what the rights holder allows; otherwise link to the watch page.
  const canEmbed = clip.restriction.embeddable === true && clip.embed_url;
  console.log(`${home} - ${away}: ${canEmbed ? clip.embed_url : clip.url}`);
}

const { current_page, page_count, total_count } = data.pagination;
console.log(`\npage ${current_page} of ${page_count}, ${total_count} clips in total`);
console.log(`requests left in the current window: ${response.headers.get("x-rate-limit-remaining")}`);

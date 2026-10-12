# Google Search for AstrBot

Search Google from an AstrBot conversation using your own Ace Data Cloud account. The `google_search` Agent tool returns structured web titles, links, and snippets synchronously, so there is no task ID or polling step.

[简体中文指南](readme/README_zh_Hans.md) · [Google Search API](https://platform.acedata.cloud/documents?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=googlesearchastrbot_readme_documents) · [Current prices](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=googlesearchastrbot_readme_pricing)

## 1. Find and install

In AstrBot WebUI, open **Extensions → Plugins → AstrBot Plugin Market** and search **Google Search**. Check for **Google Search by Ace Data Cloud**, author **acedatacloud**, and the Google Search service icon, then select **Install**. Under **Installed**, verify that the plugin is enabled without a load error.

The AstrBot Cloud listing has not yet been published. After the source release is merged, use **Installed → Install (+) → Install from URL** with `https://github.com/AceDataCloud/GoogleSearchAstrBot` for a preview. A URL installation does not establish official market discovery or installation.

## 2. Get a key with Google Search access

New account? Register and sign in first. If the Applications page has no General application yet, choose **Initialize General Application**, then continue with the key steps below.

Sign in to [Ace Data Cloud Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=googlesearchastrbot_readme_api_key). Open **General application** to copy a key, or choose **Manage Keys → Create** for a dedicated AstrBot key. A service-specific key must allow `/serp/google`. Check current pricing and balance before a search.

Copy the key value only. Do not add `Bearer ` or use a `platform-...` management token. Never place a key in a chat prompt or repository file.

## 3. Configure AstrBot

Under **Extensions → Plugins → Installed**, select the gear icon on **Google Search by Ace Data Cloud**. Enter the key in **Ace Data Cloud API key with Google Search access** and save. The UI masks the field, while the AstrBot data directory stores its original value; protect that directory.

Use a chat model that supports tool calling and enable `google_search` for the active profile and persona. Check **Extensions → Handlers** if the tool is unavailable.

## 4. Search in chat

Ask the bot:

> Use `google_search` once for `site:astrbot.app plugin development`, return 3 results, and show each title, link, and snippet.

The tool calls `/serp/google` once with `type=search`, `page=1`, and `number=3`. The response is synchronous and includes an `organic` array. Open any returned link to inspect the source; search snippets are external content and should be treated as such. There is no generation task to poll.

## 5. Check usage and troubleshoot

Open your Ace Data Cloud application usage history and filter to **Google SERP API**. If a trace ID appears in the tool response, use it for exact matching; otherwise use the key/application, API, and request time as a narrower clue without claiming a per-record match. The current cost rule charges 0.01 Credits for up to 10 results and 0.02 Credits for 11–20 results before account discounts; verify the live price before each use.

| Symptom | Check |
| --- | --- |
| Plugin fails to load | AstrBot version, **Failed to Load Plugins**, then **Data & Logs → Logs**. |
| Tool does not appear | The plugin is enabled and allowed by the active profile/persona; the model supports tool calling. |
| HTTP 401 or 403 | Key type, expiration, balance, service access, and any Allowed APIs restriction. |
| Network failure | Check request history before repeating a search; a timed-out response might still have consumed usage. |

The plugin sends the key only to `https://api.acedata.cloud`, rejects redirects, and makes no automatic paid retry. It uses Python's standard library and needs no extra package.

## Verified local run

On an isolated AstrBot `v4.28.2` instance, the plugin loaded and ChatUI invoked `google_search` once with the example query. It returned three relevant AstrBot plugin documentation results. [Sanitized evidence](tests/e2e-results.json) records the input and result titles. The public market listing and install remain unverified.

## Brand asset

`logo.png` is the unmodified current [Google Search service icon](https://cdn.acedata.cloud/27e11e555d.png), SHA-256 `cf8b5ead614e5ef7aed0f0a3de1b490563a3812c00f5328ec66d8efc16a2bfc1`.

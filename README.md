# Innisai festival calendar

`festivals.json` is read by the Innisai app (about once a week when the phone is online).
A GitHub Action rebuilds it on the 1st of every month from the open-source `holidays` Python package. No API key needed.

## One-time setup
1. On GitHub create a **public** repo named `innisai-festivals`.
2. Upload everything in this folder (keep the `.github/workflows` folder).
3. Repo > Actions > "Update festivals.json" > Run workflow once to check it works (green tick).
4. In the app project open `app/src/main/java/com/innisai/app/data/Festivals.kt` and replace `YOUR_GITHUB_USER` in `REMOTE_URL` with your GitHub user name. Build the app again.

The app also carries a copy of this file inside it, so festivals work offline and before the first download.
Eid dates are estimates (moon sighting), so those entries have `"grace": 1` and the app also shows them the next day.

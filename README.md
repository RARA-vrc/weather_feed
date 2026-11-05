# room1206 の天気フィード

ワールドの温度計（`Room1206Climate`）が読む、日本の 16 都市の最新の気温です。気象庁のアメダスから 10 分ごとに取り、
`docs/room1206_weather.json` に書きます。GitHub Pages がこのファイルを配信します。

- GitHub Pages（`*.github.io`）は VRChat の String Loading で信頼されているドメインです。プレイヤーは「Allow Untrusted URLs」を入れなくても読めます。
- 出典は気象庁ホームページです。ワールドでは気温の横に「気象庁」と出します。
- 1 回の実行で気象庁に送るリクエストは 2 つだけです（`latest_time.txt` と、その時刻の `map/….json`）。

## 準備（あなたの GitHub で 1 回だけ）

1. GitHub で新しい **public** リポジトリを作る（例: `room1206-weather`）。
2. このフォルダの中身を、そのリポジトリの一番上に置く。
   - `make_weather.py`
   - `.github/workflows/weather.yml`
   - `docs/room1206_weather.json`（最初の 1 つ。なくても最初の実行で作られます）
   - `README.md`
3. リポジトリの **Settings → Pages** で「Deploy from a branch」→ ブランチ `main`、フォルダ `/docs` → Save。
4. **Actions** タブで workflow「weather」を開き、**Run workflow** で一度手で動かす。
5. 数分後に `https://<あなたのユーザー名>.github.io/<リポジトリ名>/room1206_weather.json` を開いて、JSON が見えれば完了。
6. その URL を Claude に伝える（`unity/Setup/climate_setup.cs.txt` の `weatherUrl` に入れて、ワールドに組み込みます）。

## 注意

- GitHub の定期実行は、混んでいると数分遅れることがあります。
- 公開リポジトリで 60 日間なにも動きがないと、定期実行が止められることがあります。止まったら Actions タブから再開してください。
- 気象庁のこのデータは公式の API ではないため、形式が変わることがあります。そのときはワールドは月ごとの表で動き続けます（温度計の外気は「—」になります）。
- 都市の並びと名前は `Room1206Climate.cs` と同じです（0 が東京）。

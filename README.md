# n96j collection

An **open source** collection of links to old Windows builds (ISOs, VMs, pre-releases, service packs, DDKs, symbols) and to programs, MSDN discs, books and drivers. A simple site made for beginners.

**Important:** this repository **does not host any Windows or program files.** Every link points to [archive.org](https://archive.org). All software belongs to its respective owners.

## How the site works

Go to **Downloads**, pick the **Windows**, the **kind** (official, beta, modded) and the **language**, then press **Download**. Or type in the search box (`xp portuguese`, `7 ultimate 64`). 32-bit and 64-bit of the same release share one row.

## Files

```
index.html      home page
builds.html     step-by-step Windows builds browser + search
programs.html   Programs & Extras: Steam betas, MSDN/TechNet, books, drivers, software (searchable)
credits.html    photo credits and licenses
css/style.css   styles (Pantone colors)
js/app.js       step-by-step browser and search
data/builds.js  the builds list (generated)
data/extras.js  the Programs & Extras list (generated)
tools/          scripts + .txt lists: sources/ -> data/builds.js, sources_extras/ -> data/extras.js
assets/img/     optional place for your own images
```

## Publish on GitHub Pages

1. Create a repository and upload these files.
2. Go to **Settings, then Pages**.
3. Under *Source* pick **Deploy from a branch**, branch `main`, folder `/ (root)`.
4. Wait a minute. Your site appears at `https://YOUR-USER.github.io/REPO-NAME/`.

## Add more builds

The `.txt` lists use `Name: URL` lines and `## Section` headings. To update the site, run:

```
python tools/txt_para_js.py tools/sources/*.txt
```

Put new `.txt` lists in `tools/sources/`. Files named `02_...` become **Extras (Service Packs, DDK, symbols)** and files named `03_...` become **Unverified (check before using)**; any other name is sorted by the script (official, beta or modded) and keeps the cleaned-up names.

For the **Programs & Extras** page (things that are not Windows installs), put lists in `tools/sources_extras/` and run:

```
python tools/extras_para_js.py tools/sources_extras/*.txt
```

`## Section` headings become categories. Clearly off-topic items (videos, music, unrelated books) go to the "Videos, media and off-topic" category; edit the `OFF` pattern in `tools/extras_para_js.py` to change that. The script turns codes like `w7 sp1 ult ptbr x64` into **Windows 7 SP1 Ultimate — Portuguese (Brazil)**, detects language, 32/64-bit and kind, and merges duplicates.

## Contributing

Found a broken link or want to suggest something? Open an issue or a pull request.

## Pantone palette

Classic Blue `#0F4C81` · Living Coral `#FF6F61` · Ultra Violet `#5F4B8B` · Greenery `#88B04B` · Marigold `#FDAC53` · Serenity `#92A8D1` · Rose Quartz `#F7CAC9`

## Photos

Photos are loaded from [Wikimedia Commons](https://commons.wikimedia.org) under free licenses (a mix of old and new hardware). Authors and licenses are listed on `credits.html`.

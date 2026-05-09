# Publishing `subq-quickstart` as its own repo

The canonical development copy lives at `companion/subq-quickstart/` inside this monorepo. To mirror it to **`github.com/tinarezvanian/subq-quickstart`**:

## Option A — new repo, one-time push

```bash
cd companion/subq-quickstart
git init
git add .
git commit -m "Initial commit: SubQ quickstart examples + benchmarks"
git branch -M main
git remote add origin git@github.com:tinarezvanian/subq-quickstart.git
git push -u origin main
```

## Option B — subtree split from parent repo (keeps history)

From the **LLMs repo root**:

```bash
git subtree split --prefix=companion/subq-quickstart -b subq-quickstart-split
git push git@github.com:tinarezvanian/subq-quickstart.git subq-quickstart-split:main
```

Then add the remote as a second remote on `main` only if you intend ongoing subtree workflow (advanced).

## After publish

- Update README companion link and [cover_letter.md](../cover_letter.md) if the URL differs.
- Pin the real PyPI package name for `subq` in `requirements.txt` when SubQ ships it.

# agent_translator
A learning and language translation agent. This combines LLM translation, search, and semantic language understanding.

> Just show me the code.

## Basic usage

### Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### CLI

Translate English → Spanish (auto-detect if not specified):

```bash
python translator.py "Hello world"
```

Force source/target:

```bash
python translator.py -s en -t es "How are you?"
python translator.py -s es -t en "¿Cómo estás?"
```

Use stdin:

```bash
echo "Buenos días" | python translator.py
```

Custom LibreTranslate URL:

```bash
python translator.py -u https://translate.astian.org "buenas noches"
```

### Local LibreTranslate (free for <200 words)

Run locally via Docker:

```bash
docker run -p 5000:5000 libretranslate/libretranslate
```

By default, short texts (≤200 words) will prefer the local server at `http://localhost:5000` if reachable. You can control this behavior:

```bash
# Use local for short texts (default)
python translator.py "hola mundo"

# Disable local preference
python translator.py --no-local-short "hola mundo"

# Change local URL or threshold
python translator.py --local-url http://127.0.0.1:5000 --short-threshold 150 "hola mundo"

# Environment variables
export LT_LOCAL_URL=http://localhost:5000
export LT_LOCAL_SHORT_THRESHOLD=200
export LT_DISABLE_LOCAL_SHORT=0  # set to 1 to disable
```


## Contributing


## License

MIT
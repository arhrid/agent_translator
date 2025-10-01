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


## Contributing


## License

MIT
# eng-to-spa
English → Spanish text translator built in Python with deep-translator.

## 🚀 Features
- Translate single phrases, full files, or stdin input  
- Local JSON cache to skip re-translating the same text  
- CLI-friendly and easy to extend  
- Lightweight — only depends on `deep-translator`

---

## 📦 Installation
Clone this repository and install dependencies:

```bash
git clone https://github.com/hacker6171/eng-to-spa.git
cd eng-to-spa
pip install -r requirements.txt
```

# 💻 Usage
## Translate a single phrase
```bash
python eng_to_spa.py "Hello, how are you?"
```
## Translate from a file
```bash
python eng_to_spa.py -f input.txt -o output.txt
```
## Pipe input (stdin)
```bash
echo "Good morning" | python eng_to_spa.py --stdin
```
## Specify source and target languages
```bash
python eng_to_spa.py "I love programming" --source en --target es
```
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

This project is licensed under the MIT License. See LICENSE.

---

✅ **Instructions:**

1. Replace `YOUR_GITHUB_USER` with your GitHub username.  
2. Save this as `README.md` in your `eng-to-spa` folder.  
3. Commit and push to GitHub:  
```powershell
git add README.md
git commit -m "Add complete README"
git push

from flask import Flask, render_template, request, jsonify
from kmp import KMP_search
from lcs import LCS
from palindrome import manacher
from trie import Trie  # Import Trie class

app = Flask(__name__)
trie = Trie()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'file1' not in request.files:
        return jsonify({"error": "file1 is required"}), 400

    text1 = request.files['file1'].read().decode('utf-8')
    text2 = request.files.get('file2')
    if text2:
        text2 = text2.read().decode('utf-8')

    algorithm = request.form['algorithm']
    result = ""

    # Insert words into Trie for auto-completion
    # (rest of your code)

    # Insert words into Trie for auto-completion
    for word in text1.split():
        trie.insert(word)

    if algorithm == 'KMP':
        pattern = request.form['pattern']
        if pattern:
            matches = list(KMP_search(text1, pattern))
            for match in matches:
                text1 = text1[:match] + '<span class="highlight-yellow">' + text1[match:match+len(pattern)] + '</span>' + text1[match+len(pattern):]
            result = text1

    elif algorithm == 'LCS' and text2:
        result = LCS(text1, text2)
        text1 = text1.replace(result, f'<span class="highlight-blue">{result}</span>')
        text2 = text2.replace(result, f'<span class="highlight-blue">{result}</span>')

    elif algorithm == 'Palindrome':
        palindrome = manacher(text1)
        result = text1.replace(palindrome, f'<span class="highlight-green">{palindrome}</span>')

    return render_template('index.html', text1=text1, text2=text2, result=result, algorithm=algorithm)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    prefix = request.args.get('prefix', '')
    suggestions = trie.autocomplete(prefix)
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)




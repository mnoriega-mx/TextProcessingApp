from flask import Flask, render_template, request, jsonify
from kmp import KMP_search
from lcs import LCS
from palindrome import manacher
from trie import Trie  # Import Trie class

app = Flask(__name__)
trie = Trie()

# Global variables to track matches and current match index
current_matches = []
current_match = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    global current_matches, current_match

    text1 = request.form.get('file1Content', '')
    pattern = request.form.get('pattern', '')
    algorithm = request.form.get('algorithm', '')

    if not text1:
        return jsonify({"error": "Text 1 is required"}), 400

    result = text1

    # Insert words into Trie for auto-completion
    for word in text1.split():
        trie.insert(word)

    if algorithm == 'KMP' and pattern:
        current_matches = list(KMP_search(text1, pattern))
        current_match = 0  # Reset to the first match
        if current_matches:
            match = current_matches[current_match]
            result = text1[:match] + '<span class="highlight-yellow">' + text1[match:match+len(pattern)] + '</span>' + text1[match+len(pattern):]

    elif algorithm == 'LCS':
        text2 = request.form.get('file2Content', '')
        result = LCS(text1, text2)

        text1_highlighted = text1.replace(result, f'<span class="highlight-blue">{result}</span>')
        text2_highlighted = text2.replace(result, f'<span class="highlight-blue">{result}</span>')
        # Return both highlighted texts and algorithm name
        return jsonify({"text1": text1_highlighted, "text2": text2_highlighted, "algorithm": algorithm})

    elif algorithm == 'Palindrome':
        palindrome = manacher(text1)
        result = text1.replace(palindrome, f'<span class="highlight-green">{palindrome}</span>')

    return jsonify({"result": result, "algorithm": algorithm})

@app.route('/navigate', methods=['POST'])
def navigate():
    print("Navigate")
    global current_matches, current_match

    text1 = request.form.get('file1Content', '')
    pattern = request.form.get('pattern', '')
    direction = request.form.get('direction')

    if direction == 'left':
        current_match = max(current_match - 1, 0)  # Decrement, but not below 0
    elif direction == 'right':
        current_match = min(current_match + 1, len(current_matches) - 1)  # Increment, but not beyond match count

    if not current_matches or current_match >= len(current_matches):
        return jsonify({"result": text1})

    print(current_match)
    match = current_matches[current_match]
    result = text1[:match] + '<span class="highlight-yellow">' + text1[match:match+len(pattern)] + '</span>' + text1[match+len(pattern):]

    return jsonify({"result": result})

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    prefix = request.args.get('prefix', '')
    suggestions = trie.autocomplete(prefix)
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)

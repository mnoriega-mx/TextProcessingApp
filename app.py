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
    # Retrieve the file content from the form data instead of request.files
    text1 = request.form.get('file1Content', '')
    text2 = request.form.get('file2Content', None)
    algorithm = request.form.get('algorithm', '')
    
    if not text1:
        return jsonify({"error": "Text 1 is required"}), 400

    result = ""

    # Insert words into Trie for auto-completion
    for word in text1.split():
        trie.insert(word)

    if algorithm == 'KMP':
        pattern = request.form.get('pattern', '')
        if pattern:  # Only search if a pattern is provided
            matches = list(KMP_search(text1, pattern))
            for match in matches:
                text1 = text1[:match] + '<span class="highlight-yellow">' + text1[match:match+len(pattern)] + '</span>' + text1[match+len(pattern):]
        else:
            # If pattern is empty, return the original text without highlights
            text1 = text1

        result = text1

    elif algorithm == 'LCS' and text2:
        result = LCS(text1, text2)
        # Highlight LCS in both text1 and text2
        text1_highlighted = text1.replace(result, f'<span class="highlight-blue">{result}</span>')
        text2_highlighted = text2.replace(result, f'<span class="highlight-blue">{result}</span>')

        # Return both highlighted texts and algorithm name
        return jsonify({"text1": text1_highlighted, "text2": text2_highlighted, "algorithm": algorithm})

    elif algorithm == 'Palindrome':
        palindrome = manacher(text1)
        result = text1.replace(palindrome, f'<span class="highlight-green">{palindrome}</span>')

    # Return the result and the algorithm name
    return jsonify({"result": result, "algorithm": algorithm})




@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    prefix = request.args.get('prefix', '')
    suggestions = trie.autocomplete(prefix)
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)



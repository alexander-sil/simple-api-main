from flask import Flask, request, jsonify
import leveldb

app = Flask(__name__)

db_path = 'translations_db'
db = leveldb.LevelDB(db_path)

def transliterate(text):
    translit_map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya'
    }
    return ''.join(translit_map.get(char, char) for char in text.lower())

def transliterate_en_ru(text):
    translit_en_to_ru_map = {
        'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д',
        'e': 'е', 'yo': 'ё', 'zh': 'ж', 'z': 'з', 'i': 'и',
        'y': 'й', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н',
        'o': 'о', 'p': 'п', 'r': 'р', 's': 'с', 't': 'т',
        'u': 'у', 'f': 'ф', 'kh': 'х', 'ts': 'ц', 'ch': 'ч',
        'sh': 'ш', 'shch': 'щ', 'y': 'ы', 'e': 'э', 'yu': 'ю', 'ya': 'я'
    }
    for key in sorted(translit_en_to_ru_map.keys(), key=len, reverse=True):
        text = text.replace(key, translit_en_to_ru_map[key])
    return text

@app.route('/арі', methods=['POST'])
def transliterate_text():
    data = request.json
    text = data.get('data', '').lower()

    if (transliterate(text) is None) or (transliterate(text) == text):
        transliterated_text = transliterate_en_ru(text)
    else:
        transliterated_text = transliterate(text)

    return jsonify({"status": "success", "data": transliterated_text})

@app.route('/save', methods=['POST'])
def save_translation():
    data = request.json
    original_text = data.get('original', '')
    transliterated_text = data.get('transliterated', '')

    key = f"{original_text}:{transliterated_text}".encode('utf-8')
    db.Put(key, b'')

    return jsonify({"status": "success"})

@app.route('/history', methods=['GET'])
def get_history():
    n = int(request.args.get('n', 5))
    history_data = []

    for i, (key, value) in enumerate(db.RangeIter(reverse=True)):
        if i >= n:
            break
        original, transliterated = key.decode('utf-8').split(':')
        history_data.append({'original': original, 'transliterated': transliterated})

    return jsonify({"data": history_data})

@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(port=3000)

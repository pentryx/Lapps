from flask import Flask, request, jsonify

app = Flask(__name__)

def decrypt_code(input_code, keyword):
    # İlk olarak, 9'dan çıkarma işlemini tersine çevir
    reversed_code = ''.join(str(9 - int(digit)) for digit in input_code)

    # Sırayı daebfc'den abcdef sırasına göre geri yerleştir
    rearranged_num = (
        reversed_code[1] + reversed_code[3] + reversed_code[5] +
        reversed_code[0] + reversed_code[2] + reversed_code[4]
    )

    # Şifreleme anahtarını kullanarak XOR işlemini tersine çevir
    decrypted_code = ''.join(
        chr(ord(rearranged_num[i]) ^ ord(keyword[i % len(keyword)]))
        for i in range(len(rearranged_num))
    )

    return decrypted_code

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    input_code = data.get('input_code')
    keyword = data.get('keyword')

    if not input_code or not keyword:
        return jsonify({"error": "Both 'input_code' and 'keyword' are required."}), 400

    try:
        result = decrypt_code(input_code, keyword)
        return jsonify({"decrypted_code": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# इन-मेमोरी डेटाबेस (अकाउंट्स को स्टोर करने के लिए डिक्शनरी)
# फॉर्मेट: { accountNumber: { "name": "...", "balance": 0.0 } }
bank_database = {}
account_counter = 1001

@app.route('/')
def home():
    # Frontend पेज को लोड करेगा
    return render_template('index.html')

# API: नया अकाउंट बनाएं
@app.route('/api/create_account', methods=['POST'])
def create_account():
    global account_counter
    data = request.json
    name = data.get('name')
    initial_deposit = float(data.get('deposit', 0.0))
    
    if not name:
        return jsonify({"success": False, "message": "नाम दर्ज करना आवश्यक है!"}), 400
        
    acc_no = str(account_counter)
    account_counter += 1
    
    bank_database[acc_no] = {
        "name": name,
        "balance": initial_deposit
    }
    
    return jsonify({
        "success": True, 
        "message": "अकाउंट सफलतापूर्वक बन गया है!", 
        "account_no": acc_no,
        "balance": initial_deposit
    })

# API: बैलेंस चेक करें
@app.route('/api/balance/<acc_no>', methods=['GET'])
def get_balance(acc_no):
    if acc_no in bank_database:
        return jsonify({
            "success": True,
            "name": bank_database[acc_no]["name"],
            "balance": bank_database[acc_no]["balance"]
        })
    return jsonify({"success": False, "message": "अकाउंट नंबर नहीं मिला!"}), 404

# API: पैसे जमा करें (Deposit)
@app.route('/api/deposit', methods=['POST'])
def deposit():
    data = request.json
    acc_no = data.get('account_no')
    amount = float(data.get('amount', 0))
    
    if acc_no in bank_database:
        if amount <= 0:
            return jsonify({"success": False, "message": "अमान्य राशि!"}), 400
        
        bank_database[acc_no]["balance"] += amount
        return jsonify({
            "success": True,
            "message": f"सफलतापूर्वक जमा किए गए: ₹{amount}",
            "new_balance": bank_database[acc_no]["balance"]
        })
    return jsonify({"success": False, "message": "अकाउंट नंबर नहीं मिला!"}), 404

# API: पैसे निकालें (Withdraw)
@app.route('/api/withdraw', methods=['POST'])
def withdraw():
    data = request.json
    acc_no = data.get('account_no')
    amount = float(data.get('amount', 0))
    
    if acc_no in bank_database:
        if amount <= 0:
            return jsonify({"success": False, "message": "अमान्य राशि!"}), 400
            
        if bank_database[acc_no]["balance"] >= amount:
            bank_database[acc_no]["balance"] -= amount
            return jsonify({
                "success": True,
                "message": f"सफलतापूर्वक निकाले गए: ₹{amount}",
                "new_balance": bank_database[acc_no]["balance"]
            })
        else:
            return jsonify({"success": False, "message": "पर्याप्त बैलेंस नहीं है!"}), 400
            
    return jsonify({"success": False, "message": "अकाउंट नंबर नहीं मिला!"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

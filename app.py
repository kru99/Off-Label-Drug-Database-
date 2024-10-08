from flask import Flask, jsonify, request
import json

# Your OffLabelDictionary class here
class OffLabelDictionary:
    drug_dictionary = {}

    @classmethod
    def add_drug(cls, drug_name, approved_uses, off_label_uses, side_effects, interactions):
        cls.drug_dictionary[drug_name] = {
            "Approved Uses": approved_uses,
            "Off-label Uses": off_label_uses,
            "Side Effects": side_effects,
            "Interactions": interactions
        }

    @classmethod
    def modify_drug(cls, drug_name, approved_uses, off_label_uses, side_effects, interactions):
        if drug_name in cls.drug_dictionary:
            cls.drug_dictionary[drug_name] = {
                "Approved Uses": approved_uses,
                "Off-label Uses": off_label_uses,
                "Side Effects": side_effects,
                "Interactions": interactions
            }
        else:
            print(f'{drug_name} was not found in the dictionary!')

    @classmethod
    def remove_drug(cls, drug_name):
        if drug_name in cls.drug_dictionary:
            del cls.drug_dictionary[drug_name]
        else:
            print(f'{drug_name} was not found in the dictionary!')

    @classmethod
    def display_drug(cls, drug_name):
        if drug_name in cls.drug_dictionary:
            print(json.dumps(cls.drug_dictionary[drug_name], indent=4))
        else:
            print(f'{drug_name} was not found in the dictionary!')

    @classmethod
    def save_to_file(cls, filename="off_label_dictionary.json"):
        with open(filename, 'w') as f:
            json.dump(cls.drug_dictionary, f, indent=4)
        print(f'Dictionary saved to {filename}')

    @classmethod
    def load_from_file(cls, filename="off_label_dictionary.json"):
        try:
            with open(filename, 'r') as f:
                cls.drug_dictionary = json.load(f)
            print(f'Dictionary loaded from {filename}')
        except FileNotFoundError:
            print(f'{filename} not found!')

# Load the dictionary from the JSON file
OffLabelDictionary.load_from_file()

# Create a Flask application
app = Flask(__name__)

@app.route("/")
def home():
    return "<p>Welcome to the OfflabelRX API!</p>"

@app.route("/api/drugs", methods=['GET'])
def get_all_drugs():
    return jsonify(OffLabelDictionary.drug_dictionary)

@app.route("/api/drug/<name>", methods=['GET'])
def get_drug(name):
    drug = OffLabelDictionary.drug_dictionary.get(name)
    if drug:
        return jsonify(drug)
    else:
        return jsonify({"error": "Drug not found"}), 404

@app.route("/api/drug", methods=['POST'])
def add_drug():
    data = request.json
    drug_name = data.get('name')
    approved_uses = data.get('approved_uses', [])
    off_label_uses = data.get('off_label_uses', [])
    side_effects = data.get('side_effects', [])
    interactions = data.get('interactions', [])

    if not drug_name:
        return jsonify({"error": "Drug name is required"}), 400

    OffLabelDictionary.add_drug(drug_name, approved_uses, off_label_uses, side_effects, interactions)
    OffLabelDictionary.save_to_file()
    return jsonify({"message": "Drug added successfully"}), 201

@app.route("/api/drug/<name>", methods=['PUT'])
def modify_drug(name):
    if name not in OffLabelDictionary.drug_dictionary:
        return jsonify({"error": "Drug not found"}), 404

    data = request.json
    approved_uses = data.get('approved_uses', [])
    off_label_uses = data.get('off_label_uses', [])
    side_effects = data.get('side_effects', [])
    interactions = data.get('interactions', [])

    OffLabelDictionary.modify_drug(name, approved_uses, off_label_uses, side_effects, interactions)
    OffLabelDictionary.save_to_file()
    return jsonify({"message": "Drug updated successfully"}), 200

@app.route("/api/drug/<name>", methods=['DELETE'])
def delete_drug(name):
    if name not in OffLabelDictionary.drug_dictionary:
        return jsonify({"error": "Drug not found"}), 404

    OffLabelDictionary.remove_drug(name)
    OffLabelDictionary.save_to_file()
    return jsonify({"message": "Drug deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)

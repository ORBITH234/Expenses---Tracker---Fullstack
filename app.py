from flask import Flask, request, jsonify, render_template_string
import json, os

app = Flask(__name__)
FILE = "expenses.json"

def load():
    if not os.path.exists(FILE):
        return []
    with open(FILE) as f:
        return json.load(f)

def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

HTML = """
<!DOCTYPE html><html><head><title>Expense Tracker - ORBITH234</title>
<meta name=viewport content="width=device-width, initial-scale=1">
<style>body{font-family:Arial;padding:20px;max-width:600px;margin:auto;background:#f5f5f5}
.card{background:white;padding:15px;border-radius:10px;margin:10px 0}
input,select,button{width:100%;padding:10px;margin:5px 0;border-radius:5px;border:1px solid #ccc}
button{background:#000;color:white;font-weight:bold}</style></head>
<body><h2>💰 ORBITH234 Expense Tracker</h2>
<div class=card><h3>Add Expense</h3>
<input id=amount placeholder=Amount type=number>
<input id=category placeholder="Category e.g Food">
<input id=desc placeholder=Description>
<button onclick=add()>Add</button></div>
<div class=card><h3>Expenses</h3><div id=list>Loading...</div><h4 id=total></h4></div>
<script>
async function load(){let r=await fetch('/api/expenses');let d=await r.json();
let h='';let total=0;d.forEach((e,i)=>{h+=`<div>${e.category}: ₦${e.amount} - ${e.desc} <button onclick=del(${i})>x</button></div>`;total+=parseFloat(e.amount)});
document.getElementById('list').innerHTML=h||'No expenses';document.getElementById('total').innerHTML='Total: ₦'+total;}
async function add(){let a=document.getElementById('amount').value,c=document.getElementById('category').value,d=document.getElementById('desc').value;
await fetch('/api/expenses',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({amount:a,category:c,desc:d})});load();}
async function del(i){await fetch('/api/expenses/'+i,{method:'DELETE'});load();}load();
</script></body></html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/api/expenses", methods=["GET","POST"])
def expenses():
    data=load()
    if request.method=="POST":
        j=request.json
        data.append({"amount":j["amount"],"category":j["category"],"desc":j["desc"]})
        save(data)
        return jsonify({"ok":True})
    return jsonify(data)

@app.route("/api/expenses/<int:idx>", methods=["DELETE"])
def delete(idx):
    data=load()
    if 0<=idx<len(data):
        data.pop(idx)
        save(data)
    return jsonify({"ok":True})

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)

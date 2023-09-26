from flask import Flask, request, json
import tokenBalance  # 确保tokenBalance.py在同一目录下，或已正确设置PYTHONPATH

app = Flask(__name__)

@app.route('/api/token', methods=['POST'])
def check_billing():
    data = request.json
    api_key = data.get('api_key')
    
    if not api_key:
        response = app.response_class(
            response=json.dumps({"Status": 0, "Error": "未输入API Key"}, ensure_ascii=False),
            status=400,
            mimetype='application/json'
        )
        return response
    
    result = tokenBalance.check_billing(api_key)
    response = app.response_class(
        response=json.dumps(result, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)


# npm install pm2 -g
# pm2 start app.py --interpreter python3 --name ok-billing

# curl -X POST -H "Content-Type: application/json" -d '{"api_key":"sk-EqwiUa1p6g2DGAZr1262BdA9C68b4628A3B43bCa1870871f"}' http://194.163.156.110:5005/api/bull/token
# curl -X POST -H "Content-Type: application/json" -d '{"api_key":"sk-EqwiUa1p6g2DGAZr1262BdA9C68b4628A3B43bCa1870872f"}' https://billing.openkey.cloud/api/token
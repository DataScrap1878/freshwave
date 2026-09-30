from flask import Flask, jsonify
import pandas as pd
import sqlite3

app=Flask(__name__)

@app.route("/health", methods = ["GET"])
def get_health():
        conn = sqlite3.connect("business_data.db")
        conn.close()
        return jsonify({"status":"ok"}), 200
        


@app.route("/sales", methods = ["GET"])
def get_sales():
        conn = sqlite3.connect("business_data.db")
        sales =pd.read_sql("SELECT * FROM final_consolidated limit 100",conn)
        conn.close()
        return jsonify(sales.to_dict(orient='records'))

@app.route("/salesbycity", methods = ["GET"])
def get_salesbycity():
        conn = sqlite3.connect("business_data.db")
        salesbycity =pd.read_sql("SELECT * FROM sales_by_city",conn)
        conn.close()
        return jsonify(salesbycity.to_dict(orient='records'))


if __name__ == "__main__" :
    app.run(debug=True)


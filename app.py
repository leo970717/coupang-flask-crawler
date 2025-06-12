
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ 쿠팡 키워드 크롤러가 실행 중입니다. /crawl?q=검색어 로 사용하세요."

@app.route("/crawl", methods=["GET"])
def crawl_coupang():
    keyword = request.args.get("q")
    if not keyword:
        return jsonify({"error": "검색어(q)가 필요합니다."}), 400

    url = f"https://www.coupang.com/np/search?q={keyword}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select("ul.search-product-list li.search-product")[:3]

        results = []
        for item in items:
            name_tag = item.select_one("div.name")
            link_tag = item.select_one("a")

            if name_tag and link_tag:
                title = name_tag.text.strip()
                link = "https://www.coupang.com" + link_tag.get("href")
                results.append({
                    "title": title,
                    "link": link
                })

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

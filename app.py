import math

from flask import Flask, render_template, request

app = Flask(__name__)


def bmi_guidance(bmi):
    if bmi < 18.5:
        return {
            "label": "體重過輕",
            "tone": "low",
            "advice": "留意是否攝取足夠且均衡的營養，並搭配適度肌力活動，逐步建立穩定體重。",
            "summary": "目前體重偏輕，重點在於穩定熱量與營養攝取，避免長時間空腹和過度節食。",
            "details": [
                "每餐維持固定進食時間，增加主食、蛋白質與蔬果，避免營養攝取不足。",
                "每週安排 2–3 次適度肌力訓練，協助維持骨骼與肌肉健康。",
                "若持續體重下降、疲勞、睡眠不佳或食慾明顯降低，建議諮詢醫師或營養師。",
            ],
        }
    if bmi < 24:
        return {
            "label": "健康體位",
            "tone": "healthy",
            "advice": "維持均衡飲食、規律運動與穩定睡眠，繼續維持這種健康節奏。",
            "summary": "目前體位處於健康範圍，重點是保持飲食平衡與生活節律，避免忽略長期習慣。",
            "details": [
                "以全穀雜糧、蛋白質、蔬菜與水分攝取為主，維持每日有規律的三餐。",
                "每週累積至少 150 分鐘中等強度活動，搭配日常步行和伸展。",
                "保持每晚 7–8 小時睡眠，並持續關注壓力管理與情緒穩定。",
            ],
        }
    if bmi < 27:
        return {
            "label": "體重過重",
            "tone": "high",
            "advice": "從小而穩定的飲食與活動調整著手，逐步改善體重與健康風險。",
            "summary": "目前 BMI 超出健康範圍，建議先控制熱量來源並增加日常活動量，循序改善。",
            "details": [
                "減少含糖飲料、油炸與高熱量零食，增加蔬菜、水果與高纖食物的攝取。",
                "以走路、騎車、伸展與力量訓練等方式增加每日活動量，逐步提高代謝。",
                "若有腰圍增加、倦怠或睡眠呼吸問題，建議安排健康檢查與專業評估。",
            ],
        }
    return {
        "label": "肥胖",
        "tone": "high",
        "advice": "建議從飲食結構、活動量與生活習慣一起調整，必要時尋求專業協助。",
        "summary": "目前 BMI 偏高，若長期未改善，可能增加代謝與心血管風險，建議儘早調整。",
        "details": [
            "先從飲食習慣調整開始，例如減少高糖、高油、高鹽食物，增加蔬果與蛋白質。",
            "逐步增加每週運動時間，從日常步行和輕度有氧訓練開始，避免過度壓力。",
            "若有高血壓、高血糖、關節不適或睡眠呼吸中止等情況，請與醫師或營養師討論個別計畫。",
        ],
    }


def parse_positive_number(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) and number > 0 else None


@app.route("/", methods=["GET", "POST"])
def index():
    name_input = ""
    height_input = ""
    weight_input = ""
    errors = {}
    result = None

    if request.method == "POST":
        name_input = request.form.get("name", "").strip()
        height_input = request.form.get("height", "").strip()
        weight_input = request.form.get("weight", "").strip()
        height = parse_positive_number(height_input)
        weight = parse_positive_number(weight_input)

        if height is None:
            errors["height"] = "請輸入大於 0 的有效身高（公分）。"
        if weight is None:
            errors["weight"] = "請輸入大於 0 的有效體重（公斤）。"

        if not errors:
            height_meters = height / 100
            height_squared = height_meters * height_meters
            if not math.isfinite(height_squared) or height_squared == 0:
                errors["height"] = "無法使用這組數值計算 BMI，請檢查身高與體重。"
            else:
                bmi = weight / height_squared
                if not math.isfinite(bmi) or bmi == 0:
                    errors["weight"] = "無法使用這組數值計算 BMI，請檢查身高與體重。"
                else:
                    displayed_bmi = round(bmi, 1)
                    guidance = bmi_guidance(displayed_bmi)
                    user_name = name_input or "你"
                    result = {
                        "bmi": f"{displayed_bmi:.1f}",
                        "user_name": user_name,
                        **guidance,
                    }

    return render_template(
        "index.html",
        name_input=name_input,
        height_input=height_input,
        weight_input=weight_input,
        errors=errors,
        result=result,
    )


if __name__ == "__main__":
    app.run(debug=True)

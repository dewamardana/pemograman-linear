from flask import Flask, render_template, request
from scipy.optimize import linprog

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Ambil input jumlah minimal unit protein dan energi dari form
            min_protein = float(request.form.get("min_protein"))
            min_energi = float(request.form.get("min_energi"))

            # Menyelesaikan masalah linear programming
            c = [10, 8]  # Biaya pakan A dan B
            A = [[-3, -2], [-2, -4]]  # Koefisien batasan (protein, energi)
            b = [-min_protein, -min_energi]  # Nilai batasan (input dari pengguna)
            x_bounds = [(0, None), (0, None)]  # Batasan non-negatif

            result = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds, method="highs")

            if result.success:
                pakan_a = result.x[0]
                pakan_b = result.x[1]
                biaya_minimal = result.fun
                return render_template(
                    "index.html",
                    pakan_a=pakan_a,
                    pakan_b=pakan_b,
                    biaya_minimal=biaya_minimal,
                )
            else:
                return render_template("index.html", error="Tidak ditemukan solusi.")
        except Exception as e:
            return render_template("index.html", error=str(e))
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

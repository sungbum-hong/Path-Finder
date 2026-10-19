"""최종 보고서용 통합 그림 4장.
모든 숫자는 팀 분석보고서(자료조사 1~5) 본문과 표에 적힌 값을 그대로 옮겼다.
"""
import glob
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Patch

# 한글 폰트: 시스템(나눔고딕) 또는 저장소 fonts/ 폴더에서 찾는다
for f in (glob.glob("/usr/share/fonts/truetype/nanum/NanumGothic*.ttf")
          + glob.glob(os.path.join(os.path.dirname(__file__), "fonts", "NanumGothic*.ttf"))):
    font_manager.fontManager.addfont(f)
plt.rcParams.update({
    "font.family": ["NanumGothic", "DejaVu Sans"], "axes.unicode_minus": False,
    "savefig.dpi": 300, "font.size": 10,
    "axes.spines.top": False, "axes.spines.right": False,
})
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs", "figures", "")
os.makedirs(OUT, exist_ok=True)
INK, QUIET, GRID = "#1F2328", "#6B7280", "#E5E7EB"
# 팀 기존 그림과 같은 색
GRADE = {"상": "#2E8B57", "중": "#F0B940", "하": "#C0392B"}
TYPE = {"A": "#C0392B", "B": "#F0A020", "C": "#8B7BC4", "D": "#CFD8DC"}


def source(fig, text, y=-0.02):
    fig.text(0.01, y, "자료: " + text, fontsize=7.5, color=QUIET, ha="left", va="top")


# ------------------------------------------------------------------
# 그림 1. 접근성 등급별 증거 사슬 (자료조사 2·3)
# ------------------------------------------------------------------
panels = [
    ("정류장 300m 안 고령인구", "%", [90, 77, 44], "{:.0f}%", "등급 산정 지표"),
    ("버스 배차 간격 중앙값", "분", [10, 20, 58], "{:.0f}분", "등급 산정 지표"),
    ("70세 이상 차량 이동 비중", "%", [18, 31, 57], "{:.0f}%", "ρ = -0.92"),
    ("60세 이상 평균 이동거리", "km", [6.6, 8.2, 13.9], "{:.1f}km", "ρ = -0.75"),
    ("65세 이상 1명당 하루 이동", "회", [2.1, 2.6, 2.4], "{:.1f}회", "차이 없음 (p = 0.27)"),
]
fig, axes = plt.subplots(1, 5, figsize=(13, 3.9))
for i, (ax, (name, unit, vals, fmt, note)) in enumerate(zip(axes, panels)):
    flat = i == 4
    cols = ["#9CA3AF"] * 3 if flat else [GRADE[g] for g in "상중하"]
    bars = ax.bar(["상", "중", "하"], vals, color=cols, width=0.62)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v * 1.02, fmt.format(v), ha="center", va="bottom",
                fontsize=10, fontweight="bold", color=INK)
    ax.set_ylim(0, max(vals) * 1.25)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_title(name, fontsize=10.5, fontweight="bold", color=INK, pad=8)
    ax.text(0.5, -0.2, note, transform=ax.transAxes, ha="center", fontsize=8.5,
            color="#C0392B" if not flat and "ρ" in note else QUIET)
    ax.tick_params(axis="x", length=0, labelsize=10)
    if i == 2:
        ax.annotate("", xy=(-0.18, 0.5), xytext=(-0.02, 0.5), xycoords="axes fraction")
fig.text(0.01, 1.07, "접근성이 낮을수록 버스는 멀고 드물며, 고령자는 차로 멀리 간다 — 이동 횟수는 같다",
         fontsize=14, fontweight="bold", color=INK, ha="left")
fig.text(0.01, 1.0, "버스 접근성 종합 등급(자료조사 2)별 값, 2025년 · 상 22곳, 중 24곳, 하 20곳 · ρ는 66개 시군구 접근성 종합 점수와의 순위상관",
         fontsize=9, color=QUIET, ha="left")
# 원인 → 결과 구분선
fig.add_artist(plt.Line2D([0.405, 0.405], [0.08, 0.9], color=GRID, linewidth=1.2, transform=fig.transFigure))
fig.text(0.21, 0.9, "버스 환경 (자료조사 2)", ha="center", fontsize=9, color=QUIET)
fig.text(0.70, 0.9, "고령자의 실제 이동 (자료조사 3, 2025년 10월 평일)", ha="center", fontsize=9, color=QUIET)
fig.tight_layout(rect=(0, 0.02, 1, 0.88))
source(fig, "국토교통부·서울·인천·경기 버스 정류장·노선 자료, 서울시·KT 수도권 생활이동(OA-22298·22299·22655), 행정안전부 고령인구현황", y=0.0)
fig.savefig(OUT + "report_fig1_접근성등급별_증거사슬.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

# ------------------------------------------------------------------
# 그림 2. 유형별 규모와 치사율 (자료조사 4)
# ------------------------------------------------------------------
types = ["A", "C", "B", "D"]
names = {"A": "A 우선 검토", "B": "B 사고 예방", "C": "C 이동 편의", "D": "D 유지"}
pop = {"A": 67.8, "B": 86.6, "C": 57.9, "D": 278.5}           # 만 명
far = {"A": 32.0, "B": 14.8, "C": 29.4, "D": 49.9}            # 300m 밖 고령자, 만 명
cfr = {"A": 1.3, "B": 0.7, "C": 1.6, "D": 0.9}                # 사고 100건당 사망
n = {"A": 10, "B": 12, "C": 10, "D": 34}

fig = plt.figure(figsize=(12.5, 4.0))
ax = fig.add_axes([0.04, 0.12, 0.6, 0.62])
rows = [("65세 이상 인구\n490.9만 명", pop), ("정류장 300m 밖 고령자\n126.0만 명", far)]
for yi, (lab, d) in enumerate(rows):
    tot = sum(d.values())
    left = 0
    for t in types:
        w = d[t] / tot * 100
        ax.barh(yi, w, left=left, color=TYPE[t], edgecolor="white", height=0.62)
        if w >= 6:
            ax.text(left + w / 2, yi, f"{names[t].split()[0]}\n{w:.0f}%", ha="center", va="center", fontsize=9,
                    color="white" if t in "AC" else INK, fontweight="bold")
        left += w
ax.set_yticks([0, 1]); ax.set_yticklabels([r[0] for r in rows], fontsize=9.5)
ax.invert_yaxis(); ax.set_xlim(0, 100); ax.set_xticks([])
ax.spines["left"].set_visible(False); ax.spines["bottom"].set_visible(False)
ax.tick_params(axis="y", length=0)
# A+C 강조 괄호
ac_pop = (pop["A"] + pop["C"]) / sum(pop.values()) * 100
ac_far = (far["A"] + far["C"]) / sum(far.values()) * 100
ax.text(0, -0.55, f"접근성 '하' 20곳(A·C형) → 고령인구의 {ac_pop:.0f}%", fontsize=9.5, color=INK, fontweight="bold")
ax.text(0, 1.6, f"접근성 '하' 20곳(A·C형) → 버스가 먼 고령자의 {ac_far:.0f}%", fontsize=9.5, color="#C0392B", fontweight="bold")
ax.legend(handles=[Patch(color=TYPE[t], label=f"{names[t]} ({n[t]}곳)") for t in "ABCD"],
          loc="upper center", bbox_to_anchor=(0.5, -0.32), ncol=4, frameon=False, fontsize=8.5)

ax2 = fig.add_axes([0.72, 0.12, 0.26, 0.62])
vals = [cfr[t] for t in types]
b = ax2.barh([names[t] for t in types], vals, color=[TYPE[t] for t in types], height=0.6)
for bar, v in zip(b, vals):
    ax2.text(v + 0.04, bar.get_y() + bar.get_height() / 2, f"{v:.1f}명", va="center", fontsize=9.5, fontweight="bold",
             bbox=dict(fc="white", ec="none", pad=0.6), zorder=5)
ax2.axvline(1.0, color=QUIET, linestyle="--", linewidth=0.9)
ax2.text(1.02, 3.55, "수도권 1.0", fontsize=8, color=QUIET)
ax2.invert_yaxis(); ax2.set_xlim(0, 2.0); ax2.set_xticks([])
ax2.spines["left"].set_visible(False); ax2.spines["bottom"].set_visible(False); ax2.tick_params(axis="y", length=0)
ax2.set_title("사고 100건당 사망 (치사율)", fontsize=10, fontweight="bold", loc="left", color=INK)

fig.text(0.01, 0.97, f"버스가 불편한 20곳(A·C형)에 고령인구는 {ac_pop:.0f}%뿐이지만, 버스가 먼 고령자는 {ac_far:.0f}%가 산다",
         fontsize=14, fontweight="bold", color=INK, ha="left")
fig.text(0.01, 0.89, "사고 위험(자료조사 1) × 버스 접근성(자료조사 2) 유형별 비중, 2025년 · 치사율은 2023~2025년",
         fontsize=9, color=QUIET, ha="left")
source(fig, "TAAS 노인운전자 교통사고 2023~2025, 행정안전부 고령인구현황, 자료조사 2 접근성 분석", y=-0.12)
fig.savefig(OUT + "extra_유형별_규모와_치사율.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

# ------------------------------------------------------------------
# 그림 3. 우선 검토(A형) 10곳 프로필 (자료조사 4 표)
# ------------------------------------------------------------------
rowsA = [  # 시군구, 사고율, 치사율, 300m안, 배차, 1명당이동, 70+차량, 이중취약, 세부유형
    ("광주시", 62.2, 0.85, 42.7, 56, 2.34, 58, True, "이동 포기형"),
    ("안산시", 55.7, 0.44, 74.3, 48, 2.45, 38, False, "운전 지속형"),
    ("평택시", 55.6, 1.58, 58.0, 59, 2.62, 53, True, "운전 지속형"),
    ("이천시", 53.2, 1.91, 41.1, 117, 2.78, 62, True, "운전 지속형"),
    ("안성시", 53.0, 2.77, 38.6, 151, 2.54, 68, True, "운전 지속형"),
    ("화성시", 52.4, 1.02, 56.5, 64, 3.01, 57, True, "운전 지속형"),
    ("양주시", 48.7, 1.08, 53.9, 50, 2.43, 54, True, "이동 포기형"),
    ("김포시", 48.4, 0.99, 61.4, 27, 2.63, 53, False, "운전 지속형"),
    ("여주시", 46.0, 3.32, 31.5, 150, 2.52, 77, True, "운전 지속형"),
    ("양평군", 44.8, 2.46, 21.9, 187, 2.19, 76, True, "이동 포기형"),
]
core = {"평택시", "이천시", "안성시", "여주시", "양평군"}  # 세 기준 모두 A형
rowsA.sort(key=lambda r: (r[0] not in core, -r[2]))
cols = [("사고율\n(1만 명당)", 1, "high", "{:.1f}", 39.0),
        ("치사율\n(100건당 사망)", 2, "high", "{:.2f}", 1.0),
        ("정류장 300m 안\n고령인구 (%)", 3, "low", "{:.0f}", 74.4),
        ("배차 간격\n중앙값 (분)", 4, "high", "{:.0f}", 30),
        ("70세 이상\n차량 비중 (%)", 6, "high", "{:.0f}", 29.6)]
ref_label = ["66곳 중앙값 39", "수도권 1.0", "수도권 74", "이중 취약 기준 30", "66곳 중앙값 30"]

fig, ax = plt.subplots(figsize=(11, 5.6))
ax.set_xlim(0, 8.2); ax.set_ylim(len(rowsA) + 1.4, -1.3); ax.axis("off")
cmap = plt.get_cmap("Reds")
x0 = 1.6
for j, (h, idx, worse, fmt, ref) in enumerate(cols):
    ax.text(x0 + j * 1.15 + 0.55, -0.6, h, ha="center", va="center", fontsize=9, fontweight="bold", color=INK)
    v = np.array([r[idx] for r in rowsA], float)
    # 수도권 기준값 대비 얼마나 나쁜지로 색칠 (기준보다 좋으면 흰색)
    bad = (v / ref - 1) if worse == "high" else (1 - v / ref)
    lvl = np.clip(bad / np.nanmax([bad.max(), 1e-9]), 0, 1)
    for i, (val, l) in enumerate(zip(v, lvl)):
        ax.add_patch(plt.Rectangle((x0 + j * 1.15, i + 0.05), 1.1, 0.9, color=cmap(0.12 + 0.68 * l) if l > 0 else "#F7F7F7"))
        ax.text(x0 + j * 1.15 + 0.55, i + 0.5, fmt.format(val), ha="center", va="center", fontsize=9.5,
                color="white" if l > 0.6 else INK, fontweight="bold" if l > 0.6 else "normal")
    ax.text(x0 + j * 1.15 + 0.55, len(rowsA) + 0.55, ref_label[j], ha="center", va="center", fontsize=8, color=QUIET)
for i, r in enumerate(rowsA):
    star = "★ " if r[0] in core else "   "
    ax.text(1.5, i + 0.5, star + r[0], ha="right", va="center", fontsize=10,
            fontweight="bold" if r[0] in core else "normal", color="#C0392B" if r[0] in core else INK)
    ax.text(x0 + 5 * 1.15 + 0.15, i + 0.5, r[8] + ("" if r[7] else "  · 이중 취약 아님"), va="center",
            fontsize=9, color=INK if r[8] == "운전 지속형" else "#6B4FA0")
ax.text(x0 + 5 * 1.15 + 0.15, -0.6, "세부 유형 (자료조사 3)", va="center", fontsize=9, fontweight="bold", color=INK)
ax.plot([0.2, 8.1], [5.0, 5.0], color=QUIET, linewidth=0.8, linestyle=":")
ax.text(0.2, len(rowsA) + 0.55, "비교 기준", fontsize=8, color=QUIET, va="center")
fig.text(0.01, 0.98, "우선 검토 10곳 중 평택·이천·안성·여주·양평은 어떤 기준으로 봐도 우선 검토 지역이다",
         fontsize=14, fontweight="bold", color=INK, ha="left")
fig.text(0.01, 0.93, "A형(사고 위험 상위 1/3 + 접근성 '하') 10곳 · ★ = 3분위·중앙값·치사율 기준 모두에서 A형 · 색이 진할수록 수도권 기준보다 나쁨",
         fontsize=9, color=QUIET, ha="left")
source(fig, "자료조사 1(TAAS 2023~2025), 자료조사 2(2025), 자료조사 3(수도권 생활이동 2025년 10월 수요일), 자료조사 4", y=0.03)
fig.savefig(OUT + "extra_우선검토10곳_프로필.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

# ------------------------------------------------------------------
# 그림 4. 결론: 세 지역의 문제와 처방 (자료조사 5)
# ------------------------------------------------------------------
cards = [
    ("서울특별시 송파구", "B형 · 사고 예방 중점", TYPE["B"],
     [("7.7만 명", "65세 이상 면허 소지자\n(서울 최다)"), ("546건", "고령 운전자 사고, 2025\n(서울 2위)"),
      ("89% · 10.9분", "정류장 300m 안 고령인구\n· 배차 간격")],
     "운전하는 고령자가 많아 사고도 많지만,\n대중교통은 충분하다",
     ["1회성 교통카드 → 지속형 대중교통 이용 지원", "안전교육·인지검사와 사고 다발 교차로 개선"]),
    ("경기도 양평군", "A형 · 우선 검토", TYPE["A"],
     [("22%", "정류장 300m 안 고령인구"), ("187분", "버스 배차 간격 중앙값\n(수도권 최장)"),
      ("76%", "70세 이상 이동 중 차량")],
     "버스가 멀고 드물어 운전을 그만둘 수 없고,\n똑버스 운행 근거도 없다",
     ["조건부 면허·페달 오조작 방지장치로 안전 운전", "똑버스 도입, 행복택시 마을(30개) 확대",
      "면허 미보유자 교통비 차등(연 12만 원) 강화"]),
    ("인천광역시 강화군", "C형 · 이동 편의 중점", TYPE["C"],
     [("40.8%", "65세 이상 인구 비율\n(인천 최고)"), ("6.6명", "사고 100건당 사망\n(수도권 1.0명)"),
      ("74%", "70세 이상 이동 중 차량")],
     "사고는 적지만 한 번 나면 치명적이고,\n수요응답형 교통 없이 공공형버스만 있다",
     ["경로당 거점의 병원 연계 수요응답형 교통", "반납자에게 장기 이동 바우처 지급"]),
]
fig = plt.figure(figsize=(13, 6.6))
fig.text(0.01, 0.975, "서울은 '사고', 경기·인천 외곽은 '이동권'이 문제다 — 처방도 달라야 한다",
         fontsize=15, fontweight="bold", color=INK, ha="left")
fig.text(0.01, 0.935, "자료조사 4 유형별 대표 지역 · 지역 → 문제 → 해결", fontsize=9.5, color=QUIET, ha="left")
for k, (name, tlabel, color, stats, problem, fixes) in enumerate(cards):
    x = 0.01 + k * 0.333
    w = 0.315
    ax = fig.add_axes([x, 0.04, w, 0.86]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.03",
                                facecolor="white", edgecolor="#D1D5DB", linewidth=1.2))
    ax.add_patch(FancyBboxPatch((0, 0.86), 1, 0.14, boxstyle="round,pad=0,rounding_size=0.03",
                                facecolor=color, edgecolor=color))
    ax.add_patch(plt.Rectangle((0, 0.86), 1, 0.04, color=color))
    ax.text(0.05, 0.945, name, fontsize=13, fontweight="bold", color="white", va="center")
    ax.text(0.05, 0.885, tlabel, fontsize=9, color="white", va="center")
    for s, (big, small) in enumerate(stats):
        y = 0.76 - s * 0.135
        ax.text(0.05, y, big, fontsize=17, fontweight="bold", color=color if color != TYPE["B"] else "#C77700", va="center")
        ax.text(0.5, y, small, fontsize=8.5, color=QUIET, va="center", linespacing=1.3)
    ax.plot([0.05, 0.95], [0.395, 0.395], color="#E5E7EB", linewidth=1)
    ax.text(0.05, 0.36, "문제", fontsize=9, fontweight="bold", color=INK, va="top")
    ax.text(0.05, 0.315, problem, fontsize=9.3, color=INK, va="top", linespacing=1.45)
    ax.text(0.05, 0.19, "해결", fontsize=9, fontweight="bold", color=INK, va="top")
    for f_i, fx in enumerate(fixes):
        ax.text(0.05, 0.145 - f_i * 0.05, "• " + fx, fontsize=8.8, color=INK, va="top")
source(fig, "자료조사 1~5 (경찰청 운전면허소지자현황 2025.12.31, TAAS 2025, 자료조사 2·3 접근성·생활이동, 지자체 발표)", y=0.02)
fig.savefig(OUT + "report_fig4_결론_3개지역.png", bbox_inches="tight", facecolor="white")
plt.close(fig)
print("done")

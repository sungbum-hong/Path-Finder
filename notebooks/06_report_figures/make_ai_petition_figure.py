import glob
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Polygon, Circle, FancyArrowPatch

for f in (glob.glob("/usr/share/fonts/truetype/nanum/NanumGothic*.ttf")
          + glob.glob(os.path.join(os.path.dirname(__file__), "fonts", "NanumGothic*.ttf"))):
    font_manager.fontManager.addfont(f)
plt.rcParams.update({"font.family": ["NanumGothic", "DejaVu Sans"], "axes.unicode_minus": False, "savefig.dpi": 300})

INK, QUIET, LINE = "#1F2328", "#6B7280", "#D1D5DB"
RED, RED_T = "#C0392B", "#F6D5D1"
BLUE, BLUE_T = "#2F6FDE", "#E3ECFB"
PURPLE = "#8B7BC4"
W, H = 1300, 760
PT = 0.72

fig = plt.figure(figsize=(W / 100, H / 100))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")


def box(x, y, w, h, fc="white", ec=LINE, lw=1.2, r=10, z=1):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z))


def t(x, y, s, size=11, bold=False, color=INK, ha="left", va="baseline", z=5, **kw):
    ax.text(x, y, s, fontsize=size * PT, fontweight="bold" if bold else "normal", color=color,
            ha=ha, va=va, zorder=z, **kw)


def chip(x, y, s, fc=BLUE_T, color=BLUE, size=10.5):
    w = 14 + len(s) * size * 0.95
    box(x, y, w, 24, fc=fc, ec=fc, r=12, z=6)
    t(x + w / 2, y + 16.5, s, size, True, color, ha="center", z=7)
    return w


def arrow(p0, p1, color=QUIET, style="-|>", rad=0.0, lw=1.4, z=4):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=14, color=color, linewidth=lw,
                                 connectionstyle=f"arc3,rad={rad}", zorder=z))


# ---------- 제목 ----------
t(24, 40, "AI 이동 국민신문고: \"여기에 이것이 있었으면\"을 지도에 모아 대체교통 입지를 고른다", 17, True)
t(24, 66, "자료조사 5 정책 제안 개념도 · 데이터 진단(자료조사 2·4·5) + 주민 요청 + AI 분류로 DRT·공공형 택시 후보지를 추천", 10.5, color=QUIET)

# ---------- 기존 지도 vs 제안 ----------
box(24, 86, 600, 74)
t(44, 112, "기존 접근성 지도 (예: Wheelmap)", 11, True, QUIET)
t(44, 140, "\"여기는 이것 덕분에 편해요\"", 13, True, INK)
t(604, 140, "이미 있는 것을 기록", 10, color=QUIET, ha="right")
arrow((632, 123), (664, 123), color=INK, lw=1.8)
box(672, 86, 604, 74, fc=RED_T, ec=RED, lw=1.8)
t(692, 112, "AI 이동 국민신문고 (제안)", 11, True, RED)
t(692, 140, "\"여기에 이것이 있었으면 좋겠어요\"", 13, True, INK)
t(1256, 140, "필요한 것을 모아 입지를 고른다", 10, color=INK, ha="right")

# ---------- 예시 화면 (휴대폰) ----------
px, py, pw, ph = 36, 186, 270, 470
box(px, py, pw, ph, fc="#111827", ec="#111827", r=26)
sx, sy, sw, sh = px + 12, py + 34, pw - 24, ph - 60
box(sx, sy, sw, sh, fc="white", ec="white", r=8, z=2)
t(px + pw / 2, py + 22, "이동 요청 지도", 9.5, True, "white", ha="center")
# 격자 지도
gx0, gy0, cs, nx, ny = sx + 10, sy + 12, 22, 10, 9
vuln = {(6, 1), (7, 1), (6, 2), (7, 2), (8, 2), (7, 3), (8, 3), (2, 6), (3, 6), (2, 7), (3, 7), (4, 7), (7, 6), (8, 7)}
for i in range(nx):
    for j in range(ny):
        c = RED if (i, j) in vuln else "#EEF0F3"
        ax.add_patch(plt.Rectangle((gx0 + i * cs + 1, gy0 + j * cs + 1), cs - 2, cs - 2, color=c,
                                   alpha=0.55 if (i, j) in vuln else 1, zorder=3))
ax.plot([gx0, gx0 + nx * cs], [gy0 + 4.5 * cs, gy0 + 3.2 * cs], color="#9CA3AF", linewidth=3, zorder=3)  # 도로
ax.add_patch(Circle((gx0 + 1.5 * cs, gy0 + 4.2 * cs), 5, color=BLUE, zorder=4))  # 기존 정류장
# 핀
pinx, piny = gx0 + 7.5 * cs, gy0 + 2.5 * cs
ax.add_patch(Polygon([[pinx - 7, piny - 10], [pinx + 7, piny - 10], [pinx, piny + 4]], color=INK, zorder=6))
ax.add_patch(Circle((pinx, piny - 14), 8, color=INK, zorder=6))
ax.add_patch(Circle((pinx, piny - 14), 3.2, color="white", zorder=7))
# 말풍선
bx, by = sx + 10, gy0 + ny * cs + 12
box(bx, by, sw - 20, 58, fc="#F9FAFB", ec=LINE, r=8, z=5)
t(bx + 10, by + 22, "\"마을회관 앞에 똑버스", 10, True, z=6)
t(bx + 10, by + 42, "정류장이 있었으면 좋겠어요\"", 10, True, z=6)
# AI 분류 결과
t(bx, by + 82, "AI 분류", 9.5, True, BLUE)
cy = by + 90
chip(bx, cy, "수단: DRT 정류장")
chip(bx, cy + 30, "목적: 병원·장보기")
chip(bx, cy + 60, "이동취약 격자: 해당", fc=RED_T, color=RED)
t(px + pw / 2, py + ph + 22, "예시 화면 · 실제 데이터 아님", 9.5, color=QUIET, ha="center")
t(gx0, gy0 + ny * cs + 6, "■ 이동취약 격자   ● 기존 정류장", 7.5, color=QUIET, va="top", z=6)

# ---------- 4단계 흐름 ----------
steps = [
    ("1", "진단", "데이터", RED,
     ["100m 격자에 정류장 300m 밖", "고령자를 그리고, 유형(A~D)과", "DRT 공백을 겹쳐", "이동취약 격자를 자동 표시"],
     "AI: 공간 분석"),
    ("2", "요청 수집", "주민 + AI", BLUE,
     ["주민이 지도에 위치를 찍고", "\"여기에 ○○이 있었으면\"을", "남기면, AI가 요청 문장을", "수단별로 분류"],
     "AI: 문장 분류"),
    ("3", "입지 추천", "데이터 × 요청", PURPLE,
     ["요청이 모인 지점 중", "이동취약 격자와 겹치는 곳을", "DRT 권역·행복택시 마을", "후보로 우선 추천"],
     "AI: 우선순위"),
    ("4", "효과 확인", "자료조사 3과 연결", "#2E8B57",
     ["도입 뒤 고령자 차량 이동", "비중이 줄었는지 월별", "생활이동 자료로 확인하고", "결과를 지도에 공개"],
     "지표: 70세 이상 차량 비중"),
]
x0, y0, cw, chh, gap = 340, 196, 218, 268, 22
for k, (num, name, who, col, lines, badge) in enumerate(steps):
    x = x0 + k * (cw + gap)
    box(x, y0, cw, chh, fc="white", ec=col, lw=1.6)
    ax.add_patch(Circle((x + 30, y0 + 32), 16, color=col, zorder=6))
    t(x + 30, y0 + 38, num, 13, True, "white", ha="center", z=7)
    t(x + 56, y0 + 30, name, 14, True)
    t(x + 56, y0 + 50, who, 9.5, color=QUIET)
    for i, ln in enumerate(lines):
        t(x + 18, y0 + 92 + i * 24, ln, 10.5)
    chip(x + 18, y0 + chh - 44, badge, fc="#F3F4F6", color=col, size=9.5)
    if k < 3:
        arrow((x + cw + 2, y0 + chh / 2), (x + cw + gap - 2, y0 + chh / 2), color=INK, lw=1.6)
# 수단 분류 칩 (2단계 아래)
sx2 = x0 + 1 * (cw + gap)
t(sx2, y0 + chh + 31, "분류 예시", 9, True, QUIET)
cx = sx2 + 58
for lab in ["DRT", "공공형 택시", "정류장", "병원 연계"]:
    cx += chip(cx, y0 + chh + 14, lab, size=9) + 6
# 순환 화살표 (4 → 1)
arrow((x0 + 3 * (cw + gap) + cw / 2, y0 + chh + 4), (x0 + cw / 2, y0 + chh + 4), color=QUIET, rad=-0.18, lw=1.3)
t(x0 + 1.5 * (cw + gap) + cw / 2 + 120, y0 + chh + 92, "결과 공개 → 다음 해 진단과 요청에 반영", 10, color=QUIET, ha="center")

# ---------- 초기 적용 지역 ----------
box(340, 600, 936, 60, fc="#F9FAFB", ec=LINE)
t(360, 625, "초기 적용", 11, True, RED)
t(440, 625, "버스 접근성 '하' + 수요응답형 교통 근거를 찾지 못한 7곳 (자료조사 5 그림 2)", 10.5, True)
t(440, 648, "양평 · 가평 · 포천 · 동두천 · 남양주 · 강화 · 옹진  —  정류장 300m 밖 고령자 약 19.0만 명", 10.5, color=INK)

t(24, H - 14, "자료: 자료조사 2(100m 격자 도보 접근성), 자료조사 3(70세 이상 차량 비중), 자료조사 4(지역 유형), 자료조사 5(대체교통 현황). 개념도이며 화면과 요청 문장은 예시.",
  8, color=QUIET)
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs", "figures")
os.makedirs(OUT, exist_ok=True)
fig.savefig(os.path.join(OUT, "report_fig5_AI이동국민신문고_개념도.png"), facecolor="white", bbox_inches="tight")
print("saved")

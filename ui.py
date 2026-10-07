"""Small presentation helpers: a themed header, source cards, and check cards rendered as HTML."""

from __future__ import annotations

import html

import streamlit as st

CSS = """
<style>
#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {visibility:hidden; height:0;}
.block-container {max-width: 960px; padding-top: 2.2rem; padding-bottom: 3rem;}
h1, h2, h3 {font-family: Georgia, "Source Serif 4", serif; letter-spacing: -0.01em;}
.eyebrow {font-size: .78rem; letter-spacing: .14em; text-transform: uppercase; color: #B4561E; font-weight: 700; margin-bottom: .25rem;}
.hero {margin-bottom: .6rem;}
.hero h1 {font-size: 2.3rem; margin: 0 0 .35rem 0; line-height: 1.15;}
.hero p {font-size: 1.05rem; color: #4A5866; margin: 0;}
.infobar {background:#FFFFFF; border:1px solid #DCE1DE; border-left:6px solid #2F7FA6; border-radius:14px; padding: 12px 18px; margin: 12px 0 20px 0; font-size: .97rem; color:#4A5866; line-height: 1.5;}
.card {background:#FFFFFF; border:1px solid #DCE1DE; border-radius:14px; padding:14px 18px; margin:10px 0;}
.card.src {font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .92rem; color:#10212B;}
.card.src .line {display:flex; gap:12px; padding:5px 0; border-bottom:1px dashed #ECEFEC;}
.card.src .line:last-child {border-bottom:none;}
.id {display:inline-block; min-width:44px; text-align:center; background:#EEF2F0; color:#2F7FA6; border-radius:8px; padding:1px 8px; font-size:.8rem; font-weight:700;}
.chk {display:flex; gap:14px; align-items:flex-start; background:#FFFFFF; border:1px solid #DCE1DE; border-left:6px solid #9FB2BA; border-radius:14px; padding:14px 18px; margin:10px 0;}
.chk.ok {border-left-color:#2E8B57;}
.chk.flag {border-left-color:#C8452B; background:#FFF7F5;}
.chk.unknown {border-left-color:#D99A2B; background:#FFFBF2;}
.chk .body {flex:1;}
.chk .text {font-size:1.02rem; line-height:1.45; margin-bottom:4px;}
.chk .meta {font-size:.86rem; color:#4A5866;}
.pill {display:inline-block; font-size:.74rem; font-weight:700; letter-spacing:.06em; text-transform:uppercase; border-radius:999px; padding:4px 10px; white-space:nowrap; margin-top:2px;}
.pill.ok {background:#E4F3EA; color:#1F6B43;}
.pill.flag {background:#FBE3DE; color:#9B2F1C;}
.pill.unknown {background:#FBEFD6; color:#8A5A0E;}
.pill.cite {background:#EEF2F0; color:#4A5866;}
.section {font-size:.8rem; letter-spacing:.12em; text-transform:uppercase; color:#4A5866; font-weight:700; margin:18px 0 6px 0;}
.note {font-size:.9rem; color:#4A5866; margin-top:8px;}
table.rank {width:100%; border-collapse:collapse; background:#fff; border:1px solid #DCE1DE; border-radius:14px; overflow:hidden; font-size:.95rem;}
table.rank th {text-align:left; background:#F0F3F1; color:#4A5866; font-weight:700; padding:10px 14px; font-size:.8rem; letter-spacing:.08em; text-transform:uppercase;}
table.rank td {padding:10px 14px; border-top:1px solid #ECEFEC;}
table.rank tr.top td {background:#EAF4F9; font-weight:700;}
.stTabs [data-baseweb="tab"] {font-size:1rem; padding: 10px 6px;}
.stTabs [aria-selected="true"] {color:#B4561E;}
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def hero(eyebrow: str, title: str, subtitle: str) -> None:
    st.markdown(
        f'<div class="hero"><div class="eyebrow">{html.escape(eyebrow)}</div><h1>{html.escape(title)}</h1>'
        f'<p>{html.escape(subtitle)}</p></div>',
        unsafe_allow_html=True,
    )


def info(text: str) -> None:
    st.markdown(f'<div class="infobar">{html.escape(text)}</div>', unsafe_allow_html=True)


def section(label: str) -> None:
    st.markdown(f'<div class="section">{html.escape(label)}</div>', unsafe_allow_html=True)


def source_card(rows: list[tuple[str, str]]) -> None:
    lines = "".join(f'<div class="line"><span class="id">{html.escape(i)}</span><span>{html.escape(t)}</span></div>' for i, t in rows)
    st.markdown(f'<div class="card src">{lines}</div>', unsafe_allow_html=True)


def check_card(text: str, status: str, meta: str, cite: str | None = None, label: str | None = None) -> None:
    """status: ok | flag | unknown | neutral; label overrides the chip text"""
    label = label or {"ok": "verified", "flag": "flagged", "unknown": "unknown", "neutral": "stated"}[status]
    cite_html = f' <span class="pill cite">cite {html.escape(cite)}</span>' if cite else ""
    st.markdown(
        f'<div class="chk {status}"><div class="body"><div class="text">{html.escape(text)}</div>'
        f'<div class="meta">{html.escape(meta)}{cite_html}</div></div><span class="pill {status}">{label}</span></div>',
        unsafe_allow_html=True,
    )


def rank_table(rows: list[dict]) -> None:
    head = "".join(f"<th>{h}</th>" for h in ["#", "Candidate", "Boltz-2 confidence", "Affinity (pIC50)", "ProteinMPNN score", "Composite"])
    body = ""
    for i, r in enumerate(rows, 1):
        cls = ' class="top"' if i == 1 else ""
        body += (f"<tr{cls}><td>{i}</td><td>{html.escape(r['candidate'])}</td><td>{r['confidence']:.3f}</td>"
                 f"<td>{r['affinity_pIC50']:.2f}</td><td>{r['mpnn_score']:.3f}</td><td>{r['composite']:.4f}</td></tr>")
    st.markdown(f'<table class="rank"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>', unsafe_allow_html=True)

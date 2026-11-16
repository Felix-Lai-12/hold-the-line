"""report.md -> report.html -> report.pdf (headless Chrome)."""
import markdown, pathlib, subprocess, tempfile
D = pathlib.Path(__file__).parent
md = (D / "report.md").read_text()
body = markdown.markdown(md, extensions=["tables", "fenced_code", "md_in_html"])
css = """@page{size:A4;margin:25mm 25mm}body{font-family:'Times New Roman',Georgia,'PingFang TC','Heiti TC',serif;font-size:11pt;line-height:1.35;color:#111}
h1{font-size:16pt;line-height:1.25;margin:0 0 6px}h2{font-size:12.5pt;margin:16px 0 6px}p,li{text-align:justify}
table{border-collapse:collapse;margin:8px 0;font-size:9pt}th,td{border:1px solid #999;padding:3px 6px}th{background:#eee}
img{max-width:100%;display:block;margin:8px auto}.authors{display:flex;gap:48px;margin:6px 0 12px;font-size:10pt}.abstract{border:1px solid #bbb;background:#f6f6f6;padding:6px 12px;margin:8px 0 14px}.small table{font-size:7.5pt}.small td,.small th{padding:2px 4px}.cap{font-size:9pt;color:#333;margin-top:-2px}h3{font-size:11pt;margin:12px 0 4px}code{font-family:Menlo,monospace;font-size:8.5pt}em{color:#333}figure{margin:10px 0}figcaption{font-size:9pt;color:#333;line-height:1.3}.note{font-size:8.5pt;color:#444}.box{border-left:3px solid #999;background:#f6f6f6;padding:4px 10px;margin:8px 0;font-size:9.5pt}figure,.keep{break-inside:avoid;page-break-inside:avoid}h2{break-after:avoid;page-break-after:avoid}"""
html = f"<!doctype html><html><head><meta charset='utf-8'><title>Which Way Does It Lean? (Apart AI x Epistemics Sprint, Nov 2026)</title><style>{css}</style></head><body>{body}</body></html>"
(D / "report.html").write_text(html)
with tempfile.TemporaryDirectory() as prof:
    subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless=new", "--disable-gpu",
                    "--use-mock-keychain", f"--user-data-dir={prof}", "--no-pdf-header-footer",
                    f"--print-to-pdf={D / 'report.pdf'}", (D / "report.html").as_uri()], check=True, timeout=120,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("ok")

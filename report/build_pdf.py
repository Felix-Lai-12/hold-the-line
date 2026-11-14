"""report.md -> report.html -> report.pdf (headless Chrome)."""
import markdown, pathlib, subprocess, tempfile
D = pathlib.Path(__file__).parent
md = (D / "report.md").read_text()
body = markdown.markdown(md, extensions=["tables", "fenced_code"])
css = """@page{size:A4;margin:18mm 17mm}body{font-family:'Times New Roman',Georgia,'PingFang TC','Heiti TC',serif;font-size:10.5pt;line-height:1.38;color:#111}
h1{font-size:16pt;line-height:1.25;margin:0 0 6px}h2{font-size:12.5pt;margin:16px 0 6px}p,li{text-align:justify}
table{border-collapse:collapse;margin:8px 0;font-size:9pt}th,td{border:1px solid #999;padding:3px 6px}th{background:#eee}
img{max-width:100%;display:block;margin:8px auto}code{font-family:Menlo,monospace;font-size:8.5pt}em{color:#333}"""
html = f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{body}</body></html>"
(D / "report.html").write_text(html)
with tempfile.TemporaryDirectory() as prof:
    subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless=new", "--disable-gpu",
                    "--use-mock-keychain", f"--user-data-dir={prof}", "--no-pdf-header-footer",
                    f"--print-to-pdf={D / 'report.pdf'}", (D / "report.html").as_uri()], check=True, timeout=120,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("ok")

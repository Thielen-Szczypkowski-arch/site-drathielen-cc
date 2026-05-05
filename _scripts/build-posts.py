#!/usr/bin/env python3
"""
Gera blog/SLUG.html a partir de cada _posts/blog/SLUG.md
e insere/atualiza o card correspondente em blog/index.html.
"""

import os
import re
import glob
from datetime import datetime

try:
    import yaml
    import markdown as md_lib
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml", "markdown", "-q"])
    import yaml
    import markdown as md_lib

POSTS_DIR   = "_posts/blog"
BLOG_DIR    = "blog"
INDEX_FILE  = "blog/index.html"
HOME_FILE   = "index.html"
BASE_URL    = "https://www.drathielen.com.br"

MESES = {
    1:"janeiro",2:"fevereiro",3:"março",4:"abril",
    5:"maio",6:"junho",7:"julho",8:"agosto",
    9:"setembro",10:"outubro",11:"novembro",12:"dezembro"
}

GLOBAL_CSS = """@font-face{font-family:'Inter';font-style:normal;font-weight:400 500;font-display:swap;src:url('/assets/fonts/inter-latin.woff2') format('woff2')}@font-face{font-family:'Outfit';font-style:normal;font-weight:400 700;font-display:swap;src:url('/assets/fonts/outfit-latin.woff2') format('woff2')}:root{--bronze:#ac9273;--bronze-dark:#8a7358;--bronze-light:#c4ab8e;--bronze-pale:rgba(172,146,115,0.12);--brown:#524334;--cream:#f4f0eb;--cream-light:#f9f7f4;--white:#ffffff;--text-dark:#2a1f14;--text-muted:#7a6a5a;--text-light:#a89880;--wa-green:#25d366;--radius-sm:12px;--radius-md:20px;--radius-lg:32px;--radius-pill:100px;--shadow-sm:0 2px 10px rgba(82,67,52,0.05);--shadow-md:0 8px 28px rgba(82,67,52,0.08);--shadow-lg:0 16px 48px rgba(82,67,52,0.10);--shadow-photo:0 8px 24px rgba(82,67,52,0.07),0 1px 6px rgba(172,146,115,0.05)}*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}body{font-family:'Inter',sans-serif;color:var(--text-dark);background:var(--cream-light);overflow-x:hidden}img{display:block;max-width:100%}h1,h2,h3,h4{font-family:'Outfit',sans-serif;line-height:1.15}h1{font-size:clamp(2.6rem,5.5vw,4.8rem);font-weight:700;letter-spacing:-0.02em}h2{font-size:clamp(1.9rem,3.5vw,2.8rem);font-weight:600}h3{font-size:clamp(1.15rem,1.8vw,1.4rem);font-weight:600}p{line-height:1.75;color:var(--text-muted)}.container{max-width:1500px;margin:0 auto;padding:0 24px}.section-pad{padding:100px 0}.section-pad-top{padding-top:100px}.section-label{font-size:0.68rem;font-weight:600;letter-spacing:0.22em;text-transform:uppercase;color:var(--bronze);display:inline-block;margin-bottom:14px}.badge-pill{display:inline-flex;align-items:center;gap:6px;padding:6px 16px;border-radius:var(--radius-pill);border:1px solid var(--bronze);color:var(--bronze);font-size:0.73rem;font-weight:500;letter-spacing:0.05em}.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:14px 32px;border-radius:var(--radius-pill);font-family:'Inter',sans-serif;font-size:0.875rem;font-weight:600;text-decoration:none;cursor:pointer;border:none;transition:transform 0.2s ease,box-shadow 0.2s ease,background 0.2s ease}.btn:hover{transform:translateY(-2px);box-shadow:var(--shadow-md)}.btn:active{transform:scale(0.97)}.btn-primary{background:var(--bronze);color:var(--white)}.btn-primary:hover{background:var(--bronze-dark)}.btn-outline{background:transparent;color:var(--text-dark);border:1.5px solid rgba(42,31,20,0.22)}.btn-outline:hover{border-color:var(--bronze);color:var(--bronze);box-shadow:none}.btn-dark{background:var(--brown);color:var(--white)}.btn-dark:hover{background:#3d3025}.btn-white{background:var(--white);color:var(--brown)}.btn-sm{padding:10px 22px;font-size:0.8rem}.wave{display:block;width:100%;overflow:hidden;line-height:0;margin-bottom:-2px}.wave svg{display:block;width:100%}.fade-up{opacity:0;transform:translateY(36px);transition:opacity 0.7s cubic-bezier(0.22,1,0.36,1),transform 0.7s cubic-bezier(0.22,1,0.36,1)}.fade-up.visible{opacity:1;transform:translateY(0)}.fade-up:nth-child(2){transition-delay:0.10s}.fade-up:nth-child(3){transition-delay:0.18s}.fade-up:nth-child(4){transition-delay:0.26s}.fade-up:nth-child(5){transition-delay:0.34s}.fade-up:nth-child(6){transition-delay:0.42s}.fade-left{opacity:0;transform:translateX(-40px);transition:opacity 0.7s cubic-bezier(0.22,1,0.36,1),transform 0.7s cubic-bezier(0.22,1,0.36,1)}.fade-left.visible{opacity:1;transform:translateX(0)}.fade-right{opacity:0;transform:translateX(40px);transition:opacity 0.7s cubic-bezier(0.22,1,0.36,1),transform 0.7s cubic-bezier(0.22,1,0.36,1)}.fade-right.visible{opacity:1;transform:translateX(0)}.scale-in{opacity:0;transform:scale(0.92);transition:opacity 0.6s cubic-bezier(0.22,1,0.36,1),transform 0.6s cubic-bezier(0.22,1,0.36,1)}.scale-in.visible{opacity:1;transform:scale(1)}@media (prefers-reduced-motion:reduce){.fade-up,.fade-left,.fade-right,.scale-in{opacity:1;transform:none;transition:none}.fade-up.visible,.fade-left.visible,.fade-right.visible,.scale-in.visible{transition:none}@keyframes waPulse{0%,100%{box-shadow:0 6px 20px rgba(37,211,102,0.4)}}}.skip-link{position:absolute;top:-100%;left:16px;z-index:9999;background:var(--bronze);color:var(--white);padding:10px 20px;border-radius:0 0 var(--radius-sm) var(--radius-sm);font-size:0.85rem;font-weight:600;text-decoration:none;transition:top 0.2s}.skip-link:focus{top:0}:focus-visible{outline:2px solid var(--bronze);outline-offset:3px;border-radius:4px}.btn:focus-visible{outline-offset:4px;border-radius:var(--radius-pill)}.nav-cta:focus-visible{outline-offset:4px;border-radius:var(--radius-pill)}.logo:focus-visible{border-radius:6px}header{position:fixed;top:0;left:0;right:0;z-index:100;padding:20px 0;transition:background 0.35s ease,box-shadow 0.35s ease,padding 0.35s ease}header.scrolled{background:rgba(249,247,244,0.96);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);box-shadow:0 1px 0 rgba(172,146,115,0.15),0 4px 20px rgba(0,0,0,0.05);padding:12px 0}.header-inner{display:flex;align-items:center;justify-content:space-between}.logo{text-decoration:none;display:flex;align-items:center}.logo-img{height:80px;width:auto;display:block;transition:height 0.35s ease}header.scrolled .logo-img{height:60px}nav{display:flex;align-items:center;gap:28px}nav a{font-size:0.8rem;font-weight:500;color:rgba(255,255,255,0.9);text-decoration:none;letter-spacing:0.04em;transition:color 0.2s;cursor:pointer}nav a:hover,nav a.active{color:var(--bronze-light)}.nav-cta{padding:10px 22px;background:var(--bronze);color:var(--white) !important;border-radius:var(--radius-pill);font-size:0.78rem !important;font-weight:600 !important;transition:background 0.2s !important}.nav-cta:hover{background:var(--bronze-dark) !important;transform:none !important}header.scrolled nav a{color:var(--text-muted)}header.scrolled nav a:hover,header.scrolled nav a.active{color:var(--bronze)}header.scrolled .nav-cta{background:var(--bronze) !important}header.scrolled .nav-cta:hover{background:var(--bronze-dark) !important}header.header-dark nav a{color:var(--text-muted)}header.header-dark nav a:hover,header.header-dark nav a.active{color:var(--bronze)}header.header-dark .nav-cta{background:var(--bronze) !important}.hamburger{display:none;flex-direction:column;gap:5px;cursor:pointer;background:none;border:none;padding:4px}.hamburger span{display:block;width:22px;height:2px;background:var(--text-dark);border-radius:2px;transition:all 0.3s}.mobile-menu{display:flex;position:fixed;inset:0;background:var(--cream-light);z-index:99;flex-direction:column;align-items:center;justify-content:center;gap:16px;padding:80px 24px 40px;opacity:0;visibility:hidden;pointer-events:none;transition:opacity 0.28s ease,visibility 0.28s}.mobile-menu.open{opacity:1;visibility:visible;pointer-events:auto}.mobile-menu a{font-family:'Outfit',sans-serif;font-size:1.3rem;color:var(--text-dark);text-decoration:none;font-weight:500;transition:color 0.2s;min-height:44px;display:flex;align-items:center;transform:translateY(12px);opacity:0;transition:color 0.2s,transform 0.35s cubic-bezier(0.22,1,0.36,1),opacity 0.35s}.mobile-menu.open a{transform:translateY(0);opacity:1}.mobile-menu.open a:nth-child(2){transition-delay:0.04s}.mobile-menu.open a:nth-child(3){transition-delay:0.08s}.mobile-menu.open a:nth-child(4){transition-delay:0.12s}.mobile-menu.open a:nth-child(5){transition-delay:0.16s}.mobile-menu.open a:nth-child(6){transition-delay:0.20s}.mobile-menu a:hover{color:var(--bronze)}.mobile-menu .nav-cta{margin-top:8px;padding:13px 36px;background:var(--bronze);color:var(--white) !important;border-radius:var(--radius-pill);font-family:'Inter',sans-serif;font-size:0.88rem !important;font-weight:600;letter-spacing:0.04em}.mobile-menu .nav-cta:hover{background:var(--bronze-dark);color:var(--white) !important}.mobile-close{position:absolute;top:22px;right:22px;background:none;border:none;font-size:1.8rem;cursor:pointer;color:var(--text-dark);min-width:44px;min-height:44px;display:flex;align-items:center;justify-content:center}.page-hero{background:var(--cream-light);padding:160px 0 80px;position:relative;overflow:hidden}.page-hero::before,.article-hero::before{content:'';position:absolute;top:40px;right:8%;z-index:0;width:380px;height:380px;border-radius:50%;background:radial-gradient(circle,rgba(172,146,115,0.09) 0%,transparent 70%);pointer-events:none}.page-hero .container{position:relative;z-index:1}.page-hero-inner{max-width:700px}.breadcrumb{display:flex;align-items:center;gap:8px;margin-bottom:24px;font-size:0.75rem;color:var(--text-light)}.breadcrumb a{color:var(--text-light);text-decoration:none;transition:color 0.2s}.breadcrumb a:hover{color:var(--bronze)}.breadcrumb a{cursor:pointer}.breadcrumb span{color:var(--bronze-light)}.page-hero h1{margin-bottom:20px}.page-hero .lead{font-size:1.05rem;color:var(--text-muted);line-height:1.75;max-width:580px}.page-hero-wave{position:absolute;bottom:-2px;left:0;right:0}.stats-strip{display:flex;border-radius:var(--radius-lg);overflow:hidden;background:var(--white);box-shadow:var(--shadow-sm);border:1px solid rgba(172,146,115,0.12);margin-top:36px}.stat-item{flex:1;text-align:center;padding:20px 14px;border-right:1px solid rgba(172,146,115,0.1)}.stat-item:last-child{border-right:none}.stat-num{display:block;font-family:'Outfit',sans-serif;font-size:1.9rem;font-weight:700;color:var(--bronze);line-height:1;margin-bottom:4px}.stat-label{font-size:0.68rem;color:var(--text-muted);font-weight:500;line-height:1.3}footer{background:var(--brown);padding:60px 0 28px}.footer-inner{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:48px;margin-bottom:44px}.footer-brand .logo{color:var(--white)}.footer-brand .logo span{color:rgba(255,255,255,0.45)}.footer-brand p{font-size:0.82rem;color:rgba(255,255,255,0.5);margin-top:14px;line-height:1.7;max-width:280px}.social-links{display:flex;gap:10px;margin-top:22px}.social-link{width:44px;height:44px;border-radius:12px;border:1px solid rgba(255,255,255,0.18);display:flex;align-items:center;justify-content:center;text-decoration:none;transition:all 0.2s;cursor:pointer}.social-link:hover{background:rgba(255,255,255,0.1);border-color:rgba(255,255,255,0.35)}.social-link svg{width:17px;height:17px;color:rgba(255,255,255,0.65)}.footer-col h4{font-size:0.68rem;font-weight:600;letter-spacing:0.14em;text-transform:uppercase;color:rgba(255,255,255,0.4);margin-bottom:18px;font-family:'Inter',sans-serif}.footer-col a{display:block;font-size:0.83rem;color:rgba(255,255,255,0.7);text-decoration:none;margin-bottom:10px;transition:color 0.2s;padding:2px 0}.footer-col a:hover{color:rgba(255,255,255,0.95)}.footer-bottom{border-top:1px solid rgba(255,255,255,0.09);padding-top:22px;display:flex;align-items:center;justify-content:space-between}.footer-bottom p{font-size:0.72rem;color:rgba(255,255,255,0.55)}.footer-bottom-links{display:flex;gap:18px}.footer-bottom-links a{font-size:0.7rem;color:rgba(255,255,255,0.5);text-decoration:none;min-height:44px;display:flex;align-items:center}.footer-bottom-links a:hover{color:rgba(255,255,255,0.8)}.about-photo img,.strip-photo img,.entry-img img{filter:drop-shadow(0 5px 14px rgba(82,67,52,0.06))}.quick-card{box-shadow:var(--shadow-sm);transition:box-shadow 0.3s ease,transform 0.3s ease}.quick-card:hover{box-shadow:var(--shadow-md);transform:translateY(-4px)}.valor-card{box-shadow:var(--shadow-sm);transition:box-shadow 0.3s ease,transform 0.3s ease}.valor-card:hover{box-shadow:var(--shadow-md);transform:translateY(-4px)}.info-card{box-shadow:var(--shadow-sm);transition:box-shadow 0.3s ease,transform 0.3s ease}.info-card:hover{box-shadow:var(--shadow-md)}.form-box{box-shadow:var(--shadow-md)}.wa-cta-box{box-shadow:var(--shadow-sm)}.map-wrap{box-shadow:var(--shadow-lg)}.galeria-item{box-shadow:var(--shadow-sm);transition:box-shadow 0.3s ease,transform 0.3s ease}.galeria-item:hover{box-shadow:var(--shadow-md);transform:translateY(-4px)}.stats-strip{transition:box-shadow 0.3s ease}.stats-strip:hover{box-shadow:var(--shadow-md)}#cookie-banner{position:fixed;bottom:0;left:0;right:0;z-index:200;background:rgba(30,22,14,0.97);backdrop-filter:blur(12px);padding:18px 32px;display:flex;align-items:center;justify-content:space-between;gap:24px;box-shadow:0 -4px 24px rgba(0,0,0,0.18);transform:translateY(100%);transition:transform 0.4s cubic-bezier(0.22,1,0.36,1)}#cookie-banner.visible{transform:translateY(0)}#cookie-banner p{font-size:0.82rem;color:rgba(255,255,255,0.72);margin:0;max-width:680px;line-height:1.6}#cookie-banner p a{color:var(--bronze-light);text-decoration:underline}.cookie-btns{display:flex;gap:10px;flex-shrink:0}.cookie-btn-accept{padding:9px 22px;background:var(--bronze);color:var(--white);border:none;border-radius:var(--radius-pill);font-size:0.8rem;font-weight:600;cursor:pointer;transition:background 0.2s;font-family:'Inter',sans-serif;white-space:nowrap}.cookie-btn-accept:hover{background:var(--bronze-dark)}.cookie-btn-decline{padding:9px 18px;background:transparent;color:rgba(255,255,255,0.5);border:1px solid rgba(255,255,255,0.2);border-radius:var(--radius-pill);font-size:0.8rem;cursor:pointer;transition:all 0.2s;font-family:'Inter',sans-serif;white-space:nowrap}.cookie-btn-decline:hover{color:rgba(255,255,255,0.8);border-color:rgba(255,255,255,0.4)}@media (max-width:600px){#cookie-banner{flex-direction:column;padding:20px 20px;text-align:center}.cookie-btns{width:100%;justify-content:center}}.wa-float{position:fixed;bottom:26px;right:26px;z-index:150;width:58px;height:58px;border-radius:50%;background:var(--wa-green);display:flex;align-items:center;justify-content:center;box-shadow:0 6px 20px rgba(37,211,102,0.4);text-decoration:none;transition:transform 0.3s ease;animation:waPulse 2.8s infinite}.wa-float:hover{transform:scale(1.1);animation:none;box-shadow:0 8px 28px rgba(37,211,102,0.5)}.wa-float svg{width:30px;height:30px;color:white}@keyframes waPulse{0%,100%{box-shadow:0 6px 20px rgba(37,211,102,0.4),0 0 0 0 rgba(37,211,102,0.35)}55%{box-shadow:0 6px 20px rgba(37,211,102,0.4),0 0 0 14px rgba(37,211,102,0)}}.lightbox{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.92);z-index:200;align-items:center;justify-content:center}.lightbox.open{display:flex}.lightbox img{max-width:88vw;max-height:88vh;object-fit:contain;border-radius:10px}.lightbox-close{position:absolute;top:18px;right:22px;background:none;border:none;color:white;font-size:1.8rem;cursor:pointer;line-height:1;opacity:0.7;transition:opacity 0.2s}.lightbox-close:hover{opacity:1}.lightbox-prev,.lightbox-next{position:absolute;top:50%;transform:translateY(-50%);background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.18);color:white;font-size:1.4rem;cursor:pointer;padding:12px 15px;border-radius:12px;transition:background 0.2s}.lightbox-prev:hover,.lightbox-next:hover{background:rgba(255,255,255,0.18)}.lightbox-prev{left:14px}.lightbox-next{right:14px}@media (max-width:1024px){nav{display:none}.hamburger{display:flex}.footer-inner{grid-template-columns:1fr 1fr}}@media (max-width:768px){h1{font-size:2.2rem}h2{font-size:1.7rem}.section-pad{padding:70px 0}.footer-inner{grid-template-columns:1fr 1fr;gap:28px}.footer-bottom{flex-direction:column;gap:10px;text-align:center}.page-hero{padding:130px 0 60px}}@media (max-width:600px){.footer-inner{grid-template-columns:1fr}}@media (max-width:480px){.container{padding:0 16px}.btn{padding:13px 26px}}"""

ARTICLE_CSS = """.article-hero{background:var(--cream-light);padding:140px 0 0;position:relative}.article-hero-inner{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:stretch}.article-hero-text{padding-bottom:60px;display:flex;flex-direction:column;justify-content:center}.article-hero-img-wrap{display:flex;align-items:flex-end}.article-hero-img{width:100%;border-radius:0;overflow:hidden;background:var(--cream-light);height:480px}.article-hero-img img{width:100%;height:100%;object-fit:cover;object-position:center top;display:block}.article-body{background:var(--white);padding:80px 0 100px;margin-top:-1px}.article-layout{display:grid;grid-template-columns:1fr 280px;gap:56px;align-items:start}.article-content{}.article-content h2{font-size:1.6rem;margin:40px 0 16px}.article-content h3{font-size:1.2rem;margin:32px 0 12px;font-family:'Inter',sans-serif;font-weight:600}.article-content p{margin-bottom:20px;font-size:0.95rem;line-height:1.85}.article-content ul{padding-left:24px;margin-bottom:20px}.article-content li{font-size:0.93rem;color:var(--text-muted);line-height:1.75;margin-bottom:8px}.article-content blockquote{border-left:3px solid var(--bronze);padding:16px 24px;margin:28px 0;background:var(--cream-light);border-radius:0 12px 12px 0}.article-content blockquote p{margin:0;font-style:italic;color:var(--text-dark)}.article-content table{width:100%;border-collapse:collapse;margin:28px 0;font-size:0.88rem;border-radius:12px;overflow:hidden;box-shadow:var(--shadow-sm)}.article-content thead tr{background:var(--bronze);color:#fff}.article-content th{padding:12px 16px;text-align:left;font-weight:600;font-size:0.78rem;letter-spacing:0.04em;text-transform:uppercase}.article-content td{padding:11px 16px;color:var(--text-muted);border-bottom:1px solid rgba(172,146,115,0.1)}.article-content tbody tr:last-child td{border-bottom:none}.article-content tbody tr:nth-child(even){background:var(--cream-light)}.article-content tbody tr:hover{background:var(--cream)}.article-meta{display:flex;align-items:center;gap:16px;margin-bottom:28px;flex-wrap:wrap}.article-tag{font-size:0.68rem;background:var(--bronze);color:#fff;padding:4px 12px;border-radius:100px;font-weight:600}.article-tag-secondary{font-size:0.68rem;background:var(--bronze-pale);color:var(--bronze);padding:4px 12px;border-radius:100px;font-weight:600;border:1px solid rgba(172,146,115,0.25)}.article-tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:20px;padding-top:20px;border-top:1px solid rgba(172,146,115,0.12)}.article-date{font-size:0.75rem;color:var(--text-light)}.article-cta{background:var(--cream);border-radius:20px;padding:32px;margin:48px 0 0;text-align:center}.article-cta h3{font-size:1.3rem;margin-bottom:10px}.article-cta p{margin-bottom:20px;max-width:440px;margin-left:auto;margin-right:auto}.back-link{display:inline-flex;align-items:center;gap:6px;font-size:0.8rem;color:var(--bronze);text-decoration:none;font-weight:600;margin-bottom:32px}.article-sidebar{position:sticky;top:88px}.sidebar-widget{background:var(--cream-light);border-radius:16px;padding:24px;margin-bottom:20px;border:1px solid rgba(172,146,115,0.12)}.sidebar-widget-title{font-family:'Outfit',sans-serif;font-size:0.72rem;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:var(--bronze);margin-bottom:16px}.sidebar-cat-list{list-style:none;padding:0;margin:0}.sidebar-cat-list li{border-bottom:1px solid rgba(172,146,115,0.1)}.sidebar-cat-list li:last-child{border-bottom:none}.sidebar-cat-list a{display:flex;align-items:center;justify-content:space-between;padding:9px 0;font-size:0.82rem;color:var(--text-muted);text-decoration:none;transition:color 0.2s}.sidebar-cat-list a:hover{color:var(--bronze)}.sidebar-cat-list a.active{color:var(--bronze);font-weight:600}.sidebar-cat-count{font-size:0.7rem;background:var(--bronze-pale);color:var(--bronze);padding:2px 8px;border-radius:100px;font-weight:600}.sidebar-tags{display:flex;flex-wrap:wrap;gap:6px}.sidebar-tag{font-size:0.72rem;background:var(--white);color:var(--text-muted);padding:5px 12px;border-radius:100px;border:1px solid rgba(172,146,115,0.2);text-decoration:none;transition:all 0.2s;font-weight:500}.sidebar-tag:hover{background:var(--bronze-pale);color:var(--bronze);border-color:rgba(172,146,115,0.35)}.post-nav{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:48px;padding-top:32px;border-top:1px solid rgba(172,146,115,0.12)}.post-nav-item{display:flex;flex-direction:column;gap:4px;padding:16px 20px;background:var(--cream-light);border-radius:12px;text-decoration:none;border:1px solid rgba(172,146,115,0.12);transition:all 0.2s}.post-nav-item:hover{border-color:var(--bronze);background:var(--bronze-pale)}.post-nav-item.next{text-align:right}.post-nav-label{font-size:0.68rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:var(--bronze)}.post-nav-title{font-size:0.82rem;color:var(--text-dark);font-weight:500;line-height:1.4}.post-nav-item.prev .post-nav-label::before{content:'← '}.post-nav-item.next .post-nav-label::after{content:' →'}@media(max-width:900px){.article-layout{grid-template-columns:1fr}.article-sidebar{position:static}.sidebar-widget{padding:20px}}@media(max-width:768px){.article-hero-inner{grid-template-columns:1fr;align-items:start}.article-hero-text{padding-bottom:32px;display:block}.article-hero-img-wrap{display:block}.article-hero-img{border-radius:0}.article-hero-img img{height:auto;min-height:0}}@media(max-width:600px){.post-nav{grid-template-columns:1fr}}"""

HEADER_HTML = """<header id="header" class="header-dark">
  <div class="container">
    <div class="header-inner">
      <a href="/" class="logo"><img src="../assets/logo-original.webp" alt="Dra. Thielen Szczypkowski" class="logo-img" width="529" height="226"></a>
      <nav><a href="/sobre">Sobre</a><a href="/tratamentos">Tratamentos</a><a href="/blog/" class="active">Blog</a><a href="/contato">Contato</a><a href="/contato" class="nav-cta">Agendar consulta</a></nav>
      <button class="hamburger" id="hamburger" aria-label="Menu"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="mobile-menu" id="mobileMenu">
  <button class="mobile-close" id="mobileClose">&#x2715;</button>
  <a href="/sobre">Sobre</a><a href="/tratamentos">Tratamentos</a><a href="/blog/">Blog</a><a href="/contato">Contato</a><a href="/contato" class="nav-cta">Agendar consulta</a>
</div>"""

FOOTER_HTML = """<div class="wave" style="background:#ffffff"><svg viewBox="0 0 1440 80" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none"><path d="M0,40 C360,80 1080,0 1440,40 L1440,80 L0,80 Z" fill="#524334"/></svg></div>
<footer><div class="container"><div class="footer-inner"><div class="footer-brand"><a href="/" class="logo"><img src="../assets/logo-branco.webp" alt="Dra. Thielen Szczypkowski" class="logo-img" width="529" height="226"></a><p>Cirurgiã Vascular especialista em Flebologia Estética. Santo André, SP.</p></div><div class="footer-col"><h4>Navegação</h4><a href="/sobre">Sobre</a><a href="/tratamentos">Tratamentos</a><a href="/blog/">Blog</a><a href="/contato">Contato</a></div><div class="footer-col"><h4>Estética das Pernas</h4><a href="/blog/uso-meias">Meias de compressão</a><a href="/blog/anticoncepcional">Anticoncepcional e varizes</a><a href="/blog/varizes-verao">Varizes no verão</a><a href="/blog/sintomas-varizes">Sintomas de varizes</a><a href="/blog/laser-endovenoso">Laser endovenoso</a></div><div class="footer-col"><h4>Informações úteis</h4><a href="tel:+5511943211890">+55 (11) 94321-1890</a><a href="mailto:contato@drathielen.com.br">contato@drathielen.com.br</a></div></div><div class="footer-bottom"><p>Copyright &copy; 2026 Dra. Thielen Szczypkowski. · CRM-SP 99.530</p><div class="footer-bottom-links"><a href="/politica-de-privacidade">Política de Privacidade</a></div></div></div></footer>
<a href="https://wa.me/5511943211890?text=Ol%C3%A1!" target="_blank" rel="noopener noreferrer" class="wa-float" aria-label="WhatsApp"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg></a>
<script src="../js/main.js" defer></script>"""

GTM_HEAD = """<!-- Google Tag Manager (delayed) -->
<script>window.addEventListener('load',function(){setTimeout(function(){var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtm.js?id=GTM-PZK9GKW';document.head.appendChild(s);window.dataLayer=window.dataLayer||[];window.dataLayer.push({'gtm.start':new Date().getTime(),event:'gtm.js'});},2000)});</script>
<!-- End Google Tag Manager (delayed) -->"""

GTM_BODY = """<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PZK9GKW"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""


def parse_frontmatter(text):
    """Extrai frontmatter YAML e corpo Markdown."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', text, re.DOTALL)
    if not match:
        return {}, text
    meta = yaml.safe_load(match.group(1)) or {}
    body = match.group(2)
    return meta, body


def slugify(filename):
    return os.path.splitext(os.path.basename(filename))[0]


def format_date_br(date_val):
    """Converte date/string para '22 de abril de 2026'."""
    if isinstance(date_val, str):
        try:
            date_val = datetime.strptime(date_val[:10], "%Y-%m-%d").date()
        except ValueError:
            return str(date_val)
    return f"{date_val.day} de {MESES[date_val.month]} de {date_val.year}"


def format_date_iso(date_val):
    if isinstance(date_val, str):
        return date_val[:10]
    return date_val.strftime("%Y-%m-%d")


def build_tags_html(tags_val):
    """Converte campo tags (string 'a, b' ou lista) em HTML de chips."""
    if not tags_val:
        return ""
    if isinstance(tags_val, str):
        tags = [t.strip() for t in tags_val.split(",") if t.strip()]
    else:
        tags = [str(t).strip() for t in tags_val if str(t).strip()]
    if not tags:
        return ""
    chips = "".join(f'<span class="article-tag article-tag-secondary">{t}</span>' for t in tags)
    return f'<div class="article-tags">{chips}</div>'


def build_post_html(meta, body_md, slug, sidebar_html_str="", post_nav_html=""):
    title       = meta.get("title", "Post")
    description = meta.get("description", "")
    lead        = meta.get("lead", "")
    category    = meta.get("category", "Saúde Vascular")
    tags_val    = meta.get("tags", "")
    image       = meta.get("image", "")
    image_alt   = meta.get("image_alt", title)
    cta_title   = meta.get("cta_title", "Quer avaliar seu caso?")
    cta_text    = meta.get("cta_text", "Agende uma avaliação vascular.")
    date_val    = meta.get("date", "")
    date_br     = format_date_br(date_val) if date_val else ""
    date_iso    = format_date_iso(date_val) if date_val else ""
    post_url    = f"{BASE_URL}/blog/{slug}"

    # Imagem: remove caminho relativo se vier com ../assets/ ou /assets/
    image_path  = re.sub(r'^(\.\.\/)?assets\/', '', image) if image else ""
    image_full  = f"{BASE_URL}/assets/{image_path}" if image_path else ""
    image_src   = f"../assets/{image_path}" if image_path else ""

    tags_html = build_tags_html(tags_val)

    body_html = md_lib.markdown(body_md, extensions=["extra"])

    wa_text = f"Olá! Li o artigo sobre {title.lower()} e gostaria de agendar uma avaliação."
    import urllib.parse
    wa_url = f"https://wa.me/5511943211890?text={urllib.parse.quote(wa_text)}"

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8"><meta name="theme-color" content="#ac9273">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{description}">
  <title>{title} | Blog Dra. Thielen</title>
  <meta property="og:type" content="article">
  <meta property="og:title" content="{title} | Blog Dra. Thielen">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{post_url}">
  <meta property="og:image" content="{image_full}">
  <meta property="og:locale" content="pt_BR">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="canonical" href="{post_url}">
  <style>{GLOBAL_CSS}</style>
  <style>{ARTICLE_CSS}</style>
  <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title} | Blog Dra. Thielen",
  "description": "{description}",
  "image": "{image_full}",
  "datePublished": "{date_iso}",
  "author": {{
    "@type": "Physician",
    "name": "Dra. Thielen Szczypkowski",
    "url": "https://www.drathielen.com.br/sobre.html"
  }},
  "publisher": {{
    "@type": "MedicalBusiness",
    "name": "Dra. Thielen Szczypkowski — Cirurgia Vascular",
    "url": "https://www.drathielen.com.br"
  }},
  "mainEntityOfPage": "{post_url}"
}}
  </script>
{GTM_HEAD}
</head>
<body>
{GTM_BODY}
{HEADER_HTML}

<section class="article-hero">
  <div class="container">
    <div class="article-hero-inner">
      <div class="article-hero-text">
        <div class="breadcrumb fade-up"><a href="/">Início</a><span>/</span><a href="/blog/">Blog</a><span>/</span><span>{title}</span></div>
        <div class="article-meta fade-up"><span class="article-tag">{category}</span><span class="article-date">{date_br}</span></div>
        <h1 class="fade-up">{title}</h1>
        <p class="lead fade-up" style="margin-top:20px;">{lead}</p>
      </div>
      {("<div class='article-hero-img-wrap fade-right'><div class='article-hero-img'><img src='" + image_src + "' alt='" + image_alt + "'></div></div>") if image_src else "<div></div>"}
    </div>
  </div>
  <div class="page-hero-wave wave"><svg viewBox="0 0 1440 80" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none"><path d="M0,40 C360,80 1080,0 1440,40 L1440,80 L0,80 Z" fill="#ffffff"/></svg></div>
</section>

<section class="article-body">
  <div class="container">
    <div class="article-layout">
    <div class="article-content">
      <a href="/blog/" class="back-link">← Voltar ao Blog</a>
      {body_html}
      {post_nav_html}
      {tags_html}
      <div class="article-cta">
        <h3>{cta_title}</h3>
        <p>{cta_text}</p>
        <a href="{wa_url}" target="_blank" rel="noopener noreferrer" class="btn btn-primary">Agendar avaliação</a>
      </div>
    </div>
    {sidebar_html_str}
    </div>
  </div>
</section>

{FOOTER_HTML}
</body>
</html>"""
    return html


def build_card_html(meta, slug):
    title    = meta.get("title", "Post")
    lead     = meta.get("lead", "")
    category = meta.get("category", "Saúde Vascular")
    image    = meta.get("image", "")
    date_val = meta.get("date", "")
    date_br  = format_date_br(date_val) if date_val else ""

    image_path = re.sub(r'^(\.\.\/)?assets\/', '', image) if image else ""
    image_src  = f"/assets/{image_path}" if image_path else ""
    title_esc  = title.replace('"', '&quot;')
    lead_esc   = lead[:100] + "…" if len(lead) > 100 else lead

    img_tag = f'<img src="{image_src}" alt="{title_esc}" loading="lazy">' if image_src else ""

    return f"""<!-- POST:{slug} -->
<a href="/blog/{slug}" class="blog-card fade-up">
  <div class="blog-thumb">{img_tag}</div>
  <div class="blog-body">
    <div class="blog-meta">
      <span class="blog-date">{date_br}</span>
      <span class="blog-tag">{category}</span>
    </div>
    <h3>{title}</h3>
    <p>{lead_esc}</p>
    <span class="blog-read">Ler mais →</span>
  </div>
</a>
<!-- /POST:{slug} -->"""


def update_index(card_html, slug):
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = rf'<!-- POST:{re.escape(slug)} -->.*?<!-- /POST:{re.escape(slug)} -->'
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, card_html, content, flags=re.DOTALL)
    else:
        # Insere antes do fechamento da blog-grid
        marker = "<!-- /BLOG-GRID -->"
        if marker in content:
            content = content.replace(marker, card_html + "\n" + marker)
        else:
            # Fallback: insere antes de </section> da listagem
            content = content.replace("</div>\n</section>", f"{card_html}\n</div>\n</section>", 1)

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(content)


def build_home_card_html(meta, slug, delay):
    title    = meta.get("title", "Post")
    lead     = meta.get("lead", "")
    category = meta.get("category", "Saúde Vascular")
    image    = meta.get("image", "")

    image_path = re.sub(r'^(\.\.\/)?assets\/', '', image) if image else ""
    image_src  = f"/assets/{image_path}" if image_path else ""
    title_esc  = title.replace('"', '&quot;')
    lead_esc   = lead[:140] + "…" if len(lead) > 140 else lead

    img_tag = f'<img src="{image_src}" alt="{title_esc}" loading="lazy">' if image_src else ""

    return f"""      <a href="/blog/{slug}" class="blog-card fade-up" style="text-decoration:none;transition-delay:{delay}s">
        <div class="blog-thumb">
          {img_tag}
        </div>
        <div class="blog-body">
          <p class="blog-date">{category}</p>
          <h3>{title}</h3>
          <p>{lead_esc}</p>
          <span class="blog-read">Ler artigo →</span>
        </div>
      </a>"""


def update_home_cards(all_posts_meta):
    """Regenera os 4 cards da home com os posts mais recentes."""
    if not os.path.exists(HOME_FILE):
        return
    # all_posts_meta vem ordenado por data asc — inverte e pega os 4 mais recentes com lead+image
    posts = [p for p in all_posts_meta if p.get("title") and p.get("lead") and p.get("image")]
    posts = list(reversed(posts))
    top4 = posts[:4]

    delays = ["0.08", "0.16", "0.24", "0.32"]
    cards = []
    for i, p in enumerate(top4):
        meta = {
            "title":    p.get("title", ""),
            "lead":     p.get("lead", ""),
            "category": p.get("cat", p.get("category", "Saúde Vascular")),
            "image":    p.get("image", ""),
        }
        cards.append(build_home_card_html(meta, p["slug"], delays[i] if i < 4 else "0.32"))

    block = "<!-- HOME-CARDS-START -->\n" + "\n".join(cards) + "\n      <!-- HOME-CARDS-END -->"

    with open(HOME_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r'<!-- HOME-CARDS-START -->.*?<!-- HOME-CARDS-END -->'
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, block, content, flags=re.DOTALL)
        with open(HOME_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Home: cards atualizados com {len(top4)} posts mais recentes")
    else:
        print("Home: marcadores HOME-CARDS-START/END não encontrados, pulando")


SITEMAP_FILE = "sitemap.xml"


def update_sitemap(post_paths):
    """Insere ou atualiza entradas de posts novos no sitemap.xml."""
    from datetime import date as _date
    today = _date.today().strftime("%Y-%m-%d")

    with open(SITEMAP_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    for post_path in post_paths:
        slug = slugify(post_path)
        url = f"{BASE_URL}/blog/{slug}"
        entry = f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>"

        if f"<loc>{url}</loc>" in content:
            content = re.sub(
                rf'(<loc>{re.escape(url)}</loc>\s*<lastmod>)[^<]*(</lastmod>)',
                rf'\g<1>{today}\g<2>',
                content
            )
        else:
            content = content.replace("</urlset>", entry + "\n\n</urlset>")

    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write(content)


CAT_ORDER = ["Saúde Vascular", "Tratamentos", "Estética", "Prevenção", "Dicas"]
MESES_NUM = {"janeiro":1,"fevereiro":2,"março":3,"abril":4,"maio":5,"junho":6,
             "julho":7,"agosto":8,"setembro":9,"outubro":10,"novembro":11,"dezembro":12}


def collect_all_posts_meta():
    """Lê todos os .md e .html do blog para montar sidebar e navegação."""
    import re as _re
    all_posts = []

    # Posts do CMS (.md)
    for p in glob.glob(os.path.join(POSTS_DIR, "*.md")):
        slug = slugify(p)
        with open(p, encoding="utf-8") as f:
            raw = f.read()
        meta, _ = parse_frontmatter(raw)
        if not meta.get("title"):
            continue
        tags_raw = meta.get("tags", "")
        tags = [t.strip() for t in tags_raw.split(",")] if isinstance(tags_raw, str) else [str(t) for t in tags_raw]
        all_posts.append({
            "slug": slug, "title": meta.get("title",""), "date": str(meta.get("date","")),
            "cat": meta.get("category",""), "tags": [t for t in tags if t],
            "lead": meta.get("lead",""), "image": meta.get("image","")
        })

    # Posts HTML existentes
    for p in glob.glob(os.path.join(BLOG_DIR, "*.html")):
        s = os.path.splitext(os.path.basename(p))[0]
        if s in ("index", "TEMPLATE"):
            continue
        with open(p, encoding="utf-8") as f:
            content = f.read()
        m = _re.search(r'<span class="article-date">([^<]+)</span>', content)
        date_str = m.group(1) if m else ""
        m2 = _re.search(r'<span class="article-tag">([^<]+)</span>', content)
        cat = m2.group(1) if m2 else ""
        tags = _re.findall(r'<span class="article-tag-secondary">([^<]+)</span>', content)
        m3 = _re.search(r'<h1[^>]*>([^<]+)</h1>', content)
        title = m3.group(1).strip() if m3 else s
        # Evita duplicar post que já existe como .md
        if not any(x["slug"] == s for x in all_posts):
            all_posts.append({"slug": s, "title": title, "date": date_str, "cat": cat, "tags": tags})

    def sort_key(p):
        import re as _r
        m = _r.match(r'(\d+) de (\w+) de (\d+)', p["date"])
        if m:
            return (int(m.group(3)), MESES_NUM.get(m.group(2), 0), int(m.group(1)))
        try:
            return tuple(int(x) for x in p["date"][:10].split("-"))
        except Exception:
            return (0, 0, 0)

    all_posts.sort(key=sort_key)
    return all_posts


def build_sidebar_html(all_posts, active_cat, active_tags):
    cat_counts = {}
    all_tags = {}
    for p in all_posts:
        cat_counts[p["cat"]] = cat_counts.get(p["cat"], 0) + 1
        for t in p["tags"]:
            all_tags[t] = all_tags.get(t, 0) + 1

    cats = [c for c in CAT_ORDER if c in cat_counts] + [c for c in cat_counts if c not in CAT_ORDER]
    cat_items = ""
    for c in cats:
        a = ' class="active"' if c == active_cat else ""
        cat_items += f'<li><a href="/blog/?cat={c.lower().replace(" ","-")}"{a}>{c}<span class="sidebar-cat-count">{cat_counts[c]}</span></a></li>'

    tag_items = ""
    for t, _ in sorted(all_tags.items(), key=lambda x: -x[1]):
        style = ' style="background:var(--bronze-pale);color:var(--bronze);border-color:rgba(172,146,115,0.35)"' if t in active_tags else ""
        tag_items += f'<a href="/blog/?tag={t.replace(" ","-")}" class="sidebar-tag"{style}>{t}</a>'

    return f'<aside class="article-sidebar"><div class="sidebar-widget"><p class="sidebar-widget-title">Categorias</p><ul class="sidebar-cat-list">{cat_items}</ul></div><div class="sidebar-widget"><p class="sidebar-widget-title">Tags</p><div class="sidebar-tags">{tag_items}</div></div></aside>'


def build_post_nav_html(all_posts, slug):
    idx = next((i for i, p in enumerate(all_posts) if p["slug"] == slug), None)
    if idx is None:
        return ""
    prev_p = all_posts[idx - 1] if idx > 0 else None
    next_p = all_posts[idx + 1] if idx < len(all_posts) - 1 else None

    def shorten(t): return t[:60] + "…" if len(t) > 60 else t

    prev_html = f'<a href="/blog/{prev_p["slug"]}" class="post-nav-item prev"><span class="post-nav-label">Anterior</span><span class="post-nav-title">{shorten(prev_p["title"])}</span></a>' if prev_p else '<div></div>'
    next_html = f'<a href="/blog/{next_p["slug"]}" class="post-nav-item next"><span class="post-nav-label">Próximo</span><span class="post-nav-title">{shorten(next_p["title"])}</span></a>' if next_p else ''

    return f'<nav class="post-nav" aria-label="Navegação entre posts">{prev_html}{next_html}</nav>'


def main():
    posts = glob.glob(os.path.join(POSTS_DIR, "*.md"))
    if not posts:
        print("Nenhum post encontrado em", POSTS_DIR)
        return

    all_posts_meta = collect_all_posts_meta()

    for post_path in posts:
        slug = slugify(post_path)
        with open(post_path, "r", encoding="utf-8") as f:
            raw = f.read()

        meta, body_md = parse_frontmatter(raw)
        if not meta.get("title"):
            print(f"Pulando {post_path} — sem título no frontmatter")
            continue

        # Monta sidebar e navegação
        tags_raw = meta.get("tags", "")
        tags_list = [t.strip() for t in tags_raw.split(",")] if isinstance(tags_raw, str) else [str(t) for t in tags_raw]
        sidebar = build_sidebar_html(all_posts_meta, meta.get("category", ""), tags_list)
        post_nav = build_post_nav_html(all_posts_meta, slug)

        # Gera HTML do post
        post_html = build_post_html(meta, body_md, slug, sidebar_html_str=sidebar, post_nav_html=post_nav)
        out_path  = os.path.join(BLOG_DIR, f"{slug}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(post_html)
        print(f"Gerado: {out_path}")

        # Atualiza card no index
        card_html = build_card_html(meta, slug)
        update_index(card_html, slug)
        print(f"Card atualizado no index: {slug}")

    update_sitemap(posts)
    print("Sitemap atualizado")

    update_home_cards(all_posts_meta)


if __name__ == "__main__":
    main()

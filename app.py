import base64
import glob
import hashlib
import hmac
import html
import io
import json
import os
import urllib.parse
from datetime import date

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

BRAND = "Luxe By Madiha"
STATUSES = ["New", "Packed", "Shipped", "Delivered", "Returned", "Cancelled"]
LOW_STOCK = 2
PHONE_LOCAL = "03363488291"
PHONE_INTL = "923363488291"
WA_LINK = f"https://wa.me/{PHONE_INTL}?text=" + urllib.parse.quote("Hi Luxe By Madiha, I want to know about your new arrivals.")
KHAADI_URL = "https://www.khaadi.com/pk/"

# ======================= EDIT THESE (your shop details) =======================
TAGLINE = "Authentic Khaadi pret, chosen with love."
INSTAGRAM_URL = "https://www.instagram.com/luxebymadihaa/"   # e.g. "https://www.instagram.com/yourpage"  (leave empty to hide)
FACEBOOK_URL = "https://www.facebook.com/madisonlinestore"    # e.g. "https://www.facebook.com/yourpage"  (leave empty to hide)
DELIVERY_INFO = "Delivery time and charges depend on your city or country. Message us on WhatsApp and we will confirm both before you order."
PAYMENT_INFO = "Message us on WhatsApp to confirm the payment options available for your order."
RETURN_INFO = "Please message us on WhatsApp before ordering to confirm exchange and return details."
WHY_US = [
    ("✅", "Authentic branded stock", "Real Khaadi ready-to-wear pieces."),
    ("💬", "Easy WhatsApp ordering", "Send a message, we confirm size and availability."),
    ("📦", "Carefully packed", "Every order is checked and packed with care."),
]
CATEGORIES = ["Khaadi Pret", "Festive", "Casual", "Formal"]
# Add REAL customer reviews only, like: ("Ayesha", "Beautiful suit, exactly as shown!")
REVIEWS = []
# ==============================================================================

st.set_page_config(page_title=BRAND, page_icon="👗", layout="wide")
st.markdown(f'<div style="text-align:center;font-weight:700;font-size:18px;">📞 Contact / WhatsApp: <a href="{WA_LINK}" target="_blank">{PHONE_LOCAL}</a></div>', unsafe_allow_html=True)
WA_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#ffffff"><path d="'
    'M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z'
    '"/></svg>'
)
WA_ICON = "data:image/svg+xml;base64," + base64.b64encode(WA_SVG.encode("utf-8")).decode("ascii")
WA_BUTTON = (
    f'<a href="{WA_LINK}" target="_blank" title="Chat on WhatsApp" '
    'style="position:fixed;bottom:24px;right:24px;z-index:9999;width:56px;height:56px;'
    'border-radius:50%;background:#25D366;display:flex;align-items:center;justify-content:center;'
    'box-shadow:0 4px 12px rgba(0,0,0,0.3);">'
    f'<img src="{WA_ICON}" width="32" height="32" alt="WhatsApp"></a>'
)
st.markdown(WA_BUTTON, unsafe_allow_html=True)

STYLE = (
    "<style>"
    ".stMarkdown h1,.stMarkdown h2,.stMarkdown h3,.stMarkdown h4{text-align:center;font-weight:800;}"
    "[data-testid='stHeading']{text-align:center;}"
    "div[data-baseweb='tab-list']{justify-content:center;}"
    "button[data-baseweb='tab'] p{font-weight:700;}"
    ".stLinkButton a,.stButton button,.stDownloadButton button,[data-testid^='stBaseLinkButton']{font-weight:700;}"
    ".stLinkButton a p,.stButton button p,.stDownloadButton button p{font-weight:700;}"
    "</style>"
)
st.markdown(STYLE, unsafe_allow_html=True)

HERO = (
    '<div style="background:linear-gradient(135deg,#F3E6D8,#FFF8F0);border:1px solid #E6D3B8;'
    'border-radius:16px;padding:32px 24px;text-align:center;margin-bottom:16px;">'
    '<div style="font-size:13px;letter-spacing:3px;color:#B8860B;">BRANDED READY-TO-WEAR</div>'
    f'<div style="font-size:40px;font-weight:700;color:#3A2A1E;margin:8px 0;">👗 {BRAND}</div>'
    f'<div style="font-size:18px;color:#5a4636;">{TAGLINE}</div></div>'
)
st.markdown(HERO, unsafe_allow_html=True)

top_buttons = [("💬 Order on WhatsApp", WA_LINK), ("🛍️ Official Khaadi site", KHAADI_URL)]
if INSTAGRAM_URL:
    top_buttons.append(("📸 Instagram", INSTAGRAM_URL))
if FACEBOOK_URL:
    top_buttons.append(("👍 Facebook", FACEBOOK_URL))
for col, (label, url) in zip(st.columns(len(top_buttons)), top_buttons):
    col.link_button(label, url, use_container_width=True)

cols = st.columns(len(WHY_US))
for col, (icon, title, text) in zip(cols, WHY_US):
    col.markdown(
        '<div style="background:#FFFFFF;border:1px solid #E6D3B8;border-radius:12px;padding:16px;'
        f'text-align:center;height:130px;"><div style="font-size:28px;">{icon}</div>'
        f'<div style="font-weight:700;color:#3A2A1E;margin-top:4px;">{title}</div>'
        f'<div style="font-size:14px;color:#5a4636;margin-top:4px;">{text}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("#### Browse by category")
cat_cols = st.columns(len(CATEGORIES))
for col, cat in zip(cat_cols, CATEGORIES):
    cat_link = f"https://wa.me/{PHONE_INTL}?text=" + urllib.parse.quote(f"Hi {BRAND}, I am interested in {cat}.")
    col.link_button(f"✨ {cat}", cat_link, use_container_width=True)
st.write("")


def empty_orders():
    return pd.DataFrame({
        "Date": pd.Series(dtype="str"), "Customer": pd.Series(dtype="str"),
        "Phone": pd.Series(dtype="str"), "Product": pd.Series(dtype="str"),
        "Qty": pd.Series(dtype="int"), "Price": pd.Series(dtype="float"),
        "Paid": pd.Series(dtype="bool"), "Status": pd.Series(dtype="str"),
    })


def empty_stock():
    return pd.DataFrame({
        "Product": pd.Series(dtype="str"), "Brand": pd.Series(dtype="str"),
        "Size": pd.Series(dtype="str"), "Colour": pd.Series(dtype="str"),
        "Buy Price": pd.Series(dtype="float"), "Sell Price": pd.Series(dtype="float"),
        "In Stock": pd.Series(dtype="int"),
    })


def empty_catalog():
    return pd.DataFrame({
        "Photo": pd.Series(dtype="str"), "Name": pd.Series(dtype="str"), "Price": pd.Series(dtype="str"),
    })


TABLES = {"stock": empty_stock, "orders": empty_orders, "catalog": empty_catalog}


def coerce_types(loaded, empty_fn):
    base = empty_fn()
    loaded = loaded.fillna("")
    for col in base.columns:
        if col not in loaded.columns:
            loaded[col] = ""
    loaded = loaded[list(base.columns)].copy()
    for col in base.columns:
        kind = base[col].dtype.kind
        if kind == "f":
            loaded[col] = pd.to_numeric(loaded[col], errors="coerce").fillna(0.0)
        elif kind == "i":
            loaded[col] = pd.to_numeric(loaded[col], errors="coerce").fillna(0).astype(int)
        elif kind == "b":
            loaded[col] = loaded[col].astype(str).str.lower().isin(["true", "1", "yes"])
        else:
            loaded[col] = loaded[col].astype(str)
    return loaded.reset_index(drop=True)


def stock_label(row):
    return " | ".join(str(row[c]) for c in ("Product", "Size", "Colour") if str(row[c]).strip())


def find_stock_index(stock_df, label):
    for i, r in stock_df.iterrows():
        if stock_label(r) == label:
            return i
    return None


def take_from_stock(stock_df, label, qty):
    """Reduce stock for an order. Returns (new_df, found, had_before)."""
    i = find_stock_index(stock_df, label)
    if i is None:
        return stock_df, False, 0
    new_df = stock_df.copy()
    had = int(new_df.loc[i, "In Stock"])
    new_df.loc[i, "In Stock"] = max(had - int(qty), 0)
    return new_df, True, had


def put_back_in_stock(stock_df, label, qty):
    """Add pieces back after a cancelled or returned order. Returns (new_df, found)."""
    i = find_stock_index(stock_df, label)
    if i is None:
        return stock_df, False
    new_df = stock_df.copy()
    new_df.loc[i, "In Stock"] = int(new_df.loc[i, "In Stock"]) + int(qty)
    return new_df, True


# ---------------- Google Sheets storage (optional) ----------------
@st.cache_resource
def _spreadsheet():
    import gspread

    info = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT_JSON"])
    client = gspread.service_account_from_dict(info)
    return client.open_by_key(st.secrets["SHEET_ID"])


def sheets_status():
    try:
        _ = st.secrets["GOOGLE_SERVICE_ACCOUNT_JSON"]
        _ = st.secrets["SHEET_ID"]
    except Exception:
        return False, "Google Sheets is not connected, so data is kept only while this page is open."
    try:
        _spreadsheet()
        return True, "Connected to Google Sheets. Your changes are saved automatically."
    except Exception as e:
        return False, f"Could not connect to Google Sheets: {e}"


SHEETS_READY, SHEETS_MSG = sheets_status()


def _worksheet(name, header):
    import gspread

    sh = _spreadsheet()
    try:
        return sh.worksheet(name)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title=name, rows=200, cols=max(len(header), 8))
        ws.update(values=[header], range_name="A1", value_input_option="RAW")
        return ws


def sheet_load(name, empty_fn):
    base = empty_fn()
    header = list(base.columns)
    ws = _worksheet(name, header)
    values = ws.get_all_values()
    if len(values) <= 1:
        return base
    head = values[0]
    width = len(head)
    rows = [(r + [""] * width)[:width] for r in values[1:]]
    return coerce_types(pd.DataFrame(rows, columns=head), empty_fn)


def sheet_save(name, df):
    header = list(df.columns)
    ws = _worksheet(name, header)
    data = [header] + df.fillna("").astype(str).values.tolist()
    if ws.row_count < len(data) + 20:
        ws.resize(rows=len(data) + 50)
    if ws.col_count < len(header):
        ws.resize(cols=len(header))
    ws.clear()
    ws.update(values=data, range_name="A1", value_input_option="RAW")


def table_hash(df):
    return hashlib.md5(df.fillna("").astype(str).to_csv(index=False).encode("utf-8")).hexdigest()


@st.cache_data(ttl=120, show_spinner=False)
def public_catalog():
    """Photo -> (name, price), shown to every visitor under the slideshow.
    Read from Google Sheets if connected, otherwise from catalog.csv in the GitHub repo."""
    try:
        if SHEETS_READY:
            df = sheet_load("catalog", empty_catalog)
        elif os.path.exists("catalog.csv"):
            df = coerce_types(pd.read_csv("catalog.csv", dtype=str), empty_catalog)
        else:
            return {}
    except Exception:
        return {}
    return {r["Photo"]: (r["Name"], r["Price"]) for _, r in df.iterrows() if r["Photo"]}


def ensure_tables(owner):
    for key, fn in TABLES.items():
        if key not in st.session_state:
            df0 = fn()
            if key == "catalog" and not SHEETS_READY and os.path.exists("catalog.csv"):
                try:
                    df0 = coerce_types(pd.read_csv("catalog.csv", dtype=str), fn)
                except Exception:
                    pass
            st.session_state[key] = df0
            st.session_state["hash_" + key] = table_hash(df0)
        if owner and SHEETS_READY and not st.session_state.get("synced_" + key) and not st.session_state.get("loaderr_" + key):
            try:
                df = sheet_load(key, fn)
                st.session_state[key] = df
                st.session_state["hash_" + key] = table_hash(df)
                st.session_state["synced_" + key] = True
            except Exception as e:
                st.session_state["loaderr_" + key] = str(e)


def persist(key):
    """Save a table to Google Sheets when it has changed (owner only)."""
    if not (OWNER and SHEETS_READY and st.session_state.get("synced_" + key)):
        return
    df = st.session_state[key]
    h = table_hash(df)
    if h != st.session_state.get("hash_" + key):
        try:
            sheet_save(key, df)
            st.session_state["hash_" + key] = h
            if key == "catalog":
                public_catalog.clear()
        except Exception as e:
            st.warning(f"Could not save to Google Sheets: {e}")


def storage_note(tag):
    if SHEETS_READY:
        st.caption("☁️ " + SHEETS_MSG)
        errs = [st.session_state.get("loaderr_" + k) for k in TABLES if st.session_state.get("loaderr_" + k)]
        if errs:
            st.error(f"Could not load your saved data: {errs[0]}")
        if st.button("🔄 Reload from Google Sheets", key=f"reload_{tag}"):
            for k in TABLES:
                st.session_state.pop("synced_" + k, None)
                st.session_state.pop("loaderr_" + k, None)
            st.rerun()
    else:
        st.warning(SHEETS_MSG + " Download your CSV before closing.")


def csv_restore(key, label, empty_fn, bool_cols=()):
    up = st.file_uploader(label, type="csv", key=f"up_{key}")
    if up is not None and st.button("Load uploaded file", key=f"load_{key}"):
        loaded = pd.read_csv(up, dtype=str).fillna("")
        st.session_state[key] = coerce_types(loaded, empty_fn)
        st.rerun()


@st.cache_data
def load_slides():
    files = []
    for ext in ("jpg", "jpeg", "png", "webp", "JPG", "JPEG", "PNG", "WEBP"):
        files += glob.glob(f"images/*.{ext}") + glob.glob(f"*.{ext}")
    slides = []
    for f in sorted(set(files)):
        try:
            img = Image.open(f).convert("RGB")
            img.thumbnail((600, 600))
            buf = io.BytesIO()
            img.save(buf, "JPEG", quality=65)
            data = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
            slides.append((f.split("/")[-1], data))
        except Exception:
            continue
    return slides


SLIDE_TEMPLATE = """
<style>
 .box{position:relative;max-width:520px;margin:auto;font-family:sans-serif}
 .s{display:none;text-align:center} .s.on{display:block}
 .s img{width:100%;max-height:520px;object-fit:contain;border-radius:12px}
 .n{margin-top:8px;font-size:18px;font-weight:700;color:#3A2A1E}
 .p{font-size:16px;color:#B8860B;margin-top:2px}
 .o{display:inline-block;margin-top:10px;padding:10px 22px;background:#25D366;color:#fff;
    text-decoration:none;border-radius:24px;font-weight:600}
 .b{position:absolute;top:35%;background:rgba(0,0,0,.45);color:#fff;border:0;font-size:22px;
    padding:6px 12px;cursor:pointer;border-radius:50%}
</style>
<div class="box">__ITEMS__
 <button class="b" style="left:6px" onclick="go(-1)">&#10094;</button>
 <button class="b" style="right:6px" onclick="go(1)">&#10095;</button>
</div>
<script>
 var i=0, s=document.querySelectorAll('.s');
 function show(){s.forEach(function(e,k){e.classList.toggle('on',k===i)})}
 function go(n){i=(i+n+s.length)%s.length;show()}
 show(); setInterval(function(){go(1)},4000);
</script>"""


def slideshow_html(slides, catalog):
    parts = []
    for n, (fname, data) in enumerate(slides, 1):
        name, price = catalog.get(fname, ("", ""))
        label = name or f"the item in photo {n}"
        text = f"Hi {BRAND}, I want to order: {label}" + (f" ({price})" if price else "")
        link = f"https://wa.me/{PHONE_INTL}?text=" + urllib.parse.quote(text)
        cap = ""
        if name:
            cap += f'<div class="n">{html.escape(name)}</div>'
        if price:
            cap += f'<div class="p">{html.escape(price)}</div>'
        parts.append(
            f'<div class="s"><img src="{data}">{cap}'
            f'<a class="o" href="{link}" target="_blank">💬 Order this</a></div>'
        )
    return SLIDE_TEMPLATE.replace("__ITEMS__", "".join(parts))


def owner_unlocked():
    try:
        real = str(st.secrets["OWNER_PASSWORD"])
    except Exception:
        real = ""
    with st.sidebar:
        st.markdown("### 🔒 Owner login")
        entered = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Owner password")
        if not entered:
            return False
        if not real:
            st.warning("Owner password is not set in Streamlit Secrets yet.")
            return False
        ok = hmac.compare_digest(entered.encode("utf-8"), real.encode("utf-8"))
        if ok:
            st.success("Owner mode is on ✅")
        else:
            st.error("Wrong password")
        return ok


OWNER = owner_unlocked()
ensure_tables(OWNER)

if OWNER:
    tab_new, tab_info, tab_about, tab_dash, tab_cat, tab1, tab2, tab3, tab4 = st.tabs(
        ["🆕 New Arrivals", "ℹ️ Info & FAQ", "📖 About this app", "📊 Dashboard", "🖼️ Catalog",
         "💰 Price & Profit", "🧵 Stock", "📦 Orders", "✍️ Caption Maker"]
    )
else:
    tab_new, tab_info, tab_about = st.tabs(["🆕 New Arrivals", "ℹ️ Info & FAQ", "📖 About this app"])

# ---------------- Tab 0: New Arrivals slideshow ----------------
with tab_new:
    st.subheader("New arrivals at Luxe By Madiha")
    slides = load_slides()
    if slides:
        components.html(slideshow_html(slides, public_catalog()), height=760)
    else:
        st.info(
            "No photos yet. Create a folder named `images` in your GitHub repo and upload "
            "photos of your own stock (jpg or png). They will start playing here as a slideshow."
        )
    b1, b2 = st.columns(2)
    b1.link_button("🛍️ See official Khaadi website", KHAADI_URL, use_container_width=True)
    b2.link_button("💬 Order on WhatsApp", WA_LINK, use_container_width=True)
    if REVIEWS:
        st.markdown("#### What our customers say")
        rc = st.columns(min(len(REVIEWS), 3))
        for i, (who, text) in enumerate(REVIEWS):
            rc[i % len(rc)].markdown(
                '<div style="background:#FFFFFF;border:1px solid #E6D3B8;border-radius:12px;padding:14px;'
                f'margin-bottom:10px;"><div style="color:#B8860B;">★★★★★</div>'
                f'<div style="color:#3A2A1E;margin:6px 0;">{text}</div>'
                f'<div style="font-size:13px;color:#5a4636;">— {who}</div></div>',
                unsafe_allow_html=True,
            )

# ---------------- Info & FAQ ----------------
with tab_info:
    st.subheader("Delivery, payment and returns")
    st.markdown(f"**🚚 Delivery:** {DELIVERY_INFO}")
    st.markdown(f"**💳 Payment:** {PAYMENT_INFO}")
    st.markdown(f"**🔁 Returns and exchange:** {RETURN_INFO}")

    st.subheader("Size guide")
    st.write(
        "Sizes can differ between styles. For the best fit, measure yourself and send us the numbers on WhatsApp. "
        "We will confirm the right size before you order."
    )
    st.markdown(
        "- **Bust:** measure around the fullest part, keeping the tape level.\n"
        "- **Waist:** measure around the narrowest part.\n"
        "- **Hips:** measure around the fullest part.\n"
        "- **Shirt length:** from the top of the shoulder down to where you want the hem."
    )
    size_msg = urllib.parse.quote(f"Hi {BRAND}, I need help choosing a size. My measurements: bust __, waist __, hips __, length __.")
    st.link_button("📏 Send my measurements on WhatsApp", f"https://wa.me/{PHONE_INTL}?text={size_msg}")

    st.subheader("Frequently asked questions")
    with st.expander("How do I place an order?"):
        st.write("Send us a message on WhatsApp with the photo of the piece you like and your size. We confirm availability, price and delivery, then you confirm your order.")
    with st.expander("Are the pieces original?"):
        st.write("We sell genuine branded ready-to-wear stock.")
    with st.expander("What if my size is not shown?"):
        st.write("Message us on WhatsApp. Stock changes often, so we will check what is available.")
    with st.expander("How long does delivery take?"):
        st.write(DELIVERY_INFO)
    with st.expander("How can I pay?"):
        st.write(PAYMENT_INFO)
    with st.expander("Can I return or exchange?"):
        st.write(RETURN_INFO)

# ---------------- About this app ----------------
with tab_about:
    st.subheader("About this app")
    st.markdown(
        """
**Luxe By Madiha Manager** is a small web app for a ready-to-wear clothing seller. It gives customers an easy
way to see new arrivals and order on WhatsApp, and gives the shop owner one place to run the business.

#### The problem
Small online clothing sellers often keep stock, orders and prices in chats, notebooks and memory. This makes it hard to:
- know what price to set once delivery, packaging and ads are counted,
- know which sizes and pieces are left,
- remember who has paid and which orders are still to be packed or shipped,
- show customers the latest pieces with a price and a quick way to order.

#### Who it is for
Independent sellers on Instagram, Facebook and WhatsApp who sell branded or ready-made clothing and do not
need a full online store.

#### The solution
- **For customers:** a slideshow of new arrivals with name, price and an Order button that opens WhatsApp with the product already written, plus delivery info, size help and FAQs.
- **For the owner (password protected):** price and profit calculator, stock tracker with low-stock alerts, order and payment tracker, a daily dashboard, a photo catalog and an Instagram caption maker.
- **Saved data:** stock and orders can be downloaded as CSV files (or saved automatically to the owner's Google Sheet when connected). The photo catalog is read from a simple catalog file.

#### How it is built
Python and Streamlit, Google Sheets for storage, and free hosting on Streamlit Community Cloud.

#### Ideas for the future
- Reduce stock automatically when an order is added.
- Monthly sales and profit reports.
- Customer records for repeat buyers and new-arrival messages.
- Order slips as PDF.
- A possible plan model: a free basic version for new sellers and a paid version with saved data, reports and several staff logins.
        """
    )

# Everything below is for the shop owner only.
if not OWNER:
    st.stop()

# ---------------- Tab 1: Price & Profit ----------------
with tab1:
    st.subheader("What price should I put on this piece?")
    c1, c2 = st.columns(2)
    with c1:
        buy = st.number_input("Buying price per piece (Rs)", min_value=0.0, value=4500.0, step=100.0)
        packaging = st.number_input("Packaging (Rs)", min_value=0.0, value=150.0, step=50.0)
        delivery = st.number_input("Delivery cost you pay (Rs)", min_value=0.0, value=250.0, step=50.0)
    with c2:
        ads = st.number_input("Ads / boost cost per order (Rs)", min_value=0.0, value=200.0, step=50.0)
        fees = st.number_input("COD / payment fees (Rs)", min_value=0.0, value=100.0, step=50.0)
        other = st.number_input("Other costs (Rs)", min_value=0.0, value=0.0, step=50.0)

    margin = st.slider("Profit margin you want (%)", 5, 150, 30)
    discount = st.slider("Sale discount you plan to give (%)", 0, 60, 0)

    cost = buy + packaging + delivery + ads + fees + other
    price = round(cost * (1 + margin / 100), -1)
    sale_price = price * (1 - discount / 100)
    profit = price - cost
    profit_sale = sale_price - cost

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total cost per piece", f"Rs {cost:,.0f}")
    m2.metric("Suggested price", f"Rs {price:,.0f}")
    m3.metric("Profit per piece", f"Rs {profit:,.0f}")
    m4.metric("Real margin", f"{(profit / price * 100) if price else 0:.0f}%")
    if discount:
        if profit_sale < 0:
            st.error(f"At {discount}% off (Rs {sale_price:,.0f}) you lose Rs {-profit_sale:,.0f} per piece.")
        else:
            st.info(f"At {discount}% off (Rs {sale_price:,.0f}) you still make Rs {profit_sale:,.0f} per piece.")

# ---------------- Tab 2: Stock ----------------
with tab2:
    st.subheader("My stock")
    with st.form("add_stock", clear_on_submit=True):
        s1, s2, s3, s4 = st.columns(4)
        sp = s1.text_input("Product", placeholder="Embroidered 3-piece")
        sb = s2.text_input("Brand", placeholder="e.g. Khaadi")
        ss = s3.text_input("Size", placeholder="S / M / L")
        sc = s4.text_input("Colour")
        t1, t2, t3 = st.columns(3)
        s_buy = t1.number_input("Buy price (Rs)", min_value=0.0, value=0.0, step=100.0)
        s_sell = t2.number_input("Sell price (Rs)", min_value=0.0, value=0.0, step=100.0)
        s_qty = t3.number_input("Pieces in stock", min_value=0, value=1, step=1)
        if st.form_submit_button("➕ Add to stock", use_container_width=True):
            if sp:
                row = pd.DataFrame([{
                    "Product": sp, "Brand": sb, "Size": ss, "Colour": sc,
                    "Buy Price": float(s_buy), "Sell Price": float(s_sell), "In Stock": int(s_qty),
                }])
                st.session_state["stock"] = pd.concat([st.session_state["stock"], row], ignore_index=True)
            else:
                st.warning("Please enter the product name.")

    st.session_state["stock"] = st.data_editor(
        st.session_state["stock"], num_rows="dynamic", use_container_width=True, key="stock_editor"
    )
    persist("stock")
    sdf = st.session_state["stock"]
    pieces = int(sdf["In Stock"].sum()) if len(sdf) else 0
    stock_cost = float((sdf["In Stock"] * sdf["Buy Price"]).sum()) if len(sdf) else 0.0
    stock_sales = float((sdf["In Stock"] * sdf["Sell Price"]).sum()) if len(sdf) else 0.0
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Pieces in stock", pieces)
    k2.metric("Money tied up (cost)", f"Rs {stock_cost:,.0f}")
    k3.metric("If all sold", f"Rs {stock_sales:,.0f}")
    k4.metric("Expected profit", f"Rs {stock_sales - stock_cost:,.0f}")

    if len(sdf):
        low = sdf[sdf["In Stock"] <= LOW_STOCK]
        if len(low):
            st.warning(f"Low or finished stock ({len(low)} items): " + ", ".join(
                f"{r['Product']} {r['Size']} ({int(r['In Stock'])} left)" for _, r in low.iterrows()))

    storage_note("stock")
    st.download_button("⬇️ Download stock (CSV)", sdf.to_csv(index=False).encode("utf-8"),
                       file_name="luxe_stock.csv", mime="text/csv")
    csv_restore("stock", "Upload saved stock (CSV)", empty_stock)

# ---------------- Tab 3: Orders ----------------
with tab3:
    st.subheader("Orders")
    flash = st.session_state.pop("order_msg", None)
    if flash:
        getattr(st, flash[0])(flash[1])

    OTHER = "Other (type the name below)"
    stock_labels = [stock_label(r) for _, r in st.session_state["stock"].iterrows()]
    with st.form("add_order", clear_on_submit=True):
        a1, a2 = st.columns(2)
        customer = a1.text_input("Customer name")
        phone = a2.text_input("Phone / WhatsApp")
        p1, p2 = st.columns(2)
        pick = p1.selectbox("Product from your stock", [OTHER] + stock_labels)
        custom = p2.text_input("Or type a product name", placeholder="Only if it is not in your stock list")
        b1, b2, b3, b4 = st.columns(4)
        o_qty = b1.number_input("Qty", min_value=1, value=1, step=1)
        o_price = b2.number_input("Price per piece (Rs)", min_value=0.0, value=0.0, step=100.0,
                                  help="Leave 0 to use the sell price from your stock list.")
        o_paid = b3.checkbox("Paid")
        o_status = b4.selectbox("Status", STATUSES)
        if st.form_submit_button("➕ Add order", use_container_width=True):
            product = custom.strip() if pick == OTHER else pick
            if customer and product:
                price = float(o_price)
                stock_note_text = ""
                stock_df = st.session_state["stock"]
                if pick != OTHER:
                    idx = find_stock_index(stock_df, pick)
                    if idx is not None and price == 0:
                        price = float(stock_df.loc[idx, "Sell Price"])
                row = pd.DataFrame([{
                    "Date": str(date.today()), "Customer": customer, "Phone": phone,
                    "Product": product, "Qty": int(o_qty), "Price": price,
                    "Paid": bool(o_paid), "Status": o_status,
                }])
                st.session_state["orders"] = pd.concat([st.session_state["orders"], row], ignore_index=True)
                kind, text = "success", "Order added."
                if pick != OTHER and o_status not in ("Cancelled", "Returned"):
                    new_stock, found, had = take_from_stock(stock_df, pick, int(o_qty))
                    if found:
                        st.session_state["stock"] = new_stock
                        if int(o_qty) > had:
                            kind, text = "warning", f"Order added, but you only had {had} in stock, so stock is now 0."
                        else:
                            text = f"Order added. Stock reduced by {int(o_qty)}."
                st.session_state["order_msg"] = (kind, text)
                persist("orders")
                persist("stock")
                st.rerun()
            else:
                st.warning("Please enter the customer name and choose or type a product.")

    st.session_state["orders"] = st.data_editor(
        st.session_state["orders"], num_rows="dynamic", use_container_width=True,
        column_config={
            "Status": st.column_config.SelectboxColumn(options=STATUSES),
            "Paid": st.column_config.CheckboxColumn(),
        },
        key="orders_editor",
    )
    persist("orders")
    df = st.session_state["orders"]
    active = df[~df["Status"].isin(["Cancelled", "Returned"])] if len(df) else df
    amount = active["Qty"] * active["Price"] if len(active) else pd.Series(dtype="float")
    total = float(amount.sum()) if len(active) else 0.0
    received = float(amount[active["Paid"] == True].sum()) if len(active) else 0.0
    o1, o2, o3, o4 = st.columns(4)
    o1.metric("Active orders", len(active))
    o2.metric("Total sales", f"Rs {total:,.0f}")
    o3.metric("Received", f"Rs {received:,.0f}")
    o4.metric("Pending payment", f"Rs {total - received:,.0f}")
    if len(df):
        st.bar_chart(df["Status"].value_counts())

    st.markdown("**Cancel or return an order and put it back in stock**")
    st.caption("If you only change the Status inside the table above, stock is not changed. Use this instead.")
    open_orders = df[~df["Status"].isin(["Cancelled", "Returned"])] if len(df) else df
    choices = {
        f"{r['Customer']} | {r['Product']} x{int(r['Qty'])} ({r['Date']})": i for i, r in open_orders.iterrows()
    }
    if choices:
        r1, r2, r3 = st.columns([3, 1, 1])
        chosen = r1.selectbox("Order", list(choices), key="restock_pick")
        new_status = r2.selectbox("Mark as", ["Cancelled", "Returned"], key="restock_status")
        r3.write("")
        if r3.button("Update and restock", key="restock_btn"):
            oi = choices[chosen]
            orders_df = st.session_state["orders"].copy()
            label = orders_df.loc[oi, "Product"]
            qty = int(orders_df.loc[oi, "Qty"])
            orders_df.loc[oi, "Status"] = new_status
            st.session_state["orders"] = orders_df
            new_stock, found = put_back_in_stock(st.session_state["stock"], label, qty)
            if found:
                st.session_state["stock"] = new_stock
                st.session_state["order_msg"] = ("success", f"Marked as {new_status}. {qty} piece(s) put back in stock.")
            else:
                st.session_state["order_msg"] = ("info", f"Marked as {new_status}. This product is not in your stock list, so stock was not changed.")
            persist("orders")
            persist("stock")
            st.rerun()
    else:
        st.write("No open orders.")

    storage_note("orders")
    st.download_button("⬇️ Download orders (CSV)", df.to_csv(index=False).encode("utf-8"),
                       file_name="luxe_orders.csv", mime="text/csv")
    csv_restore("orders", "Upload saved orders (CSV)", empty_orders)

# ---------------- Tab 4: Caption Maker ----------------
with tab4:
    st.subheader("Instagram caption maker")
    p1, p2 = st.columns(2)
    name = p1.text_input("Product name", placeholder="Rose Embroidered 3-Piece")
    colour = p2.text_input("Colour", placeholder="Dusty Rose")
    q1, q2, q3 = st.columns(3)
    kind = q1.selectbox("Type", ["Khaadi", "Ethnic", "Lawn", "Formal", "Bridal", "Casual"])
    cap_price = q2.text_input("Price", placeholder="Rs 7,500")
    occasion = q3.selectbox("Occasion", ["Everyday", "Eid", "Wedding", "Party", "Festive"])
    sizes = st.text_input("Sizes available (optional)", placeholder="S, M, L")
    wa = st.text_input("Your WhatsApp number (optional, with country code)", value=PHONE_INTL)

    if st.button("✨ Make captions", use_container_width=True):
        if not name:
            st.warning("Please enter the product name.")
        else:
            col = f" in {colour}" if colour else ""
            pr = f"\n💸 Price: {cap_price}" if cap_price else ""
            sz = f"\n📏 Sizes: {sizes}" if sizes else ""
            order_line = "📩 DM or WhatsApp to order"
            tags = (f"#LuxeByMadiha #{kind}Suit #{occasion}Collection #PakistaniFashion "
                    "#ReadyToWear #PretWear #DesiFashion #ShopLocal #WomenFashion #OOTD")
            captions = [
                f"✨ Meet the {name}{col}.\nReady to wear and made for {occasion.lower()} moments.{pr}{sz}\n{order_line}",
                f"Elegance, ready when you are. 💫\n{name}{col} is now at {BRAND}.{pr}{sz}\nLimited stock, so grab yours before it's gone.\n{order_line}",
                f"New in at {BRAND} 🤍\n{name}{col}: graceful, ready to wear and made to stand out at your next {occasion.lower()} event.{pr}{sz}\n{order_line}",
            ]
            for i, c in enumerate(captions, 1):
                st.markdown(f"**Option {i}**")
                st.code(c + "\n\n" + tags, language=None)
            if wa:
                msg = urllib.parse.quote(f"Hi {BRAND}, I want to order: {name}{col}")
                st.link_button("Test WhatsApp order link", f"https://wa.me/{wa}?text={msg}")


# ---------------- Dashboard ----------------
with tab_dash:
    st.subheader("Your shop at a glance")
    d_orders = st.session_state["orders"]
    d_stock = st.session_state["stock"]
    if len(d_orders) == 0 and len(d_stock) == 0:
        st.info("Add items in the Stock tab and orders in the Orders tab. This page will summarise them for you.")
    else:
        live = d_orders[~d_orders["Status"].isin(["Cancelled", "Returned"])] if len(d_orders) else d_orders
        today_orders = live[live["Date"] == str(date.today())] if len(live) else live
        to_ship = live[live["Status"].isin(["New", "Packed"])] if len(live) else live
        unpaid = live[live["Paid"] == False] if len(live) else live
        unpaid_amount = float((unpaid["Qty"] * unpaid["Price"]).sum()) if len(unpaid) else 0.0
        low_items = d_stock[d_stock["In Stock"] <= LOW_STOCK] if len(d_stock) else d_stock

        g1, g2, g3, g4 = st.columns(4)
        g1.metric("Orders today", len(today_orders))
        g2.metric("To pack / ship", len(to_ship))
        g3.metric("Payments pending", f"Rs {unpaid_amount:,.0f}")
        g4.metric("Low stock items", len(low_items))

        if len(unpaid):
            st.markdown("**Customers with pending payment**")
            show = unpaid[["Customer", "Phone", "Product", "Qty", "Price"]].copy()
            show["Amount"] = show["Qty"] * show["Price"]
            st.dataframe(show, use_container_width=True, hide_index=True)
        if len(low_items):
            st.markdown("**Low or finished stock**")
            st.dataframe(low_items[["Product", "Brand", "Size", "Colour", "In Stock"]], use_container_width=True, hide_index=True)
    storage_note("dash")


# ---------------- Catalog ----------------
with tab_cat:
    st.subheader("Photo catalog")
    st.write(
        "Choose a slideshow photo, then give it a name and a price. Customers see these under the photo, "
        "with an Order button. Changes can take about two minutes to show for customers."
    )
    storage_note("catalog")
    photo_names = [name for name, _ in load_slides()]
    st.session_state["catalog"] = st.data_editor(
        st.session_state["catalog"],
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Photo": st.column_config.SelectboxColumn(options=photo_names),
            "Name": st.column_config.TextColumn(help="e.g. Embroidered 3-piece, Maroon"),
            "Price": st.column_config.TextColumn(help="e.g. Rs 7,500"),
        },
        key="catalog_editor",
    )
    persist("catalog")
    if not SHEETS_READY:
        st.warning(
            "Without Google Sheets, customers see these names and prices only from a file named catalog.csv in your GitHub repo."
        )
        st.download_button(
            "⬇️ Download catalog.csv",
            st.session_state["catalog"].to_csv(index=False).encode("utf-8"),
            file_name="catalog.csv",
            mime="text/csv",
        )
        st.caption(
            "Steps: fill the table above, click Download, then upload that catalog.csv to your GitHub repo "
            "(Add file, Upload files, Commit). Customers see it after the app refreshes."
        )

import base64
import glob
import io
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
INSTAGRAM_URL = ""   # e.g. "https://www.instagram.com/yourpage"  (leave empty to hide)
FACEBOOK_URL = ""    # e.g. "https://www.facebook.com/yourpage"  (leave empty to hide)
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
st.markdown(f"📞 **Contact / WhatsApp:** [{PHONE_LOCAL}]({WA_LINK})")
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

HERO = (
    '<div style="background:linear-gradient(135deg,#F3E6D8,#FFF8F0);border:1px solid #E6D3B8;'
    'border-radius:16px;padding:32px 24px;text-align:center;margin-bottom:16px;">'
    '<div style="font-size:13px;letter-spacing:3px;color:#B8860B;">BRANDED READY-TO-WEAR</div>'
    f'<div style="font-size:40px;font-weight:700;color:#3A2A1E;margin:8px 0;">👗 {BRAND}</div>'
    f'<div style="font-size:18px;color:#5a4636;">{TAGLINE}</div></div>'
)
st.markdown(HERO, unsafe_allow_html=True)

h1, h2, h3, h4 = st.columns(4)
h1.link_button("💬 Order on WhatsApp", WA_LINK, use_container_width=True)
h2.link_button("🛍️ Official Khaadi site", KHAADI_URL, use_container_width=True)
if INSTAGRAM_URL:
    h3.link_button("📸 Instagram", INSTAGRAM_URL, use_container_width=True)
if FACEBOOK_URL:
    h4.link_button("👍 Facebook", FACEBOOK_URL, use_container_width=True)

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


if "orders" not in st.session_state:
    st.session_state["orders"] = empty_orders()
if "stock" not in st.session_state:
    st.session_state["stock"] = empty_stock()


def csv_restore(key, label, empty_fn, bool_cols=()):
    up = st.file_uploader(label, type="csv", key=f"up_{key}")
    if up is not None and st.button("Load uploaded file", key=f"load_{key}"):
        loaded = pd.read_csv(up, dtype=str).fillna("")
        base = empty_fn()
        for col in base.columns:
            if col not in loaded.columns:
                loaded[col] = ""
        loaded = loaded[list(base.columns)]
        for col in base.columns:
            kind = base[col].dtype.kind
            if kind == "f":
                loaded[col] = pd.to_numeric(loaded[col], errors="coerce").fillna(0.0)
            elif kind == "i":
                loaded[col] = pd.to_numeric(loaded[col], errors="coerce").fillna(0).astype(int)
            elif kind == "b":
                loaded[col] = loaded[col].astype(str).str.lower().isin(["true", "1", "yes"])
        st.session_state[key] = loaded
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
            caption = ""
            slides.append((caption, data))
        except Exception:
            continue
    return slides


def slideshow_html(slides):
    items = "".join(
        f'<div class="s"><img src="{d}"><div class="c">{c}</div></div>' for c, d in slides
    )
    return f"""
<style>
 .box{{position:relative;max-width:520px;margin:auto;font-family:sans-serif}}
 .s{{display:none;text-align:center}} .s.on{{display:block}}
 .s img{{width:100%;max-height:560px;object-fit:contain;border-radius:12px}}
 .c{{margin-top:8px;font-size:16px;color:#444}}
 .b{{position:absolute;top:45%;background:rgba(0,0,0,.45);color:#fff;border:0;font-size:22px;
     padding:6px 12px;cursor:pointer;border-radius:50%}}
</style>
<div class="box">{items}
 <button class="b" style="left:6px" onclick="go(-1)">&#10094;</button>
 <button class="b" style="right:6px" onclick="go(1)">&#10095;</button>
</div>
<script>
 var i=0, s=document.querySelectorAll('.s');
 function show(){{s.forEach(function(e,k){{e.classList.toggle('on',k===i)}})}}
 function go(n){{i=(i+n+s.length)%s.length;show()}}
 show(); setInterval(function(){{go(1)}},3500);
</script>"""


tab_new, tab_info, tab_dash, tab1, tab2, tab3, tab4 = st.tabs(
    ["🆕 New Arrivals", "ℹ️ Info & FAQ", "📊 Dashboard", "💰 Price & Profit", "🧵 Stock", "📦 Orders", "✍️ Caption Maker"]
)

# ---------------- Tab 0: New Arrivals slideshow ----------------
with tab_new:
    st.subheader("New arrivals at Luxe By Madiha")
    slides = load_slides()
    if slides:
        components.html(slideshow_html(slides), height=680)
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

    st.caption("Stock is kept only while this page is open. Download your CSV before closing.")
    st.download_button("⬇️ Download stock (CSV)", sdf.to_csv(index=False).encode("utf-8"),
                       file_name="luxe_stock.csv", mime="text/csv")
    csv_restore("stock", "Upload saved stock (CSV)", empty_stock)

# ---------------- Tab 3: Orders ----------------
with tab3:
    st.subheader("Orders")
    with st.form("add_order", clear_on_submit=True):
        a1, a2, a3 = st.columns(3)
        customer = a1.text_input("Customer name")
        phone = a2.text_input("Phone / WhatsApp")
        product = a3.text_input("Product", placeholder="e.g. Embroidered 3-piece, Maroon, M")
        b1, b2, b3, b4 = st.columns(4)
        o_qty = b1.number_input("Qty", min_value=1, value=1, step=1)
        o_price = b2.number_input("Price per piece (Rs)", min_value=0.0, value=0.0, step=100.0)
        o_paid = b3.checkbox("Paid")
        o_status = b4.selectbox("Status", STATUSES)
        if st.form_submit_button("➕ Add order", use_container_width=True):
            if customer and product:
                row = pd.DataFrame([{
                    "Date": str(date.today()), "Customer": customer, "Phone": phone,
                    "Product": product, "Qty": int(o_qty), "Price": float(o_price),
                    "Paid": bool(o_paid), "Status": o_status,
                }])
                st.session_state["orders"] = pd.concat([st.session_state["orders"], row], ignore_index=True)
            else:
                st.warning("Please enter customer name and product.")

    st.session_state["orders"] = st.data_editor(
        st.session_state["orders"], num_rows="dynamic", use_container_width=True,
        column_config={
            "Status": st.column_config.SelectboxColumn(options=STATUSES),
            "Paid": st.column_config.CheckboxColumn(),
        },
        key="orders_editor",
    )
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

    st.caption("Orders are kept only while this page is open. Download your CSV before closing.")
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
    st.caption("Your data lives only in this browser session. Download your CSV files from the Stock and Orders tabs to keep them.")

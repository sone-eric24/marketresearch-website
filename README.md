# WS Market Research – website (Django)

The new website for **ws-marketresearch.com**, rebuilt in Django from the content of
the old WordPress site.

It is built to load quickly on slow mobile networks:

- **No JavaScript** and **no web fonts**. It uses the phone's own fonts.
- **One small stylesheet** (about 9 KB, about 2.5 KB compressed).
- Pages are **compressed (gzip)** and **cached** on the server.
- Images load only when they scroll into view, and browsers keep them for 30 days.
- The menu, FAQ and forms all work without JavaScript.

## What's inside

| Page | Address |
|---|---|
| Home | `/` |
| About | `/about/` |
| Services (7) | `/services/` and `/services/<name>/` |
| Case studies (6) | `/case-studies/` and `/case-studies/<name>/` |
| Insights / blog (5 articles) | `/blog/` and `/blog/<name>/` |
| FAQ (9 questions) | `/faq/` |
| Contact form | `/contact/` |
| Privacy policy | `/privacy/` |
| Admin (edit everything) | `/manage-ws/` |

Old WordPress addresses (for example `/2025/07/23/market-entry-challenges-in-cameroon/`,
`/service/...`, `/about-us/`, `/contact-us/`) redirect to the new pages, so links on
Google keep working. The thousands of spam addresses the hackers created answer
**410 Gone**, which tells Google to remove them.

## Project layout

```
config/            settings, main URL list, wsgi
content/           the app: models, views, admin, contact form
  fixtures/        initial_content.json – the content taken from WordPress
templates/         HTML pages
static/            CSS and icon
media/uploads/     images (copy them from the old site, see below)
passenger_wsgi.py  entry point for cPanel
tools/             scripts used to import the WordPress content
```

## Run it on your computer

You need Python 3.10 or newer.

```bash
git clone https://github.com/sone-eric24/marketresearch-website.git
cd marketresearch-website

python -m venv .venv
# Windows:      .venv\Scripts\activate
# Mac / Linux:  source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate                         # creates the database
python manage.py loaddata initial_content        # adds the content from WordPress
python manage.py createsuperuser                 # your admin login
python manage.py runserver
```

Open http://127.0.0.1:8000. The admin is at http://127.0.0.1:8000/manage-ws/.

## Images

The database backup contains the text but not the image files. In cPanel's
**File Manager**, download these files from `public_html/wp-content/uploads/` and put
them in `media/uploads/`, keeping the same folders (for example
`media/uploads/2025/01/yaounde-central-ws-marketresearch.jpg`):

```
2022/05/market-in-cameroon.jpg
2022/05/ngo-and-market-research.jpg
2022/05/portfolio-6.jpg
2022/05/portfolio-7.jpg
2022/05/report-at-ws-market-research.avif
2022/05/ws-report.png
2025/01/photo-of-roundabout-in-yaounde.jpeg
2025/01/yaounde-central-ws-marketresearch.jpg
2025/02/pm-office.jpg
2025/05/shopping-8042865_1280-1024x1024.png
```

⚠️ **Copy only image files** (`.jpg`, `.png`, `.avif`). The old site was hacked, and
hackers often hide `.php` files inside `uploads`. Never copy `.php` files.

Tip for slow networks: before uploading an image, make it smaller (for example
1200 px wide) with a free tool such as https://squoosh.app.

## Put it online with cPanel ("Setup Python App")

1. **Clean up first.** In File Manager, move the old WordPress files out of
   `public_html` (or delete them after you've downloaded the images you need).
2. In cPanel, open **Terminal** (or use SSH) and run:
   ```bash
   git clone https://github.com/sone-eric24/marketresearch-website.git ~/marketresearch-website
   ```
3. Open **Setup Python App** → **Create Application**:
   - Python version: 3.10 or newer
   - Application root: `marketresearch-website`
   - Application URL: `ws-marketresearch.com`
   - Application startup file: `passenger_wsgi.py`
   - Application entry point: `application`
4. On the same page, add the **environment variables** listed in `.env.example`
   (at least `DJANGO_DEBUG=False`, `DJANGO_SECRET_KEY` and `DJANGO_ALLOWED_HOSTS`).
5. Copy the "Enter to the virtual environment" command shown at the top of the page,
   run it in Terminal, then:
   ```bash
   cd ~/marketresearch-website
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py loaddata initial_content
   python manage.py collectstatic --noinput
   python manage.py createsuperuser
   ```
6. Click **Restart** in Setup Python App, then open https://ws-marketresearch.com.
7. Turn on free HTTPS in cPanel's **SSL/TLS Status** (AutoSSL) if it isn't on already,
   then switch on **Force HTTPS Redirect** for the domain in cPanel → **Domains**.

### Updating the site later

```bash
cd ~/marketresearch-website
git pull
# (enter the virtual environment first)
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```
Then click **Restart** in Setup Python App.

> Run `loaddata initial_content` **only once**. Running it again would undo any
> changes you made to those items in the admin.

## Editing content

Log in at `/manage-ws/`. You can add and edit articles, services, case studies and
FAQs, and read contact form messages. The text fields accept HTML (`<p>`, `<h2>`,
`<ul><li>`, `<strong>`, `<a href="">`).

Company details (phone, email, address, hours, social links) are in
`SITE_INFO` at the bottom of `config/settings.py`.

## Contact form

Every message is saved in the admin under **Contact messages**. If you set the
`EMAIL_*` variables (see `.env.example`), each message is also emailed to
`CONTACT_EMAIL`. A hidden field blocks most spam robots.

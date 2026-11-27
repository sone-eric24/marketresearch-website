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

The 10 images from the old site are already in this repo, in `media/uploads/`. They
were resized to at most 1200 px wide and compressed (about 860 KB in total, down
from 1.7 MB), so they come with the code when you `git clone` or `git pull`.

Images you upload later through the admin are saved in `media/uploads/<year>/<month>/`.

⚠️ The old site was hacked. Never copy `.php` files from the old `wp-content/uploads`
folder: hackers often hide malicious code there. `.gitignore` blocks `.php` files in `media/`.

Tip for slow networks: before uploading an image, make it smaller (for example
1200 px wide) with a free tool such as https://squoosh.app.

## Put it online with Render

See **[DEPLOY.md](DEPLOY.md)** for step-by-step instructions, and for cheaper
hosts you can move to later.

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

### Service stories

Each service page tells a short client story in three chapters. In the admin, open a
service and fill in:

- **Headline**: the client's situation in one sentence.
- **Challenge**: the problem the client faces.
- **Journey**: one step per line, written as `Step title: what happens`.
- **Outcome**: what the client walks away with.
- **Icon**: pick one from the list.

### Home and About page text

The text that is not in the admin (who we help, our story, values, process steps,
testimonials and key figures) is in `content/site_data.py`. The **key figures** list is
empty on purpose: add real numbers there and the section appears on the home page.

### Icons and illustrations

All icons are in one file, `static/img/icons.svg`, and the illustrations are
`static/img/hero-research.svg`, `static/img/story-path.svg` and one picture per service in
`static/img/services/` (named after the icon you pick for the service in the admin). They
were drawn for this site, so there is no licence to worry about, and they use the brand
colours. The service pictures are made by `tools/illustrations/make_service_art.py`.

The two photos in `static/img/photos/` (a market and Yaoundé) come from the old website.

## Contact form

Every message is saved in the admin under **Contact messages**. If you set the
`EMAIL_*` variables (see `.env.example`), each message is also emailed to
`CONTACT_EMAIL`. A hidden field blocks most spam robots.

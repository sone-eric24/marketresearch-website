# Putting the website online with Render

This guide is for doing it yourself in the Render website. You don't need to
type any commands. Everything Render needs is already in the code:

| File | What it does |
|---|---|
| `render.yaml` | Tells Render how to build and run the site (a "Blueprint"). |
| `bin/build.sh` | Installs the Python packages and collects the CSS/images. |
| `bin/start.sh` | Updates the database, then starts the web server (gunicorn). |
| `content/management/commands/prepare_site.py` | Loads the starting content the first time, and creates your admin login. |
| `Procfile`, `Dockerfile` | Not used by Render. They let you move to another host later (see the end). |

## How it works (in plain words)

- **gunicorn** is the "real" web server. `runserver` is only for your computer.
- **Settings come from environment variables** (little name = value pairs you type
  in the dashboard), so the same code works on your computer, on Render and anywhere else.
- **The database is SQLite**, a single file. On Render the code folder is wiped at
  every deploy, so the database file and uploaded images live on a small
  **persistent disk** mounted at `/var/data`. That's why the site uses Render's
  **Starter** plan: the free plan has no disk, so you'd lose every edit and contact
  message at each restart.

**Cost:** Starter web service (about $7 a month) + 1 GB disk (about $0.25 a month).
Check https://render.com/pricing for current prices.

## Step 1. Create a Render account

1. Go to https://render.com and click **Get Started**.
2. Choose **Sign up with GitHub**. This lets Render read your repository.
3. Add a payment card under **Account settings → Billing** (needed for the Starter plan).

## Step 2. Create the site from the Blueprint

1. In the dashboard click **New → Blueprint**.
2. Pick the **marketresearch-website** repository. (If you don't see it, click
   "Configure GitHub" and give Render access to it.)
3. Render reads `render.yaml` and shows one web service called **ws-marketresearch**
   with a disk called **data**.
4. Render asks you to fill in the secret values. Type:

   | Name | What to put |
   |---|---|
   | `DJANGO_SUPERUSER_USERNAME` | The name you'll log in with, e.g. `eric` |
   | `DJANGO_SUPERUSER_EMAIL` | Your email |
   | `DJANGO_SUPERUSER_PASSWORD` | A strong password, at least 12 characters |
   | `CONTACT_EMAIL` | Where contact form messages are sent, e.g. `contact@ws-marketresearch.com` |
   | `EMAIL_HOST` | Your mail server, e.g. `mail.ws-marketresearch.com` (leave empty to skip emails) |
   | `EMAIL_PORT` | `465` |
   | `EMAIL_HOST_USER` | The email account's address |
   | `EMAIL_HOST_PASSWORD` | The email account's password |

   You don't need to make a secret key: Render generates `DJANGO_SECRET_KEY` for you.
5. Click **Apply**. The first build takes a few minutes. You can watch it under **Logs**.

When it says **Live**, open the address Render shows at the top
(something like `https://ws-marketresearch.onrender.com`). The pages, articles and
images are already there. Log in at `/manage-ws/` with the username and password
from step 4.

> Contact messages are always saved in the admin, even if email isn't set up.

## Step 3. Connect your domain (ws-marketresearch.com)

1. In Render open the service → **Settings → Custom Domains → Add Custom Domain**.
   Add `ws-marketresearch.com`, then add `www.ws-marketresearch.com`.
2. Render shows the DNS records to create. Log in where your domain is managed
   (for example your cPanel host's **Zone Editor**) and add exactly those records.
   Usually that's an **A** record for `ws-marketresearch.com` and a **CNAME** for `www`.
3. Wait until Render shows **Verified** (minutes to a few hours). Render then gives
   you free HTTPS automatically.

⚠️ If your email is hosted at the same company as the domain, **don't touch the MX
records**, or email will stop working. Only change the records Render asks for.

## Updating the site later

Push (or merge a pull request) to the `main` branch on GitHub. Render rebuilds and
restarts the site by itself. Your database and uploaded images on the disk are kept.

Starting content is loaded **only once**, when the database is empty, so your
admin edits are never overwritten.

## If something goes wrong

- **The build failed:** open **Logs** in Render and read the last red lines.
- **"Bad Request (400)":** the address you opened isn't in `DJANGO_ALLOWED_HOSTS`.
  Add it under **Environment** (separated by commas, no spaces) and save.
- **"CSRF verification failed" when logging in:** add the same address with
  `https://` in front to `DJANGO_CSRF_TRUSTED_ORIGINS`.
- **Forgot the admin password:** open the service → **Shell** and run
  `python manage.py changepassword <username>`.

## Backups

Your whole site's data is one file: `/var/data/db.sqlite3`. Render takes daily
snapshots of the disk, which you can restore under the service's **Disks** tab.
To keep your own copy, open **Shell** and run
`python manage.py dumpdata --exclude contenttypes --exclude auth.permission > /var/data/backup.json`,
then download it with the Render CLI or copy the text.

---

# Moving to a cheaper host later

Nothing in the code is tied to Render. The site only needs: Python, the
environment variables from `.env.example`, a place where the database file and
`media/` folder are kept, and the start command `bash bin/start.sh`.
To move, copy two things from the old host: **`db.sqlite3`** and the **`media/`** folder.

| Option | Roughly per month | Good to know |
|---|---|---|
| **cPanel shared hosting** ("Setup Python App") | $2–5, often already paid with the domain | Cheapest. Already supported: follow "Put it online with cPanel" in `README.md`. Slower and less control. |
| **PythonAnywhere** | about $5 | Made for Python/Django beginners. Paid plan needed for your own domain. Point the WSGI file at `config.wsgi`. |
| **Small VPS** (Hetzner, Contabo, DigitalOcean...) | $4–6 | Best value and full control, but you look after the server. Install Docker, then `docker build -t site .` and `docker run -d -p 80:8000 -v site-data:/data -e DJANGO_SECRET_KEY=... -e DJANGO_ALLOWED_HOSTS=... site`. Add HTTPS with Caddy or Nginx. |
| **Fly.io / Koyeb / Railway** | pay as you go, a few dollars for a site this small | Use the `Dockerfile` (or `Procfile` on Railway) and attach a volume at `/data`. |

Prices change often, so check each provider's pricing page before choosing.

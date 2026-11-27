# WordPress → Django content import

These two scripts created `content/fixtures/initial_content.json` from the old
WordPress database backup. You only need them again if you want to redo the import.

```bash
# 1. Turn the .sql backup into JSON (takes about 10 seconds)
python tools/wordpress_import/parse_sql.py backup.sql data.json \
    wps8_posts wps8_postmeta wps8_terms wps8_term_taxonomy wps8_term_relationships wps8_options

# 2. Keep only the real content and write the Django fixture
python tools/wordpress_import/build_fixture.py data.json content/fixtures/initial_content.json
```

`build_fixture.py` needs `beautifulsoup4` (`pip install beautifulsoup4`).

**Important:** the old site was hacked. The script keeps only posts written by the
owner account (WordPress user ID 1) and drops the ~7,000 spam posts. Never commit
the `.sql` file to GitHub, because it contains user password hashes.

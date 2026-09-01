---
name: kwiki
description: Read, search, and edit pages on wiki.kestell.org, the private Wiki.js site. Use for any request to look something up on the wiki, add or update a wiki page, move or rename pages, review or roll back page history, find broken links, or upload an image. Drives the Wiki.js GraphQL API through a bundled client.
argument-hint: "[what to do on the wiki]"
---

# Wiki

`wiki.kestell.org` is a Wiki.js 2.5 site reachable over Tailscale. It has no
public DNS records. Pages are Markdown, the locale is `en`, and paths carry no
locale prefix: the page `notes/dns` is served at
`https://wiki.kestell.org/notes/dns`.

[wiki.py](assets/wiki.py) drives the site's GraphQL API. It is a `uv` script, so it
declares its own dependencies and needs no virtualenv.

## Running it

```sh
WIKI=~/.agents/skills/kwiki/assets/wiki.py
$WIKI list
$WIKI --help
$WIKI <command> --help
```

Every command prints its results on stdout and its counts, confirmations, and
warnings on stderr, so output pipes cleanly. `--json` gives machine-readable
output for the commands that list things. Paths may be given bare
(`notes/dns`), with a leading slash, or as a full page URL.

The API key is read from `WIKI_TOKEN`, else from the file named by
`WIKI_TOKEN_FILE`, else from `~/.config/wiki/token`. Install it once:

```sh
mkdir -p ~/.config/wiki
chmod 700 ~/.config/wiki
printf '%s' '<key>' > ~/.config/wiki/token
chmod 600 ~/.config/wiki/token
```

The key is the `claude-automation` entry in
`~/src/proxmox/docs/logins.md`. It covers pages, assets, and comments, and is
refused on users, groups, API keys, and site settings. `WIKI_URL` and
`WIKI_LOCALE` override the site and locale.

## Finding things

There are two searches, and they look at different things.

`search` asks Wiki.js. Its configured engine matches **titles, descriptions, and
paths only, and only on published pages**. It never looks at page content.

```sh
$WIKI search dns                 # pages whose title, description, or path says dns
$WIKI search dns --path notes    # the same, under notes/
```

`grep` fetches the Markdown source of every page and matches a regex against
it. This is how to search page **content**, and it covers unpublished pages
too.

```sh
$WIKI grep '10\.0\.0\.[0-9]+'         # regex over every page's source
$WIKI grep -i caddy -C 2              # case-insensitive, two lines of context
$WIKI grep tailscale -l               # just the page paths
$WIKI grep 'TODO' --path runbooks     # only under runbooks/
```

Reach for `grep` when the question is about what a page says, and for `search`
when it is about what a page is called. To answer "is this documented
anywhere", run `grep`.

For orientation rather than search:

```sh
$WIKI list                  # every page: id, path, title, tags; ! marks unpublished
$WIKI list --tag runbook    # only pages carrying a tag
$WIKI list --order UPDATED  # most recently changed last
$WIKI tree                  # top level of the hierarchy
$WIKI tree notes            # one subtree
$WIKI tags                  # every tag in use
```

## Reading a page

```sh
$WIKI get notes/dns                  # Markdown source on stdout
$WIKI get notes/dns --meta           # title, description, tags, dates, URL
$WIKI get notes/dns --json           # everything, as JSON
$WIKI get notes/dns --version 41     # an earlier version's source
```

## Writing a page

`put` creates the page when the path is new and updates it otherwise, so
`--title` is needed only on creation. Content comes from `--file`, `--content`,
or stdin.

```sh
$WIKI put notes/dns --title "DNS" --description "Private names" --file dns.md --tag runbook
$WIKI put notes/dns --content "$(cat dns.md)"
$WIKI put notes/dns --file dns.md --tag runbook --tag network   # --tag replaces the tag list
$WIKI put notes/scratch --title "Scratch" --content "…" --draft # unpublished
$WIKI put notes/scratch --file scratch.md --publish             # publish it
```

`--tag` replaces the page's whole tag list. Omit it and the existing tags are
kept. Likewise omitting `--title` or `--description` on an update keeps what is
there.

### Editing an existing page

Pull the page down with its metadata, edit the file, check the diff, push it
back. This is the loop to use for any edit to a page that already exists.

```sh
$WIKI get notes/dns --frontmatter > dns.md
# edit dns.md — the body, or title/description/tags in the frontmatter
$WIKI diff notes/dns --file dns.md --frontmatter    # what the write would change
$WIKI put notes/dns --file dns.md --frontmatter     # write it back
```

`--frontmatter` puts a YAML block ahead of the content holding `path`, `title`,
`description`, `tags`, `locale`, `id`, `updatedAt`, and `isPublished`. On the
way back in, `put` takes title, description, tags, and published state from that
block, and uses `updatedAt` to check that nobody changed the page in the
meantime. If someone did, the write is refused and says so; re-read the page,
reapply the edit, and push again. `--force` writes anyway and discards the other
change.

## Moving and deleting

Wiki.js has no folders of its own — the hierarchy is inferred from page paths.
Moving a whole section therefore means moving each page in it, which `-r` does.

```sh
$WIKI move notes/dns notes/networking/dns        # move or rename one page
$WIKI move notes archive/notes -r -n            # preview a subtree move
$WIKI move notes archive/notes -r               # do it
```

`delete` cannot be undone through the API. `history`, `diff`, and `restore` all
work through the live page, so once it is gone every version of it is out of
reach as well. Prefer moving a page into a trash or archive path over deleting
it, and confirm with the user before deleting anything they did not ask to have
deleted.

```sh
$WIKI move notes/dns trash/dns    # reversible
$WIKI delete notes/dns            # not
```

## History

```sh
$WIKI history notes/dns          # version ids, dates, authors, actions
$WIKI diff notes/dns 41          # version 41 against the live page
$WIKI diff notes/dns 41 48       # two versions against each other
$WIKI restore notes/dns 41       # roll the content back to version 41
```

`restore` puts back the content and description of that version. It leaves the
current tags alone, so reapply them with `put --tag` if they mattered.

## Links and images

```sh
$WIKI links               # every internal page link
$WIKI links --broken      # links pointing at pages that do not exist
```

Wiki.js records only internal page links, so external URLs, anchors, and asset
paths never show up as broken.

```sh
$WIKI assets                                  # folders and files at the root
$WIKI assets diagrams                         # one folder
$WIKI upload network.png --folder diagrams    # creates the folder if needed
```

`upload` prints the path to reference from a page.

The API key can upload but not delete, so `delete-asset` reports `Forbidden`
until the key gains that permission. Remove a stray asset through
Administration → Assets.

## Writing pages

- Write Markdown. Wiki.js renders it with `markdown-it`.
- Link between pages with absolute paths: `[DNS](/notes/dns)`. A relative
  target resolves against the current page's own path, so `[DNS](dns)` on
  `notes/networking` points at `notes/networking/dns`.
- Every page needs a `title`; a `description` is what `search` matches on, so
  give each page one worth matching.
- Give a section a landing page at its own path — `notes` alongside
  `notes/dns` — or the hierarchy shows a folder with nothing to read.

## Escape hatch

For anything the commands above do not cover, send GraphQL directly. The schema
is introspectable.

```sh
$WIKI query '{pages{list(locale:"en",orderBy:PATH){path title}}}'
$WIKI query 'query($p:String!){pages{singleByPath(path:$p,locale:"en"){id hash}}}' '{"p":"notes/dns"}'
$WIKI query @query.graphql
```

Two Wiki.js behaviors the client already handles, worth knowing before writing
raw queries. `tags` is optional in the `update` schema but the resolver maps
over it unconditionally, so an update that omits it writes the content and then
reports failure. `singleByPath` raises a GraphQL error for a missing page
instead of returning null.

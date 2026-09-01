#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pyyaml>=6.0.3",
#     "requests>=2.34.2",
# ]
# ///
"""Wiki.js client.

Environment:

    WIKI_URL         site root, default https://wiki.kestell.org
    WIKI_LOCALE      locale code, default en
    WIKI_TOKEN       API key
    WIKI_TOKEN_FILE  file holding the API key, default ~/.config/wiki/token
"""

import argparse
import difflib
import json
import mimetypes
import os
import pathlib
import re
import sys
import urllib.parse

import requests
import yaml

SITE = os.environ.get("WIKI_URL", "https://wiki.kestell.org").rstrip("/")
ENDPOINT = SITE + "/graphql"
LOCALE = os.environ.get("WIKI_LOCALE", "en")
BATCH = 25
FRONTMATTER = ("path", "title", "description", "tags", "locale", "id",
               "updatedAt", "isPublished")


def fail(message):
    sys.exit(f"wiki: {message}")


def note(message):
    """Counts and confirmations go to stderr so stdout stays pipeable."""
    sys.stdout.flush()
    print(message, file=sys.stderr)


def token():
    value = os.environ.get("WIKI_TOKEN")
    if value and value.strip():
        return value.strip()
    path = pathlib.Path(
        os.environ.get("WIKI_TOKEN_FILE") or "~/.config/wiki/token"
    ).expanduser()
    if path.is_file():
        value = path.read_text().strip()
        if value:
            return value
    fail(f"no API key. Set WIKI_TOKEN, or write the key to {path}.")


_session = None


def session():
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers["Authorization"] = f"Bearer {token()}"
    return _session


def call(query, variables=None, tolerate=None):
    try:
        response = session().post(
            ENDPOINT, json={"query": query, "variables": variables or {}}, timeout=30
        )
    except requests.RequestException as error:
        fail(f"cannot reach {ENDPOINT}: {error}")
    if response.status_code != 200:
        fail(f"http {response.status_code} from {ENDPOINT}: {response.text[:500]}")
    payload = response.json()
    if "errors" in payload:
        messages = "; ".join(e.get("message", "?") for e in payload["errors"])
        if tolerate and tolerate in messages:
            return None
        if messages == "Forbidden":
            messages = ("Forbidden. Either the API key is invalid, or the call is "
                        "outside its scope: the key covers pages, assets, and "
                        "comments, and is refused on users, groups, keys, and "
                        "settings.")
        fail(f"graphql error: {messages}")
    return payload["data"]


def check(result):
    """Wiki.js reports mutation failures inside responseResult, not as errors."""
    outcome = result["responseResult"]
    if not outcome["succeeded"]:
        fail(outcome["message"] or f"error {outcome['errorCode']}")
    return result


def norm(path):
    """Accept a wiki path, a leading-slash path, or a full page URL."""
    path = path.strip()
    if "://" in path:
        path = urllib.parse.unquote(urllib.parse.urlsplit(path).path)
    path = path.strip("/")
    if path.startswith(f"{LOCALE}/"):
        path = path[len(LOCALE) + 1:]
    return path


def url_for(path):
    return f"{SITE}/{path}"


def find(path):
    """Return the page at path, or None. singleByPath errors when it is missing."""
    data = call(
        "query($p:String!,$l:String!){pages{singleByPath(path:$p,locale:$l)"
        "{id path title description isPublished updatedAt tags{tag}}}}",
        {"p": path, "l": LOCALE},
        tolerate="does not exist",
    )
    return data["pages"]["singleByPath"] if data else None


def require(path):
    page = find(path)
    if not page:
        fail(f"no such page: {path}")
    return page


def page_list(tags=None, order="PATH", limit=None):
    data = call(
        "query($l:String!,$o:PageOrderBy!,$g:[String!]){pages{"
        "list(locale:$l,orderBy:$o,tags:$g)"
        "{id path title description isPublished updatedAt tags}}}",
        {"l": LOCALE, "o": order, "g": tags or None},
    )
    listing = data["pages"]["list"]
    return listing[:limit] if limit else listing


def fetch_contents(items):
    """Fetch page content in batches, one GraphQL request per batch of BATCH."""
    out = {}
    for start in range(0, len(items), BATCH):
        chunk = items[start:start + BATCH]
        fields = " ".join(
            f'a{i}:single(id:{page["id"]}){{path content}}'
            for i, page in enumerate(chunk)
        )
        data = call("{pages{" + fields + "}}")["pages"]
        for i in range(len(chunk)):
            page = data[f"a{i}"]
            if page:
                out[page["path"]] = page["content"]
    return out


def emit(args, value, render):
    if args.json:
        print(json.dumps(value, indent=2))
    else:
        render(value)


def split_frontmatter(text):
    """Return (metadata, content). metadata is None when there is no frontmatter."""
    if not text.startswith("---"):
        return None, text
    parts = text.split("\n", 1)
    if parts[0].strip() != "---" or len(parts) == 1:
        return None, text
    closing = re.search(r"^---[ \t]*$", parts[1], re.MULTILINE)
    if not closing:
        return None, text
    head = parts[1][:closing.start()]
    body = parts[1][closing.end():].lstrip("\n")
    try:
        meta = yaml.safe_load(head)
    except yaml.YAMLError as error:
        fail(f"bad frontmatter: {error}")
    if not isinstance(meta, dict):
        return None, text
    return meta, body


def join_frontmatter(page, content):
    meta = {k: page[k] for k in FRONTMATTER if k in page}
    if isinstance(meta.get("tags"), list) and meta["tags"] and isinstance(
        meta["tags"][0], dict
    ):
        meta["tags"] = [t["tag"] for t in meta["tags"]]
    head = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True,
                          default_flow_style=False)
    return f"---\n{head}---\n\n{content}"


def read_content(args):
    if args.file:
        text = pathlib.Path(args.file).read_text()
    elif args.content is not None:
        text = args.content
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        fail("no content. Pass --file, --content, or pipe to stdin.")
    if getattr(args, "frontmatter", False):
        meta, body = split_frontmatter(text)
        if meta is None:
            fail("--frontmatter given but the content has no YAML frontmatter")
        return meta, body
    return None, text


def cmd_list(args):
    listing = page_list(args.tag, args.order, args.limit)

    def render(rows):
        for page in rows:
            flag = " " if page["isPublished"] else "!"
            tags = " ".join("#" + t for t in page["tags"] or [])
            line = f"{flag} {page['id']:>4}  {page['path']:<44} {page['title']}"
            print(line + (f"  {tags}" if tags else ""))
        note(f"{len(rows)} page(s). ! marks unpublished.")

    emit(args, listing, render)


def cmd_tree(args):
    if args.path:
        query = ("query($l:String!,$p:String!){pages{tree(path:$p,mode:ALL,"
                 "locale:$l,includeAncestors:false)"
                 "{id path title depth isFolder pageId}}}")
        variables = {"l": LOCALE, "p": norm(args.path)}
    else:
        query = ("query($l:String!){pages{tree(parent:0,mode:ALL,"
                 "locale:$l,includeAncestors:false)"
                 "{id path title depth isFolder pageId}}}")
        variables = {"l": LOCALE}
    items = call(query, variables)["pages"]["tree"] or []

    def render(rows):
        for item in rows:
            indent = "  " * max(0, item["depth"] - 1)
            name = item["path"].rsplit("/", 1)[-1]
            mark = "/" if item["isFolder"] else ""
            print(f"{indent}{name}{mark}    {item['title']}")
        note(f"{len(rows)} entry/entries. A folder with no page of its own has "
             "no content to read.")

    emit(args, items, render)


def cmd_search(args):
    result = call(
        "query($q:String!,$p:String,$l:String!){pages{search(query:$q,path:$p,"
        "locale:$l){results{id path title description locale} suggestions totalHits}}}",
        {"q": args.query, "p": norm(args.path) if args.path else None, "l": LOCALE},
    )["pages"]["search"]

    def render(value):
        for hit in value["results"]:
            print(f"{hit['path']:<44} {hit['title']}")
            if hit["description"]:
                print(f"{'':<44} {hit['description']}")
        note(f"{value['totalHits']} hit(s). This searches page titles, "
             "descriptions, and paths of published pages only — never page "
             "content. Use `grep` to search content.")
        if value["suggestions"]:
            note("did you mean: " + ", ".join(value["suggestions"]))

    emit(args, result, render)


def cmd_grep(args):
    try:
        pattern = re.compile(args.pattern, re.IGNORECASE if args.ignore_case else 0)
    except re.error as error:
        fail(f"bad pattern: {error}")
    prefix = norm(args.path) if args.path else None
    listing = [p for p in page_list() if not prefix or p["path"].startswith(prefix)]
    matches = []
    for path, content in sorted(fetch_contents(listing).items()):
        lines = content.splitlines()
        hits = [i for i, line in enumerate(lines) if pattern.search(line)]
        if hits:
            matches.append({
                "path": path,
                "matches": [
                    {
                        "line": i + 1,
                        "text": lines[i],
                        "before": lines[max(0, i - args.context):i],
                        "after": lines[i + 1:i + 1 + args.context],
                    }
                    for i in hits
                ],
            })

    def render(rows):
        for page in rows:
            if args.files_only:
                print(page["path"])
                continue
            for hit in page["matches"]:
                for offset, line in enumerate(hit["before"]):
                    print(f"{page['path']}-{hit['line'] - len(hit['before']) + offset}- {line}")
                print(f"{page['path']}:{hit['line']}: {hit['text']}")
                for offset, line in enumerate(hit["after"]):
                    print(f"{page['path']}-{hit['line'] + 1 + offset}- {line}")
        total = sum(len(p["matches"]) for p in rows)
        note(f"{total} match(es) in {len(rows)} of {len(listing)} page(s) searched.")

    emit(args, matches, render)


def cmd_tags(args):
    data = call("{pages{tags{tag title}}}")["pages"]["tags"]

    def render(rows):
        for tag in rows:
            print(f"{tag['tag']:<28} {tag['title'] or ''}")
        note(f"{len(rows)} tag(s)")

    emit(args, data, render)


def cmd_get(args):
    path = norm(args.path)
    page = require(path)
    if args.version:
        data = call(
            "query($i:Int!,$v:Int!){pages{version(pageId:$i,versionId:$v)"
            "{pageId path title description tags locale isPublished content "
            "versionId versionDate action authorName}}}",
            {"i": page["id"], "v": args.version},
        )["pages"]["version"]
        if not data:
            fail(f"no version {args.version} of {path}")
    else:
        data = call(
            "query($i:Int!){pages{single(id:$i){id path title description content "
            "isPublished tags{tag} locale createdAt updatedAt authorName editor}}}",
            {"i": page["id"]},
        )["pages"]["single"]
    if args.json:
        print(json.dumps(data, indent=2))
    elif args.meta:
        print(f"path        {data['path']}")
        print(f"title       {data['title']}")
        print(f"description {data['description']}")
        tags = data["tags"]
        if tags and isinstance(tags[0], dict):
            tags = [t["tag"] for t in tags]
        print(f"tags        {' '.join(tags or [])}")
        print(f"published   {data['isPublished']}")
        for field in ("id", "createdAt", "updatedAt", "authorName", "editor",
                      "versionId", "versionDate"):
            if field in data:
                print(f"{field:<11} {data[field]}")
        print(f"url         {url_for(data['path'])}")
    elif args.frontmatter:
        sys.stdout.write(join_frontmatter(data, data["content"]))
    else:
        sys.stdout.write(data["content"])


def cmd_put(args):
    path = norm(args.path)
    meta, content = read_content(args)
    meta = meta or {}
    page = find(path)
    title = args.title or meta.get("title")
    description = args.description if args.description is not None \
        else meta.get("description")
    tags = args.tag if args.tag else meta.get("tags")
    if page:
        if not args.force and meta.get("updatedAt"):
            conflict = call(
                "query($i:Int!,$d:Date!){pages{checkConflicts(id:$i,checkoutDate:$d)}}",
                {"i": page["id"], "d": str(meta["updatedAt"])},
            )["pages"]["checkConflicts"]
            if conflict:
                fail(f"{path} changed since it was read "
                     f"({meta['updatedAt']} -> {page['updatedAt']}). "
                     "Re-read it and reapply your edit, or pass --force.")
        published = page["isPublished"]
        if meta.get("isPublished") is not None:
            published = bool(meta["isPublished"])
        if args.publish:
            published = True
        if args.draft:
            published = False
        # tags is optional in the update schema, but the resolver maps over it
        # unconditionally, so always send the full list.
        check(call(
            "mutation($i:Int!,$c:String!,$t:String!,$d:String!,$g:[String]!,"
            "$b:Boolean!){pages{update(id:$i,content:$c,title:$t,description:$d,"
            "tags:$g,isPublished:$b){responseResult{succeeded errorCode message}"
            "page{id path}}}}",
            {
                "i": page["id"],
                "c": content,
                "t": title or page["title"],
                "d": description if description is not None
                else page["description"] or "",
                "g": tags if tags is not None else [t["tag"] for t in page["tags"]],
                "b": published,
            },
        )["pages"]["update"])
        note(f"updated {path} (id {page['id']}) {url_for(path)}")
        return
    if not title:
        fail("--title is required when creating a page")
    result = check(call(
        "mutation($c:String!,$d:String!,$p:String!,$t:String!,$l:String!,"
        "$g:[String]!,$b:Boolean!){pages{create(content:$c,description:$d,"
        "editor:\"markdown\",isPublished:$b,isPrivate:false,locale:$l,path:$p,"
        "tags:$g,title:$t){responseResult{succeeded errorCode message}"
        "page{id path}}}}",
        {
            "c": content,
            "d": description or "",
            "p": path,
            "t": title,
            "l": LOCALE,
            "g": tags or [],
            "b": not args.draft,
        },
    )["pages"]["create"])
    note(f"created {path} (id {result['page']['id']}) {url_for(path)}")


def move_one(page_id, destination):
    check(call(
        "mutation($i:Int!,$p:String!,$l:String!){pages{"
        "move(id:$i,destinationPath:$p,destinationLocale:$l)"
        "{responseResult{succeeded errorCode message}}}}",
        {"i": page_id, "p": destination, "l": LOCALE},
    )["pages"]["move"])


def cmd_move(args):
    source = norm(args.path)
    destination = norm(args.destination)
    if args.recursive:
        # Wiki.js has no subtree move; every page under the prefix moves on its own.
        moves = [
            (p["id"], p["path"], destination + p["path"][len(source):])
            for p in page_list()
            if p["path"] == source or p["path"].startswith(source + "/")
        ]
        if not moves:
            fail(f"no pages at or under {source}")
    else:
        page = require(source)
        moves = [(page["id"], source, destination)]
    for page_id, old, new in moves:
        if args.dry_run:
            print(f"{old} -> {new}")
        else:
            move_one(page_id, new)
            note(f"moved {old} -> {new} (id {page_id})")
    if args.dry_run:
        note(f"{len(moves)} page(s) would move. Re-run without --dry-run.")


def cmd_delete(args):
    path = norm(args.path)
    page = require(path)
    check(call(
        "mutation($i:Int!){pages{delete(id:$i)"
        "{responseResult{succeeded errorCode message}}}}",
        {"i": page["id"]},
    )["pages"]["delete"])
    note(f"deleted {path} (id {page['id']}). Its versions are unreachable now too.")


def cmd_history(args):
    path = norm(args.path)
    page = require(path)
    data = call(
        "query($i:Int!,$s:Int!){pages{history(id:$i,offsetPage:0,offsetSize:$s)"
        "{total trail{versionId versionDate authorName actionType "
        "valueBefore valueAfter}}}}",
        {"i": page["id"], "s": args.limit},
    )["pages"]["history"]

    def render(value):
        for entry in value["trail"] or []:
            change = ""
            if entry["valueBefore"] or entry["valueAfter"]:
                change = f"  {entry['valueBefore']} -> {entry['valueAfter']}"
            print(f"{entry['versionId']:>6}  {entry['versionDate']}  "
                  f"{entry['actionType']:<10} {entry['authorName']}{change}")
        note(f"{value['total']} version(s) of {path} (id {page['id']})")

    emit(args, data, render)


def version_content(page_id, version_id):
    data = call(
        "query($i:Int!,$v:Int!){pages{version(pageId:$i,versionId:$v){content}}}",
        {"i": page_id, "v": version_id},
    )["pages"]["version"]
    if not data:
        fail(f"no version {version_id}")
    return data["content"]


def current_content(page_id):
    return call(
        "query($i:Int!){pages{single(id:$i){content}}}", {"i": page_id}
    )["pages"]["single"]["content"]


def cmd_diff(args):
    path = norm(args.path)
    page = require(path)
    if args.file:
        if args.version is not None:
            fail("pass either --file or version numbers, not both")
        text = pathlib.Path(args.file).read_text()
        if args.frontmatter:
            meta, text = split_frontmatter(text)
            if meta is None:
                fail("--frontmatter given but the file has no YAML frontmatter")
        left, left_name = current_content(page["id"]), f"{path} (live)"
        right, right_name = text, args.file
    elif args.version is None:
        fail("pass a version number or --file")
    elif args.to is None:
        left = version_content(page["id"], args.version)
        left_name = f"{path}@{args.version}"
        right, right_name = current_content(page["id"]), f"{path} (live)"
    else:
        left = version_content(page["id"], args.version)
        left_name = f"{path}@{args.version}"
        right = version_content(page["id"], args.to)
        right_name = f"{path}@{args.to}"
    lines = list(difflib.unified_diff(
        left.splitlines(keepends=True), right.splitlines(keepends=True),
        left_name, right_name,
    ))
    sys.stdout.writelines(lines)
    if lines and not lines[-1].endswith("\n"):
        print()
    if not lines:
        note("no difference")


def cmd_restore(args):
    path = norm(args.path)
    page = require(path)
    check(call(
        "mutation($i:Int!,$v:Int!){pages{restore(pageId:$i,versionId:$v)"
        "{responseResult{succeeded errorCode message}}}}",
        {"i": page["id"], "v": args.version},
    )["pages"]["restore"])
    note(f"restored {path} to version {args.version}")


def strip_locale(path):
    return path[len(LOCALE) + 1:] if path.startswith(f"{LOCALE}/") else path


def cmd_links(args):
    rows = call(
        "query($l:String!){pages{links(locale:$l){id path title links}}}",
        {"l": LOCALE},
    )["pages"]["links"] or []
    rows = [
        {"path": strip_locale(r["path"]), "title": r["title"],
         "links": sorted({strip_locale(t) for t in r["links"]})}
        for r in rows
    ]
    rows.sort(key=lambda r: r["path"])
    if not args.broken:
        def render(value):
            for row in value:
                for target in row["links"]:
                    print(f"{row['path']} -> {target}")
            note(f"{sum(len(r['links']) for r in value)} internal link(s). "
                 "External links, anchors, and assets are not tracked.")

        emit(args, rows, render)
        return
    known = {p["path"] for p in page_list()}
    broken = [
        {"path": r["path"], "missing": [t for t in r["links"] if t not in known]}
        for r in rows
    ]
    broken = [r for r in broken if r["missing"]]

    def render(value):
        for row in value:
            for target in row["missing"]:
                print(f"{row['path']} -> {target}")
        note(f"{sum(len(r['missing']) for r in value)} broken link(s) on "
             f"{len(value)} page(s)")

    emit(args, broken, render)


def folder_id(path, create=False):
    """Walk asset folder slugs from the root. Root is folder 0."""
    current = 0
    for slug in [s for s in norm(path).split("/") if s] if path else []:
        folders = call(
            "query($p:Int!){assets{folders(parentFolderId:$p){id name slug}}}",
            {"p": current},
        )["assets"]["folders"] or []
        match = next((f for f in folders if f["slug"] == slug), None)
        if match:
            current = match["id"]
            continue
        if not create:
            fail(f"no asset folder: {path}")
        check(call(
            "mutation($p:Int!,$s:String!){assets{createFolder(parentFolderId:$p,"
            "slug:$s){responseResult{succeeded errorCode message}}}}",
            {"p": current, "s": slug},
        )["assets"]["createFolder"])
        folders = call(
            "query($p:Int!){assets{folders(parentFolderId:$p){id slug}}}",
            {"p": current},
        )["assets"]["folders"] or []
        match = next((f for f in folders if f["slug"] == slug), None)
        if not match:
            fail(f"created asset folder {slug} but cannot find it")
        note(f"created asset folder {slug}")
        current = match["id"]
    return current


def cmd_assets(args):
    parent = folder_id(args.folder) if args.folder else 0
    data = call(
        "query($p:Int!){assets{folders(parentFolderId:$p){id name slug} "
        "list(folderId:$p,kind:ALL){id filename ext mime fileSize}}}",
        {"p": parent},
    )["assets"]
    prefix = norm(args.folder) + "/" if args.folder else ""

    def render(value):
        for folder in value["folders"] or []:
            print(f"{folder['slug'] + '/':<40} folder")
        for asset in value["list"] or []:
            print(f"{prefix + asset['filename']:<40} "
                  f"{asset['fileSize']:>9}  {asset['mime']}  "
                  f"{url_for(prefix + asset['filename'])}")
        note(f"{len(value['folders'] or [])} folder(s), "
             f"{len(value['list'] or [])} file(s)")

    emit(args, data, render)


def cmd_upload(args):
    path = pathlib.Path(args.file).expanduser()
    if not path.is_file():
        fail(f"no such file: {path}")
    parent = folder_id(args.folder, create=True) if args.folder else 0
    name = args.name or path.name
    mime = mimetypes.guess_type(name)[0] or "application/octet-stream"
    # Wiki.js takes uploads on the REST endpoint /u, not GraphQL. Both parts of
    # the multipart body are named mediaUpload: first the JSON options, then the
    # file itself.
    files = (
        ("mediaUpload", (None, json.dumps({"folderId": parent}), "application/json")),
        ("mediaUpload", (name, path.read_bytes(), mime)),
    )
    try:
        response = session().post(f"{SITE}/u", files=files, timeout=120)
    except requests.RequestException as error:
        fail(f"cannot reach {SITE}/u: {error}")
    if response.status_code != 200:
        fail(f"http {response.status_code} uploading {name}: {response.text[:500]}")
    target = (norm(args.folder) + "/" if args.folder else "") + name
    note(f"uploaded {name} ({mime}, {path.stat().st_size} bytes) "
         f"as {url_for(target)}")
    print(f"/{target}")


def cmd_delete_asset(args):
    target = norm(args.path)
    folder, _, filename = target.rpartition("/")
    parent = folder_id(folder) if folder else 0
    assets = call(
        "query($p:Int!){assets{list(folderId:$p,kind:ALL){id filename}}}",
        {"p": parent},
    )["assets"]["list"] or []
    match = next((a for a in assets if a["filename"] == filename), None)
    if not match:
        fail(f"no such asset: {target}")
    check(call(
        "mutation($i:Int!){assets{deleteAsset(id:$i)"
        "{responseResult{succeeded errorCode message}}}}",
        {"i": match["id"]},
    )["assets"]["deleteAsset"])
    note(f"deleted asset {target} (id {match['id']})")


def cmd_query(args):
    query = args.query
    if query.startswith("@"):
        query = pathlib.Path(query[1:]).read_text()
    variables = json.loads(args.variables) if args.variables else {}
    print(json.dumps(call(query, variables), indent=2))


parser = argparse.ArgumentParser(
    prog="wiki", description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
sub = parser.add_subparsers(dest="cmd", required=True, metavar="COMMAND")


def add(name, help, structured=True):
    p = sub.add_parser(name, help=help, description=help)
    if structured:
        p.add_argument("--json", action="store_true", help="machine-readable output")
    else:
        p.set_defaults(json=False)
    return p


p = add("list", "List every page, published or not.")
p.add_argument("--tag", action="append", metavar="TAG",
               help="only pages carrying this tag; repeatable")
p.add_argument("--order", default="PATH",
               choices=["PATH", "TITLE", "CREATED", "UPDATED", "ID"])
p.add_argument("--limit", type=int, metavar="N")
p.set_defaults(func=cmd_list)

p = add("tree", "Show the page hierarchy.")
p.add_argument("path", nargs="?", help="subtree to show; default the whole wiki")
p.set_defaults(func=cmd_tree)

p = add("search", "Search page titles, descriptions, and paths. Not content.")
p.add_argument("query")
p.add_argument("--path", metavar="PREFIX", help="restrict to this path prefix")
p.set_defaults(func=cmd_search)

p = add("grep", "Search the markdown source of every page with a regex.")
p.add_argument("pattern")
p.add_argument("--path", metavar="PREFIX", help="restrict to this path prefix")
p.add_argument("-i", "--ignore-case", action="store_true")
p.add_argument("-C", "--context", type=int, default=0, metavar="N",
               help="show N lines of context around each match")
p.add_argument("-l", "--files-only", action="store_true", help="print paths only")
p.set_defaults(func=cmd_grep)

p = add("tags", "List every tag in use.")
p.set_defaults(func=cmd_tags)

p = add("get", "Print a page's markdown source.", structured=False)
p.add_argument("path")
p.add_argument("--json", action="store_true", help="the whole page as JSON")
p.add_argument("--meta", action="store_true", help="metadata instead of content")
p.add_argument("--frontmatter", action="store_true",
               help="prepend YAML frontmatter, for editing and putting back")
p.add_argument("--version", type=int, metavar="ID",
               help="read this version instead of the current one")
p.set_defaults(func=cmd_get)

p = add("put", "Create or update a page.", structured=False)
p.add_argument("path")
p.add_argument("--title", help="required when creating")
p.add_argument("--description")
p.add_argument("--file", metavar="PATH", help="read content from a file")
p.add_argument("--content", help="content as a literal string")
p.add_argument("--tag", action="append", metavar="TAG",
               help="replaces the page's tags; repeatable")
p.add_argument("--frontmatter", action="store_true",
               help="take title, description, and tags from the content's YAML "
                    "frontmatter, and refuse the write if the page changed since "
                    "its updatedAt")
p.add_argument("--force", action="store_true",
               help="write even if the page changed since it was read")
p.add_argument("--draft", action="store_true", help="leave the page unpublished")
p.add_argument("--publish", action="store_true", help="publish an unpublished page")
p.set_defaults(func=cmd_put)

p = add("move", "Move or rename a page, or a whole subtree.", structured=False)
p.add_argument("path")
p.add_argument("destination")
p.add_argument("-r", "--recursive", action="store_true",
               help="also move every page under PATH")
p.add_argument("-n", "--dry-run", action="store_true", help="print the moves only")
p.set_defaults(func=cmd_move)

p = add("delete", "Delete a page and every version of it. Cannot be undone.",
        structured=False)
p.add_argument("path")
p.set_defaults(func=cmd_delete)

p = add("history", "List a page's versions.")
p.add_argument("path")
p.add_argument("--limit", type=int, default=25, metavar="N")
p.set_defaults(func=cmd_history)

p = add("diff", "Diff a version against the live page, another version, or a file.",
        structured=False)
p.add_argument("path")
p.add_argument("version", type=int, nargs="?")
p.add_argument("to", type=int, nargs="?")
p.add_argument("--file", metavar="PATH", help="diff the live page against this file")
p.add_argument("--frontmatter", action="store_true",
               help="strip YAML frontmatter from --file before diffing")
p.set_defaults(func=cmd_diff)

p = add("restore", "Roll a page back to an earlier version.", structured=False)
p.add_argument("path")
p.add_argument("version", type=int)
p.set_defaults(func=cmd_restore)

p = add("links", "List internal page links.")
p.add_argument("--broken", action="store_true",
               help="only links pointing at pages that do not exist")
p.set_defaults(func=cmd_links)

p = add("assets", "List asset folders and files.")
p.add_argument("folder", nargs="?", help="folder to list; default the root")
p.set_defaults(func=cmd_assets)

p = add("upload", "Upload a file to an asset folder, creating the folder if needed.",
        structured=False)
p.add_argument("file")
p.add_argument("--folder", metavar="SLUG", help="destination folder; default the root")
p.add_argument("--name", help="store under this filename instead")
p.set_defaults(func=cmd_upload)

p = add("delete-asset", "Delete an uploaded asset.", structured=False)
p.add_argument("path", help="folder/filename, or just filename at the root")
p.set_defaults(func=cmd_delete_asset)

p = add("query", "Run a raw GraphQL query. @file reads it from a file.",
        structured=False)
p.add_argument("query")
p.add_argument("variables", nargs="?", help="JSON object")
p.set_defaults(func=cmd_query)

args = parser.parse_args()
args.func(args)

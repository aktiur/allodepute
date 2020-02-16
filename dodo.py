from pathlib import Path
from zipfile import ZipFile

from doit import create_after

from scripts import (
    telecharger,
    correspondances_partis,
    correspondances_groupes,
    masser_fichier_deputes,
)

URLS = {
    "laposte_hexasmal.csv": "https://datanova.legroupe.laposte.fr/explore/dataset/laposte_hexasmal/download/?format=csv&timezone=Europe/Berlin&use_labels_for_header=true",
    "contours_circonscriptions.json": "https://www.data.gouv.fr/s/resources/carte-des-circonscriptions-legislatives-2012-et-2017/20170721-135742/france-circonscriptions-legislatives-2012.json",
    "assemblee_nationale.zip": "http://data.assemblee-nationale.fr/static/openData/repository/15/amo/deputes_actifs_mandats_actifs_organes/AMO10_deputes_actifs_mandats_actifs_organes_XV.json.zip",
}

DATA_DIR = Path(__file__).parent / "data"
AN_DIR = DATA_DIR / "assemblee_nationale"
IMAGE_DIR = Path(__file__).parent / "static" / "deputes"


def django_manage(*cmd):
    return ["pipenv", "run", "src/manage.py", *cmd]


def task_dossier():
    for name, dir in [("data", DATA_DIR), ("an", AN_DIR), ("image", IMAGE_DIR)]:
        yield {
            "name": name,
            "targets": [dir],
            "actions": [(dir.mkdir, [], {"parents": True})],
            "uptodate": [True],
        }


def task_telecharger():
    for file, url in URLS.items():
        path = DATA_DIR / file
        yield {
            "name": file,
            "task_dep": ["dossier:data"],
            "targets": [path],
            "uptodate": [True],
            "actions": [(telecharger, [url, path], {})],
        }


def task_unzip_assemblee_nationale():
    zip_path = DATA_DIR / "assemblee_nationale.zip"

    def unzip_an():
        with ZipFile(zip_path) as z:
            for file in z.infolist():
                if file.is_dir():
                    continue

                file.filename = Path(file.filename).name
                z.extract(file, path=AN_DIR)

    return {
        "task_dep": ["dossier:an"],
        "file_dep": [zip_path],
        "actions": [unzip_an],
    }


def task_liste_deputes():
    def deps():
        return {"file_dep": [str(p) for p in AN_DIR.glob("PA*.json")]}

    return {"task_dep": ["unzip_assemblee_nationale"], "actions": [deps]}


def task_liste_organes():
    def deps():
        return {"file_dep": [str(p) for p in AN_DIR.glob("PO*.json")]}

    return {"task_dep": ["unzip_assemblee_nationale"], "actions": [deps]}


def task_correspondances():
    return {
        "calc_dep": ["liste_organes"],
        "actions": [
            (correspondances_partis, [AN_DIR]),
            (correspondances_groupes, [AN_DIR]),
        ],
        "uptodate": [True],
    }


def task_masser_fichier_deputes():
    target = DATA_DIR / "deputes.csv"
    return {
        "calc_dep": ["liste_deputes"],
        "targets": [target],
        "getargs": {
            "corr_groupes": ("correspondances", "groupes"),
            "corr_partis": ("correspondances", "partis"),
        },
        "actions": [(masser_fichier_deputes, [], {"dir": AN_DIR, "dest": target})],
    }


def task_import_code_postaux():
    path = DATA_DIR / "laposte_hexasmal.csv"

    return {
        "file_dep": [path],
        "uptodate": [True],
        "actions": [django_manage("import_codes_postaux", "-s", path)],
    }


def task_import_circonscriptions():
    path = DATA_DIR / "contours_circonscriptions.json"

    return {
        "file_dep": [path],
        "uptodate": [True],
        "actions": [django_manage("import_circonscriptions", "-s", path)],
    }


def task_import_deputes():
    src = DATA_DIR / "deputes.csv"
    return {
        "file_dep": [src],
        "actions": [django_manage("import_deputes", "-s", src)],
    }


@create_after(
    executed="unzip_assemblee_nationale", target_regex="static/deputes/[0-9]+\.jpg$"
)
def task_telecharger_photos():
    for json_file in AN_DIR.glob("PA*.json"):
        name = json_file.stem[2:]
        target = IMAGE_DIR / f"{name}.jpg"
        url = f"http://www2.assemblee-nationale.fr/static/tribun/15/photos/{name}.jpg"

        yield {
            "name": name,
            "file_dep": [json_file],
            "task_dep": ["dossier:image"],
            "targets": [IMAGE_DIR / f"{name}.jpg"],
            "actions": [f"curl -s -S {url} -o {target}"],
        }

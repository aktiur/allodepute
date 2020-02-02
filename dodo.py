from pathlib import Path
from zipfile import ZipFile

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


def django_manage(*cmd):
    return ["pipenv", "run", "src/manage.py", *cmd]


def task_creer_dossier_data():
    return {"targets": [DATA_DIR], "actions": [DATA_DIR.mkdir], "uptodate": [True]}


def task_telecharger():
    for file, url in URLS.items():
        path = DATA_DIR / file
        yield {
            "name": file,
            "targets": [path],
            "uptodate": [True],
            "actions": [(telecharger, [url, path], {})],
        }


def task_unzip_assemblee_nationale():
    zip_path = DATA_DIR / "assemblee_nationale.zip"

    with ZipFile(zip_path) as z:
        targets = [
            AN_DIR / Path(f.filename).name for f in z.infolist() if not f.is_dir()
        ]

    def unzip_an():
        AN_DIR.mkdir(exist_ok=True)

        with ZipFile(zip_path) as z:
            for file in z.infolist():
                if file.is_dir():
                    continue

                file.filename = Path(file.filename).name
                z.extract(file, path=AN_DIR)

    return {
        "file_dep": [zip_path],
        "targets": targets,
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
        "actions": [django_manage("import_codes_postaux", "-s", path)],
    }


def task_import_circonscriptions():
    path = DATA_DIR / "contours_circonscriptions.json"

    return {
        "file_dep": [path],
        "actions": [django_manage("import_circonscriptions", "-s", path)],
    }


def task_import_deputes():
    dir = DATA_DIR / "assemblee_nationale"
    return {
        "calc_dep": ["liste_deputes"],
        "actions": [django_manage("import_deputes", "-d", str(dir))],
    }

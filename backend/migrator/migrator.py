import importlib
import logging

import os
import re

from singletons.db import Db


LOGGER = logging.getLogger("migrator")


class Migration:
    def __init__(self, _id, name, _type):
        """
        Una classe che rappresenta una migration

        :param _id: id (`str` o `int`)
        :param name: nome migration
        :param _type: `sql` o `py`
        """
        self.id = int(_id)
        self.name = name if name is not None else ""
        self.type = _type
        self.file_name = "m{id}{name}.{ext}".format(
            id=self.id, name="_{}".format(self.name) if name is not None else "", ext=self.type
        )


async def save_db_version(db_version):
    """
    Aggiorna db_version nel database

    :param db_version: nuova versione database
    :return:
    """
    async with Db().acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("UPDATE db_version SET db_version = %s WHERE 1 LIMIT 1", (db_version,))
            await conn.commit()


def get_migration(_id, migrations):
    """
    Ritorna l'oggetto `Migration` con `id` = `_id`
    da una lista contenente oggetti `Migration`

    :param _id: id migration
    :param migrations: lista oggetti `Migration`
    :return: `None` o oggetto `Migration`
    """
    for i in migrations:
        if i.id == _id:
            return i
    return None


async def migrate():
    """
    Esegue tutte le migration.
    Bisogna collegarsi prima al database di eseguire questa coroutine

    :return:
    :raise:
    """
    # Controlla se ci sono tabelle nel db
    async with Db().acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""SELECT COUNT(DISTINCT table_name) as c
                                 FROM information_schema.columns
                                 WHERE table_schema = %s""", (Db().config["db"],))
            db_empty = (await cur.fetchone())["c"] <= 0

            # Se ci sono tabelle, prova a leggere `db_version`
            if not db_empty:
                await cur.execute("SELECT db_version FROM db_version LIMIT 1")
                db_version_in_db = await cur.fetchone()
                db_version = 0 if db_version_in_db is None else db_version_in_db["db_version"]
            else:
                db_version = 0

    # Prendi la lista di file sql e py da eseguire
    files = os.listdir(os.path.join(os.path.dirname(__file__), "migrations"))
    migrations = []
    new_migrations = []
    for i in files:
        matches = re.search("(?:m)(\d+)(?:_(.+))?\.(sql|py)", i, re.IGNORECASE)
        if matches is None:
            continue
        m = Migration(*matches.groups())
        migrations.append(m)
        if m.id > db_version:
            new_migrations.append(m)

    # Controlla se ci sono migration da eseguire
    if len(new_migrations) == 0:
        LOGGER.info("No new migrations. The database is already up to date!")
        return

    # Esegui migrations
    LOGGER.info("Current db version: {}@{}".format(Db().config["db"], db_version))
    db_version += 1
    current_migration = get_migration(db_version, migrations)
    while current_migration is not None:
        LOGGER.info("Executing {}".format(current_migration.file_name))

        if current_migration.type == "sql":
            # Leggi ed esegui file sql
            with open(
                os.path.join(os.path.dirname(__file__), "migrations/{}".format(current_migration.file_name)), "r"
            ) as f:
                data = f.read()
            async with Db().acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(data)
                    await conn.commit()
        elif current_migration.type == "py":
            # Importa modulo py
            module = importlib.import_module("migrator.migrations.{}".format(current_migration.file_name[:-3]))
            migr = getattr(module, "do")
            await migr()

        # Migration eseguita, aggiorna `db_version`
        LOGGER.info("Migration {} executed with no errors".format(current_migration.file_name))
        await save_db_version(db_version)

        # Vai alla prossima migration
        db_version += 1
        current_migration = get_migration(db_version, migrations)
    LOGGER.info("All migrations executed correctly")

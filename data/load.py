import aiofiles
import argparse
import asyncio
import sys
from os import path

import asyncpg

sys.path.append(path.join(path.dirname(path.realpath(__file__)), ".."))

from pt_bot.settings import Settings


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, help="Path to sql script to be launched")
    return parser.parse_args()


async def _run_script(dsn: str, file_path: str) -> None:
    connection = await asyncpg.connect(dsn=dsn)

    async with aiofiles.open(file_path) as f:
        await connection.execute(await f.read())

    await connection.close()


async def main() -> None:
    settings = Settings()
    dsn = settings.db_dsn.replace("+asyncpg", "")

    args = _parse_args()
    await _run_script(dsn, args.file)


if __name__ == "__main__":
    asyncio.run(main())

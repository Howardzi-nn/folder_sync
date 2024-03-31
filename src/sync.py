import os
import shutil
import argparse
import asyncio
import filecmp
import hashlib
import inspect

import utils


async def get_file_md5(file_path):
    # Calculate the MD5 hash
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


async def synchronize_folders(source_folder, replica_folder, logger):
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            source_file = str(os.path.join(root, file))
            replica_file = os.path.join(
                replica_folder, os.path.relpath(source_file, source_folder))

            if not os.path.exists(replica_file) or not filecmp.cmp(
                    source_file, replica_file):
                source_md5 = await get_file_md5(source_file)
                logger.debug(
                    f"[{inspect.currentframe().f_code.co_name}] "
                    f"source: {source_md5}"
                )

                replica_md5 = None
                if os.path.exists(replica_file):
                    replica_md5 = await get_file_md5(replica_file)
                    logger.debug(
                        f"[{inspect.currentframe().f_code.co_name}] "
                        f"replica: {replica_md5}"
                    )

                if not os.path.exists(
                        replica_file) or replica_md5 != source_md5:
                    os.makedirs(os.path.dirname(replica_file), exist_ok=True)
                    shutil.copy2(source_file, replica_file)
                    if replica_md5 is None:
                        logger.info(
                            f"[{inspect.currentframe().f_code.co_name}] "
                            f"Replica file {file} does not exist, "
                            f"copied file {source_file} to {replica_file}")
                    else:
                        logger.info(
                            f"[{inspect.currentframe().f_code.co_name}] MD5 "
                            f"hashes not match, copied file"
                            f"{source_file} to {replica_file}")
                else:
                    logger.info(
                        f"[{inspect.currentframe().f_code.co_name}] Skipping "
                        f"file {source_file} as MD5 hashes match")


async def synchronize_folders_delete(source_folder, replica_folder, logger):
    # Delete empty folders in replica folder
    for root, dirs, files in os.walk(replica_folder):
        for file in files:
            replica_file = str(os.path.join(root, file))
            source_file = os.path.join(
                source_folder, os.path.relpath(replica_file, replica_folder))

            if not os.path.exists(source_file):
                os.remove(replica_file)
                logger.info(
                    f"[{inspect.currentframe().f_code.co_name}] "
                    f"Deleted {file} file {replica_file}")


async def synchronize_empty_folders(source_folder, replica_folder, logger):
    # Create empty folders in replica folder
    for root, dirs, _ in os.walk(source_folder):
        for directory in dirs:
            source_sub_folder = str(os.path.join(root, directory))
            replica_sub_folder = os.path.join(
                replica_folder, os.path.relpath(
                    source_sub_folder, source_folder))

            if not os.path.exists(replica_sub_folder):
                os.makedirs(replica_sub_folder)
                logger.info(
                    f"[{inspect.currentframe().f_code.co_name}] "
                    f"Created empty folder {replica_sub_folder}"
                )

    # Try to delete empty folders in replica folder
    for root, dirs, _ in os.walk(replica_folder, topdown=False):
        for directory in dirs:
            replica_sub_folder = str(os.path.join(root, directory))
            source_sub_folder = os.path.join(
                source_folder, os.path.relpath(
                    replica_sub_folder, replica_folder)
            )

            if not os.path.exists(source_sub_folder):
                if not os.listdir(replica_sub_folder):
                    logger.info(
                        f"[{inspect.currentframe().f_code.co_name}] "
                        f"Deleting empty folder {replica_sub_folder}"
                    )
                    try:
                        os.rmdir(replica_sub_folder)
                    except OSError as e:
                        logger.error(
                            f"[{inspect.currentframe().f_code.co_name}] "
                            f"Error occurred while deleting folder "
                            f"{replica_sub_folder}: {e}"
                        )
                else:
                    logger.warning(
                        f"[{inspect.currentframe().f_code.co_name}] "
                        f"Folder {replica_sub_folder} "
                        f"is not empty, skipping deletion"
                    )


async def main():
    parser = argparse.ArgumentParser(
        description="Folder synchronization program")

    parser.add_argument(
        "-i",
        "--interval",
        type=float,
        default=1,
        help="Synchronization interval in seconds (default: 1)"
    )
    parser.add_argument(
        "-l",
        "--log",
        help="Path to the log file",
        default=f"logs/{utils.get_datetime_logname()}"
    )
    parser.add_argument(
        "-r",
        "--replica",
        help="Path to the replica folder",
        default="src/test/replica"
    )
    parser.add_argument(
        "-s",
        "--source",
        help="Path to the source folder",
        default="src/test/source"
    )
    parser.add_argument(
        "-sync",
        help="For use in periodic synchronization",
        action="store_true"
    )

    args = parser.parse_args()

    logger = utils.setup_logging(args.log)
    logger.info("Starting folder synchronization program")

    if args.sync:
        logger.debug("Starting in synchronization mode")
        while True:
            await synchronize_folders(args.source, args.replica, logger)
            await synchronize_folders_delete(args.source, args.replica, logger)
            await synchronize_empty_folders(args.source, args.replica, logger)
            await asyncio.sleep(args.interval)
    else:
        logger.debug("Starting in one-run mode")
        await synchronize_folders(args.source, args.replica, logger)
        await synchronize_folders_delete(args.source, args.replica, logger)
        await synchronize_empty_folders(args.source, args.replica, logger)


if __name__ == "__main__":
    asyncio.run(main())

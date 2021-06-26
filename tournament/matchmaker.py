# Copyright 2021 Softwerks LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import logging

logger: logging.Logger = logging.getLogger(__name__)

INTERVAL: int = 5


async def run() -> None:
    logger.info("matchmaker started")
    try:
        while True:
            sleep_task: asyncio.Task = asyncio.create_task(asyncio.sleep(INTERVAL))
            match_task: asyncio.Task = asyncio.create_task(match())
            await asyncio.gather(sleep_task, match_task)
    except asyncio.CancelledError:
        sleep_task.cancel()
        match_task.cancel()
        logger.info("matchmaker stopped")


async def match() -> None:
    try:
        await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass

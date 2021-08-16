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
import json
import logging
import time
from typing import Dict, List

import aioredis
import backgammon

from . import redis

logger: logging.Logger = logging.getLogger(__name__)

INTERVAL: float = 1.0


async def run() -> None:
    try:
        while True:
            start: float = time.perf_counter()
            await _clock()
            elapsed: float = time.perf_counter() - start
            if elapsed >= INTERVAL:
                logger.warning(f"clock took {round(elapsed, 1)}s to execute")
            else:
                await asyncio.sleep(INTERVAL - elapsed)
    except asyncio.CancelledError:
        pass


async def _clock() -> None:
    try:
        now: int = int(time.time() * 1000)

        conn: aioredis.Redis = await redis.get_connection()

        for game_id in await conn.zrangebyscore("clock", 0, now, encoding="utf-8"):
            await _expire_game(game_id)

        await conn.zremrangebyscore("clock", 0, now)
    except asyncio.CancelledError:
        pass


async def _expire_game(game_id: str) -> None:
    conn: aioredis.Redis = await redis.get_connection()

    game_data: Dict[str, str] = await conn.hgetall(f"game:{game_id}", encoding="utf-8")

    game: backgammon.Backgammon = backgammon.Backgammon(
        game_data["position"], game_data["match"]
    )

    if game.match.player is backgammon.match.Player.ZERO:
        game.match.player_1_score = game.match.length
    else:
        game.match.player_0_score = game.match.length
    game.match.game_state = backgammon.match.GameState.GAME_OVER

    await conn.hset(f"game:{game_id}", "match", game.match.encode())

    msg: Dict[str, str] = {
        "code": "update",
        "id": game.encode(),
        "time0": game_data["time_0"],
        "time1": game_data["time_1"],
        "timestamp": game_data["timestamp"],
    }
    await conn.publish(game_id, json.dumps(msg))

    logger.info(f"Expired game: {game_id}")

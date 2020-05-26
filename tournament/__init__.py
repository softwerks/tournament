# Copyright 2019 Softwerks LLC
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
import signal
import websockets


class Tournament:
    def __init__(self, port):
        self.port = port
        self.loop = asyncio.get_event_loop()
        self.shutdown = self.loop.create_future()
        self.loop.add_signal_handler(signal.SIGINT, self.shutdown.set_result, None)

    async def handler(self, websocket, path):
        async for message in websocket:
            print("incoming")
            await websocket.send(message)
        print("closed")

    async def serve(self):
        async with websockets.serve(self.handler, "localhost", self.port):
            await self.shutdown

    def run(self):
        self.loop.run_until_complete(self.serve())
        self.loop.stop()
        self.loop.close()

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

import argparse

from tournament import Tournament


parser = argparse.ArgumentParser(description="Tournament")
parser.add_argument("-p", "--port", default=5555, type=int, help="port number")
args = parser.parse_args()
tournament = Tournament(args.port)
tournament.run()

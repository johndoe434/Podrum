################################################################################
#                                                                              #
#  ____           _                                                            #
# |  _ \ ___   __| |_ __ _   _ _ __ ___                                        #
# | |_) / _ \ / _` | '__| | | | '_ ` _ \                                       #
# |  __/ (_) | (_| | |  | |_| | | | | | |                                      #
# |_|   \___/ \__,_|_|   \__,_|_| |_| |_|                                      #
#                                                                              #
# Copyright 2021 Podrum Studios                                                #
#                                                                              #
# Permission is hereby granted, free of charge, to any person                  #
# obtaining a copy of this software and associated documentation               #
# files (the "Software"), to deal in the Software without restriction,         #
# including without limitation the rights to use, copy, modify, merge,         #
# publish, distribute, sublicense, and/or sell copies of the Software,         #
# and to permit persons to whom the Software is furnished to do so,            #
# subject to the following conditions:                                         #
#                                                                              #
# The above copyright notice and this permission notice shall be included      #
# in all copies or substantial portions of the Software.                       #
#                                                                              #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR   #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,     #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER       #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING      #
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS #
# IN THE SOFTWARE.                                                             #
#                                                                              #
################################################################################

from block.block_ids import block_ids
from block.block_states import block_states

class block_map:
    def __init__(self) -> None:
        self.legacy_to_runtime_ids: dict = {}
        self.runtime_to_legacy_ids: dict = {}
        for runtime_id, state in enumerate(block_states):
            if "LegacyStates" in state:
                for legacy_state in state["LegacyStates"]:
                    self.register_block(legacy_state["id"], legacy_state["val"], runtime_id)
                      
    @staticmethod
    def hash_legacy_id(block_id: int, meta: int) -> int:
        return (block_id << 4) | meta
    
    @staticmethod
    def unhash_legacy_id(hashed_legacy_id: int) -> tuple:
        return hashed_legacy_id >> 4, hashed_legacy_id & 0x0f
                
    def register_block(self, block_id: int, meta: int, runtime_id: int) -> None:
        hashed_legacy_id: int = block_map.hash_legacy_id(block_id, meta)
        self.legacy_to_runtime_ids[hashed_legacy_id]: int = runtime_id
        if runtime_id in self.runtime_to_legacy_ids:
            if isinstance(self.runtime_to_legacy_ids[runtime_id], list):
                if len(self.runtime_to_legacy_ids[runtime_id]) > 0:
                    self.runtime_to_legacy_ids[runtime_id].append(hashed_legacy_id)
                    return
        self.runtime_to_legacy_ids[runtime_id]: list = [hashed_legacy_id]

    def runtime_to_legacy_id(self, runtime_id: int, legacy_state_offset: int = 0) -> tuple:
        return block_map.unhash_legacy_id(self.runtime_to_legacy_ids[runtime_id][legacy_state_offset])
    
    def legacy_to_runtime_id(self, block_id: int, meta: int) -> int:
        return self.legacy_to_runtime_ids[block_map.hash_legacy_id(block_id, meta)]

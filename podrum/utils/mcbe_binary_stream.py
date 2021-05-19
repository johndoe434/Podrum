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

from binary_utils.binary_stream import binary_stream
from utils.math.vector_2 import vector_2
from utils.math.vector_3 import vector_3

class mcbe_binary_stream(binary_stream):
    def read_string(self) -> str:
        return self.read(self.read_var_int()).decode()
    
    def write_string(self, value: str) -> None:
        self.write_var_int(len(value))
        self.write(value.encode())
        
    def read_byte_array(self) -> bytes:
        return self.read(self.read_var_int())
    
    def write_byte_array(self, value: bytes) -> None:
        self.write_var_int(len(value))
        self.write(value)
        
    def read_behavior_pack_infos(self) -> list:
        behavior_pack_infos: list = []
        length: int = self.read_short_le()
        for i in range(0, length):
            behavior_pack_infos.append({
                "uuid": self.read_string(),
                "version": self.read_string(),
                "size": self.read_unsigned_long_le(),
                "content_key": self.read_string(),
                "sub_pack_name": self.read_string(),
                "content_identity": self.read_string(),
                "has_scripts": self.read_bool()
            })
        return behavior_pack_infos
            
    def write_behavior_pack_infos(self, value: list) -> None:
        self.write_short_le(len(value))
        for behavior_pack_info in value:
            self.write_string(behavior_pack_info["uuid"])
            self.write_string(behavior_pack_info["version"])
            self.write_unsigned_long_le(behavior_pack_info["size"])
            self.write_string(behavior_pack_info["content_key"])
            self.write_string(behavior_pack_info["sub_pack_name"])
            self.write_string(behavior_pack_info["content_identity"])
            self.write_bool(behavior_pack_info["has_scripts"])
            
    def read_resource_pack_infos(self) -> list:
        resource_pack_infos: list = []
        length: int = self.read_short_le()
        for i in range(0, length):
            resource_pack_infos.append({
                "uuid": self.read_string(),
                "version": self.read_string(),
                "size": self.read_unsigned_long_le(),
                "content_key": self.read_string(),
                "sub_pack_name": self.read_string(),
                "content_identity": self.read_string(),
                "has_scripts": self.read_bool(),
                "rtx_enabled": self.read_bool()
            })
        return resource_pack_infos
            
    def write_resource_pack_infos(self, value: list) -> None:
        self.write_short_le(len(value))
        for resource_pack_info in value:
            self.write_string(resource_pack_info["uuid"])
            self.write_string(resource_pack_info["version"])
            self.write_unsigned_long_le(resource_pack_info["size"])
            self.write_string(resource_pack_info["content_key"])
            self.write_string(resource_pack_info["sub_pack_name"])
            self.write_string(resource_pack_info["content_identity"])
            self.write_bool(resource_pack_info["has_scripts"])
            self.write_bool(resource_pack_info["rtx_enabled"])
            
    def read_resource_pack_id_versions(self) -> list:
        resource_pack_id_versions: list = []
        length: int = self.read_var_int()
        for i in range(0, length):
            resource_pack_id_versions.append({
                "uuid": self.read_string(),
                "version": self.read_string(),
                "name": self.read_string()
            })
        return resource_pack_id_versions
        
    def write_resource_pack_id_versions(self, value: list) -> None:
        self.write_var_int(len(value))
        for resource_pack_id_version in value:
            self.write_string(resource_pack_id_version["uuid"])
            self.write_string(resource_pack_id_version["version"])
            self.write_string(resource_pack_id_version["name"])
            
    def read_resource_pack_ids(self) -> list:
        resource_pack_ids: list = []
        length: int = self.read_short_le()
        for i in range(0, length):
            resource_pack_ids.append(self.read_string())
        return resource_pack_ids
        
    def write_resource_pack_ids(self, value: list) -> None:
        self.write_short_le(len(value))
        for resource_pack_id in value:
            self.write_string(resource_pack_id)
            
    def read_experiment(self) -> dict:
        return {
            "name": self.read_string(),
            "enabled": self.read_bool()
        }
        
    def write_experiment(self, value: dict) -> None:
        self.write_string(value["name"])
        self.write_bool(value["enabled"])
        
    def read_experiments(self) -> list:
        experiments: list = []
        length: int = self.read_int_le()
        for i in range(0, length):
            experiments.append(self.read_experiment())
        return experiments
        
    def write_experiments(self, value: list) -> None:
        self.write_int_le(len(value))
        for experiment in value:
            self.write_experiment(experiment)
            
    def read_gamemode(self) -> int:
        return self.read_signed_var_int()
        
    def write_gamemode(self, value: int) -> None:
        self.write_signed_var_int(value)
        
    def read_game_rule(self) -> dict:
        game_rule: dict = {
            "name": self.read_string(),
            "type": self.read_var_int()
        }
        if game_rule["type"] == 1:
            game_rule["value"]: bool = self.read_bool()
        elif game_rule["type"] == 2:
            game_rule["value"]: int = self.read_signed_var_int()
        elif game_rule["type"] == 3:
            game_rule["value"]: float = self.read_float_le()
        return game_rule
        
    def write_game_rule(self, value: dict) -> None:
        self.write_string(value["name"])
        self.write_var_int(value["type"])
        if value["type"] == 1:
            self.write_bool(value["value"])
        elif value["type"] == 2:
            self.write_signed_var_int(value["value"])
        elif value["type"] == 3:
            self.write_float_le(value["value"])
            
    def read_game_rules(self) -> list:
        game_rules: list = []
        length: int = self.read_var_int()
        for i in range(0, length):
            game_rules.append(self.read_game_rule())
        return game_rules
        
    def write_game_rules(self, value: list) -> None:
        self.write_var_int(len(value))
        for game_rule in value:
            self.write_game_rule(game_rule)
            
    def read_blob(self) -> dict:
        return {
            "hash": self.read_unsigned_long_le(),
            "payload": self.read_byte_array()
        }
        
    def write_blob(self, value: dict) -> None:
        self.write_unsigned_long_le(value["hash"])
        self.write_byte_array(value["payload"])

    def read_block_palette(self) -> list:
        block_palette: list = []
        length: int = self.read_var_int()
        for i in range(0, length):
            entry: dict = {
                "name": self.read_string()
            }
            block_palette.append(entry)

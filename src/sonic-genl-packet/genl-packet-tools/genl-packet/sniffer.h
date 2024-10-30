// Copyright 2021 ONF
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef SNIFFER_H_
#define SNIFFER_H_

#include "receive_genetlink.h"
//debug access to the genl-packet library.

//[StringToHex(str)] returns a hex representation of a binary string str. 
//Requires: [str] is a string of ASCII characters.
std::string StringToHex(const std::string& str);

//[customCallbackRecieve(callback)] creates a genetlink listen thread with a custom provided callback function [callback] and joins it.
//Returns: Nothing unless something went wrong and the listener thread could not be joined.
//WARNING: If used you are responsible for setting up and declaring your own flags within your callback function.
int customCallbackRecieve(packet_metadata::ReceiveCallbackFunction callback);


#endif //SNIFFER_H_

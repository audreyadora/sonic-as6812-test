// Copyright 2021 Google LLC
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

#ifndef GENL_PACKET_RECEIVE_GENETLINK_H_
#define GENL_PACKET_RECEIVE_GENETLINK_H_
#include <functional>
#include <thread>

namespace packet_metadata {

    // Alias of the Receive Callback function used by the Receive thread to
    // be invoked on every packet from the hardware.
    using ReceiveCallbackFunction = std::function<void(
    const std::string& src_port_name, const std::string& target_port_name,
    const std::string& payload)>;

    std::thread StartReceive(packet_metadata::ReceiveCallbackFunction 
    callback_function);
}

#endif //GENL_PACKET_RECEIVE_GENETLINK_H_

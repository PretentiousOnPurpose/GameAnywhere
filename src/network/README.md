# Websocket server

## Exceptions

A server room can stop for 3 possible reasons:
- the game ends
- an agent disconnects
- the server is killed

The shutdown flow handles all these cases and goes like this:
```
(network-thread)
,--- The server dies -> interrupts all rooms and asks them to disconnect the agents
* The server closes the I/O context. No asynchronous operations are possible anymore.
|,--- an agent disconnects
* Agent disconnected
|
|  (game thread)
|  * The next time the game tries to ask that agent, it raises an exception and ends the game.
|  |,--- The game ends naturally
|  * The game ends
|  * The game asks the server to close the room (asynchronously). Then the game thread ends.
|
* If the I/O context is closed, the request is ignored.
|    If not, the server interrupts the room and asks him to disconnect all agents. (They were possibly already disconnected)
|
| / The game thread is joined, the room is closed and removed from the room list.
\`--
```

## License

The content of this directory is a near-identical copy of [the Boost WebSocket chat example](https://github.com/vinniefalco/CppCon2018).
It is distributed under the [Boost Software license v1.0](https://www.boost.org/LICENSE_1_0.txt):

Boost Software License - Version 1.0 - August 17th, 2003

Permission is hereby granted, free of charge, to any person or organization
obtaining a copy of the software and accompanying documentation covered by
this license (the "Software") to use, reproduce, display, distribute,
execute, and transmit the Software, and to prepare derivative works of the
Software, and to permit third-parties to whom the Software is furnished to
do so, all subject to the following:

The copyright notices in the Software and this entire statement, including
the above license grant, this restriction and the following disclaimer,
must be included in all copies of the Software, in whole or in part, and
all derivative works of the Software, unless such copies or derivative
works are solely in the form of machine-executable object code generated by
a source language processor.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT
SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE
FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
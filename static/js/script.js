/** @module script.js
 *  @since 2022.02.12, 03:34
 *  @changed 2022.02.12, 03:34
 */

$(document).ready(function () {
  // start up the SocketIO connection to the server
  // var socket = io.connect('http://localhost:5000');
  var socket = io.connect('/');
  console.log('@:script', {
    io: typeof io,
    socket: socket,
  });
  // debugger;
  // this is a callback that triggers when the "message" event is emitted by the server.
  socket.on('message', function(data) {
    console.log('@:script:message', data);
    // debugger;
  });
  socket.emit('join', { room: 'my_room' });
});

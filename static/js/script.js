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
  // this is a callback that triggers when the "message" event is emitted by the server.
  socket.on('message', function on_message(data) {
    console.log('@:script:on_message', data);
    // debugger;
  });
  socket.on('connect_error', function connect_error(err) {
    console.log('@:script:connect_error', err);
    // debugger;
  });
  socket.emit('join', { room: 'my_room' });
});

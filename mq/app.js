var amqp = require('amqplib/callback_api');
var io = require('socket.io').listen(3000);

amqp.connect('amqp://localhost', function(error0, connection) {
    if (error0) {
        throw error0;
    }
    connection.createChannel(function(error1, channel) {
        if (error1) {
            throw error1;
        }

        var queue = 'web_status';

        channel.assertQueue(queue, {
            durable: false
        });
        console.log(" [*] Waiting for messages in %s. To exit press CTRL+C", queue);

        io.sockets.on('connection', function (socket) {
            console.log(" [S] Connected")
            channel.consume(queue, function(msg) {
                console.log(" [x] Received %s", msg.content.toString());
                socket.emit('status', msg.content.toString());
            }, {
                noAck: true
            });
        });

        
    });
});
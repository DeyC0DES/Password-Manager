package com.emailSender.emailSenderPMG.config.rabbitMQ;

import org.springframework.amqp.rabbit.connection.ConnectionFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class RabbitMQConnection implements CommandLineRunner {

    private final ConnectionFactory connectionFactory;

    public RabbitMQConnection(ConnectionFactory connectionFactory) {
        this.connectionFactory = connectionFactory;
    }

    @Override
    public void run(String... args) throws Exception {
        connectionFactory.createConnection().close();
    }

}

package com.emailSender.emailSenderPMG.consumers;

import com.emailSender.emailSenderPMG.dtos.EmailRecordDto;
import com.emailSender.emailSenderPMG.models.EmailModel;
import com.emailSender.emailSenderPMG.services.EmailSender;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.handler.annotation.Payload;
import org.springframework.stereotype.Component;

@Component
public class EmailConsumer {

    @Autowired
    private EmailSender emailSender;

    @RabbitListener(queues="${broker.queue.email.name}")
    public void listenEmailQueue(@Payload EmailRecordDto emailRecordDto) {
        var emailModel = new EmailModel();
        BeanUtils.copyProperties(emailRecordDto, emailModel);
        emailSender.sendEmail(emailModel);
    }

}

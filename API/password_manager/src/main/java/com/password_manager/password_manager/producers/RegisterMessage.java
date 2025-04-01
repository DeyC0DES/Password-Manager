package com.password_manager.password_manager.producers;

import com.password_manager.password_manager.dtos.EmailDto;
import com.password_manager.password_manager.models.UserModel;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class RegisterMessage {

    private final RabbitTemplate rabbitTemplate;

    @Value("${broker.queue.email.name}")
    private String routingKey;

    public RegisterMessage(RabbitTemplate rabbitTemplate) {
        this.rabbitTemplate = rabbitTemplate;
    }

    public void publishRegisterMessageEmail(UserModel userModel) {

        var emailDto = new EmailDto();
        emailDto.setTo(userModel.getEmail());
        emailDto.setSubject("Thanks for register on the Password Manager!! :3");
        emailDto.setText("Hello,\n" +
                "\n" +
                " Now you can access the Password Manager features, please, if you are thinking on use that for real\n" +
                "consider do some changes to make it more security, im doing this things just for study, maybe on the future i will make it more security."
        );

        rabbitTemplate.convertAndSend("", routingKey, emailDto);
    }

}

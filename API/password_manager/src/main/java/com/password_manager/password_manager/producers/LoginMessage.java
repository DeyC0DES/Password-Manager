package com.password_manager.password_manager.producers;

import com.password_manager.password_manager.dtos.EmailDto;
import com.password_manager.password_manager.models.UserModel;
import com.password_manager.password_manager.services.IpService;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;

@Component
public class LoginMessage {

    private final RabbitTemplate rabbitTemplate;
    private final IpService ipService;

    @Value("${broker.queue.email.name}")
    private String routingKey;

    public LoginMessage(RabbitTemplate rabbitTemplate, IpService ipService) {
        this.rabbitTemplate = rabbitTemplate;
        this.ipService = ipService;
    }

    public void publishLoginAuthorizedMessageEmail(UserModel userModel) {

        String publicIp = this.ipService.getPublicIp();
        String localIp = this.ipService.getLocalIp();
        String country = this.ipService.getUserCountry(publicIp);
        String state = this.ipService.getUserState(publicIp);
        String city = this.ipService.getUserCity(publicIp);

        var emailDto = new EmailDto();
        emailDto.setTo(userModel.getEmail());
        emailDto.setSubject("A new login has detected!");
        emailDto.setText("Hello,\n" +
                "\n"+
                " We detected a new login at your account, here below have the information about this login:\n" +
                "\n" +
                "  - Day: " + LocalDate.now() +
                "\n  - Time: " + LocalTime.now().format(DateTimeFormatter.ofPattern("HH:mm")) +
                "\n  - PUBLIC IP: " + publicIp +
                "\n  - LOCAL IP:" + localIp +
                "\n  - COUNTRY: " + country +
                "\n  - STATE: " + state +
                "\n  - CITY: " + city
        );

        rabbitTemplate.convertAndSend("", routingKey, emailDto);
    }



}

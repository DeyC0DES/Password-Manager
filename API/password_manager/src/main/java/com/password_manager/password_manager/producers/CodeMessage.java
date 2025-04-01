package com.password_manager.password_manager.producers;

import com.password_manager.password_manager.dtos.EmailDto;
import com.password_manager.password_manager.models.CodeModel;
import com.password_manager.password_manager.models.UserModel;
import com.password_manager.password_manager.services.IpService;
import org.aspectj.apache.bcel.classfile.Code;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;

@Component
public class CodeMessage {

    private final RabbitTemplate rabbitTemplate;
    private final IpService ipService;

    @Value("${broker.queue.email.name}")
    private String routingKey;

    public CodeMessage(RabbitTemplate rabbitTemplate, IpService ipService) {
        this.rabbitTemplate = rabbitTemplate;
        this.ipService = ipService;
    }

    public void publishLoginRequestMessageEmail(UserModel userModel, CodeModel codeModel) {
        String publicIp = this.ipService.getPublicIp();
        String localIp = this.ipService.getLocalIp();
        String country = this.ipService.getUserCountry(publicIp);
        String state = this.ipService.getUserState(publicIp);
        String city = this.ipService.getUserCity(publicIp);

        var emailDto = new EmailDto();
        emailDto.setTo(userModel.getEmail());
        emailDto.setSubject("A new login request!!");
        emailDto.setText("Hello,\n" +
                "\n" +
                " If u dont recognize this login, please consider change your password, " +
                "you can see more information of this login below:\n" +
                "\n" +
                "Code: " + codeModel.getCode() +
                "\n\n" +
                "  - Day: " + LocalDate.now() +
                "\n  - Time: " + LocalTime.now().format(DateTimeFormatter.ofPattern("HH:mm")) +
                "\n  - PUBLIC IP: " + publicIp +
                "\n  - LOCAL IP: " + localIp +
                "\n  - COUNTRY: " + country +
                "\n  - STATE: " + state +
                "\n  - CITY: " + city
        );

        rabbitTemplate.convertAndSend("", routingKey, emailDto);
    }

    public void publishChangeEmailMessageEmail(UserModel userModel, CodeModel codeModel) {

        String publicIp = this.ipService.getPublicIp();
        String localIp = this.ipService.getLocalIp();
        String country = this.ipService.getUserCountry(publicIp);
        String state = this.ipService.getUserState(publicIp);
        String city = this.ipService.getUserCity(publicIp);

        var emailDto = new EmailDto();
        emailDto.setTo(userModel.getEmail());
        emailDto.setSubject("A change email request!!");
        emailDto.setText("Hello,\n" +
                "\n" +
                " If u dont recognize this change, please consider change your password, " +
                "you can see more information of this change below:\n" +
                "\n" +
                "Code: " + codeModel.getCode() +
                "\n\n" +
                "  - Day: " + LocalDate.now() +
                "\n  - Time: " + LocalTime.now().format(DateTimeFormatter.ofPattern("HH:mm")) +
                "\n  - PUBLIC IP: " + publicIp +
                "\n  - LOCAL IP: " + localIp +
                "\n  - COUNTRY: " + country +
                "\n  - STATE: " + state +
                "\n  - CITY: " + city
        );

        rabbitTemplate.convertAndSend("", routingKey, emailDto);
    }

    public void publishEmailChangedMessageEmail(UserModel userModel, String new_email) {

        String publicIp = this.ipService.getPublicIp();
        String localIp = this.ipService.getLocalIp();
        String country = this.ipService.getUserCountry(publicIp);
        String state = this.ipService.getUserState(publicIp);
        String city = this.ipService.getUserCity(publicIp);

        var emailDto = new EmailDto();
        emailDto.setTo(userModel.getEmail());
        emailDto.setSubject("A change has detected!");
        emailDto.setText("Hello,\n" +
                "\n"+
                " Your email has been changed, here below have the information about this change:\n" +
                "\n" +
                "  - New Email: " + new_email+
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

    public void publishChangePasswordMessageEmail(UserModel userModel, CodeModel codeModel) {

        String publicIp = this.ipService.getPublicIp();
        String localIp = this.ipService.getLocalIp();
        String country = this.ipService.getUserCountry(publicIp);
        String state = this.ipService.getUserState(publicIp);
        String city = this.ipService.getUserCity(publicIp);

        var emailDto = new EmailDto();
        emailDto.setTo(userModel.getEmail());
        emailDto.setSubject("A new password request!!");
        emailDto.setText("Hello,\n" +
                "\n" +
                " If u dont recognize this change, please consider change your password, " +
                "you can see more information of this change below:\n" +
                "\n" +
                "Code: " + codeModel.getCode() +
                "\n\n" +
                "  - Day: " + LocalDate.now() +
                "\n  - Time: " + LocalTime.now().format(DateTimeFormatter.ofPattern("HH:mm")) +
                "\n  - PUBLIC IP: " + publicIp +
                "\n  - LOCAL IP: " + localIp +
                "\n  - COUNTRY: " + country +
                "\n  - STATE: " + state +
                "\n  - CITY: " + city
        );

        rabbitTemplate.convertAndSend("", routingKey, emailDto);
    }

    public void publishPasswordChangedMessageEmail(UserModel userModel) {

        String publicIp = this.ipService.getPublicIp();
        String localIp = this.ipService.getLocalIp();
        String country = this.ipService.getUserCountry(publicIp);
        String state = this.ipService.getUserState(publicIp);
        String city = this.ipService.getUserCity(publicIp);

        var emailDto = new EmailDto();
        emailDto.setTo(userModel.getEmail());
        emailDto.setSubject("Your password has changed!");
        emailDto.setText("Hello,\n" +
                "\n"+
                " Your password has been changed, here below have the information about this change:\n" +
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

    public void publishDeleteMessageEmail(UserModel userModel, CodeModel codeModel) {
        String publicIp = this.ipService.getPublicIp();
        String localIp = this.ipService.getLocalIp();
        String country = this.ipService.getUserCountry(publicIp);
        String state = this.ipService.getUserState(publicIp);
        String city = this.ipService.getUserCity(publicIp);

        var emailDto = new EmailDto();
        emailDto.setTo(userModel.getEmail());
        emailDto.setSubject("A new delete account request!!");
        emailDto.setText("Hello,\n" +
                "\n" +
                " If u dont recognize this request, please consider change your password, " +
                "you can see more information of this below:\n" +
                "\n" +
                "Code: " + codeModel.getCode() +
                "\n\n" +
                "  - Day: " + LocalDate.now() +
                "\n  - Time: " + LocalTime.now().format(DateTimeFormatter.ofPattern("HH:mm")) +
                "\n  - PUBLIC IP: " + publicIp +
                "\n  - LOCAL IP: " + localIp +
                "\n  - COUNTRY: " + country +
                "\n  - STATE: " + state +
                "\n  - CITY: " + city
        );

        rabbitTemplate.convertAndSend("", routingKey, emailDto);
    }
}

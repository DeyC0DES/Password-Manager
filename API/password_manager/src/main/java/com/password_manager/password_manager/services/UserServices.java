package com.password_manager.password_manager.services;

import com.password_manager.password_manager.Repositories.UserRepository;
import com.password_manager.password_manager.models.UserModel;
import com.password_manager.password_manager.producers.CodeMessage;
import com.password_manager.password_manager.producers.LoginMessage;
import com.password_manager.password_manager.producers.RegisterMessage;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

import java.util.Optional;
import java.util.UUID;

@Service
public class UserServices {

    private final UserRepository userRepository;
    private final LoginMessage loginMessage;
    private final RegisterMessage registerMessage;
    private final CodeMessage codeMessage;

    public UserServices(UserRepository userRepository, IpService ipService, LoginMessage loginMessage, RegisterMessage registerMessage, CodeMessage codeMessage) {
        this.userRepository = userRepository;
        this.loginMessage = loginMessage;
        this.registerMessage = registerMessage;
        this.codeMessage = codeMessage;
    }

    // send email messages
    public void publishLoginMessage(UserModel userModel) {
        this.loginMessage.publishLoginAuthorizedMessageEmail(userModel);
    }

    public void publishRegisterMessage(UserModel userModel) {
        this.registerMessage.publishRegisterMessageEmail(userModel);
    }

    // requests
    @Transactional
    public void save(UserModel userModel) {
        userModel = this.userRepository.save(userModel);
        this.publishRegisterMessage(userModel);
    }

    public void update(UserModel userModel) {
        this.userRepository.save(userModel);
    }

    public Optional<UserModel> findById(UUID id) {
        return this.userRepository.findById(id);
    }

    public Optional<UserModel> findByEmail(String email) {
        return this.userRepository.findByEmail(email);
    }

    public void delete(UserModel userModel) {
        this.userRepository.delete(userModel);
    }
}
